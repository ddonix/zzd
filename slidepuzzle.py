#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import numpy as np 
import random
import cPickle as pickle
import os
import sys

class spuzzleTree:
    initsearch = 8      #一次最小搜索深度
    maxsearch  = 12     #一次最大搜索深度
    MaxDeep  = 500      #总最大搜索深度
    weight = None       #比较权重       这4个参数都需要设定，并可以学习(高级)

    def __init__(self, da, dis):
        self.data = da
        self.data2 = None
        
        if dis == None:
            self.distance = self.getdistance()
        else:
            self.distance = dis
        
        self.father = None
        self.prevstep = None

        self.deep = 1
        self.child = []
        
        self.min = self
        self.maxdeep = 1
    
        
    def copypuzzle(self):
        da = self.data.copy()
        result = spuzzle_4X4(da, self.distance)
        result.data2 = self.data2.copy()
        return result
    
    def move(self,s):
        raise NotImplementedError
    
    def getsteps(self):
        raise NotImplementedError
        
    def equal(self, t):
        raise NotImplementedError
    
    def writeweight(self):
        raise NotImplementedError
    
    @classmethod
    def trainweight(cls, block, count):
        print("....学习weight...")
        while count > 0:
            count -= 1
            tmplist = []

            b = 0
            while b < block:
                while True:
                    puzzle = cls.randompuzzle()
                    puzzle.display()
                    tmp = puzzle.solvepuzzle()
                    if tmp == None:
                        continue
                    tmplist.append(tmp)
                    break
                b += 1
            puzzle.optweight(tmplist)
            puzzle.writeweight()
    
    def printTree(self):#深度遍历
        self.display()
        print("deep %d"%self.deep)
        for c in self.child:
            c.printTree()

    def __search(self):#增加一层遍历
        if self.child == []:
            steps = self.getsteps()
            for s in steps:
                c = self.copypuzzle()
                c.move(s)
                
                self.maxdeep = c.deep = self.deep + 1
                if c.distance < self.min.distance:
                    self.min = c
                
                c.father = self
                self.child.append(c)
        else:
            for c in self.child:
                c.__search()
                if c.min.distance < self.min.distance:
                    self.min = c.min
                if c.maxdeep > self.maxdeep:
                    self.maxdeep = c.maxdeep
        
        fa = self.father
        while fa != None:
            if fa.min.distance > self.min.distance:
                fa.min = self.min
            if fa.maxdeep < self.maxdeep:
                fa.maxdeep = self.maxdeep
            fa = fa.father
    
    def search(self, d):#增加一层遍历
        while d > 0:
            d -= 1
            self.__search()

    def cutTree(self, ch):
        self.child.remove(ch)
        self.min = self
        for c in self.child:
            if self.min == None:
                self.min = c.min
            elif c.min.distance < self.min.distance:
                self.min = c.min
        
        fa = self.father
        while fa != None:
            fa.min = self.min
            fa = fa.father
    
    def solvepuzzle(self):
        result = self
        cutTrees  = []
        while result.distance != 0:
            if result.deep >= spuzzleTree.MaxDeep:
                break
            while True:
                result.search(1)
                if result.maxdeep - result.deep < spuzzleTree.initsearch:
                    continue
                else:
                    break
                
            if result.min.distance == result.distance:
                while True:
                    result.search(1)
                    if result.min.distance < result.distance:
                        break
                    elif result.maxdeep - result.deep == spuzzleTree.maxsearch:
                        break
                    continue
            
            fa = None
            if result.min.distance >= result.distance:
                fa = result.father
            for c in cutTrees:
                if c.equal(result.min) == True:
                    fa = result.father       
            if fa == None:
                result = result.min
                result.display()
            else:                
                print("back off.")
                fa.cutTree(result)
                cutTrees.append(result)
                result = fa
        
        if result.distance != 0:
            print("solve puzzle error")
            return result
        else:
            print("solve puzzle success")
            return None

    def displayAnswer(self):
        s = self.min
        if s.distance != 0:
            print("solve puzzle error.I am sorry!")
            return
        li = []
        while s!= None:
            li.insert(0,s)
            s = s.father
        for s in li:
            s.display()
        
class spuzzle_4X4(spuzzleTree):
    @staticmethod
    def readweight():
        spuzzle_4X4.weight = np.empty([15],dtype='int32')
        if os.path.exists('./puzzleweight.txt'):
            f = open('./puzzleweight.txt', 'r')
            spuzzle_4X4.weight = pickle.load(f)
            f.close()
        else:
            for i in np.arange(15):
                spuzzle_4X4.weight[i] = 1
            spuzzle_4X4.weight[0] = 1000
            spuzzle_4X4.weight[1] = 800
            spuzzle_4X4.weight[2] = 600
            spuzzle_4X4.weight[3] = 400
            spuzzle_4X4.weight[4] = 100
            spuzzle_4X4.weight[8] = 80
            spuzzle_4X4.weight[12] = 60
            spuzzle_4X4.weight[5] = 10
            spuzzle_4X4.weight[6] = 8
            spuzzle_4X4.weight[7] = 6

    def __init__(self, da, dis):
        spuzzleTree.__init__(self, da, dis)
        self.data2 = np.empty([16], dtype='int32')
        for v in np.arange(16):
            i = self.data[v]
            self.data2[i] = v
    
    
    def equal(self, t):
        return (self.data == t.data).all()
    
    def optweight(self, parm):
        w = np.zeros(16, dtype='int32')
        for tmp in parm:
            for v in np.arange(16):
                if tmp.data[v] != v:
                    w[v] += 1
        print(w)
        
    @staticmethod
    def randompuzzle():
        Target = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
        p = spuzzle_4X4(Target, dis=None)
        p.ruffle(300)
        return p

    def writeweight(self):
        f = open('./puzzleweight.txt', 'wb')
        pickle.dump(spuzzle_4X4.weight, f)
        f.close()
        return

    def display(self):
        step = {0:"up", 1:"down", 2:"left", 3:"right", None:"init"}
        show = np.empty([4,4], dtype='int32')
        for i in [0,1,2,3]:
            for j in [0,1,2,3]:
                show[i][j] = (self.data2[i*4+j]+1)%16
        print(show)
        print("deep %d distance %d prevstep %s"%(self.deep, self.distance, step[self.prevstep]))
        print("................")

    def getsteps(self):
        p = self.data[15] 
        p0 = p/4
        p1 = p%4
        flag = [1,1,1,1]
        if p0 == 0:
            flag[0] = 0
        if p0 == 3:
            flag[1] = 0
        if p1 == 0:
            flag[2] = 0
        if p1 == 3:
            flag[3] = 0
        if self.prevstep == 0:
            flag[1] = 0
        if self.prevstep == 1:
            flag[0] = 0
        if self.prevstep == 2:
            flag[3] = 0
        if self.prevstep == 3:
            flag[2] = 0
        steps = []
        for i in [0,1,2,3]:
            if flag[i] == 1:
                steps.append(i)
        return steps
    
    def getdistance(self):
        self.distance = 0
        for v in np.arange(15):
            p = self.data[v]
            i1 = v/4
            j1 = v%4
            i2 = p/4
            j2 = p%4
            self.distance += (abs(i2-i1)+abs(j2-j1))*spuzzle_4X4.weight[v]
        return self.distance 
       
    def getdistanceChange(self, v, p1, p2):
        i = v/4
        j = v%4
        i1 = p1/4
        j1 = p1%4
        i2 = p2/4
        j2 = p2%4
        d1 = (abs(i1-i)+abs(j1-j))*spuzzle_4X4.weight[v]
        d2 = (abs(i2-i)+abs(j2-j))*spuzzle_4X4.weight[v]
        return d2-d1

    def move(self, s):
        p = self.data[15]
        p2 = None
        if s == 0:
            if p > 3:
                p2 = p-4
        
        if s == 1:
            if p < 12:
                p2 = p+4
        
        if s == 2:
            if p%4 > 0:
                p2 = p-1

        if s == 3:
            if p%4 < 3:
                p2 = p+1

        if p2 != None:
            a = self.data2[p2]
            b = self.getdistanceChange(a,p2,p)
            
            self.data[15] = p2
            self.data[a] = p
            
            self.data2[p2] = 15
            self.data2[p] = a
            
            self.distance += b
            
            self.prevstep = s
    
    def ruffle(self, count):
        while(count > 0):
            p = self.data[15] 
            p0 = p/4
            p1 = p%4
            s = random.randint(0,3)
            if s == 0 and (self.prevstep == 1 or p0 == 0):
                continue
            if s == 1 and (self.prevstep  == 0 or p0 == 3):
                continue
            if s == 2 and (self.prevstep == 3 or p1 == 0):
                continue
            if s == 3 and (self.prevstep == 2 or p1 == 3):
                continue
            self.move(s)
            count -= 1

def main():
    if len(sys.argv) == 1: 
        print("read  读取权重")
        print("train 学习权重")
        print("rpuzzle  随机生成迷宫解迷")
        print("ipuzzle 输入迷宫解迷")
        return
    
    spuzzle_4X4.readweight()
    if sys.argv[1] == 'read':
        print("weight")
        print(spuzzle_4X4.weight)
    elif sys.argv[1] == 'train':
        print("学习前weight")
        print(spuzzle_4X4.weight)
        spuzzle_4X4.trainweight(50,1)
        print("学习后weight")
        print(spuzzle_4X4.weight) 
    elif sys.argv[1] == 'rpuzzle':
        print("...随机生成迷宫解迷...")
        p = spuzzle_4X4.randompuzzle()
        p.prevstep = None
        print("...迷宫...")
        p.display()
        p.solvepuzzle()
        p.displayAnswer()
    elif sys.argv[1] == 'ipuzzle':
        idata = np.empty([16], dtype='int32')
        i = 0
        try:
            for tmp in [0,1,2,3]:
                for n in raw_input().split(' '):
                    idata[(int(n)+15)%16] = i
                    i += 1
        except ValueError as err:
            print("input right format")
        
        p = spuzzle_4X4(idata, None)
        print("...迷宫...")
        p.display()
        p.solvepuzzle()
        p.displayAnswer()
    else:
        print("read  读取权重")
        print("train 学习权重")
        print("rpuzzle  随机生成迷宫解迷")
        print("ipuzzle 输入迷宫解迷")
    return
main()
