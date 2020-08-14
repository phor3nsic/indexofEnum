import requests
import sys
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://www.smartvivoempresa.com.br/wp-content/uploads/"
extenxions = ['.txt','.sql','.zip','.rar','.bak','.old','.csv','.xml','.doc','.docx']
DIRS = []
debug = True
proxy_debug = None

proxy = {
	"http":"http://127.0.0.1:8080",
	"https":"http://127.0.0.1:8080"
}

if debug == True:
	proxy_debug = proxy

def check():
	req = requests.get(url, proxies=proxy_debug, verify=False)
	if req.status_code == 200 and "Index of" not in  req.text:
		print("[-]No Index of found!")
		sys.exit()

def checkExt(url, path):
	if path == None:
		path = ""

	req = requests.get(url+path, proxies=proxy_debug, verify=False)
	for x in extenxions:
		if x in req.text:
			print(f"{url+path}/{x}")

def getContent(url,path):
	global DIRS

	if path == None:
		path = ""

	page = requests.get(url+path, proxies=proxy_debug, verify=False)
	soup = BeautifulSoup(page.content, "html.parser")
	content = []

	for x in soup.find_all("a"):
		if x.get("href")[-1] == "/":
			content.append(x.get("href"))
	del content[0:1]

	for x in content:
		DIRS.append(path+x)
	
def main():
	check()
	checkExt(url, None)
	getContent(url, None)
	for x in DIRS:
		checkExt(url, x)
		getContent(url, x)

	print(DIRS)

if __name__ == '__main__':
	main()


