import random
class card:
    def __init__(self,num,flower):
        self.num=num
        self.flower=flower
    def __eq__(self,card2):
        return self.num==card2.num
    def isMagic(self):
        return 2 if self.num==2 else 1 if self.num==11 and self.flower=='C' else 0
    def __str__(self):
        if self.num in range(2,11):
            t=str(self.num)
        elif self.num==1:
            t='A'
        elif self.num==11:
            t='J'
        elif self.num==12:
            t='Q'
        elif self.num==13:
            t='K'
        return t+self.flower
    def __int__(self):
        if self.num in range(3,11):
            return self.num
        elif self.isMagic():
            return 0
        else:
            return 10
def Cards(s):
    out=""
    for i in s:
        out+=str(i)+" "
    return out
def totalPoints(s):
    total=0
    for i in s:
        total+=int(i)
    return total
won=0
cards=[card(n,f) for n in range(1,14) for f in "CDHS"]
random.shuffle(cards)
p={0:cards[0:7],1:cards[7:14]}
cards=cards[14:]
recent=cards.pop()
curMagic=0
def refill():
                global cards,p
                cards=[card(n,f) for n in range(1,14) for f in "CDHS"]
                for x in p.keys():
                    for item in p[x]:
                        try:
                            cards.remove(item)
                        except:
                            print(Cards(cards),"---",Cards(p[0]),Cards(p[1]),item)
                            input()
                if len(cards)<=1:
                    input("CARDS EXHAUSTED")
                random.shuffle(cards)
def dropAndTake(pi, cardNow):
    global recent,won,curMagic,cards
    Cim= cardNow.isMagic()
    if Cim:
        p[pi].remove(cardNow)
        curMagic+=cardNow.num
    else:
        for i in p[pi]:
            if i==cardNow:
                p[pi].remove(i)
        if not recent==cardNow:
            try:
                p[pi].append(cards.pop())
            except IndexError:
                refill()
                p[pi].append(cards.pop())
        if totalPoints(p[pi])<10:
            won+=1
            print("Player[%d] Won - place %d"%(pi,won))
            print("p[%d] :"%pi+Cards(p[pi]))
            del p[pi]
            input()
    recent=cardNow
def game(pi):
    global curMagic,cards
    ci=None
    hasMagic2, hasClaverJack, hasRecentMagic=False, False, False
    CJI,M2I=-1,-1
    Rim=recent.isMagic()
    for i in p[pi]:
        if hasMagic2 and hasClaverJack:
            break
        Cim=i.isMagic()
        if Cim:
            if Cim==2:
                hasMagic2=True
                M2I=i
            elif Cim==1:
                hasClaverJack=True
                CJI=i
            if Cim==Rim:
                ci=i
                hasRecentMagic=True
    if curMagic:
        if not hasRecentMagic:
            #penalty
            if len(cards)<curMagic:
                refill()
            if len(cards)<curMagic:
                input("CARDS EXHAUSTED")
            p[pi]+=cards[:curMagic]
            cards=cards[curMagic:]
            curMagic=0
            return 0
    elif hasClaverJack:ci=CJI
    elif hasMagic2:ci=M2I
    else:
        max=-1
        for i in p[pi]:
            if int(i)>max:
                max=int(i)
                ci=i
    dropAndTake(pi,ci)
def start():
    pi=0
    while len(p)>1:
        print("p[%d] :"%pi+Cards(p[pi]))
        print("recent "+str(recent)+" left cards"+str(len(cards)))
        game(pi)
        print("p[%d] :"%pi+Cards(p[pi]))
        print("recent "+str(recent))
        #input()
        pi^=1
start()
