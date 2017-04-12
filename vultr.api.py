作者：QI
链接：https://www.zhihu.com/question/33840488/answer/121266925
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

# coding: utf-8

import sys, requests, socket
# 自己写的日志类
from Utils import logging

import platform

if platform.platform().startswith("Windows"):
	import win_inet_pton

class VultrManager():

	def __init__(self, account):
		self.name = socket.gethostname()
		self.proxies = {"http": "socks5://127.0.0.1:1081", "https": "socks5://127.0.0.1:1081"}
		if account == "account1":
			key = "key of account1"
			self.SSHKEYID = "57bbfc97ae887"
			self.SCRIPTID = 21252
		elif account == "account2":
			key = "key of account2"
			self.SSHKEYID = "57c8e90240e81"
			self.SCRIPTID = 21554
		self.api = {"API-KEY": key}

	def listServers(self):
		url = "https://api.vultr.com/v1/server/list"
		res = requests.get(url, headers = self.api, proxies = self.proxies)
		servers = res.json()
		return servers

	def getServerInfo(self, mid):
		servers = self.listServers()
		for server in servers:
			serverId = server
			hostname = servers[serverId]["label"]
			hostId = hostname.split("-")[-1]
			if hostId == mid:
				for info in servers[serverId]:
					print info + "\t" + str(servers[serverId][info])

	def getServersInfo(self):
		infos = []
		servers = self.listServers()
		for server in servers:
			serverId = server
			hostname = servers[serverId]["label"]
			ip = servers[serverId]["main_ip"]
			info = [serverId, hostname, ip]
			infos.append(info)
			print serverId + "\t" + hostname + "\t" + ip
		return infos

	def getOneId(self, mid):
		servers = self.listServers()
		for server in servers:
			serverId = server
			hostname = servers[serverId]["label"]
			hostId = hostname.split("-")[-1]
			if hostId == mid:
				return serverId, hostname
		return None, None

	def createOne(self, mids):
		if not type(mids) == list:
			mids = [mids]
		url = "https://api.vultr.com/v1/server/create"
		serverId = None
		for mid in mids:
			name = hostGroup + "-" + str(mid)
			argvs = {
				"DCID": 19,
				"OSID": 160,
				"VPSPLANID": 29,
				"SCRIPTID": self.SCRIPTID,
				"SSHKEYID": self.SSHKEYID,
				"hostname": name,
				"label": name
			}
			res = requests.post(url, headers = self.api, data = argvs, proxies = self.proxies)
			if res.status_code != 200:
				log = "create server " + name + " failed, " + res.text
				logging("e", log)
			else:
				serverId = res.json()["SUBID"]
				log = "server " + name + " created, its id is " + serverId
				logging("i", log)
		return serverId

	def createMany(self, start, end):
		for i in range(start, end+1):
			self.createOne(i)

	def destroyOne(self, mids):
		if not type(mids) == list:
			mids = [mids]
		result = None
		for mid in mids:
			serverId, hostname = self.getOneId(mid)
			url = "https://api.vultr.com/v1/server/destroy"
			data = {"SUBID": serverId}
			res = requests.post(url, headers = self.api, proxies = self.proxies, data = data)
			if res.status_code == 200:
				log = hostname + " destroyed"
				logging("i", log)
				result = True
			else:
				log = "Failed, status code: " + str(res.status_code)
		return result

	def rebootOne(self, mids):
		if not type(mids) == list:
			mids = [mids]
		result = None
		for mid in mids:
			serverId, hostname = self.getOneId(mid)
			url = "https://api.vultr.com/v1/server/reboot"
			data = {"SUBID": serverId}
			res = requests.post(url, headers = self.api, proxies = self.proxies, data = data)
			if res.status_code == 200:
				log = hostname + " rebooted"
				logging("i", log)
				result = True
			else:
				log = "Failed, status code: " + str(res.status_code)
		return result

	def destroyMe(self):
		hostId = self.name.split("-")[-1]
		serverId, hostname = self.getOneId(hostId)
		if not serverId:
			log = "can not find you, misson failed"
			logging("e", log)
			return
		else:
			sd = self.destroyOne(hostId)
			return sd

	def destroyAll(self):
		servers = self.getServersInfo()
		for server in servers:
			serverId, hostname, ip = server
			hostId = hostname.split("-")[-1]
			self.destroyOne(hostId)

	def rebootAll(self):
		servers = self.getServersInfo()
		for server in servers:
			serverId, hostname, ip = server
			hostId = hostname.split("-")[-1]
			self.rebootOne(hostId)

	def updateScript(self):
		url = "https://api.vultr.com/v1/startupscript/update"
		with open("vultr.sh", "r") as f:
			script = f.read()
		data = {
			"SCRIPTID": self.SCRIPTID,
			"name": "default",
			"script": script
		}
		res = requests.post(url, headers = self.api, proxies = self.proxies, data = data)
		if res.status_code == 200:
			log = str(self.SCRIPTID) + " updated"
			logging("i", log)
		else:
			print res.status_code

if __name__ == "__main__":
	hostGroup = "yourgroup"
	account = sys.argv[1]
	mode = sys.argv[2]
	vultrManager = VultrManager(account)
	if mode == "ia":
		vultrManager.getServersInfo()
	elif mode == "io":
		mid = sys.argv[3]
		vultrManager.getServerInfo(mid)
	elif mode == "co":
		mids = []
		for i in range(len(sys.argv)-3):
			mid = sys.argv[i+3]
			mids.append(mid)
		vultrManager.createOne(mids)
	elif mode == "cm":
		mid_s = int(sys.argv[3])
		mid_e = int(sys.argv[4])
		vultrManager.createMany(mid_s, mid_e)
	elif mode == "do":
		mids = []
		for i in range(len(sys.argv)-3):
			mid = sys.argv[i+3]
			mids.append(mid)
		vultrManager.destroyOne(mids)
	elif mode == "dm":
		vultrManager.destroyMe()
	elif mode == "da":
		vultrManager.destroyAll()
	elif mode == "ro":
		mids = []
		for i in range(len(sys.argv)-3):
			mid = sys.argv[i+3]
			mids.append(mid)
		vultrManager.rebootOne(mids)
	elif mode == "ra":
		vultrManager.rebootAll()
	elif mode == "us":
		vultrManager.updateScript()