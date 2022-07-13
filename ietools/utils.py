__author__ = 'Gana Natarajan <gana1984@gmail.com>'

"""
Utility functions used throughout ietools
"""
from math import gcd

"""Engineering Econ Utility Functions"""

def effect(r,m, fractional = True):
    """Method to calculate effective interest rate.
    Arguments:
        
        r: float 
        APR or other interest rate for which effective rate needs to be
        calculated.
        
        m: float or int
        Number of compounding periods. In some cases, when a 
        k is used, this factor may be a float. Usually expected to be an int.
        
        fractional: bool, default True
        If fractional is true, calculations are
        performed with interest rate as a fractional value; otherwise calculations
        are performed with interest rate as a whole number, i.e. 10%, 15%, etc.
    
    Returns: {float} 
        Effective interest rate calculated using the formula (1+r/m)^m-1
    """
    if fractional:
        fract = 1.0
    else:
        fract = 100.0
    return ((1+r/(fract*m))**m - 1)*fract


def cfCommon(cash_flows):
    """ Method to generate common period cash flows, primarily for use in npv
    and ror analyses. The method follows the least common multiple (LCM) rule to
    generate cash flows over equal periods for comparing alternatives. Cash flows
    are matched with the last cash flow and the initial investment calculated
    as a net cash flow. The cash flows are then broadcasted for the period of
    the LCM.
    
    Arguments: 
        cash_flows: dict
        Cash flows for the multiple alternatives provided as a dict.
        e.g.: {'cf1':[-1000,300,400,500],'cf2':[-2000,300,400,500,600]}
    
    Returns:
        
        cash_flows: dict
        Cash flows are combined and broadcasted over the LCM period and returned
        using the original dict.
    
    Example:
        
        For the example provided above, expect the following output
        {'cf1': [-1000, 300, 400, -500, 300, 400, -500, 300, 400, -500, 300, 400, 500], 
         'cf2': [-2000, 300, 400, 500, -1400, 300, 400, 500, -1400, 300, 400, 500, 600]}
        
        This is based on an LCM of 12. Cf1 is repeated 4 times and Cf2 is repeated
        3 times, with the salvage value retained in the last cycle, as there are no
        more initial costs.
    """
    
    def _horizon(cf):
        horizon = []
        for k,v in cf.items():
            horizon.append(len(v)-1)
        return horizon
    n = _horizon(cash_flows)

    def _lcm(arr):
        lcm = 1
        for num in arr:
            lcm = lcm * num // gcd(lcm,num)
        return lcm
    
    lcm = _lcm(n)

    for i,k in enumerate(cash_flows):
        cash_flows[k][-1] = cash_flows[k][0] + cash_flows[k][-1]
        cash_flows[k] = cash_flows[k] + (cash_flows[k][1:] * int(lcm/n[i]-1))
        cash_flows[k][-1] = cash_flows[k][-1]-cash_flows[k][0]
    
    return cash_flows
