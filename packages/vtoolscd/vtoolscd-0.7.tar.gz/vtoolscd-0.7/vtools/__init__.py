"""vtools
"""
from sys import argv
import os
import subprocess
from csv import DictWriter
from tabular_log import tabular_log
from json import loads, dumps
import requests

__author__ = "help@castellanidavide.it"
__version__ = "01.01 2021-3-16"

class vtools:
	def __init__ (self, verbose=False, csv=False, dbenable=False, dburl=None, dbtoken=None, dbOStable=None, dbNETtable=None):
		"""Where it all begins
		"""
		self.setup(verbose, csv, dbenable, dburl, dbtoken, dbOStable, dbNETtable)
		self.get_machines()
		self.core()
		try:
			self.core()
		except:
			print("Error: make sure you have installed vbox on your PC")
		print(self.vmachines)

	def setup(self, verbose, csv, dbenable, dburl, dbtoken, dbOStable, dbNETtable):
		"""Setup
		"""
		# Define main variabiles
		self.verbose = verbose
		self.csv = csv
		self.dbenable = dbenable
		self.dburl = dburl
		self.dbtoken = dbtoken
		self.dbOStable = dbOStable
		self.dbNETtable = dbNETtable
		self.vboxmanage = '"C:\Work\VBoxManage"' if os.name == 'nt' else "vboxmanage"

		# Define log
		try:
			self.log = tabular_log("C:/Program Files/vtools/trace.log" if os.name == 'nt' else "~/trace.log", title = "vtools" ,verbose = self.verbose)
		except:
			self.log = tabular_log("trace.log", title = "vtools" ,verbose = self.verbose)
		self.log.print("Created log")

		# Headers
		self.OSheader = "PC_name,OS"
		self.net_header = "PC_name,network_card_name,IPv4,MAC,Attachment"
		self.log.print("Headers inizialized")

		if self.csv:
			# Define files
			self.OS = "OS.csv"
			self.net = "net.csv"
			self.log.print("Defined CSV files' infos")

			# Create header if needed
			try:
				if open(self.OS, 'r+').readline() == "":
					assert(False)
			except:
				open(self.OS, 'w+').write(self.OSheader + "\n")

			try:
				if open(self.net, 'r+').readline() == "":
					assert(False)
			except:
				open(self.net, 'w+').write(self.net_header + "\n")
			
			self.log.print("Inizialized CSV files")

	def core(self):
		"""Core of all project
		"""
		for PC, PCcode in zip(self.vmachines, self.vmachinescodes):
			try:
				OS = self.get_os(PCcode)
				if self.csv:
					DictWriter(open(self.OS, 'a+', newline=''), fieldnames=self.OSheader.split(","), restval='').writerow({"PC_name": PC, "OS": OS})
				if self.dbenable:
					try:
						response = requests.request("POST", f"{self.dburl}", headers={'Content-Type': 'application/json','Authorization': f'''Basic {self.dbtoken}'''}, data=dumps({"operation": "insert", "schema": "dev", "table": self.dbOStable, "records": [{"PC_name": PC, "OS": OS}]}))
						self.log.print(f"By DB: {response.text}")
					except:
						self.log.print(f"Failed the DB insert")
			except:
				self.log.print(f"Error taking {PC} OS")

			for i in self.get_net(PCcode):
				try:
					net = {"PC_name": PC}
					for key, value in zip(self.net_header.split(",")[1:], i):
						net[key] = value

					if self.csv:
						DictWriter(open(self.net, 'a+', newline=''), fieldnames=self.net_header.split(","), restval='').writerow(net)
					if self.dbenable:
						try:
							response = requests.request("POST", f"{self.dburl}", headers={'Content-Type': 'application/json','Authorization': f'''Basic {self.dbtoken}'''}, data=dumps({"operation": "insert", "schema": "dev", "table": self.dbNETtable, "records": [net]}))
							self.log.print(f"By DB: {response.text}")
						except:
							self.log.print(f"Failed the DB insert")
				except:
					self.log.print(f"Error taking {PC} network ifos")

			self.log.print("Stored into csv file(s)")

	def get_machines(self):
		"""Get virtual machines' name
		"""
		self.vmachines = []
		self.vmachinescodes = []
		temp=""
		take=False
		temp2=""
		take2=False

		for i in self.get_output(["list", "vms"]):
			if i == '"':
				if take == True:
					self.vmachines.append(temp)
					temp = ""
				take = not take
			elif take:
				temp += i

			if i == '{' or i == '}':
				if take2 == True:
					self.vmachinescodes.append(temp2)
					temp2 = ""
				take2 = not take2
			elif take2:
				temp2 += i

		self.log.print(f"Get VM names {self.vmachines} {self.vmachinescodes}")

	def get_output(self, array):
		""" Gets the output by the shell
		"""
		if os.name == 'nt':
			cmd = self.vboxmanage
			for i in array:
				if " " in i:
					i = "'" + i + "'"
				cmd += " "  + i

			return vtools.remove_b(subprocess.check_output(cmd, shell=False))
		else:
			return vtools.remove_b(subprocess.Popen([self.vboxmanage] + array, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0])

	def get_os(self, machine_name):
		""" Gets the vitual machine os
		"""
		_os = self.get_output(["guestproperty", "get", machine_name, "/VirtualBox/GuestInfo/OS/Product"]).replace("Value: ", "").replace("\\n", "").replace("\\r", "")
		self.log.print(f"Getted OS {_os}")
		return _os

	def remove_b(string):
		"""Removes b'' by string
		"""
		return str(string).replace("b'", "")[:-1:]
	
	def get_net(self, machine_name):
		""" Gets the vitual machine network's infos
		"""
		network = []
		temp = []
		attachments = self.get_attachments(machine_name)

		try:
			propriety = "Count"
			
			for i in range(int(self.get_output(["guestproperty", "get", machine_name, f"/VirtualBox/GuestInfo/Net/{propriety}"]).replace("Value: ", "").replace("\\n", "").replace("\\r", ""))):
				for propriety in ["Name", "V4/IP", "MAC"]:
					temp.append(vtools.remove_b(self.get_output(["guestproperty", "get", machine_name, f"/VirtualBox/GuestInfo/Net/{i}/{propriety}"]).replace("Value: ", "").replace("\\n", "").replace("\\r", "")))

				network.append(temp + [attachments[i]])
				temp = []
		except:
			pass

		self.log.print(f"Getted network infos {network}")
		return network

	def get_attachments(self, machine_name):
		""" Gets the vitual machine attachment
		"""
		attachments = []

		for i in self.get_output(["showvminfo", machine_name]).replace("\\r", "").split("\\n"):
			if "NIC" in i and "disabled" not in i:
				for j in i[i.find('MAC'):].split(", "):
					if "Attachment" in j:
						attachments.append(j.replace("Attachment: ", ""))

		self.log.print("Getted attachments")
		return attachments

def laucher():
	""" Read params lauch all
	"""
	debug = "--debug" in argv or "-d" in argv
	csv = "--csv" in argv
	dbenable = dburl = dbtoken = dbOStable = dbNETtable = None

	for arg in argv:
		if "--url=" in arg:
			dburl = arg.replace("--url=", "")
		if "--token=" in arg:
			dbtoken = arg.replace("--token=", "")
		if "--OStable=" in arg:
			dbOStable = arg.replace("--OStable=", "")
		if "--NETtable=" in arg:
			dbNETtable = arg.replace("--NETtable=", "")

	print(dburl, dbtoken, dbOStable, dbNETtable)

	if dburl != None and dbtoken != None and dbOStable != None and dbNETtable != None:
		vtools(debug, csv, True, dburl, dbtoken, dbOStable, dbNETtable)
	else:
		vtools(debug, csv)
		
if __name__ == "__main__":
	laucher()
