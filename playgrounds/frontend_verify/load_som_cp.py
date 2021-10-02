import json

d = json.loads(open('sample_cp.json').read())

print(len(d['weights'][0]))