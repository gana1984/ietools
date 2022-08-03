"""Engineering Economy."""

__author__ = 'Gana Natarajan <gana1984@gmail.com>'

""" Two classes for basic engineering economy and comparing alterantives.
The third class performs benefit-cost ratio calculations."""

import warnings


class equivalence():
    """ 
    Class to perform basic engineering economy equivalence operations like
    (P/F,i,n), etc. using generally accepted Engineering Economy notations.
    
    Parameters:
        
        convention: {'end' or 'mid'}, default 'end'
        Provides the cash flow convention to use. Only the end of year and 
        mid-year conventions are implemented. Beginnning of year convention may be
        achieved by adjusting n in many cases. So, this implementation is not 
        provided in this version.
        
        fractional: bool, default True
        If fractional is true, calculations are
        performed with interest rate as a fractional value; otherwise calculations
        are performed with interest rate as a whole number, i.e. 10%, 15%, etc.
    
    Notes:
        
        The methods in this class are designed to be used on individual cash flows
        and not a series of cash flows. So, when using the methods, the usage must
        be:
            1000*PgivenF(0.10,5) for finding the present equivalene of a $1000
            cash flow 5 periods in the future.
    
    Methods:
        
        All methods take the same arguments
        i: float
        The interest rate to be used. The methods expect fractional values by default.
        For example, 0.10, 0.50, etc. If fractional is False, then the methods expect
        to get inputs such as 10, 50 for 10% and 50%, respectively.
        
        n: int or float
        Number of periods. Conventionally, this is expected to be an integer, but
        the methods do not check for this and will accept float values as well.
    
    """
    def __init__(self,convention='end',fractional = True):
        self.conv = convention
        if fractional:
            self.fract = 1.0
        else:
            self.fract = 100.0
    
    def PgivenF(self,i,n):
        """Calculates the present value of a future cash flow"""
        if self.conv == 'end':
            return (1.0+i/self.fract)**-n  
        elif self.conv == 'mid':
            return (1.0+i/self.fract)**-(n-0.5)
    
    def FgivenP(self,i,n):
        """ Calculates the future value of a present cash flow"""
        return 1/self.PgivenF(i,n)
    
    def AgivenF(self,i,n):
        """Calculates the equal (annuity) value of a future cash flow"""
        if self.conv == 'end':
            return (i/self.fract)/((1.0+i/self.fract)**n-1)
        elif self.conv == 'mid':
            return (i/self.fract)/((1.0+i/self.fract)**(n-0.5)-1)
    
    def FgivenA(self,i,n):
        """ Calculates the future value of a series of equal cash flows (annuities)"""
        return 1/self.AgivenF(i,n)
    
    def AgivenP(self,i,n):
        """Calculates the future equal (annuity) value of a present cash flow"""
        return ((1.0+i/self.fract)**n)*self.AgivenF(i,n)
    
    def PgivenA(self,i,n):
        """ Calculates the present value of a series of equal cash flows (annuities)"""
        return 1/self.AgivenP(i,n)
    
    def PgivenG(self,i,n):
        """ Calculates the present value of future cash flows that are on an
        arithmetic gradient. Following convention, the first period gradient value
        is zero. For, correct calculations, it may be required to combine the PgivenA and
        this method together."""
        i = i/self.fract
        if self.conv == 'end':
            return (((1.0+i)**n-1)/(i**2*(1.0+i)**n)) - (n/(i*(1.0+i)**n))
        elif self.conv == 'mid':
            n = n-0.5
            return (((1.0+i)**n-1)/(i**2*(1.0+i)**n)) - (n/(i*(1.0+i)**n))
    
    def AgivenG(self,i,n):
        """ Calculates the equal (annuity) cash flows that are on an
        arithmetic gradient. Following convention, the first period gradient value
        is zero. For, correct calculations, it may be required to combine the PgivenA and
        this method together."""
        i = i/self.fract
        if self.conv == 'end':
            return 1.0/i - n/((1.0+i)**n - 1)
        elif self.conv == 'mid':
            n = n-0.5
            return 1.0/i - n/((1.0+i)**n - 1)
        
    def FgivenG(self,i,n):
        """ Calculates the future value of cash flows on an arithmetic gradient.
        Following convention, the first period gradient value is zero."""
        return ((1.0+i/self.fract)**n)*self.PgivenG(i,n)
    
    def Pgiveng(self,i,g,n):
        """ Calculates the present value of a set of future geometric cash flows.
        if g is negative, then the gradient is decreasing. If g is positive, gradient
        increasing.
        
        Arguments:
            
            i: Refer to documentation before.
            
            g: float
            The gradient percent to be used. The method expects fractional values by default.
            For example, 0.10, 0.50, etc. If fractional is False, then the method expect
            to get inputs such as 10, 50 for 10% and 50%, respectively.
            
            n: Refer to documentation before.
        """
        i = i/self.fract
        g = g/self.fract
        if self.conv == 'end':
            if i == g:
                return n/(1.0+i)
            else:
                return (1 - (1.0+g)**n * (1+i)**-n)/(i-g)
        elif self.conv == 'mid':
            n = n-0.5
            if i == g:
                return n/(1.0+i)
            else:
                return (1 - (1.0+g)**n * (1+i)**-n)/(i-g)
            
class compareAlt():
    """compareAlt uses equivalence.
    Class to perform analysis by comparing different alternatives.
    
    Parameters:
        
        cash_flow: lst or array of float
        A list of cash flows, with one cash flow representing the net cash flow for that period.
        The first entry (at index 0) is assumed to be the cash flow at period 0.
        Error handling is not implemented. It is up to the user to make sure the
        inputs are all numeric.
        
        convention: {'end' or 'mid'}, default 'end'
        Provides the cash flow convention to use. Only the end of year and 
        mid-year conventions are implemented. Beginnning of year convention may be
        achieved by adjusting n in many cases. So, this implementation is not 
        provided in this version.
        
        fractional: bool, default True
        If fractional is true, calculations are
        performed with interest rate as a fractional value; otherwise calculations
        are performed with interest rate as a whole number, i.e. 10%, 15%, etc.
    """
    
    def __init__(self,cash_flow,convention='end',fractional = True):
        self.cf = cash_flow
        self.eq = equivalence(convention = convention, fractional = fractional)
    
    def npv(self,interest):
        """ Method to calculate the present value of the cash flows at i = interest.
        Arguments:
            
            interest: float
            The interest rate to be used. The methods expect fractional values by default.
            For example, 0.10, 0.50, etc. If fractional is False, then the methods expect
            to get inputs such as 10, 50 for 10% and 50%, respectively.
        
        Returns:
            pv: float
            Present value of the cash flows using the interest rate provided. Uses
            the PgivenF method inherited from the equivalence class.
        """
        pv = 0
        for period,flow in enumerate(self.cf):
            pv += flow*self.eq.PgivenF(interest,period)
        return pv
    
    def euaw(self,interest):
        """ Method to calculate the annual worth (worth over the n periods of
        cash flow) at i = interest.
        Arguments:
            
            interest: float
            The interest rate to be used. The methods expect fractional values by default.
            For example, 0.10, 0.50, etc. If fractional is False, then the methods expect
            to get inputs such as 10, 50 for 10% and 50%, respectively.
        
        Returns: float
            Annual Worth of the cash flows using the interest rate provided. Uses
            the npv method and the AgivenP method inherited from the equivalence class.
        """
        return self.npv(interest)*self.eq.AgivenP(interest,
                       len(self.cf))
    
    def nfw(self,interest):
        """ Method to calculate the future worth of the cash flows at i = interest.
        Arguments:
            interest: float
            The interest rate to be used. The methods expect fractional values by default.
            For example, 0.10, 0.50, etc. If fractional is False, then the methods expect
            to get inputs such as 10, 50 for 10% and 50%, respectively.
        
        Returns: float
            Future Worth of the cash flows using the interest rate provided. Uses
            the npv method and the FgivenP method inherited from the equivalence class.
        """
        return self.npv(interest)*self.eq.FgivenP(interest,
                       len(self.cf))
        
    def _ppv(self,cf,interest):
        return [flow*self.eq.PgivenF(interest,period) for period,flow in enumerate(cf)]
    
    def _spv(self,ppv):
        return sum(ppv)
    
    def _dnpv(self,ppv,interest):
        #interest = interest/self.eq.fract
        return -1/(interest+1)*sum([period*x for x,period in enumerate(ppv)])
    
    def _ddnpv(self,ppv,interest):
        #interest = interest/self.eq.fract
        return (1/(interest+1)**2)*sum([(period**2)*x for x,period in enumerate(ppv)])
        
    def irr(self,guess=None,max_iter=1e7,threshold=1e-5, verbose = False, itr_to_conv = False):
        """ Method to calculate the internal rate of return of a cash flow.
        This method implements the Newton-Raphson root finding algorithm to
        find the rate r that makes the NPV of the cash flow = 0. Due to the nature
        of how the threshold argument is understood, the fractional format will 
        coverge a lot faster than the fractional = False format.
        
        Arguments:
            
            guess: float, default None
            A guess value to be provided as the start value of the IRR.
            If the user does not provide a guess value, a guess value is calculated
            as follows abs(cf[0])/sum(all other cash flows).
            
            max_iter: float, default 1e7
            Maximum number of iterations to try before stopping the root finding.
            
            threshold: float, default 1e-5
            The threshold npv value at which the iterations may stop.
            
            verbose: bool, default False
            If verbose is True, then the ror calculated at every iteration is
            printed as ("Iteration", itr, "IRR=", r).
            
            itr_to_conv: bool, default False
            If itr_to_conv is True, then the number of iterations it took to converge
            will be printed. This is intended to be a "light" verbose.
        
        Returns:
            
            r: float
            r value is returned in the format compatible with the fractional 
            specification, i.e. if fractional is True the return value will be 0.10 for
            10% IRR; otherwise the return value will be 10.
        """       
        
        itr = 0
        if guess == None:
            r = abs(self.cf[0])/sum(self.cf[1:]) * self.eq.fract
        else:
            r = guess
        npv = sum(self._ppv(self.cf,r))
        while abs(npv) > threshold:
            itr += 1
            if itr > max_iter:
                if verbose:
                    print("Failed to converge after ",itr,"iterations. Returning last value of IRR")
                return "Failed to converge.Last irr = " + r
            #print('here')
            #Calculating f(x) for the NPV equation
            ppv = self._ppv(self.cf,r)
            # Calculate the numeric equivalent of f'(x) for the NPV equation
            dnpv = self._dnpv(ppv,r/self.eq.fract)
            #ddnpv = self._ddnpv(ppv,r/self.eq.fract) - not used.
            npv = sum(ppv)
            # Newton-Raphson update rule. x = x - f(x)/f'(x)
            r -= npv/dnpv
            if verbose:
                print("Iteration: ",itr,"IRR=", r)
        if verbose or itr_to_conv:
            print("Converged after ", itr, "iterations")
        return r
    
class BCRatio():
    """ BCRatio uses compareAlt.
    A class to perform benefit cost ratio analysis.
    Parameters:
        benefit: lst or array of float
        The benefits cash flow. One cash flow per period. User is expected to
        provide positive cash flows (usually).
        
        cost: lst or array of float
        The costs of the project. Similar to benefot one cash flow per period.
        Even though these are costs, it is expected that the cash flows are
        positive.
        
        rate: float
        If fractional = True, it is expected to be fractional, i.e. 0.1 for 10%.
        If fractional = False, then this can be represented as a percentage, i.e.
        10 for 10%.
        If rate is provided, it will be used for both the benefits and costs
        cash flow.
        
        ben_rate: float
        Follows the same fractional rule as rate. User cannot provide both rate
        and ben_rate. A warning is issued if this happens and ben_rate is disregarded.
        
        cost_rate: float
        Follows the same fractional rule as rate. User cannot provide both rate
        and cost_rate. A warning is issued if this happens and cost_rate is disregarded.
        
        convention: {'end' or 'mid'}, default 'end'
        Provides the cash flow convention to use. Only the end of year and 
        mid-year conventions are implemented. Beginnning of year convention may be
        achieved by adjusting n in many cases. So, this implementation is not 
        provided in this version.
        
        fractional: bool, default True
        If fractional is true, calculations are
        performed with interest rate as a fractional value; otherwise calculations
        are performed with interest rate as a whole number, i.e. 10%, 15%, etc.
        
    Raises: ValueError
        When ben_rate is provided but not cost_rate or vice versa, a ValueError
        is raised.
        """
        
    
    def __init__(self,
                 benefit, 
                 cost,
                 rate = None,
                 ben_rate = None,
                 cost_rate = None,
                 convention='end',
                 fractional = True):
        self.benefit = benefit
        self.cost = cost

        if (rate and ben_rate) or (rate and cost_rate):
            warning = 'Rate and ben_rate or cost_rate may not be provided at the same time.\
                Either provide a single rate or provide both ben_rate and cost_rate.\
                    Rate is used as ben_rate and cost_rate'
            warnings.warn(warning)
            self.ben_rate = rate
            self.cost_rate = rate
        elif rate:
            self.ben_rate = rate
            self.cost_rate = rate
        else:
            self.ben_rate = ben_rate
            self.cost_rate = cost_rate
        
        if (ben_rate and not cost_rate) or (cost_rate and not ben_rate):
            raise ValueError("ben_rate and cost_rate must be specified. Missing argument")
            
        self._benefits = compareAlt(benefit, 
                                    convention = convention, 
                                    fractional = fractional)
        self._costs = compareAlt(cost, 
                                 convention = convention, 
                                 fractional = fractional)
    
    def bcr(self):
        """ Method to calculate benefit cost ratio.
        Returns: float
            The benefit-cost ratio is returned as a fraction.
        """
        return self._benefits.npv(self.ben_rate)/self._costs.npv(self.cost_rate)
    