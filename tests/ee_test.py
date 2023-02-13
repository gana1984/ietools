"""Tests for all IE Tools modules"""

__author__ = 'Gana Natarajan <gana1984@gmail.com>'

from ietools import EnggEcon as ee
import unittest

cf = [-1000, 200, 300, 400, 500 ]
data = ee.compareAlt(cf)
interest = 0.1

class TestCompAlt(unittest.TestCase):
   
    def test_npw(self):
        result = data.npw(interest)
        self.assertAlmostEqual(result, 71.78, places = 2)
    
    def test_euaw(self):
        result = data.euaw(interest)
        self.assertAlmostEqual(result, 18.94, places = 2)
    
    def test_nfw(self):
        result = data.nfw(interest)
        self.assertAlmostEqual(result, 115.61, places = 2)
    
    def test_irr(self):
        result = data.irr()
        self.assertAlmostEqual(result, 0.1283, places = 4)


class TestBCR(unittest.TestCase):
    def test_bcr_onerate(self):
        ben = [0, 200, 500, 700, 800]
        cost = [2000, 0, 0, 0, 500]
        data = ee.BCRatio(ben, cost, rate = 0.1)
        result = data.bcr()
        self.assertAlmostEqual(result, 0.7121, places = 4)
        
    def test_bcr_diffrate(self):
        ben = [0, 2000, 2100, 2300, 2500]
        cost = [6000, 100, 110, 120, 200]
        data = ee.BCRatio(ben, cost, ben_rate = 0.1, cost_rate = 0.15)
        result = data.bcr()
        self.assertAlmostEqual(result, 1.0984, places = 4)
    
if __name__ == "__main__":
    unittest.main()


    
