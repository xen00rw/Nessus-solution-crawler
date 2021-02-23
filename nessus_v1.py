#!/usr/bin/python
# coding: latin-1
############################################################
#                                                          #
#  by xen00rw                                              #
#  Nessus plugin solution crawler                          #
#                                                          #
############################################################



import requests
from optparse import OptionParser
import re
import os
import sys

parser = OptionParser()
parser.add_option("-f", action="store", dest="file_name", help="Define the .TXT file to crawl")
options, args = parser.parse_args()
file_name = options.file_name

if not options.file_name:
        print ("\n" + "[+] Point the .TXT file to crawl")
        print ("[+] Example: ")
        print ("$python3 nessus_v1.py -f plugins_list.txt" + "\n")
        exit()

try:
    os.remove("results.csv")
except:
    ""

file = open(file_name,"r")
final_file = open("results.csv","w")
list = file.readlines()

csv_columns = ["Plugin ID",";","Severity",";","Solution",";","HTTP Info","\n"]
final_file.writelines(csv_columns)

i = 0

def line_count(file_name):
    return sum(1 for line in open(file_name))

total_amount = line_count(file_name)

for pluginid in list:
        pluginid = pluginid.rstrip('\n')
        
        i = i + 1
        sys.stdout.write ("Plugins: " + str(i) + " of " + str(total_amount) + '\r')

        
        header = {      "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
                        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language" : "en-US,en;q=0.5",
                        "Accept-Encoding" : "gzip, deflate",
                        "Connection" : "close"}

        response = requests.get ("https://www.tenable.com/plugins/nessus/" + str(pluginid), headers=header)

        try:

            filtering_html = response.text

            solution_full = re.search("<h3>Solution<\/h3><span>(.*?)<\/section>", filtering_html, re.IGNORECASE | re.MULTILINE)
            solution_filtered =  solution_full.group() 
            solution_filtered = solution_filtered.replace("<br/>","")
            solution_clean = re.sub (r"<[^>]*|>|Solution","", solution_filtered)   


            severity_full = re.search("<strong>Severity(.*?)<\/span>", filtering_html, re.IGNORECASE | re.MULTILINE)
            severity_filtered = severity_full.group()
            severity_filtered = re.search (r"(?<=<span>)(.*?)(?=<\/span>)", severity_filtered, re.IGNORECASE | re.MULTILINE)
            severity_clean = severity_filtered.group()

            solution_clean = solution_clean.replace("&#x27;","")
            solution_clean = solution_clean.replace(";"," and")

            statinf = "OK"
 
            csv_columns = [pluginid,";",severity_clean,";",solution_clean,";",statinf,"\n"]  

            final_file.writelines(csv_columns)

        except AttributeError:
            solution_clean = "This request failed"
            statinf = "Failed"
            csv_columns = [pluginid,";",severity_clean,";",solution_clean,";",statinf,"\n"] 
            final_file.writelines(csv_columns)
