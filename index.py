import xml.etree.ElementTree as ET
import re
tree = ET.parse('../base/textDescDafitiPosthaus.xml')
root = tree.getroot()

doc = 0   #Documento
#Ndocs = 23155
#lista_inv['palavra']['documento'] = numero de vezes a palavra ocorre no documento
lista_inv = {}

for child in root:
    #child[0].text #ID
    #child[1].text #Categoria
    #child[2].text #Titulo
    #child[3].text #Descricao
    #child[4].text #Preco
    #child[5].text #Imagem
    for tag in child:
        if tag == child[4] or tag == child[5]:
            break
        elif tag != child[0]:
            par = tag.text.lower().split(' ')
            for palavra in par:
                palavra = re.sub('[^0-9a-zA-Z]+', '', palavra)
                #Se a palavra ainda nao foi indexada
                if (palavra not in lista_inv):
                    if ((palavra != ' ') and (palavra!= '')):             
                        lista_inv[palavra] = {}                   #indexar
                        lista_inv[palavra][doc] = 1                 #registrar primeira ocorrencia
                else:
                    if doc not in lista_inv[palavra]:
                        lista_inv[palavra][doc] = 1
                    lista_inv[palavra][doc] = lista_inv[palavra][doc] + 1        
    doc = doc + 1
with open('arq_inv.txt','w') as out:
    for i in lista_inv:
        #print i, lista_inv[i]
        texto = str(i) +'\t'+ str(lista_inv[i]) + '\n'
        out.write( texto)
out.close()
#Nome da imagem
#print root[14819][5].text    
print ('Numero de termos ',len(lista_inv))
print ('Numero de Docs ', doc)
