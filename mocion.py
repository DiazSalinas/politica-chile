#scrap mocion
## mainList

import urllib
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata

def request_vote(vote_id):
  baseurl="https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion="+str(vote_id)
  soup = make_soup(baseurl)
  info = soup.find("section", {"id": "info-ficha"})
  ### Proyecto
  proyecto=[]
  atributos={}
  atributos['id']="33633"
  for i in info.find_all('div',{"class":"datos-ficha"}):
    if("Proyecto Ley:" in i.find("div", {"class": "dato"}).text ):
      atributos['Proyecto']= i.find("strong").text
    if(i.find("div", {"class": "dato"}).text=="Fecha:"):
      atributos['Fecha']= i.find("strong").text
    if(i.find("div", {"class": "dato"}).text=="Materia:"):
      atributos['Materia']= i.find("strong").text
    if(i.find("div", {"class": "dato"}).text=="Sesión:"):
      atributos['Sesion']= i.find("strong").text
    if(i.find("div", {"class": "dato"}).text=="Trámite:"):
      atributos['Tramite']= i.find("strong").text
    if(i.find("div", {"class": "dato"}).text=="Tipo de Votación"):
      atributos['TipoDeVotacion']= i.find("strong").text
    if(i.find("div", {"class": "dato"}).text=="Quorum"):
      atributos['Quorum']= i.find("strong").text
    if(i.find("div", {"class": "dato"}).text=="Resultado"):
      atributos['Resultado']= i.find("strong").text
  proyecto.append(atributos)
  df=pd.DataFrame(proyecto)
  df.to_csv('output-atributes.csv')

request_vote(33633)
#base url
url = "https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion=33633"

soup = make_soup(url)

info = soup.find("section", {"id": "info-ficha"})



tabla_afavor = soup.find("table", {"id": "ContentPlaceHolder1_ContentPlaceHolder1_PaginaContent_dtlAFavor"})
tabla_encontra = soup.find("table", {"id": "ContentPlaceHolder1_ContentPlaceHolder1_PaginaContent_dtlEnContra"})
tabla_abstencion = soup.find("table", {"id": "ContentPlaceHolder1_ContentPlaceHolder1_PaginaContent_dtlAbstencion"})
tabla_organica = soup.find("table", {"id": "ContentPlaceHolder1_ContentPlaceHolder1_PaginaContent_dtlArticulo5"})

lista_afavor = tabla_afavor.find_all('a')
lista_encontra = tabla_encontra.find_all('a')
lista_abstencion = tabla_abstencion.find_all('a')
lista_org = tabla_organica.find_all('a')

# id,voto
diputados = []
voto=[]

for persona in lista_afavor:
	diputados.append(persona.get('href').split("prmID=")[1])
	voto.append("1")

for persona in lista_encontra:
	diputados.append(persona.get('href').split("prmID=")[1])
	voto.append("2")

for persona in lista_abstencion:
	diputados.append(persona.get('href').split("prmID=")[1])
	voto.append("0")

for persona in lista_org:
	diputados.append(persona.get('href').split("prmID=")[1])
	voto.append("3")

df = pd.DataFrame(list(zip(diputados, voto)), 
               columns =['id_diputado', 'voto']) 
df.head()
df.to_csv('diputados_votos_33633.csv',index=False)
"""
diputados = []
partidos = []
id_diputado = []
distrito= []

for persona in lista:
    diputados.append(persona.find('img').get('title'))
    partidos.append(persona.find_all('p')[1].text)
    distrito.append(persona.find_all('p')[0].text)
    id_diputado.append(str(persona.find('img').get('src')).split("ID=GRCL")[1])

diputados
partidos

import pandas as pd
df = pd.DataFrame(list(zip(diputados, partidos, id_diputado,distrito)), 
               columns =['senador', 'partido','id_diputado','distrito']) 
df.head()

df.to_csv('diputados.csv')
"""