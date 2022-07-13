# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 13:05:10 2022

@author: natarajang
"""
from ietools.Decision import Decision
import numpy as np
import pandas as pd
import unittest

standard = {'maxmax': ('$9 ', 625.0),
 'maxmin': ('$7 ', 225.0),
 'regret': ('$8 ', 25.0),
 'maxlik': ('$9 ', 625.0),
 'ev': ('$8 ', 625.0)}

np_std = {'maxmax': (4, 625.0),
 'maxmin': (2, 225.0),
 'regret': (3, 25.0),
 'maxlik': (4, 625.0),
 'ev': (3, 625.0)}

class TestDec(unittest.TestCase):
    def test_str(self):
        pf = 'Payoff.csv'
        result = Decision(pf)
        result.fit()
        self.assertDictEqual(result.results_, standard)
    
    def test_dict(self):
        pf = {'Steve Decision': {0: '$5 ', 1: '$6 ', 2: '$7 ', 3: '$8 ', 4: '$9 ',5: 'Prob'},
         'Domino $6': {0: 125.0, 1: 200.0, 2: 225.0, 3: 200.0, 4: 125.0, 5: 0.35},
         'Domino $7': {0: 175.0, 1: 300.0, 2: 375.0, 3: 400.0, 4: 375.0, 5: 0.25},
         'Domino $8': {0: 225.0, 1: 400.0, 2: 525.0, 3: 600.0, 4: 625.0, 5: 0.4}}
        result = Decision(pf)
        result.fit()
        self.assertEqual(result.results_, standard)
    
    def test_ndarray(self):
        pf = np.array([[125.0, 175.0, 225.0],
               [200.0, 300.0, 400.0],
               [225.0, 375.0, 525.0],
               [200.0, 400.0, 600.0],
               [125.0, 375.0, 625.0],
               [0.35, 0.25, 0.4]])
        result = Decision(pf)
        result.fit()
        self.assertEqual(result.results_, np_std)
        
    def test_dataframe(self):
        pf = pd.read_csv('Payoff.csv')
        result = Decision(pf)
        result.fit()
        self.assertEqual(result.results_, standard)

if __name__ == '__main__':
    unittest.main()

'''
pf = pd.read_csv('Payoff.csv')
dec = Decision(pf)
#print('Payoff')
#print(dec.payoff)
#print('Alternatives')
#print(dec.alts)
#print('States')
#print(dec.states)
#print('Prob')
#print(dec.prob)
dec.fit()
print(dec.results_)
pay = pf.to_dict()
dec1 = Decision(pay)
dec1.fit()
print(dec1.results_)
#print(pa.head())
'''