# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 14:36:52 2019

@author: dias
"""

from scraping import Scraping
from dataset import Dataset
import random

class m_cam(Dataset):
  
    def __init__(self,filename=None, sep = ' '):
        super().__init__(filename)
        self.pop=self.get_indiv()
        self.dict=self.dista
        self.fitness = []
    
    def fitness_geral(self): #calcula o fitness dos indivíduos na população
        self.fitness=[]
        for ind in self.pop:
            fit = 0
            for city in range(len(ind)-1):
                fit += self.dict[ind[city], ind[city+1]]
            self.fitness.append(fit)
        return self.fitness    
    
    def fit_indiv(self, indiv): #calcula o fitness só para um indivíduo
        fit = 0
        for city in range(len(indiv)-1):
            fit += self.dict[indiv[city], indiv[city+1]]
        return fit
        
   
    def troca_3(self, index, mutationRate=0.05): #troca de 3 cidades aleatoriamente dando o index do indivíduo correspondente do self.pop
        ind1 = self.pop[index]
        novo_ind = ind1[:]
        fit_ind=self.fitness[index]
        pos=[]
        for i in range(1,len(ind1)-1):
            if(random.random() < mutationRate):
                pos.append(i)
        if len(pos) > 3:
            pos=random.sample(pos, k=3)  
            I, J, K = pos[0], pos[1], pos[2]
            novo_ind[I], novo_ind[J], novo_ind[K] = ind1[J], ind1[K], ind1[I]
            fit_novo = self.fit_indiv(novo_ind)
            if fit_novo < fit_ind:
                self.pop[index] = novo_ind
                self.fitness[index] = fit_novo
        return novo_ind, fit_ind
        
        
    
    def troca_2(self, index, mutationRate=0.90): #troca de duas cidades aleatorias, dando o index do indivíduo correspondente do self.pop
        ind1 = self.pop[index]
        novo_ind = ind1[:]
        fit_ind=self.fitness[index]
        pos=[]
        for i in range(1,len(ind1)-1):
            if(random.random() < mutationRate):
                pos.append(i)
        if len(pos) > 2:
            pos=random.sample(pos, k=2) 
            I, J = pos[0] , pos[1]
            novo_ind[I], novo_ind[J] = ind1[J], ind1[I]
            fit_novo = self.fit_indiv(novo_ind)
            if fit_novo < fit_ind:
                self.pop[index] = novo_ind
                self.fitness[index] = fit_novo
        return novo_ind, fit_ind
    

    
    def troca_1(self, index, mutationRate=0.50): #função insere cidade à frente da cidade mais próxima, dando o index do indivíduo correspondente do self.pop
        ind1 = self.pop[index]
        novo_ind = ind1[:]
        fit_ind=self.fitness[index]
        lista_dists=[]
        for i in range(1,len(ind1)-1): #para nao tentar ir buscar depois cidades fora da lista
            if(random.random() < mutationRate):
                city1 = int(ind1[i])
                index_city1=i
                for i in range(len(ind1)):
                    if city1 != i:
                        lista_dists.append(self.dict[city1,i])
        lista_dists.sort()
        for name, dis in self.dict.items():    
            if lista_dists[0] == dis:
                city_mais_proxima = name[1]
        index_city_prox=ind1.index(city_mais_proxima)
        novo_ind.insert(index_city_prox, novo_ind.pop(index_city1)) 
        fit_novo = self.fit_indiv(novo_ind)
        if fit_novo < fit_ind:
            self.pop[index] = novo_ind
            self.fitness[index] = fit_novo
        return novo_ind, fit_novo
    
    def cruzamento(self): #cruzamento de dois indivíduos, insere metade de um indivíduo numa posição específica de outro indivíduo, retirando os repetidos
        n = 10 #repetição do processo de cruzamentos
        for y in range(n):
            
            ps = random.sample(range(4), 2)
            p1 = ps[0]
            p2 = ps[1]
            parent1 = self.pop[p1]
            parent2 = self.pop[p2]
            temp1 = parent1
            temp2 = parent2
            offspring = []
            s=round(len(parent1)/2)
            c1 = random.sample(temp1,s)
            c2 = random.sample(temp2,s)
            start=random.randint(0,len(self.ID))
            c1_lst=[]
            for i in range(len(temp1)):
                c1_lst.append(temp1[i])
            for i1 in range(len(c2)):
                c1_lst.insert(start,c2[i1])
            unq1 = []
            for x in c1_lst:
                if x not in unq1:
                    unq1.append(x)
            c2_lst=[]
            for n in range(len(temp2)):
                c2_lst.append(temp2[n])
            for i2 in range(len(c1)):
                c2_lst.insert(start,c1[i2])
            unq2 = []
            for x in c2_lst:
                if x not in unq2:
                    unq2.append(x)
            offspring.append(unq1)
            offspring.append(unq2)
            if self.fit_indiv(self.pop[p1]) < self.fit_indiv(unq1):
                self.pop[p1] = unq1 
            if self.fit_indiv(self.pop[p2]) < self.fit_indiv(unq2):
                self.pop[p2] = unq2 
        return offspring
            
    def best_indv(self): #seleção do melhor indivíduo e do seu fitness
        best_lst = self.fitness
        best_ind_lst = self.pop
        for i in range(len(best_lst)):
            best_ind_fit = min(best_lst)
            best_ind = best_ind_lst[i]
        for i in range(len(best_ind)):#para dar o id das cidades correcto em vez do index que começa no 0
            best_ind[i]=best_ind[i]+1
        print(best_ind_fit, best_ind)
        return best_ind_fit, best_ind

    def model(self,n): #modelo que simula n gerações e as possíveis trocas e melhorias no fitness dos indivíduos
        #como input so necessita o número de gerações desejadas
        for i in range(n):
            pop_inic = self.pop
            fit = self.fitness
            for j in range(len(pop_inic)):
                p = random.randint(0,14)
                if p != 11 and p != 10 and p!= 12 and p != 13 and p!= 14:
                    x = self.troca_2(j)
                    if x[1] >= fit[j]:
                        self.troca_2(j)
                elif p == 13:
                    self.troca_1(j)
                elif p == 14 or p == 12 or p == 11 or p == 10:
                    self.troca_3(j)

                    
            print('Resultado da '+ str(i) + 'º geração:', fit)
                

    
        
                
        
        
        
        
        
def test():
    seed = int(input('Seed:')) #Como temos várias escolhas aleatórias nas funções,definimos uma seed, para ser possível a comparação de resultados
    random.seed(seed)
    m =m_cam('file.txt')
    m.get_indiv()
    m.fitness_geral()
    m.cruzamento()
    m.model(200000)
    m.best_indv()

test()



