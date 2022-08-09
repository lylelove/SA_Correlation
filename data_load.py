import json
import numpy as np
import requests
from pyecharts import options as opts
from pyecharts.charts import Graph

hd = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/99.0.4844.82 Safari/537.36'}
url = 'https://xuanguapi.eastmoney.com/Stock/JS.aspx?type=xgq&sty=xgq&token=eastmoney&c=[gf2]&p=1&jn=kuAPFImR&ps=500&s=stockcode&st=1&r=1659237663728'
response = requests.get(url, headers=hd)
info = response.text
info = info[13:len(info)]
info = json.loads(info)
SA_list = {}
for i in info['Results']:
    SA_list[i[2:8]] = i[9:len(i) - 2]
all_lines = []
data = []
for i in range(1, 18):
    temp = []
    with open('data' + str(i) + '.json', 'r') as read_file:
        temp = json.load(read_file)
    for k in range(len(temp)):
        data.append(temp[k])
c_data = []

for i in range(len(data)):
    temp = []
    for j in range(i + 1, len(data)):
        b=[]
        c=[]
        if len(data[i][1]) >= len(data[j][1]):
            for k in range(len(data[j][1])):
                if data[i][1][k][0] == data[j][1][k][0]:
                    b.append(float(data[i][1][k][3]))
                    c.append(float(data[j][1][k][3]))
                if len(b)>500:
                    break
        else:
            for k in range(len(data[i][1])):
                if data[i][1][k][0] == data[j][1][k][0]:
                    b.append(float(data[i][1][k][3]))
                    c.append(float(data[j][1][k][3]))
                if len(b)>500:
                    break
        if len(b)>50:
            ab=np.array(b)
            ac=np.array(c)
            res = np.corrcoef(ab, ac)
            temp.append([res[0, 1],data[i][0],data[j][0]])
    c_data.append(temp)

target_items = []
for i in range(len(c_data)):
    for j in range(len(c_data[i])):
        if c_data[i][j][0] >= 0.5:
            target_items.append(c_data[i][j])

for i in range(len(target_items)):
    target_items[i][1] = SA_list[target_items[i][1]]
    target_items[i][2] = SA_list[target_items[i][2]]

SA_list_demo = set()

for i in range(len(target_items)):
    SA_list_demo.add(target_items[i][1])
    SA_list_demo.add(target_items[i][2])
SA_list_demo = list(SA_list_demo)

nodes = []
for i in range(len(SA_list_demo)):
    nodes.append(opts.GraphNode(name=SA_list_demo[i], symbol_size=10))
links = []
for i in range(len(target_items)):
    links.append(opts.GraphLink(source=target_items[i][1], target=target_items[i][2]))
c = (
    Graph()
    .add(
        "",
        nodes,
        links,
        repulsion=400,
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Graph-GraphNode-GraphLink-WithEdgeLabel")
    )
    .render("graph_with_edge_options.html")
)
