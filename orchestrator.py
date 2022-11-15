import json
import argparse
import subprocess

valid_registries = ['npm', 'pypi', 'rubygems']

class package:
    def __init__(self, name, registry) -> None:
        self.name = name
        self.registry = registry

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', nargs='?', default='packages.txt', type=str)
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

        package_list.append(package(blocks[0], blocks[1].strip()))

    return package_list

def run_module_1(package):
    print(f'[INFO] Running module 1 (candidate generator) for package: {package.name}')

    result = subprocess.run(['typogenerator/typogenerator', '-s', package.name, '-r', package.registry, '-p'], stdout=subprocess.PIPE)

    candidates = result.stdout.decode('utf-8').splitlines()

    return candidates

def main(file):
    # read and parse packages from file
    package_list = read_packages_from_file(file)

    module_1_json_list = {}

    # run module 1 for each package
    for p in package_list:
        candidates = run_module_1(p)
        candidates = json.loads(candidates[0])

        module_1_json_list[p.name] = candidates

    print(json.dumps(module_1_json_list, indent=4))

if __name__=='__main__':
    args = init()
    main(args.f)
