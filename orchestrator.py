import json
import argparse
import subprocess

valid_registries = ['npm', 'pypi', 'rubygems']

class Package:
    def __init__(self, name, registry) -> None:
        self.name = name
        self.registry = registry
        self.candidates = {}

    def stringify(self,):
        o = f'Name: {self.name}\n'
        o += f'Registry: {self.registry}\n'

        return o

    def run_module_1(self):
        print(f'[INFO] Running module 1 (candidate generator) for package: {self.name}')

        result = subprocess.run(['typogenerator/typogenerator', '-s', self.name, '-r', self.registry, '-p'], stdout=subprocess.PIPE)

        candidates = result.stdout.decode('utf-8').splitlines()

        self.candidates = json.loads(candidates[0])

    def get_candidates(self):
        return self.candidates

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', nargs='?', default='sample-packages.txt', type=str)
    args = parser.parse_args()

    return args

def read_packages_from_file(file):
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

    module_1_json_list = {}

    # run module 1 for each package
    for package in packages:
        package.run_module_1()

        module_1_json_list[package.name] = package.get_candidates()

    print(json.dumps(module_1_json_list, indent=4))

if __name__=='__main__':
    args = init()
    main(args.f)
