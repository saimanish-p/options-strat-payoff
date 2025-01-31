import numpy as np
import pandas as pd

class BaseOptionsStrategy:
    def __init__(self, start_price: float, end_price: float, step_size: float, strike_price: float = None, premium: float = None):
        self.start_price = start_price
        self.end_price = end_price
        self.step_size = step_size
        self.expiration_prices = np.arange(start_price, end_price + step_size, step_size)
        self.strike_price = strike_price
        self.premium = premium
    
class LongCall(BaseOptionsStrategy):
    def calculate_payoff(self) -> pd.DataFrame:
        payoffs = []
        for expiration_price in self.expiration_prices:
            call_value = max(expiration_price - self.strike_price, 0)
            net_payoff = call_value - self.premium
            payoffs.append((expiration_price, self.premium, call_value, net_payoff))
        
        return pd.DataFrame(
            payoffs, 
            columns=['Expiration Price', 'Premium', 'Call Value', 'Net Payoff']
        )
    def calculate_bep(self) -> float:
        return self.strike_price + self.premium
    
class ShortCall(BaseOptionsStrategy):
    def calculate_payoff(self) -> pd.DataFrame:
        payoffs = []
        for expiration_price in self.expiration_prices:
            call_value = max(expiration_price - self.strike_price, 0)
            net_payoff = self.premium - call_value
            payoffs.append((expiration_price, self.premium, call_value, net_payoff))
        
        return pd.DataFrame(
            payoffs, 
            columns=['Expiration Price', 'Premium', 'Call Value', 'Net Payoff']
        )

    def calculate_bep(self) -> float:
        return self.strike_price + self.premium

class LongPut(BaseOptionsStrategy):
    def calculate_payoff(self) -> pd.DataFrame:
        payoffs = []
        for expiration_price in self.expiration_prices:
            put_value = max(self.strike_price - expiration_price, 0)
            net_payoff = put_value - self.premium
            payoffs.append((expiration_price, self.premium, put_value, net_payoff))
        
        return pd.DataFrame(
            payoffs, 
            columns=['Expiration Price', 'Premium', 'Put Value', 'Net Payoff']
        )

    def calculate_bep(self) -> float:
        return self.strike_price - self.premium

class ShortPut(BaseOptionsStrategy):
    def calculate_payoff(self) -> pd.DataFrame:
        payoffs = []
        for expiration_price in self.expiration_prices:
            put_value = max(self.strike_price - expiration_price, 0)
            net_payoff = self.premium - put_value
            payoffs.append((expiration_price, self.premium, put_value, net_payoff))
        
        return pd.DataFrame(
            payoffs, 
            columns=['Expiration Price', 'Premium', 'Put Value', 'Net Payoff']
        )

    def calculate_bep(self) -> float:
        return self.strike_price - self.premium