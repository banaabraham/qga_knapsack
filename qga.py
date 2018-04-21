import random


def crossover(c1,c2):
    r = random.randint(1,len(c1))
    c1 = c1[:r]
    c2 = c2[r:]
    return c1+c2

def generatePop(benda,n):
    pop = []
    for i in range(n):
        c = []
        for i in range(len(benda.keys())):
            alpha = random.uniform(0,1)
            beta = 1-alpha
            c.append([alpha,beta])        
        pop.append(c)
    return pop


def qgate(pop):
    classic = []
    for i in pop:
        c = []
        for j in i:
            r = random.uniform(0,1)
            if r <= j[0]:
                c.append(0)
            else:
                c.append(1)
        classic.append(c)
    return classic

def calcVal(pop):
    totalVal = 0
    for i,k in enumerate(benda.keys()):
        if pop[i]==1:
            totalVal+=benda[k][0]
    return totalVal

def calcWg(pop):
    totalWg = 0
    for i,k in enumerate(benda.keys()):
        if pop[i]==1:
            totalWg+=benda[k][1]      
    return totalWg

def calcFit(pop):
    return calcVal(pop)/2*calcWg(pop)

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

def selectedPop(pops,cap):
    selected = []
    for pop in pops:
        if calcWg(pop)<=cap and calcWg(pop)!=0 and pop not in selected:
            selected.append(pop)
    return selected

def qgenetic_main(pop,cap,NCMax):
    NC = 0
    best = []
    while NC<NCMax:
    
        for c in pop:
            r = random.uniform(0,1)
            if r<=CP:
                selected = []
                for i in range(2):
                    selected.append(random.sample([i for i in range(len(pop))],1)[0])
                pop.append(crossover(pop[selected[0]],pop[selected[1]]))
        for c in pop:
            for qb in c:
                r = random.uniform(0,1)
                if r<=MR:
                    qb[0],qb[1] = qb[1],qb[0]
        
        classic =  qgate(pop)
        classic = selectedPop(classic,cap)
        best = bestPop(classic)
        NC+=1
    return best
        

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


CP = 0.25
MR = 0.01
NCMax = 10        
        
pop = generatePop(benda,1000)
b,k,w = qgenetic_main(pop,30,NCMax)
print(decode(b,benda))
print(calcWg(b))
