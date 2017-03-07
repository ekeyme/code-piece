#!/home/mozz/opt/bin/python3

import time
from pyquery import PyQuery
import random
import urllib.request
import json

urlBus326HuangToTian = 'http://m.tool.finded.net/index.php?m=Bus&c=Bus&a=refresh&l=Ysaa4uFcm75skQuLm0TI1w-2x-2x/0'
urlBus326TianToHuang = 'http://m.tool.finded.net/index.php?m=Bus&c=Bus&a=refresh&l=Ysaa4uFcm75skQuLm0TI1w-2x-2x/1'
BusStateCode_Here = 1
BusStateCode_Left = 0

def contentFromFileForDev():
	content = {}
	with open('TianToHuang') as f:
		content['status'] = 1
		content['info'] = f.read()
	return content
 
#response = contentFromFileForDev()
response = urllib.request.urlopen(urlBus326TianToHuang).read()[3:].decode()
response = json.loads(response)
status = response['status']
if status == 1:
	content = response['info']

	pqContent = PyQuery(content)('#upInfo li')
	#print(pqContent.size())
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	stationIndex=0
	busInfo = []
	for station in pqContent:
		stationIndex+=1

		pqStation = PyQuery(station)
		stationName = pqStation('.station').text().strip()
		stationInfo = {}
		if stationName:
			stationInfo[stationName] = []

			buses = pqStation.find('.bus')
			if buses.size() > 0:
				for bus in buses:
					if PyQuery(bus).attr('style'): # 已经离开此站
						BusStateCode = BusStateCode_Left
					else:
						BusStateCode = BusStateCode_Here
					stationInfo[stationName].append(BusStateCode)

			busInfo.append(stationInfo)

print(busInfo)

#help(PyQuery)