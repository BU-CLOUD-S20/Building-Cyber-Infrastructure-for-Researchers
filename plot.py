
#import plotly.plotly as py
#from plotly.graph_objs import *
#import plotly.express as px
import json
from numpy import array

f=  open('test.json')
d= json.load(f)
x=[]
for i in d['data']:
	int(i)
	print (i["value"])

'''
for j in d['values']:
	y=j

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
