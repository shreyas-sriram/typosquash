import csv
import json
import subprocess
from datetime import datetime

script_start_time = datetime.now()
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
        line_count += 1

dataset = dict(sorted(dataset.items()))

# print(json.dumps(dataset, indent=1))
print(f'Found {len(dataset)} typosquatting victims from the dataset.')

print(f'Running candidate generator...')

missed = 0
missed_candidates_text = []

for victim, attackers in dataset.items():
    start_time = datetime.now()
    
    result = subprocess.run(['go', 'run', 'cmd/typogen/main.go', '-s', victim, '-p'], stdout=subprocess.PIPE)

    end_time = datetime.now()

    print(f'Time to generate candidates for {victim}: {end_time - start_time}')

    candidates = result.stdout.decode('utf-8').splitlines()

    for attacker in attackers:
        if attacker not in candidates:
            missed += 1
            missed_candidates_text.append(f'Missed attacker: {attacker} for victim: {victim}')
            # print(f'Missed attacker: {attacker} for victim: {victim}')
    

script_end_time = datetime.now()

print(f'Missed: {missed} of total: {line_count - 1}')
print(f'Miss percentage: {missed / (line_count - 1) * 100}')
print(f'Duration: {script_end_time - script_start_time}')
print(f'Missed candidates:')
print('\n'.join(missed_candidates_text))
