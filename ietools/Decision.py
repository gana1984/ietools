"""Decision Making under Uncertainty"""

__author__ = 'Gana Natarajan <gana1984@gmail.com>'

""" A decision making under uncertainty class that uses the maxmin,
maxmax, minmax regret, maximum likelihood, and expected value criteria."""
import numpy as np
import pandas as pd

class Decision():
    """ Class to implement the different decision criteria.
    Parameters:
        
        payoff: {'str', 'ndarray', 'dict', or 'pandas DataFrame'}, required
        payoff matrix is always expected to be of the same format:
                      State_1     State_2 ... State_n
         --------------------------------------------
         Alternate_1 payoff_11   payoff_12...payoff_1n
         ---------------------------------------------
         Alternate_2 payoff_21   payoff_22...payoff_2n
         .
         .
         .
         ---------------------------------------------
         Alternate_m payoff_m1   payoff_m2...payoff_mn
         ----------------------------------------------
         Probability p(State_1) p(State_2)... p(State_n)
         -----------------------------------------------
         
         States and Alternates are of type str.
         Payoffs are expected to be of type float.
         The last row of the matrix must be probability of the states.
         
         In future implementations, the orientation of the matrix and
         position of the probabilities may be provided as an input by the user.
         
         If payoff is a 'str', it is expected to be a path and/or filename of type .csv.
         The file must be structured as described in the format above.
         If payoff is an 'ndarray' it is expected to be a numpy array of just the numbers,
         without any column headers or row names.
         If payoff is a 'dict' it will be coverted to a pandas DataFrame assuming
         orient = 'columns'. In future versions, other orientations will be implemented.
         If payoff is a 'pandas DataFrame' then it is expected to be in the format
         specified above.
         
         criteria: lst, default ['maxmax','maxmin','regret','maxlik','ev']
         A list of required criteria. Even is only a single criteria is needed,
         the input must be provided as a list.
     
     Attributes:
         
         states: ndarray of shape (n_states) {int or str}
         The states are stored in an array. If payoff was in a format that
         did not have states, then the array contains int 0...n. Unless needed
         do not access or modify this attribute.
         
         alts: ndarray of shape (m_alternates) {int or str}
         The alterantes are stored in an array. If payoff was in a format that
         did not have alternate names, then the array contains int 0...m. 
         Unless needed do not access or modify this attribute.
         
         prob: ndarray of shape (n_states)
         The last row of the payoff matrix containing the probabilities for each
         state
         
         payoff: ndarray of shape (m_alts, n_states)
         The payoff matrix as a numpy array.
         
         maxmax_dec_: {str or int}
         Decision using the maxmax criterion, calculated as the maximum of the
         largest payoffs in each row. The decision will be a str if names were 
         available from the input; if not the decision is just the index of the
         alternative that should be selected, following 0-indexing.
         
         maxmax_pf_: float
         The payoff corresponding to the maxmax criteria
         
         maxmin_dec_: {str or int}
         Decision using the maxmin criterion, calculated as the maximum of the
         smallest payoffs in each row. The decision will be a str if names were 
         available from the input; if not the decision is just the index of the
         alternative that should be selected, following 0-indexing.
         
         maxmin_pf_: float
         The payoff corresponding to the maxmin criterion
         
         regret_dec_: {str or int}
         Decision using the minmax regret criterion, calculated as the minimum
         of the maximum regret (opportunity cost) of each alternative. 
         The decision will be a str if names were available from the input; if 
         not the decision is just the index of the alternative that should be 
         selected, following 0-indexing.
         
         regret_pf_: float
         The payoff corresponding to the minmax regret criterion
         
         regret_: ndarray
         Regret matrix. The regret matrix is calculated as follows:
             In each column, the values are subtracted from the max in that 
             column, i.e.: opportunity cost. The regret matrix does not have
             the alternates and states - just the regret numbers. You may use
             the alts and states attributes to get these.
        
        maxlik_dec_: {str or int}
        Decision using the maximum likelihood criterion, calculated as the 
        maximum of the payoffs for the most likely state. The decision will be a str if names were 
        available from the input; if not the decision is just the index of the
        alternative that should be selected, following 0-indexing.
        
        maxlik_pf_: float
        The payoff corresponding to the maximum likelihood criterion
        
        ev_dec_: {str or int}
        Decision using the expected value criterion, calculated as the maximum 
        of the expected value from each row. Expected value is calculated as a
        dot product of payoff and probabilities. The decision will be a str if 
        names were available from the input; if not the decision is just the 
        index of the alternative that should be selected, following 0-indexing.
        
        ev_pf_: float
        The payoff corresponding to the expected value criterion
        
        results_: dict
        This attribute is a dictionary with criteria as the key and a tuple of
        (dec_,pf_) as the values. Instead of accessing each individual attribute,
        we suggest this attribute be used. Only those criteria provided in the
        parameter "criteria" are included in the dict.
        
        regret_ attribute, which stores the regret matrix is not part of this
        dict. The user has to access that attribute separately.
         
    """         
     
    def __init__(self, 
                 payoff,
                 criteria = ['maxmax','maxmin','regret','maxlik','ev'],
                 **kwargs):
        self.crit = criteria
        self.alts, self.states, self.prob, self.payoff = self._read_payoff(payoff)
        self.prob = np.reshape(self.prob,(-1,1))
        self.regret = None
        self.results_ = {}
        

    def _payoffFromDF(self,df):
        alts = df.iloc[:-1,0].values
        df = df.iloc[: , 1:]
        states = df.columns.values
        prob = df.iloc[-1].values
        payoff = df.iloc[:-1,].values
        return alts, states, prob, payoff
    
    def _read_payoff(self,payoff):
        if type(payoff) is str:
            try:
                payoff = pd.read_csv(payoff)
            except:
                raise Exception('{} is not a valid file. Please provide a valid csv file name'.format(payoff))
            alts, states, prob, payoff = self._payoffFromDF(payoff)
            #print(payoff.head())
        
        elif type(payoff) is np.ndarray:
            prob = payoff[-1,:]
            payoff = payoff[:-1,:]
            alts = np.array([i for i in range(payoff.shape[0])])
            states = np.array([i for i in range(payoff.shape[1])])
            #print(payoff,prob, sep = '\n')
            
        elif type(payoff) is dict:
            payoff = pd.DataFrame.from_dict(payoff, orient = 'columns')
            alts, states, prob, payoff = self._payoffFromDF(payoff)
            
        elif type(payoff) is pd.core.frame.DataFrame:
            alts,states,prob,payoff = self._payoffFromDF(payoff)
        
        return alts, states, prob, payoff
    
    def _build_dict(self, criteria, decision, payoff):
        self.results_.update({criteria:(decision,payoff)})
        
    def fit(self):
        """ Calculates the decision and payoffs for all the criteria mentioned
        at the time of instantiation.
        The fit method must be run for results_ to be non-empty.
        
        Raises: ValueError
            Value error is raised if the mentioned criterion does not fit
            any of the criteria defined in the class.            
        """
        for criterion in self.crit:
            if criterion == 'maxmax':
                self.maxmax_dec_ = self.alts[self.payoff.max(axis = 1).argmax()]
                self.maxmax_pf_ = self.payoff.max(axis = 1).max()
                self._build_dict(criterion, self.maxmax_dec_, self.maxmax_pf_)
            elif criterion == 'maxmin':
                self.maxmin_dec_ = self.alts[self.payoff.min(axis = 1).argmax()]
                self.maxmin_pf_ = self.payoff.min(axis = 1).max()
                self._build_dict(criterion, self.maxmin_dec_, self.maxmin_pf_)
            elif criterion == 'regret':
                self.regret_ = self.payoff.max(axis = 0) - self.payoff
                self.regret_dec_ = self.alts[self.regret_.max(axis = 1).argmin()]
                self.regret_pf_ = self.regret_.max(axis = 1).min()
                self._build_dict(criterion, self.regret_dec_, self.regret_pf_)
            elif criterion == 'maxlik':
                self.mle_dec_ = self.alts[self.payoff[:,self.prob.argmax()].argmax()]
                self.mle_pf_ = self.payoff[:,self.prob.argmax()].max()
                self._build_dict(criterion, self.mle_dec_, self.mle_pf_)
            elif criterion == 'ev':
                dotprod = self.payoff @ self.prob
                self.ev_dec_ = self.alts[dotprod.argmax()]
                self.ev_pf_ = dotprod.max()
                self._build_dict(criterion, self.ev_dec_, self.mle_pf_)
            else:
                raise ValueError(
                    'The provided criteria {} does not exist. Please check and provide an appropriate criteria'
                    .format(criterion))

