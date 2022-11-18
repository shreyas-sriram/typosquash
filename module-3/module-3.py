import os
import json
import argparse
import subprocess

package_analysis_script = '/home/shreyas/Downloads/fall-2022/capstone/code/module-3/package-analysis/run_analysis.sh' # CHANGME

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

        os.system(f'sudo rm {self.results_dir}/*')

    def run_dynamic_analysis(self):
        # print(f'[INFO] Running dynamic analysis for package: {self.name}')

        subprocess.run(['sudo', package_analysis_script, self.registry, self.name], stdout=subprocess.PIPE)

    def read_dynamic_analysis_output(self):
        # print(f'[INFO] Reading dynamic analysis output from: {self.results_dir}')

        files = os.listdir(self.results_dir)
        data = {}

        for file in files:
            if file.endswith('.json'):
                # print(f'[INFO] Reading from file: {file}')
                data = json.load(open(f'{self.results_dir}/{file}'))

        self.parse_output(data)

    def parse_output(self, data):
        # print(f'[INFO] Parsing dynamic analysis output result')

        if 'import' in data['Analysis']:
            self.import_files = data['Analysis']['import']['Files']
            self.import_sockets = data['Analysis']['import']['Sockets']
            self.import_dns = data['Analysis']['import']['DNS']

        self.install_files = data['Analysis']['install']['Files']
        self.install_sockets = data['Analysis']['install']['Sockets']
        self.install_dns = data['Analysis']['install']['DNS']

    def compare(self, p: 'Package'):
        # compare import_files
        self.compare_files(p)

        # compare import_sockets
        self.compare_sockets(p)

        # compare import_dns
        self.compare_dns(p)

    def compare_files(self, p: 'Package'):
        if self.import_files and p.import_files:
            for i in range(len(self.import_files)):
                if (self.import_files[i]['Path'] != p.import_files[i]['Path'] or
                    self.import_files[i]['Read'] != p.import_files[i]['Read'] or
                    self.import_files[i]['Write'] != p.import_files[i]['Write'] or
                    self.import_files[i]['Delete'] != p.import_files[i]['Delete']):
                    self.violated_files[self.import_files[i]['Path']] = {
                        'read': self.import_files[i]['Read'],
                        'write': self.import_files[i]['Write'],
                        'delete': self.import_files[i]['Delete'],
                    }

    def compare_sockets(self, p: 'Package'):
        if self.import_files and p.import_files:
            for i in range(len(self.import_files)):
                if (self.import_files[i]['Path'] != p.import_files[i]['Path'] or
                    self.import_files[i]['Read'] != p.import_files[i]['Read'] or
                    self.import_files[i]['Write'] != p.import_files[i]['Write'] or
                    self.import_files[i]['Delete'] != p.import_files[i]['Delete']):
                    self.violated_files[self.import_files[i]['Path']] = {
                        'read': self.import_files[i]['Read'],
                        'write': self.import_files[i]['Write'],
                        'delete': self.import_files[i]['Delete'],
                    }
        
    def compare_dns(self, p: 'Package'):
        if self.import_dns and p.import_dns:
            for i in range(len(self.import_dns)):
                for j in range(len(self.import_dns[i]['Queries'])):
                    if self.import_dns[i]['Queries'][j]['Hostname'] != p.import_dns[i]['Queries'][j]['Hostname']:
                        self.violated_dns[self.import_dns[i]['Queries'][j]['Hostname']] = True

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
        return json.dumps(output, default=lambda o: o.__dict__, sort_keys=True)

# TODO this is dead code; keeping it for future
class Baseline:
    baseline_path = './baselines/{}.json'

    def __init__(self, registry):
        self.registry = registry

        self.baseline_path = self.baseline_path.format(registry)
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
        # print(f'[INFO] Loading baseline from: {self.baseline_path}')

        data = json.load(open(self.baseline_path))

        self.import_files = data['import']['files']
        self.import_sockets = data['import']['sockets']
        self.import_dns = data['import']['dns']

        self.install_files = data['install']['files']
        self.install_sockets = data['install']['sockets']
        self.install_dns = data['install']['dns']

    def evaluate(self, package: Package):
        # print(f'[INFO] Comparing results with baseline for package: {package.name}')

        self.evaluate_files(self.import_files, package, package.import_files, package.name, 'import')
        self.evaluate_sockets(self.import_sockets, package, package.import_sockets, 'import')
        self.evaluate_dns(self.import_dns, package, package.import_dns, 'import')

        self.evaluate_files(self.install_files, package, package.install_files, package.name, 'install')
        self.evaluate_sockets(self.install_sockets, package, package.install_sockets, 'install')
        self.evaluate_dns(self.install_dns, package, package.install_dns, 'install')

    def evaluate_files(self, baseline_files, package: Package, candidate_files, package_name, command):
        # print(f'[INFO] Comparing files for command: {command}')

        ignore_list = FILE_IGNORE_LIST + [package_name]

        for file in candidate_files:
            needle = [file['Read'], file['Write'], file['Delete']]

            if not any(word in file['Path'] for word in ignore_list):
                if baseline_files.get(file['Path'], []) != needle:
                    # print(f"[CRITICAL] Violated file for command `{command}`: {file['Path']}")
                    package.new_violation('file', file['Path'], {'action': needle, 'command': command})

    def evaluate_sockets(self, baseline_sockets, package: Package, candidate_sockets, command):
        # print(f'[INFO] Comparing sockets for command: {command}')

        if not candidate_sockets:
            return
        for socket in candidate_sockets:
            needle = socket['Port']

            if baseline_sockets.get(socket['Address'], 0) != needle:
                # print(f"[CRITICAL] Violated socket for command `{command}`: {socket['Address']}")
                package.new_violation('socket', socket['Address'], {'port': socket['Port'], 'hostnames': socket['Hostnames'], 'command': command})

    def evaluate_dns(self, baseline_dns, package: Package, candidate_dns, command):
        # print(f'[INFO] Comparing DNS for command: {command}')

        if not candidate_dns:
            return

        for dns in candidate_dns[0]['Queries']:
            needle = dns['Hostname']

            if baseline_dns.get(needle, False) == False:
                # print(f"[CRITICAL] Violated DNS for command `{command}`: {dns['Hostname']}")
                package.new_violation('dns', dns['Hostname'], {'command': command})

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs='?', type=str, help='original package name')
    parser.add_argument('-t', nargs='?', type=str, help='typosquatting package name')
    parser.add_argument('-r', nargs='?', type=str, help='registry name')
    args = parser.parse_args()

    return args

def main(original_package, typosquatting_package, registry):
    t_package = Package(original_package, registry)
    t_package.run_dynamic_analysis()
    t_package.read_dynamic_analysis_output()
    
    o_package = Package(original_package, registry)
    o_package.run_dynamic_analysis()
    o_package.read_dynamic_analysis_output()

    t_package.compare(o_package)
    print(t_package.get_violation())

if __name__ == '__main__':
    args = init()

    if not (args.p or args.t or args.r):
        print('[ERROR] Usage: sudo python3 module-3.py -p <package-name> -r <registry-name>')
        os._exit(1)

    if args.r and args.r not in ['pypi', 'npm', 'rubygems']:
        print('[ERROR] Use one of: [pypi, npm, rubygems]')
        os._exit(1)

    main(args.p, args.t, args.r)
