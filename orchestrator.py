import json
import argparse
import subprocess

valid_registries = ['npm', 'pypi', 'rubygems']

# References
# 1. https://blog.phylum.io/pypi-malware-replaces-crypto-addresses-in-developers-clipboard
forbidden_files = [
    '/etc/passwd', '/etc/shadow', '/etc/group', '/etc/gshadow', '.bash_profile' # linux
    'Start Menu', 'chrome.exe', 'msedge.exe', 'launcher.exe', 'brave.exe' # TODO windows
]

class Package:
    def __init__(self, name, registry) -> None:
        self.name = name
        self.registry = registry
        
        self.candidates = {}
        self.static_violations = {}
        self.dynamic_violations = {}

        self.dynamic_violations_analysis = {}
        self.analysis_output = {} # TODO

    def stringify(self):
        o = f'Name: {self.name}\n'
        o += f'Registry: {self.registry}\n'

        return o

    def run_module_1(self):
        print(f'[INFO] Running module 1 (candidate generator) for package: {self.name}')

        result = subprocess.run(['./module-1/typogenerator/typogenerator', '-s', self.name, '-r', self.registry, '-j', '-v'], stdout=subprocess.PIPE)

        candidates = result.stdout.decode('utf-8').splitlines()

        self.candidates = json.loads(candidates[0])['results']

    def run_module_3(self, original_package: str):
        print(f'[INFO] Running module 3 (dynamic analyzer) for candidate package: {self.name}')

        result = subprocess.run(['sudo', 'python3', 'module-3.py', '-p', original_package, '-t', self.name, '-r', self.registry], stdout=subprocess.PIPE, cwd='./module-3')

        self.dynamic_violations = result.stdout.decode('utf-8').splitlines()[0]

    def get_candidates(self):
        return {'candidates': self.candidates}

    def get_dynamic_violation(self):
        return {'dynamic_violations': self.dynamic_violations}

    def get_dynamic_violation_analysis(self):
        return {'dynamic_violation_analysis': self.dynamic_violations_analysis}

    def evaluate_dynamic_violation(self):
        self.dynamic_violations_analysis['malicious'] = {}
        self.dynamic_violations_analysis['malicious']['files'] = {}
        self.dynamic_violations_analysis['malicious']['sockets'] = {}
        self.dynamic_violations_analysis['malicious']['DNS'] = {}

        self.dynamic_violations_analysis['manual_review'] = {}
        self.dynamic_violations_analysis['manual_review']['files'] = {}

        _dynamic_violations = json.loads(self.dynamic_violations)
        
        _files = _dynamic_violations['files']
        _dns = _dynamic_violations['sockets']
        _sockets = _dynamic_violations['DNS']

        self._evaluate_dynamic_violation_files(_files)
        self._evaluate_dynamic_violation_sockets(_sockets)
        self._evaluate_dynamic_violation_dns(_dns)
        
    def _evaluate_dynamic_violation_files(self, _violated_files):
        for _name, _value in _violated_files.items():
            if _name in forbidden_files:
                self.dynamic_violations_analysis['malicious']['files'][_name] = _value
            else:
                self.dynamic_violations_analysis['manual_review']['files'][_name] = _value

    def _evaluate_dynamic_violation_sockets(self, _violated_sockets):
        for _name, _value in _violated_sockets.items():
            self.dynamic_violations_analysis['malicious']['sockets'][_name] = _value

    def _evaluate_dynamic_violation_dns(self, _violated_dns):
        for _name, _value in _violated_dns.items():
            self.dynamic_violations_analysis['malicious']['DNS'][_name] = _value

    def print_dynamic_violations_analysis(self):
        print(f'\n------------------ Dynamic Analysis Results ------------------')
        
        print(f'------ Malicious Files ------')

        for name, value in self.dynamic_violations_analysis['malicious']['files'].items():
            print(f'-> {name} : {value}')

        print(f'------ Malicious Sockets ------')

        for name, value in self.dynamic_violations_analysis['malicious']['sockets'].items():
            print(f'-> {name} : {value}')

        print(f'------ Malicious DNS ------')

        for name, value in self.dynamic_violations_analysis['malicious']['DNS'].items():
            print(f'-> {name} : {value}')

        print(f'------ Manual Review Files ------')

        for name, value in self.dynamic_violations_analysis['manual_review']['files'].items():
            print(f'-> {name} : {value}')

        print('\n\n')

    def get_candidates_list(self):
        candidates_list = []

        for candidate in self.candidates:
            candidates_list.append(candidate['candidate'][0]['name'])

        return candidates_list

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', nargs='?', default='sample-packages.txt', type=str)
    args = parser.parse_args()

    return args

def read_packages_from_file(file) -> list[Package]:
    package_list = []
    lines = []

    try:
        with open(file) as f:
            lines = f.read().splitlines()
    except:
        print(f'File not found: {file}')

    for line in lines:
        blocks = line.split(',')

        if len(blocks) != 2 or blocks[1].strip() not in valid_registries:
            print(f'[ERROR] Invalid format, ignoring entry: {line}')
            continue

        package_list.append(Package(blocks[0], blocks[1].strip()))

    return package_list

def main(file):
    # read and parse packages from file
    packages = read_packages_from_file(file)

    # run module 1 for each package
    for original_package in packages:
        original_package.run_module_1()
        print(f'[INFO] Found candidates: {", ".join(original_package.get_candidates_list())}')

        for candidate in original_package.get_candidates_list():
            candidate_package = Package(candidate, original_package.registry)

            candidate_package.run_module_3(original_package.name)

            candidate_package.evaluate_dynamic_violation()
            candidate_package.print_dynamic_violations_analysis()

if __name__ == '__main__':
    args = init()
    main(args.f)
