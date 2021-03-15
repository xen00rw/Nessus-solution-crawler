#!/usr/bin/python
# coding: latin-1


import requests
from optparse import OptionParser
import re
import os
import sys

#Define the parameters we gonna use
parser = OptionParser()
parser.add_option("-f", action="store", dest="file_name", help="Define .TXT file with plugins id to crawl")
options, args = parser.parse_args()
file_name = options.file_name

#Help panel
if not options.file_name:
        print ("\n" + "[+] Define the file with plugin ids to crawl")
        print ("[+] Example: ")
        print ("$python3 nessus_crawler_v1.py -f plugin_list.txt" + "\n")
        exit()

#Remove old results file
try:
    os.remove("results.csv")
except:
    ""

#Creating results.csv file and reading plugin ids list
file = open(file_name,"r")
final_file = open("results.csv","w")
list_file = file.readlines()

#Creating .csv Columns Title
csv_columns = ["Plugin ID",";","Severity",";","Solution Type",";","HTTP Info","\n"]
final_file.writelines(csv_columns)

#Line count
i = 0

#Function to count .TXT plugins
def line_count(file_name):
    return sum(1 for line in open(file_name))

#Counting line of the file
total_plugins = line_count(file_name)

#Starting loop solution check
for pluginid in list_file:
        pluginid = pluginid.rstrip('\n')
        
        #Counter line files
        i = i + 1
        sys.stdout.write ("Plugins: " + str(i) + " of " + str(total_plugins) + '\r')

        
        #Setting Request Header (just to bypass possible WAF)
        header = {      "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
                        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language" : "en-US,en;q=0.5",
                        "Accept-Encoding" : "gzip, deflate",
                        "Connection" : "close"}

        #Starting request
        response = requests.get ("https://www.tenable.com/plugins/nessus/" + str(pluginid), headers=header)
        response = response.text

        #Decoding request
        decoded_response = response.encode('utf8').decode('ascii','ignore')

        #Trying to parse HTML with Regex
        try:

            #Request response
            filtering_html = decoded_response
  
            #Solution cleared with regex
            solution_full = re.search("Solution<\/h4><span>(.*?)<\/section>", filtering_html, re.IGNORECASE | re.MULTILINE)
            solution_filtered =  solution_full.group() 
            solution_filtered = solution_filtered.replace("<br/>","")
            solution_clean = re.sub (r"<[^>]*|>|Solution","", solution_filtered)   


            #Severity cleared with regex
            severity_full = re.search("<strong>Severity(.*?)<\/span>", filtering_html, re.IGNORECASE | re.MULTILINE)
            severity_filtered = severity_full.group()
            severity_filtered = re.search (r"(?<=<span>)(.*?)(?=<\/span>)", severity_filtered, re.IGNORECASE | re.MULTILINE)
            severityclean = severity_filtered.group()

            
            #Removing enconde strings
            solution_clean = solution_clean.replace("&#x27;","")
            solution_clean = solution_clean.replace(";"," and")

            #Did request work ?
            statinf = "OK"
        
            #Making an list to fill the .csv
            csv_columns = [pluginid,";",severityclean,";",solution_clean,";",statinf,"\n"]  

            #Filling .csv file with the cleared solution and severity
            final_file.writelines(csv_columns)

            
        #Exception for AttributeError
        except AttributeError:
        
            solution_clean = "Failed request"  
            severityclean = "Failed request"     
            statinf = "Failed"
            
            #Making an list to fill the .csv
            csv_columns = [pluginid,";",severityclean,";",solution_clean,";",statinf,"\n"] 
            
            #Filling .csv file with the cleared solution and severity
            final_file.writelines(csv_columns)
            
            
# Just tests
# print (response.headers) --> Response Headers
# print (response.request.headers) --> Request Header
# print("\n" + response.text) --> Grab request response in text
# print("\n" + response.encoding) --> Grab request encode type
