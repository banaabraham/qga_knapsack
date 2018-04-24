import random
import time
import math

#using two points crossove
def crossover(c1,c2):
    r = random.randint(1,len(c1))
    c1 = c1[:r]
    c2 = c2[r:]
    return c1+c2

#generate random qubit population
def generatePop(benda,n):
    pop = []
    for i in range(n):
        c = []
        for i in range(len(benda.keys())):
            alpha = random.uniform(0,1)
            beta = 1-alpha
            r = random.sample([0,1,2,3],1)[0]
            if r==1:
                c.append([math.sqrt(alpha),math.sqrt(beta)])     
            elif r==1:
                c.append([-math.sqrt(alpha),math.sqrt(beta)])  
            elif r==2:
                c.append([math.sqrt(alpha),-math.sqrt(beta)]) 
            else:
                c.append([-math.sqrt(alpha),-math.sqrt(beta)])
                
        pop.append(c)
    return pop

#convert qubit into classical bit            
def measure(pop):
    classic = []
    for i in pop:
        c = []
        for j in i:
            r = random.uniform(0,1)
            if r <= j[0]**2:
                c.append(0)
            else:
                c.append(1)
        classic.append(c)
    return classic

#calculate value from chromosome
def calcVal(pop):
    totalVal = 0
    for i,k in enumerate(benda.keys()):
        if pop[i]==1:
            totalVal+=benda[k][0]
    return totalVal

#calculate weight from chromosome
def calcWg(pop):
    totalWg = 0
    for i,k in enumerate(benda.keys()):
        if pop[i]==1:
            totalWg+=benda[k][1]      
    return totalWg

#calculate fitness of chromosome
def calcFit(pop):
    return calcVal(pop)/2*calcWg(pop)

#select the best chromosome according to its fitness
def bestPop(newPops):
    bestFit=0
    bestChild = []
    kamus_best = dict()
    for i in newPops:
        k = str(i)
        kamus_best[k] = calcVal(i),calcWg(i),calcFit(i)
        temp = calcFit(i)
        if bestFit<temp:
            bestFit = temp
            bestChild = i
        elif bestFit == temp:
            if calcWg(bestChild)<calcWg(i):
                bestChild=i
    return bestChild,bestFit,kamus_best 

#select chromosome that satisfy the weight cap
def selectedPop(pops,cap):
    selected = []
    for pop in pops:
        if calcWg(pop)<=cap and calcWg(pop)!=0 and pop not in selected:
            selected.append(pop)
    return selected

#qgate rotation
def qgate(pop,best,delta_theta):
    for c in pop:
        for i in range(len(c)):
            if c[i][0]>0 and c[i][1]>1:
                if best[i]==1:
                    c[i][0] = c[i][0]-delta_theta
                    c[i][1] = c[i][1]+delta_theta
                else:
                    c[i][0] = c[i][0]+delta_theta
                    c[i][1] = c[i][1]-delta_theta
            elif c[i][0]>0 and c[i][1]<0:
                if best[i]==1:
                    c[i][0] = c[i][0]+delta_theta
                    c[i][1] = c[i][1]+delta_theta
                else:
                    c[i][0] = c[i][0]-delta_theta
                    c[i][1] = c[i][1]-delta_theta
            elif c[i][0]<0 and c[i][1]>0:
                if best[i]==1:
                    c[i][0] = c[i][0]-delta_theta
                    c[i][1] = c[i][1]-delta_theta
                else:
                    c[i][0] = c[i][0]+delta_theta
                    c[i][1] = c[i][1]+delta_theta
            elif c[i][0]<0 and c[i][1]<0:
                if best[i]==1:
                    c[i][0] = c[i][0]+delta_theta
                    c[i][1] = c[i][1]-delta_theta
                else:
                    c[i][0] = c[i][0]-delta_theta
                    c[i][1] = c[i][1]+delta_theta

def aqgate(pop,best,delta_theta):
    for c in pop:
        for i in range(len(c)):
            c[i][0] = c[i][0]*math.cos(math.degrees(delta_theta))-c[i][1]*math.sin(math.degrees(delta_theta))
            c[i][1] = math.sqrt(1-c[i][0]**2)
            print(c[i])

def qgenetic_main(npop,cap,NCMax,benda):
    
    while True:
        NC = 0
        pop = generatePop(benda,npop)
        best = [random.randint(0,1) for i in range(len(pop[0]))]
        conv=0
        try:
            while NC<NCMax or conv==3:
                MR = (random.uniform(0,1)+0.2)/len(pop[0])/10
                delta_theta = 3.14/15*random.uniform(0,1)+3.14/20
                #crossover
                for c in pop:
                    r = random.uniform(0,1)
                    if r<=CP:
                        selected = []
                        for i in range(2):
                            selected.append(random.sample([i for i in range(len(pop))],1)[0])
                        pop.append(crossover(pop[selected[0]],pop[selected[1]]))
                
                #mutation
                for c in pop:
                    for qb in c:
                        r = random.uniform(0,1)
                        if r<=MR:
                            qb[0],qb[1] = qb[1],qb[0]
                
                qgate(pop,best,delta_theta)
                classic = selectedPop(measure(pop),cap)
                hasil = bestPop(classic)
                if best==hasil:
                    conv+=1
                else:
                    conv=0
                best = hasil[0]
                NC+=1
            return hasil
            break
        except Exception as e:
            npop+=1
            pass

    
def decode(chromosome,benda):
    hasil = []
    for i,v in enumerate(benda.keys()):
        if chromosome[i]==1:
            hasil.append(v)
    return hasil  
       
benda = {'sepatu': [20, 10], 'buah': [20, 10],'odol':[2,11],'sikat gigi':[20,1],
             'rokok':[100,5],'buku':[50,10],'sambiloto':[10,30],'playstation':[10,50]\
             ,'sabun':[50,10],'minuman':[10,50],'sambel':[5,10],'makanan ringan':[70,10],\
             'yet':[20,12],'another':[2,4],'rumah':[10,1000],'genting':[50,10],'sesuatu':[90,50]}

#crossoper rate
CP = 0.25
#max iteration 
NCMax = 10

t1 = time.time()
b1,k1,w1 = qgenetic_main(10,50,NCMax,benda)
t2 = time.time()
print(decode(b1,benda))
print(calcWg(b1))
print(t2-t1)
