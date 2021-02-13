#!/usr/bin/python

import requests
from optparse import OptionParser
import re
import os

#Definindo opções de argumentos e tratando
parser = OptionParser()
parser.add_option("-f", action="store", dest="file_name", help="Define o arquivo .TXT com os plugins id a serem verificados")
options, args = parser.parse_args()
file_name = options.file_name

#Exibição do painel de ajuda
if not options.file_name:
	print ("\n" + "[+] Defina o arquivo com os plugins a serem checados")
	print ("[+] $python3 nessus_grabber_v1.py -f lista_plugins.txt -o resultados" + "\n")
	exit()

#Removendo antigo resultado do script
try:
	os.remove("resultados.csv")
except:
	""

#Realizando criação do arquivo de resultado e lendo lista com plugins ID
file = open(file_name,"r")
result = open("resultados.csv","x")
lista = file.readlines()

#Criando os titulos das colunas do .csv
xx = ["ID do Plugin",";","Tipo de Solucao",";","Status HTTP","\n"]
result.writelines(xx)

#Iniciando laço de checagem da solução dos plugins da lista
for pluginid in lista:
	pluginid = pluginid.rstrip('\n')

	#Definindo as opções do Header do Request
	header = {	"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
			"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"Accept-Language" : "en-US,en;q=0.5",
			"Accept-Encoding" : "gzip, deflate",
			"Connection" : "close"}

	#Iniciando o processo da requisição
	target = requests.get ("https://www.tenable.com/plugins/nessus/" + str(pluginid), headers=header)

	#Tratativa do resultado da requisição com regex
	filtering_html = target.text
	match = re.search("<h3>Solution*</h3><span>(.*?)</span>", filtering_html, re.IGNORECASE | re.MULTILINE) #1- Filtro completo do HTML obtendo só a "Solução"
	filtered_html =  match.group() #Definindo váriavel completa com o filtro que quermos
	clear_field = re.sub (r"<[^>]*|>|Solution","", filtered_html) 	#2- Realizamos a limpeza de tags HTML que sobrarm do resultado
	statcode = str(target.status_code) #Salvando o status code do HTTP para sabermos se algum falhou na planilha final

	#Definindo o resultado em colunas
	xx = [pluginid,";",clear_field,";",statcode,"\n"]

	#Esrevendo o resultado no .csv
	result.writelines(xx)



# Somente para Teste dos Headers de Send e Response
# print (target.headers) --> Informa o header de response
# print (target.request.headers) --> Informa o header do request
# print("\n" + target.text) --> Traz o resultado completo da requisição
