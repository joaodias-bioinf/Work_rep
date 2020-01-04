# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 23:07:44 2019

@author: dias
"""

import requests
from bs4 import BeautifulSoup

class Scraping():
    
    def scraping_to_csv(self,url): #função que retira os dados do url(html) da cidade que for fornecida, neste caso foi o qatar.
        #cria ficheiro txt com os dados 
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            with open('file.txt', 'w', encoding='utf-8') as f_out:
                f_out.write(soup.prettify())
            print('done')
        except TypeError:
            print('Não foi possivel retirar o txt do url fornecido')


def test():
    url = input('url(example: http://www.math.uwaterloo.ca/tsp/world/qa194.tsp):')
    s = Scraping()
    s.scraping_to_csv(url)
        
test()
