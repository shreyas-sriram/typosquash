import csv
import json
import subprocess

dataset = {}

with open('dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count = 1
            continue
        else:
            attacker = row[0]
            victim = row[1]

            if victim in dataset:
                dataset[victim].append(attacker)
            else:
                dataset[victim] = [attacker]
            # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')

print(json.dumps(dataset, indent=1))
print(f'Found {len(dataset)} typosquatting victims from the dataset.')

print(f'Running candidate generator...')

for victim, attackers in dataset.items():
    # print(k, v)

    result = subprocess.run(['go', 'run', 'cmd/typogen/main.go', '-s', victim, '-p'], stdout=subprocess.PIPE)
    candidates = result.stdout.decode('utf-8').splitlines()

    for attacker in attackers:
        if attacker not in candidates:
            print(f'Missed attacker: {attacker} for victim: {victim}')
