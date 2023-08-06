import os
import json
import requests



ROOT = os.path.dirname(os.path.abspath(__file__))
sample_tree_file = os.path.join(ROOT,"sample_tree.py")
def add_numbers(num1,num2):
	return num1+num2

def analyze_data(filename):
	modules = []
	classes = []
	res = {}
	current_class = ''
	data = open(filename)
	for x in data:
		if 'import' in x or 'from' in x:
			modules.append(x)

		if 'class' in x:
			classes.append(x)
			c = x.split(' ')
			if c[0] == 'class':
				current_class = x.strip()
				res[current_class] = {
					'defs': [],
					'classes': []
				}
			# print('new class, ' , x)
			else:
				if current_class != '':
					# print('old class', x)
					res[current_class]['classes'].append(x.strip())

		if 'def' in x:
			if current_class != '':
				res[current_class]['defs'].append(x.strip())

	d = {}

	d['cls'] = res

	d['modules'] = modules
	# obj = json.dumps(res, indent=4)
	data.close()

	return d


def addNode(name, typed, childof, n_deci, children, pos):
	ob = {
		"nodeName": name,
		"name": "NODE NAME {0:.1f}".format(n_deci),
		"type": "type2",
		"typed": "module",

		"link": {
			"name": "Link node {0:.1f} to {1:.1f}".format(childof, n_deci),
			"nodeName": "NODE NAME {0:.1f}".format(n_deci),
			"direction": "SYNC"
		},
		"children": children
	}
	if pos == 'root':
		ob['name'] = name
		ob['link']['nodeName'] = name
		ob['link']['name'] = "Link NODE NAME 1.0"
		ob['type'] = 'type1'
		ob['typed'] = 'module'

	return ob



def get_childs(x):
	n_deci = 1.1
	n = 1.1
	r = addNode(x.split('/')[-1], "type1", n, n_deci, [], 'root')
	n_deci = 1.1
	n = 1.1

	fData = analyze_data(x)
	cl = addNode(x.split('/')[-1], "type2", n, n_deci + 1, [], 'child')
	c = {}
	for cls in fData['cls']:
		c['classes'] = addNode(cls, "type2", n, n_deci + 1, [
			addNode("Classes", "type2", n, n_deci + 2, [], 'child'),
			addNode("functions", "type2", n, n_deci + 2, [], 'child')
		], 'child')
		for x in fData['cls'][cls]['classes']:
			n_deci += 1
			c['classes']['children'][0]['children'].append(addNode(x, "type2", n, n_deci + 3, [], 'child'))
		for x in fData['cls'][cls]['defs']:
			n_deci += 1
			c['classes']['children'][1]['children'].append(addNode(x, "type2", n, n_deci + 3, [], 'child'))
	n_deci += 1
	n = n_deci
	cl['children'] = [c['classes']]
	r['children'].append(cl)
	return cl

def file_traverse(path,output_dir):
    root = get_childs(path)
    with open(sample_tree_file) as fildata:
        data = "".join(fildata.readlines())
        
    data += '<script>treeBoxes("", {0});</script>'.format(root)
    os.chmod(output_dir, 0o777)
    output_dir = os.path.join(output_dir + '/dtree.html')
    
    with open(output_dir, 'w') as f:
        f.write(data)
		
	
    return  {'tree' : root}



def folder_files_traverse(folder,output_dir):
	childrens = []
	files = os.listdir(folder )
	d = folder.split('/')[-1]
	if d == '': d = folder.split('/')[-2]
	for x in os.listdir(folder):
		if x.endswith('.py'):
			childrens.append(get_childs(folder + x))
	root = addNode(d, "type1", 0, 0, childrens, 'root')
	
	with open(sample_tree_file) as fildata:
		data = "".join(fildata.readlines())
		
	data += '<script>treeBoxes("", {0});</script>'.format(root)
	
	os.chmod(output_dir, 0o777)
	output_dir = os.path.join(output_dir + '/dtree.html')
	
	with open('dtree.html', 'w') as f:
		f.write(data)

	
	return {'tree' : root}
	

def jsonsql(dfjson,tname,sqlstr):
    sqlstr=""
    for x in dfjson.columns:
        for y in dfjson.take(1):
            y=dfjson.select("`"+x+"`").take(1)[0][0]
            try:
                if isfloat(y):
                    sqlstr+="  "+x+"  INTEGER NOT NULL,"+"\n"
                else:
                    try:
                        (datetime.datetime.strptime(str(y), '%Y-%m-%d'))==True
                        sqlstr+="  "+x+"  timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),"+"\n"
                    except:
                        sqlstr+="  "+x+"  VARCHAR,"+"\n"
            except:
                #sqlstr+="  "+x+"  VARCHAR,"+"\n"
                print("Unkown")

    finalsql="CREATE TABLE " + tname + "("+sqlstr+")"
    return finalsql



'''
#====================================EXAMPLE FOR COMPLETE FOLDER===============================
data = folder_files_traverse(folder)
f = open(outputfile, 'w')
print(data)
f.write(json.dumps( data, indent=4))
f.close()

'''
#====================================EXAMPLE FOR SINGLE FILE===============================
#data = file_traverse(filename)
#f = open(outputfile)
#f.write(json.dumps( data, indent=4))
#print(data)
#f.close()

def demo():
	path = os.path.join(ROOT, "sample_python_file.py")
	output_dir = ROOT
	data = file_traverse(path,output_dir)
	print("Demo file create successfully in " + output_dir )

