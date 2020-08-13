import requests
import sys
from bs4 import BeautifulSoup

url = ""
extenxions = ['.txt','.sql','.zip','.rar','.bak','.old','.csv','.xml','.doc','.docx']
direcs = []
debug = False
proxy_debug = None

proxy = {
	"http":"http://127.0.0.1:8080",
	"https":"http://127.0.0.1:8080"
}

if debug == True:
	proxy_debug = proxy

def check():
	req = requests.get(url, proxies=proxy_debug)
	if req.status_code == 200:
		if "Index of" in  req.text:
			pass
	else:
		print("[-]No Index of found!")
		sys.exit()

def checkExt():
	req = requests.get(url, proxies=proxy_debug)
	for x in extenxions:
		if x in req.text:
			print(f"{url}/{x}")

def getContent(url):
	page = requests.get(url, proxies=proxy_debug)
	soup = BeautifulSoup(page.content, "html.parser")
	html = list(soup.children)[2]
	body = list(html.children)[3]
	tables = list(body.children)[3]
	# as tables de arquivos comecam no array 7
	#print(list(tables.children))
	
def main():
	check()
	checkExt()
	getContent(url)

if __name__ == '__main__':
	main()


