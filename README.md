# Nessus Crawler Solution

![created](https://img.shields.io/badge/platform-linux-blue)
![language](https://img.shields.io/badge/language-python-blue)
[![Twitter](https://aleen42.github.io/badges/src/twitter.svg)](https://twitter.com/willxenoo)

Python 3 based tool to crawl through Tenable web page and get the solutions of some plugins id based on a list.
I've made this script to facilitate my work daily tasks.

## Requirements
Use the package manager to install de request lib
```bash
$ pip3 install requests
```

## Usage
The usage of the script is too easy. You just need to type one flag and the result come.
```bash
$ python3 nessus_crawler_v1.py -f plugins_id.txt

-f = File list containing all plugins id that you want to check de solution, line by line
```
After some time it'll generate an .CSV file on the same directory called "results.csv" with the solutions for each plugin id.

# P.S.
Thanks !!<

From you Friend, Xen00rw
