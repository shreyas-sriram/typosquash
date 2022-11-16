import os
import json
import argparse
import subprocess

package_analysis_script = '/home/shreyas/Downloads/fall-2022/capstone/code/package-analysis/run_analysis.sh' # CHANGME

FILE_IGNORE_LIST = [
    '.cache', 'site-packages', '__pycache__', '/tmp', 'python3.9', 'https://', # pypi
    '_cacache', 'node_modules', # npm
    '.local', '/usr/local/lib/ruby', # rubygems
    ]

class Package:
    def __init__(self, name, registry):
        self.name = name
        self.registry = registry

        self.import_files = {}
        self.import_sockets = {}
        self.import_dns = {}

        self.install_files = {}
        self.install_sockets = {}
        self.install_dns = {}

        self.results_dir = '/tmp/results'

        self.install_files = {}
        self.install_sockets = {}
        self.install_dns = {}

        self.violated_files = {}
        self.violated_sockets = {}
        self.violated_dns = {}

    def run_dynamic_analysis(self):
        print(f'[INFO] Running dynamic analysis for package: {self.name}')

        subprocess.run(['sudo', package_analysis_script, self.registry, self.name], stdout=subprocess.PIPE)

    def read_dynamic_analysis_output(self):
        print(f'[INFO] Reading dynamic analysis output from: {self.results_dir}')

        files = os.listdir(self.results_dir)
        data = {}
        
        for file in ['violated.json']:
            if file.endswith('.json'):
                print(f'[INFO] Reading from file: {file}')
                data = json.load(open(f'{self.results_dir}/{file}'))

        self.parse_output(data)

    def parse_output(self, data):
        print(f'[INFO] Parsing dynamic analysis output result')

        self.import_files = data['Analysis']['import']['Files']
        self.import_sockets = data['Analysis']['import']['Sockets']
        self.import_dns = data['Analysis']['import']['DNS']

        self.install_files = data['Analysis']['install']['Files']
        self.install_sockets = data['Analysis']['install']['Sockets']
        self.install_dns = data['Analysis']['install']['DNS']

    def new_violation(self, type, key, value):
        if type == 'file':
            self.violated_files[key] = value
        elif type == 'socket':
            self.violated_sockets[key] = value
        elif type == 'dns':
            self.violated_dns[key] = value

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_violation(self):
        output = {
            'files': self.violated_files,
            'sockets': self.violated_sockets,
            'DNS': self.violated_dns,
            }
        return json.dumps(output, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Baseline:
    baseline_path = '/home/shreyas/Downloads/fall-2022/capstone/code/module-3-rnd/{}/{}-baseline.json'

    def __init__(self, registry):
        self.registry = registry
        
        self.baseline_path = self.baseline_path.format(registry, registry)
        self.baseline = {}

        self.import_files = {}
        self.import_sockets = {}
        self.import_dns = {}

        self.install_files = {}
        self.install_sockets = {}
        self.install_dns = {}

        self.violated_files = {}
        self.violated_sockets = {}
        self.violated_dns = {}

    def load_baseline(self):
        print(f'[INFO] Loading baseline from: {self.baseline_path}')

        data = json.load(open(self.baseline_path))
    
        self.import_files = data['import']['files']
        self.import_sockets = data['import']['sockets']
        self.import_dns = data['import']['dns']

        self.install_files = data['install']['files']
        self.install_sockets = data['install']['sockets']
        self.install_dns = data['install']['dns']

    def evaluate(self, package: Package):
        print(f'[INFO] Comparing results with baseline for package: {package.name}')

        self.evaluate_files(self.import_files, package, package.import_files, package.name, 'import')
        self.evaluate_sockets(self.import_sockets, package, package.import_sockets, 'import')
        self.evaluate_dns(self.import_dns, package, package.import_dns, 'import')

        self.evaluate_files(self.install_files, package, package.install_files, package.name, 'install')
        self.evaluate_sockets(self.install_sockets, package, package.install_sockets, 'install')
        self.evaluate_dns(self.install_dns, package, package.install_dns, 'install')

    def evaluate_files(self, baseline_files, package: Package, candidate_files, package_name, command):
        print(f'[INFO] Comparing files for command: {command}')

        ignore_list = FILE_IGNORE_LIST + [package_name]

        for file in candidate_files:
            needle = [file['Read'], file['Write'], file['Delete']]

            if not any(word in file['Path'] for word in ignore_list):
                if baseline_files.get(file['Path'], []) != needle:
                    print(f"[CRITICAL] Violated file for command `{command}`: {file['Path']}")
                    package.new_violation('file', file['Path'], {'action': needle, 'command': command})

    def evaluate_sockets(self, baseline_sockets, package: Package, candidate_sockets, command):
        print(f'[INFO] Comparing sockets for command: {command}')

        if not candidate_sockets:
            return
        for socket in candidate_sockets:
            needle = socket['Port']

            if baseline_sockets.get(socket['Address'], 0) != needle:
                print(f"[CRITICAL] Violated socket for command `{command}`: {socket['Address']}")
                package.new_violation('socket', socket['Address'], {'port': socket['Port'], 'hostnames': socket['Hostnames'], 'command': command})

    def evaluate_dns(self, baseline_dns, package: Package, candidate_dns, command):
        print(f'[INFO] Comparing DNS for command: {command}')

        if not candidate_dns:
            return

        for dns in candidate_dns[0]['Queries']:
            needle = dns['Hostname']

            if baseline_dns.get(needle, False) == False:
                print(f"[CRITICAL] Violated DNS for command `{command}`: {dns['Hostname']}")
                package.new_violation('dns', dns['Hostname'], {'command': command})

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs='?', type=str, help='package name')
    parser.add_argument('-r', nargs='?', type=str, help='registry name')
    args = parser.parse_args()

    return args

def main(package, registry):
    package = Package(package, registry)
    
    package.run_dynamic_analysis()
    package.read_dynamic_analysis_output()

    baseline = Baseline(registry)

    baseline.load_baseline()
    baseline.evaluate(package)

    print(package.get_violation())


if __name__ == '__main__':
    args = init()

    if not (args.p or args.r):
        print('[ERROR] Usage: sudo python3 module-3.py -p <package-name> -r <registry-name>')
        os._exit(1)

    if args.r and args.r not in ['pypi', 'npm', 'rubygems']:
        print('[ERROR] Use one of: [pypi, npm, rubygems]')
        os._exit(1)

    main(args.p, args.r)