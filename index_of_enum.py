import requests
import sys
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if len(sys.argv) < 2:
	print(f"Ex: {sys.argv[0]} http://taget.com/files")
	sys.exit()

url = sys.argv[1]
extenxions = ['.txt','.sql','.zip','.rar','.bak','.old','.csv','.xml','.doc','.docx','.php','.py','.asp', '.aspx']
DIRS = []
debug = True
proxy_debug = None

HEADER = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0"
}

proxy = {
	"http":"http://127.0.0.1:8080",
	"https":"http://127.0.0.1:8080"
}

if debug == True:
	proxy_debug = proxy

def check():
	req = requests.get(url, proxies=proxy_debug, verify=False, headers=HEADER)
	if req.status_code == 200 and "Index of" not in  req.text:
		print("[-]No Index of found!")
		sys.exit()

def checkExt(url, path):
	if path == None:
		path = ""
	page = requests.get(url+path, proxies=proxy_debug, verify=False, headers=HEADER)
	soup = BeautifulSoup(page.content, "html.parser")
	for x in soup.find_all("a"):
		for y in extenxions:
			if y in x.get("href"):
				print(f"[+]{url}{path}{x.get('href')}")

def checkGit(url, path):
	if path == None:
		path = ""
	page = requests.get(url+path+"/.git/HEAD", proxies=proxy_debug, verify=False, headers=HEADER)
	if page.status_code == 200:
		print(f"[+]{url}{path}/.git/HEAD")
	else:
		pass

def getContent(url,path):
	global DIRS
	if path == None:
		path = ""
	page = requests.get(url+path, proxies=proxy_debug, verify=False, headers=HEADER)
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
	checkGit(url, None)
	for x in DIRS:
		checkExt(url, x)
		checkGit(url,x)
		getContent(url, x)

if __name__ == '__main__':
	main()


