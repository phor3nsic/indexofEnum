IndexOfEnum ![](img/icon.png)
===
![downloads](https://img.shields.io/github/downloads/atom/atom/total.svg)
![build](https://img.shields.io/appveyor/ci/:phor3nsic/:indexofEnum.svg)
![Python 3.x](https://img.shields.io/badge/python-v3.7-blue) 

## Install and Usage

1. Install:
```
git clone https://github.com/phor3nsic/indexofEnum
cd indexofEnum
pip3 install -r requirements.txt

``` 
2. Usage:

```
python3 indexofenum.py -u http://taget.com/
```

## Example

```
usage: indexofenum.py [-h] [-u URL] [-l LIST] [-p PROXY] [-o OUTPUT] [-w WORDLIST]

Enumerate files in index of

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Url for enum, -u http://target.com/
  -l LIST, --list LIST  List of targets for check, -l targets.txt
  -p PROXY, --proxy PROXY
                        Active Debug mode, -p http://127.0.0.1:8080
  -o OUTPUT, --output OUTPUT
                        Save output file, -o outfile.txt
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist of extentions, -w wordlist.txt
```

1. Search target:

![](img/dirs.jpg)

2. Run tool:

```
python3 indexofenum.py -u http://taget.com/ 

```
![](img/result.jpg)


## Appendix and FAQ

:::info
**Find this document incomplete?** Leave a comment!
:::

