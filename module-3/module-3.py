import os
import json
import argparse
import subprocess

package_analysis_script = '/home/shreyas/Downloads/fall-2022/capstone/code/module-3/package-analysis/run_analysis.sh' # CHANGME

FILE_IGNORE_LIST = [
    '.cache', 'site-packages', '__pycache__', '/tmp', 'python3.9', 'https://', # pypi
    '_cacache', 'node_modules', # npm
    '.local', '/usr/local/lib/ruby', # rubygems
    'README', 'pipe:', 'MANIFEST', 'DESCRIPTION', # general
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

        self.violated_files = {}
        self.violated_sockets = {}
        self.violated_dns = {}

        self.ignore_list = FILE_IGNORE_LIST + [name]

        try:
            os.system(f'sudo rm {self.results_dir}/*')
        except:
            pass

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
        self.compare_files(self.import_files, p.import_files, 'import')
        self.compare_sockets(self.import_sockets, p.import_sockets, 'import')
        self.compare_dns(self.import_dns, p.import_dns, 'import')

        self.compare_files(self.install_files, p.install_files, 'install')
        self.compare_sockets(self.install_sockets, p.install_sockets, 'install')
        self.compare_dns(self.install_dns, p.install_dns, 'install')

    def compare_files(self, new, baseline, command):
        new_files = set()
        baseline_files = set()

        for _new in new:
            if not any(word in _new['Path'] for word in self.ignore_list):
                new_files.add((_new['Path'], _new['Write'], _new['Read'], _new['Delete']))

        for _baseline in baseline:
            if not any(word in _baseline['Path'] for word in FILE_IGNORE_LIST):
                baseline_files.add((_baseline['Path'], _baseline['Write'], _baseline['Read'], _baseline['Delete']))

        for el in new_files.difference(baseline_files):
            path, write, read, delete = el
            self.violated_files[path] = {
                'read': read,
                'write': write,
                'delete': delete,
                'command': command,
            }

    def compare_sockets(self, new, baseline, command):
        new_sockets = set()
        baseline_sockets = set()

        if new:
            for _new in new:
                new_sockets.add((_new['Address'], _new['Port']))

        if baseline:
            for _baseline in baseline:
                baseline_sockets.add((_baseline['Address'], _baseline['Port']))

        for el in new_sockets.difference(baseline_sockets):
            address, port = el
            self.violated_sockets[address] = {
                'port': port,
                'command': command,
            }
        
    def compare_dns(self, new, baseline, command):
        new_dns = set()
        baseline_dns = set()

        if new:
            if 'Queries' in new[0] and len(new[0]['Queries']) > 0:
                for _query in new[0]['Queries']:
                    new_dns.add(_query['Hostname'])

        if baseline:
            if 'Queries' in baseline[0] and len(baseline[0]['Queries']) > 0:
                for _query in baseline[0]['Queries']:
                    baseline_dns.add(_query['Hostname'])

        for el in new_dns.difference(baseline_dns):
            hostname = el
            self.violated_dns[hostname] = {
                'command': command,
            }

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
    t_package = Package(typosquatting_package, registry)
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
