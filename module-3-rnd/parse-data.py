import os
import json

files = os.listdir('./data')

## IMPORT COMMAND ##

# map of file path to tuple(read, write, delete)
# file_path -> (1,1,1)
import_files_whitelist = {}

# map of addresses to port
# IP address -> port
import_sockets_whitelist = {}

# map of DNS to True
# hostname -> True
import_dns_whitelist = {}

#####################################

## INSTALL COMMAND ##

# map of file path to tuple(read, write, delete)
# file_path -> (1,1,1)
import_files_whitelist = {}

# map of addresses to port
# IP address -> port
import_sockets_whitelist = {}

# map of DNS to True
# hostname -> True
import_dns_whitelist = {}

#####################################

def parse_files(files):
    parsed_files = {}
    
    for _file in files:
        parsed_files[_file['Path']] = (_file['Read'], _file['Write'], _file['Delete'])

    return parsed_files

def parse_sockets(sockets):
    parsed_sockets = {}
    
    for _socket in sockets:
        parsed_sockets[_socket['Address']] = _socket['Port']

    return parsed_sockets

def parse_dns(dns):
    parsed_dns = {}
    
    for _dns in dns[0]['Queries']:
        parsed_dns[_dns['Hostname']] = True

    return parsed_dns

# for file in files:
for file in ['0.6.0.json']:
    # Opening JSON file
    f = open(f'./data/{file}')

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    package_name = data['Package']['Name']
    
    import_files = data['Analysis']['import']['Files']
    import_sockets = data['Analysis']['import']['Sockets']
    import_dns = data['Analysis']['import']['DNS']

    install_files = data['Analysis']['install']['Files']
    install_sockets = data['Analysis']['install']['Sockets']
    install_dns = data['Analysis']['install']['DNS']

    ##### IMPORT #####
    import_files_whitelist = parse_files(import_files)

    if len(import_sockets) > 0:
        import_sockets_whitelist = parse_sockets(import_sockets)
    
    if import_dns:
        if import_dns['Queries']:
            import_dns_whitelist = parse_dns(import_dns)

    ##### INSTALL #####
    install_files_whitelist = parse_files(install_files)

    if len(install_sockets) > 0:
        install_sockets_whitelist = parse_sockets(install_sockets)
    
    if install_dns:
        if install_dns[0]['Queries']:
            install_dns_whitelist = parse_dns(install_dns)

    # Closing file
    f.close()

    print(json.dumps(import_files_whitelist))
    print(json.dumps(import_sockets_whitelist))
    print(json.dumps(import_dns_whitelist))

    print(json.dumps(install_files_whitelist))
    print(json.dumps(install_sockets_whitelist))
    print(json.dumps(install_dns_whitelist))
