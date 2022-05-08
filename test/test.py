import requests
import time
import os

url = os.environ['URL']
token = "Token %s" %(os.environ['TOKEN'])

payload={}
headers = {
  'Authorization': token,
  'Cookie': 'csrftoken=yc2sLIXFTW23VvGOJ3pIlaxodrFf35BkCszPSvhbBMlGsfp6oWJTMknklWFXFneI'
}

for i in range(100):
	response = requests.request("GET", url, headers=headers, data=payload)
	print(response.text)
	time.sleep(1)
