"""vtools
"""
from sys import argv
import os
import subprocess
from csv import DictWriter
from tabular_log import tabular_log

__author__ = "help@castellanidavide.it"
__version__ = "01.01 2021-3-16"

class vtools:
	def __init__ (self, other=None):
		"""Where it all begins
		"""
		self.setup(other)
		self.get_machines()
		try:
			self.core()
		except:
			print("Error: make sure you have installed vbox on your PC")
		print(self.vmachines)

	def setup(self, other):
		"""Setup
		"""
		# Define main variabiles
		self.verbose = True
		self.csv = True
		self.vboxmanage = '"C:\Work\VBoxManage"' if os.name == 'nt' else "vboxmanage"

		# Define log
		self.log = tabular_log("C:/Program Files/vtools/trace.log" if os.name == 'nt' else "~\trace.log", title = "vtools" ,verbose = self.verbose)
		self.log.print("Created log")

		if self.csv:
			# Define files
			self.OS = "OS.csv" #os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "flussi", "OS.csv") if os.name == 'nt' else "OS.csv"
			self.net = "net.csv" #os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "flussi", "net.csv") if os.name == 'nt' else "net.csv"
			self.OSheader = "PC_name,OS"
			self.net_header = "PC_name,network_card_name,V4,MAC,Attachment"
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
			if self.csv:
				try:
					DictWriter(open(self.OS, 'a+', newline=''), fieldnames=self.OSheader.split(","), restval='').writerow({"PC_name": PC, "OS": self.get_os(PCcode)})
				except:
					self.log.print(f"Error taking {PC} OS")
				for i in self.get_net(PCcode):
					try:
						net = {"PC_name": PC}
						for key, value in zip(self.net_header.split(",")[1:], i):
							net[key] = value
						DictWriter(open(self.net, 'a+', newline=''), fieldnames=self.net_header.split(","), restval='').writerow(net)
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
		cmd = self.vboxmanage
		for i in array:
			if " " in i:
				i = "'" + i + "'"
			cmd += " "  + i

		return vtools.remove_b(subprocess.check_output(cmd, shell=False))

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

def laucher(other=None):
	"""Lanch all
	"""
	vtools(other)
		
if __name__ == "__main__":
	laucher('--choco')
