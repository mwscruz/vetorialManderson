import ast
import math
import re
from operator import itemgetter
import xml.etree.ElementTree as ET

lista_inv = {}
idf = {}
nDocs = 23155
#Carregar lista lista invertida
with open('arq_inv.txt','r') as arq_inv:
    for i in arq_inv:
        l = i.split('\t')        
        lista_inv[l[0]] = ast.literal_eval(l[1])    
        idf[l[0]] = 1                               #inicializa idf dos termos
arq_inv.close()

normaDoc = {}
acum = {}
similaridade = {}
for termo in lista_inv:
    #calcula/atribui idf do termo
    idf[termo] = math.log( (nDocs/float( len( lista_inv[termo] ) ) ), 2 )
    for doc in lista_inv[termo]:
        #precalculo da dorma dos documentos
        if doc not in normaDoc: #inicializa calculo norma do vetor para doc
            normaDoc[doc] = math.pow(lista_inv[termo][doc] * idf[termo], 2)
            acum[doc] = 0
            similaridade[doc] = 0
        else:                   #atualiza calculo norma do vetor para doc
            normaDoc[doc] += math.pow(lista_inv[termo][doc] * idf[termo], 2) 

for doc in normaDoc:
    normaDoc[doc] = math.sqrt(normaDoc[doc])

iConsultas = 1

for iConsultas in xrange(1,51):
    #Carregar termos da consulta
    query = {}  #onde os termos da consulta ficarao guardados
    with open('../base/consultasDafiti/'+str(iConsultas)+'.txt','r') as consulta:
        consulta = consulta.readline()
    consulta = consulta.lower().replace('\n','').split(' ')
    for termo in consulta:
        termo = re.sub('[^0-9a-zA-Z]+', '', termo)
        if termo not in query:
            query[termo] = 1
        else:
            query[termo] += 1

    normaConsulta = 0
    for doc in normaDoc:
        for termo in query:
            if (termo in lista_inv):
                #atualizo calculo norma da Consulta
                normaConsulta += math.pow( query[termo] * idf[termo], 2)
                if (doc in lista_inv[termo]):
                    #atualizo acumulador para calculo de similaridade
                    acum[doc] += lista_inv[termo][doc] * idf[termo] * query[termo] * idf[termo]

    #Conclui calculo norma da consulta
    normaConsulta = math.sqrt(normaConsulta)

    for doc in normaDoc:
        similaridade[doc] = ((acum[doc]) / ( normaDoc[doc] * normaConsulta ) )
        #reinicializa para proxima busca
        acum[doc] = 0                       

    sim = sorted(similaridade.items(), key=itemgetter(1), reverse=True)

    tree = ET.parse('../base/textDescDafitiPosthaus.xml')
    root = tree.getroot()

    with open('./resultado/resultado'+str(iConsultas)+'.txt','w') as output:
        for el in sim:
            output.write(root[el[0]][5].text+'\n')
        output.close()
            
            

