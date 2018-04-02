#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import numpy as np 
import random
import cPickle as pickle
import os
import sys

class unity:
    def __init__(self):
        self.core = None
        
    def move(self,s):
        raise NotImplementedError
    
    def getsteps(self):
        raise NotImplementedError
        
    def equal(self, t):
        raise NotImplementedError
    
    def writeweight(self):
        raise NotImplementedError
    
class human(unity):
    def __init__(self, core):
        unity.__init__(self)
        self.core = core
    
    def getsteps(self):
        return None
    
    def move(self, s):
        return None
    
def main():
    p = human(None)
    p.move(1)

main()
