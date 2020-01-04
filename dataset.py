# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 00:12:44 2019

@author: dias
"""

import numpy as np
import pandas as pd
import random
import math

class Dataset:
    
    def __init__(self,filename=None, sep= ' '):
        self.filename= filename
        self.sep = sep
        if filename is not None:
            self.data = np.genfromtxt(filename,dtype = int, delimiter=sep, skip_header= 14, skip_footer=1)#Ler o ficheiro criado com o trim das linhas que nao interessam.
            self.ID = self.data[:,0] #ID das cidades
            self.X = self.data[:,1] #Valores de X para cada cidade
            self.Y = self.data[:,2] #Valores de Y para cada cidade
            self.df = self.dist_matrix()
            self.par= self.get_par(self.df)
            self.indiv=self.get_indiv() #Lista com a primeira geração de indivíduos
            self.dista=self.dist() #Dicionário com as distâncias de cada par
            
        
    def dist_matrix(self):
        d= {'X':np.array(self.X),'Y':np.array(self.Y)}
        df=pd.DataFrame(data=d)
        return df
        
    def get_par(self,df): #função auxiliar para selecionar um par do dataframe com o X e Y
        par = {}
        for i in range(len(df)):
            row = df.iloc[i]
            par[i]=row[0],row[1]
        return par

    def dist(self): #função que cria um dicionário com as distâncias para cada par
        dista = {}
        for i in self.par:
            for j in self.par:
                if j != i:
                    fit = int(math.sqrt(((self.par[i][0]-self.par[j][0])**2)+((self.par[i][1]-self.par[j][1])**2)))#função para calcular as distancias entre os pontos de duas cidades
                    dista[i,j]=fit
        return dista
    
    def get_indiv(self): #função que cria a primeira geração de indivíduos de forma aleatória
        lista_individuos=[]
        n=10 #número de indivíduos que estamos a criar.
        for i in range(n):
            indiv = random.sample(range(0,len(self.ID)), len(self.ID))
            lista_individuos.append(indiv)
        return lista_individuos
        
    
    def dist_inicial(self): #Função que avalia o fit da primeira geração criada
        dist_ini=[]
        a=self.indiv
        for i in a:
            dist_inic=0
            for j in range(len(i)-1):
                dist_inic+=self.dista.get((i[j],i[j+1]))
            dist_ini.append(dist_inic)
        return dist_ini
        
    
    def getall(self): #função auxiliar que retorna ID, X, Y 
        return self.ID,self.X,self.Y
        
        
def test():
    Dataset('file.txt')
    #print(d.get_indiv())
    #print(d.dist_inicial())
    #print(d.dista)
    #d.dist()
    #q = d.dist_matrix()
    #d.get_par(q)
test()
