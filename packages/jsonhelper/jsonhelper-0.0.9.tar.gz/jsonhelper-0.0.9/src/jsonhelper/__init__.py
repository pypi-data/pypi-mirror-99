
from FormsValidators import Validators
from FormsValidators import FormValidation


import json

class jsontools:
	
	def pretty(data):
		try:
			return json.dumps(json.loads(data),indent=1)
		except:
			return False

	def validate(data):
		try:
			json.loads(data)
		except ValueError as err:
			print(err)
			return False
		return True

	def convertJsonToList(data):
		try:
			return json.loads(data)
		except:
			return False
	
	def convertToJson(data):

		if isinstance(data,dict):

			for k, v in data.items():
				if k.find("'") !=-1 :
					k = k.replace("'","### single quote ###")
     			
				if isinstance(v,str) and v.find("'") !=-1 :
					v = v.replace("'","### single quote ###")

				data[k]=v

			data = str(data)
			data = data.replace("'",'"')
			data = data.replace("### single quote ###","'")
			#data = data.replace('\\',"")

		try:
			return json.dumps(json.loads(data),indent=1)
		except ValueError as err:
			return False

	def open(filename):
		f = open(filename,"r")
		content = f.read()
		f.close()
		return jsontools.convertToJson(content)
	
	def save(content,filename):
		f = open(filename, "w")
		f.write(jsontools.pretty(content) +"\n")
		f.close()

