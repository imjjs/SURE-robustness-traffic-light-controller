import re
f = ['cd301423', 'ak13scd312024', 'k13scd310046', 'asyncK13scd312339', 'asyncAK13scd010911', 'tttt1']



pattern = re.compile(r'^(\d+) \(-?\d+, \d+, (-?\d+(.\d+)?)\)')

def work(filename, file2):
	data = []
	with open(filename,'r') as f:
		lines = f.readlines()
		for l in lines:
			res = pattern.match(l)
			if None == res:
				continue
			if float(res.group(2)) == -1 or float(res.group(2)) == -2:
				continue
			if int(res.group(1)) >1044:
				data.append( '{0} {1}'.format(res.group(1), float(res.group(2))))
			else:
				data.append( '{0} {1}'.format(res.group(1), float(res.group(2))))

	with open(file2, 'w') as f:
		f.write('\n'.join(data))


if __name__ == '__main__':
    for ff in f:
	work(ff + '.txt', ff + '.data')