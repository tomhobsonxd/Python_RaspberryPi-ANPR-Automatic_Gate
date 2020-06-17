import json

data = {}
data['plates'] = []
data['plates'].append({
    'name': 'Ryan L',
    'plate': 'TIS RDL',
    'make': 'TOYOTA',
    'model': 'GT86',
    'year': '2014'
})
data['plates'].append({
    'name': 'Ryan W',
    'plate': 'YEET',
    'make': 'NISSAN',
    'model': 'NIVARA',
    'year': '2016'
})
data['plates'].append({
    'name': 'Sarah L',
    'plate': 'RABBIT',
    'make': 'VAUXHALL',
    'model': 'MOKKA',
    'year': '2014'
})
data['plates'].append({
    'name': 'Steve L',
    'plate': 'TIS RDL',
    'make': 'TOYOTA',
    'model': 'GT86',
    'year': '2014'
})
data['plates'].append({
    'name': 'Sue L',
    'plate': 'TIS RDL',
    'make': 'TOYOTA',
    'model': 'GT86',
    'year': '2014'
})

with open('plates.json', 'w') as outfile:
    json.dump(data, outfile)