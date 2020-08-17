import requests
import sys
import argparse
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


banner = """

                                                       
 _         _                 ___                       
|_| ___  _| | ___  _ _  ___ |  _| ___  ___  _ _  _____ 
| ||   || . || -_||_'_|| . ||  _|| -_||   || | ||     |
|_||_|_||___||___||_,_||___||_|  |___||_|_||___||_|_|_|
                                                       


"""

parser = argparse.ArgumentParser(description='Enumerate files in index of', add_help=True)
parser.add_argument("-u", "--url", help="Url for enum, -u http://target.com/")
parser.add_argument("-l", "--list", help="List of targets for check, -l targets.txt")
parser.add_argument("-p", "--proxy", help="Active Debug mode, -p http://127.0.0.1:8080")
parser.add_argument("-o", "--output", help="Save output file, -o outfile.txt")
parser.add_argument("-w", "--wordlist", help="Wordlist of extentions, -w wordlist.txt")
args = parser.parse_args()

URLS = []
DIRS = []
extenxions = ['.txt','.sql','.zip','.rar','.bak','.old','.csv','.xml','.doc','.docx','.php','.py','.asp', '.aspx']
proxy_debug = None
OUT = None
SAVE_MODE = False 

HEADER = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0"
}

if args.url != None:
	URLS.append(args.url)

if args.list != None:
	arq = open(args.list, "r")
	for x in arq:
		try:
			x = x.decode("utf-8")
		except:
			pass
		x = x.replace("\n","")
		URLS.append(x)

if args.wordlist != None:
	arq = open(args.wordlist, "r")
	for x in arq:
		try:
			x = x.decode("utf-8")
		except:
			pass
		x = x.replace("\n","")
		extenxions = []
		extenxions.append(x)

if args.proxy != None:

	proxy = {
		"http":args.proxy,
		"https":args.proxy
	}

	proxy_debug = proxy

if args.output != None:
	OUT = args.output
	SAVE_MODE = True

def check(URL):
	req = requests.get(URL, proxies=proxy_debug, verify=False, headers=HEADER)
	
	if req.status_code == 200 :

		if "Index of" not in req.text:
			if "Directory" not in req.text:
				print("[-]No Index of found!")
				sys.exit()

	print(f"[!] Index Of Found in {URL}")
	print("[!] Searching for interesting files...")

def checkExt(URL, path):
	if path == None:
		path = ""
	page = requests.get(URL+path, proxies=proxy_debug, verify=False, headers=HEADER)
	soup = BeautifulSoup(page.content, "html.parser")
	for x in soup.find_all("a"):
		for y in extenxions:
			if y in x.get("href"):
				print(f"[+]{URL}{path}{x.get('href')}")
				if SAVE_MODE == True:
					saveinfile(OUT, f"[+]{URL}{path}{x.get('href')}")

def checkGit(URL, path):
	if path == None:
		path = ""
	page = requests.get(URL+path+"/.git/HEAD", proxies=proxy_debug, verify=False, headers=HEADER)
	if page.status_code == 200:
		print(f"[+]{url}{path}/.git/HEAD")
	else:
		pass

def getContent(URL,path):
	global DIRS
	if path == None:
		path = ""
	page = requests.get(URL+path, proxies=proxy_debug, verify=False, headers=HEADER)
	soup = BeautifulSoup(page.content, "html.parser")
	content = []
	for x in soup.find_all("a"):
		if x.get("href")[-1] == "/":
			content.append(x.get("href"))
	del content[0:1]
	for x in content:
		DIRS.append(path+x)

def saveinfile(out, text):
	arq = open(out, "a+")
	arq.write(text+"\n")
	arq.close()

def intermed(URLS):
	for URL in URLS:
		check(URL)
		checkExt(URL, None)
		getContent(URL, None)
		checkGit(URL, None)

		for x in DIRS:
			checkExt(URL, x)
			checkGit(URL,x)
			getContent(URL, x)
	
def main():
	print(banner)
	intermed(URLS)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print("[-] Exit")