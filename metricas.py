import xml.etree.ElementTree as ET

report = open('report.txt','w')
report.close()
for i in range(1,51):
    tree = ET.parse('../base/relevantes/'+str(i)+'_relevante.xml')
    root = tree.getroot()
    with open('./resultado/resultado'+str(i)+'.txt','r') as rank:
        res = rank.readlines()

    contRel = 0
    #calculo P@10
    for child in root:
        if child[0].text+'\n' in res[:10]:
            contRel = contRel + 1        
    
    report = open('report.txt','a')
    #P@10
    p = (float(contRel)/10)*100
    report.write('P@10:'+str(i)+':'+str(p)+'\n') 

    MAP = 0
    contRel = 0
    #Calculo MAP
    for j in xrange(0,23155):
        for child in root:
            if res[j] == child[0].text+'\n':
                contRel += 1
                MAP = MAP + (contRel/(j+1))

    
    #MAP
    MAP = float(MAP) / contRel
    report.write('MAP:'+str(i)+':'+str(MAP)+'\n')    
    report.write('--\n')
    rank.close()
    

