import os
import json
import argparse
import subprocess

package_analysis_script = '/home/shreyas/Downloads/fall-2022/capstone/code/package-analysis/run_analysis.sh' #CHANGME

FILE_IGNORE_LIST = [
    '.cache', 'site-packages', '__pycache__', '/tmp', 'python3.9', 'https://', # pypi
    ]

import_files_baseline = {}
import_sockets_baseline = {}
import_dns_baseline = {}
install_files_baseline = {}
install_sockets_baseline = {}
install_dns_baseline = {}

class package:
    def __init__(self, name, registry) -> None:
        self.name = name
        self.registry = registry

# class baseline:
#     def __init__(self, name, registry) -> None:
#         self.name = name
#         self.registry = registry

def load_baselines(path):
    data = json.load(open(path))
    
    import_files_baseline = data['import']['files']
    import_sockets_baseline = data['import']['sockets']
    import_dns_baseline = data['import']['dns']

    install_files_baseline = data['install']['files']
    install_sockets_baseline = data['install']['sockets']
    install_dns_baseline = data['install']['dns']

    return import_files_baseline, import_sockets_baseline, import_dns_baseline, install_files_baseline, install_sockets_baseline, install_dns_baseline

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', nargs='?', type=str, help='package name')
    parser.add_argument('-r', nargs='?', type=str, help='registry name')
    args = parser.parse_args()

    return args

def read_dynamic_analysis_output():
    files = os.listdir('/tmp/results')
    f = {}
    
    for file in files:
        if file.endswith('.json'):
            # Opening JSON files
            f = json.load(open(f'/tmp/results/{file}'))

    return f

def run_dynamic_analysis(package):
    print(f'[INFO] Running dyanmic analysis for package: {package.name}')

    subprocess.run(['sudo', package_analysis_script, package.registry, package.name], stdout=subprocess.PIPE)

def evaluate_files(candidate_files, baseline_files, package_name):
    ignore_list = FILE_IGNORE_LIST + [package_name]

    for file in candidate_files:
        needle = [file['Read'], file['Write'], file['Delete']]

        if not any(word in file['Path'] for word in ignore_list):
            if baseline_files.get(file['Path'], []) != needle:
                print(file['Path'])

def evaluate_sockets(candidate_sockets, baseline_sockets):
    for socket in candidate_sockets:
        needle = socket['Port']

        if baseline_sockets.get(socket['Address'], 0) != needle:
            print(socket['Address'])

def evaluate_dns(candidate_dns, baseline_dns):
    for dns in candidate_dns[0]['Queries']:
        needle = dns['Hostname']

        if baseline_dns.get(needle, False) == False:
            print(dns['Hostname'])

def parse_output(data):
    package_name = data['Package']['Name']

    import_files = data['Analysis']['import']['Files']
    import_sockets = data['Analysis']['import']['Sockets']
    import_dns = data['Analysis']['import']['DNS']

    install_files = data['Analysis']['install']['Files']
    install_sockets = data['Analysis']['install']['Sockets']
    install_dns = data['Analysis']['install']['DNS']

    return package_name, import_files, import_sockets, import_dns, install_files, install_sockets, install_dns

def main(package):
    run_dynamic_analysis(package)

    file_contents = read_dynamic_analysis_output()

    package_name, import_files_candidate, import_sockets_candidate, import_dns_candidate, install_files_candidate, install_sockets_candidate, install_dns_candidate = parse_output(file_contents)

    import_files_baseline, import_sockets_baseline, import_dns_baseline, install_files_baseline, install_sockets_baseline, install_dns_baseline = load_baselines(f'/home/shreyas/Downloads/fall-2022/capstone/code/module-3-rnd/{package.registry}/{package.registry}-baseline.json')

    # print(import_files_baseline)
    # print(import_sockets_baseline)
    # print(import_dns_baseline)
    # print(install_files_baseline)
    # print(install_sockets_baseline)
    # print(install_dns_baseline)

    evaluate_files(import_files_candidate, import_files_baseline, package_name)
    
    if import_sockets_candidate and len(import_sockets_candidate) > 0:
        evaluate_sockets(import_sockets_candidate, import_sockets_baseline)

    if import_dns_candidate and len(import_dns_candidate) > 0:
        evaluate_dns(import_dns_candidate, import_dns_baseline)

    evaluate_files(install_files_candidate, install_files_baseline, package_name)
    
    if install_sockets_candidate and len(install_sockets_candidate) > 0:
        evaluate_sockets(install_sockets_candidate, install_sockets_baseline)

    if install_dns_candidate and len(install_dns_candidate) > 0:
        evaluate_dns(install_dns_candidate, install_dns_baseline)

    return 0

if __name__ == '__main__':
    args = init()

    if not (args.p or args.r):
        print('[ERROR] Wrong usage')
        os._exit(1)

    main(package(args.p, args.r))
