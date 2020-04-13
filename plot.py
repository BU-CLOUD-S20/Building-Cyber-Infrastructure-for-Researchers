
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.express as px
import json


'''
previous group used json file with the following formatting:
body: { 
	'y':[],
 	'xlab': 'Time'
 	'ylab': 'Mean GCC'
 	 'x':[]
 	 }
'''

f=  open('view.json')
d= json.load(f)
y_data=[]
x_data=[]

rawdata = (d['data'])['body']

xdata = rawdata['x']
ydata = rawdata['y']
xlabel=rawdata['xlab']
ylabel=rawdata['ylab']

fig = px.scatter(x=x_data, y=y_data)
fig.show()

#for i in b['body']: #here i is body
#	x_data=x
#	y_data=y
#		print (i)
'''
	for j in i:
		print ((j,i[j]))
	
	for x in loaded_json:
	print("%s: %d" % (x, loaded_json[x]))

	for j in i['body']: 
		for k in j['y']:
			y_data.append(k['y'])
			
		for l in j['x']:
			x_data.append(l['x'])


'''
'''

for i in d['data']:
	int(i)

for j in d
	print (i["value"])p


for j in d['values']:
	x.append(i)
	y.append(i['value'])
fig=px.scatter(x=x_data,y=y_data)
fig.show()
plot_url = py.plot(fig)

'''
'''
    for p in d['data']:
    	print(p)
    	print(['value'])
    	x=p['value']

        #print('anomaly: ' + p['anomaly'])


'''
'''
loaded_json = json.loads(json_data)

py.sign_in('usernam e', 'api_key')
trace1 = {
  "name": "SF Zoo", 
  "type": "bar", 
  "x": [20, 14, 23], 
  "y": ["giraffes", "orangutans", "monkeys"], 
  "marker": {
    "line": {
      "color": "rgba(55, 128, 191, 1.0)", 
      "width": 1
    }, 
    "color": "rgba(55, 128, 191, 0.6)"
  }, 
  "orientation": "h"
}
trace2 = {
  "name": "LA Zoo", 
  "type": "bar", 
  "x": [12, 18, 29], 
  "y": ["giraffes", "orangutans", "monkeys"], 
  "marker": {
    "line": {
      "color": "rgba(255, 153, 51, 1.0)", 
      "width": 1
    }, 
    "color": "rgba(255, 153, 51, 0.6)"
  }, 
  "orientation": "h"
}
data = Data([trace1, trace2])
layout = {"barmode": "stack"}
fig = px.scatter(x=x_data, y=y_data)
plot_url = py.plot(fig)
'''
