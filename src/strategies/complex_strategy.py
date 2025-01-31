import pandas as pd
import numpy as np

class ComplexOptionsStrategies:
    def __init__(self, start_price: float, end_price: float, step_size: float):
        self.start_price = start_price
        self.end_price = end_price
        self.step_size = step_size
        self.expiration_prices = np.arange(start_price, end_price + step_size, step_size)

class BullCallSpread(ComplexOptionsStrategies):
    def __init__(self, strike_price_low, strike_price_high, premium_low, premium_high,
                 start_price, end_price, step_size):
        super().__init__(start_price, end_price, step_size)
        self.strike_price_low = strike_price_low
        self.strike_price_high = strike_price_high
        self.premium_low = premium_low
        self.premium_high = premium_high
        self.net_premium = self.premium_high - self.premium_low
    
    def calculate_payoff(self) -> pd.DataFrame:
        payoffs = []
        for expiration_price in self.expiration_prices:
            # Long call at lower strike
            call_1_value = max(expiration_price - self.strike_price_low, 0)
            # Short call at higher strike
            call_2_value = max(expiration_price - self.strike_price_high, 0)
            # Net payoff = (long call value - short call value) - net premium paid
            net_payoff = (call_1_value - call_2_value) - self.net_premium
            
            payoffs.append((
                expiration_price,
                self.premium_high,  # Premium paid for long call
                self.premium_low,   # Premium received for short call
                call_1_value,
                -call_2_value,     # Negative because it's short
                net_payoff
            ))
            
        return pd.DataFrame(
            payoffs,
            columns=['Expiration Price', 'Call 1: Premium', 'Call 2: Premium', 
                    'Call 1 Value', 'Call 2 Value (Short)', 'Net Payoff']
        )
    
    def calculate_bep(self) -> tuple:
        bep = self.strike_price_low + (self.premium_high - self.premium_low)
        return bep

class BearPutSpread(ComplexOptionsStrategies):
    def __init__(self, strike_price_high, strike_price_low, premium_high, premium_low, 
                 start_price, end_price, step_size):
        super().__init__(start_price, end_price, step_size)
        self.strike_price_high = strike_price_high  # Long put strike
        self.strike_price_low = strike_price_low    # Short put strike
        self.premium_high = premium_high            # Long put premium
        self.premium_low = premium_low              # Short put premium
        # Calculate net premium paid once
        self.net_premium = self.premium_high - self.premium_low
    
    def calculate_payoff(self) -> pd.DataFrame:
        payoffs = []
        for expiration_price in self.expiration_prices:
            # Long put at higher strike
            long_put_value = max(self.strike_price_high - expiration_price, 0)
            # Short put at lower strike
            short_put_value = max(self.strike_price_low - expiration_price, 0)
            # Net payoff = (long put value - short put value) - net premium paid
            net_payoff = (long_put_value - short_put_value) - self.net_premium
            
            payoffs.append((
                expiration_price,
                self.premium_high,   # Premium paid for long put
                self.premium_low,    # Premium received for short put
                long_put_value,
                -short_put_value,    # Negative because it's short
                net_payoff
            ))
        
        return pd.DataFrame(
            payoffs, 
            columns=['Expiration Price', 'Long Put Premium', 'Short Put Premium', 
                    'Long Put Value', 'Short Put Value', 'Net Payoff']
        )

    def calculate_bep(self) -> float:
        return self.strike_price_high - self.net_premium
    
class LongStraddle(ComplexOptionsStrategies):
    def __init__(self, strike_price, premium_call, premium_put,
                 start_price, end_price, step_size):
        super().__init__(start_price, end_price, step_size)
        # Rename variables to be more descriptive
        self.atm_strike = strike_price          # At-the-money strike price for both options
        self.call_premium = premium_call        # Premium paid for call
        self.put_premium = premium_put          # Premium paid for put
        # Calculate total cost (both premiums) once
        self.total_premium = self.call_premium + self.put_premium

    def calculate_payoff(self) -> pd.DataFrame:
        payoffs = []
        for expiration_price in self.expiration_prices:
            # Long call payoff
            long_call_value = max(expiration_price - self.atm_strike, 0)
            # Long put payoff
            long_put_value = max(self.atm_strike - expiration_price, 0)
            # Net payoff = sum of option values minus total premium paid
            net_payoff = long_call_value + long_put_value - self.total_premium
            
            payoffs.append((
                expiration_price,
                self.call_premium,
                self.put_premium,
                long_call_value,
                long_put_value,
                net_payoff
            ))
        
        return pd.DataFrame(
            payoffs, 
            columns=['Expiration Price', 'Call Premium', 'Put Premium', 
                    'Call Value', 'Put Value', 'Net Payoff']
        )

    def calculate_bep(self) -> tuple:
        # Two break-even points for straddle
        lower_bep = self.atm_strike - self.total_premium  # Lower BEP
        upper_bep = self.atm_strike + self.total_premium  # Upper BEP
        return lower_bep, upper_bep
    
class LongStrangle(ComplexOptionsStrategies):
    def __init__(self, strike_price_low, strike_price_high, premium_call, premium_put,
                 start_price, end_price, step_size):
        super().__init__(start_price, end_price, step_size)
        # Rename variables to be more descriptive
        self.put_strike = strike_price_low    # OTM put strike
        self.call_strike = strike_price_high  # OTM call strike
        self.call_premium = premium_call      # Premium paid for OTM call
        self.put_premium = premium_put        # Premium paid for OTM put
        # Calculate total cost once
        self.total_premium = self.call_premium + self.put_premium

    def calculate_payoff(self) -> pd.DataFrame:
        payoffs = []
        for expiration_price in self.expiration_prices:
            # Long OTM call payoff
            call_value = max(expiration_price - self.call_strike, 0)
            # Long OTM put payoff
            put_value = max(self.put_strike - expiration_price, 0)
            # Net payoff = sum of option values minus total premium paid
            net_payoff = call_value + put_value - self.total_premium
            
            payoffs.append((
                expiration_price,
                self.call_premium,
                self.put_premium,
                call_value,
                put_value,
                net_payoff
            ))
        return pd.DataFrame(
            payoffs, 
            columns=['Expiration Price', 'Call Premium', 'Put Premium', 
                    'Call Value', 'Put Value', 'Net Payoff']
        )
    def calculate_bep(self) -> tuple:
        # Two break-even points for strangle
        lower_bep = self.put_strike - self.total_premium   # Lower BEP
        upper_bep = self.call_strike + self.total_premium  # Upper BEP
        return lower_bep, upper_bep
    
class Strip(ComplexOptionsStrategies):
    def __init__(self, strike_price, premium_call, premium_put,
                 start_price, end_price, step_size):
        super().__init__(start_price, end_price, step_size)
        self.atm_strike = strike_price
        self.call_premium = premium_call
        self.put_premium = premium_put
        # Total cost = call premium + (2 * put premium)  # CORRECTED
        self.total_premium = self.call_premium + (2 * self.put_premium)

    def calculate_payoff(self) -> pd.DataFrame:
        payoffs = []
        for expiration_price in self.expiration_prices:
            # One call at the strike
            call_value = max(expiration_price - self.atm_strike, 0)
            
            # Two puts at the strike
            put_value = max(self.atm_strike - expiration_price, 0)
            total_put_value = 2 * put_value  # Value of TWO puts
            
            # Net payoff = value of 1 call + value of 2 puts - total premium
            net_payoff = call_value + total_put_value - self.total_premium
            
            payoffs.append((
                expiration_price,
                self.call_premium,      # Single call premium
                2 * self.put_premium,   # Two puts premium
                call_value,             # Value of 1 call
                total_put_value,        # Value of 2 puts
                net_payoff
            ))
        return pd.DataFrame(
            payoffs, 
            columns=['Expiration Price', 'Call Premium', 'Total Put Premium', 
                    'Call Value', 'Two Puts Value', 'Net Payoff']
        )
    def calculate_bep(self) -> tuple:
        # Break-even points calculation
        lower_bep = self.atm_strike - (self.total_premium / 2)  # Divide by 2 due to 2 puts
        upper_bep = self.atm_strike + self.total_premium  
        return lower_bep, upper_bep
        
class Strap(ComplexOptionsStrategies):
    def __init__(self, strike_price, premium_call, premium_put,
                 start_price, end_price, step_size):
        super().__init__(start_price, end_price, step_size)
        self.atm_strike = strike_price           # At-the-money strike for all options
        self.call_premium = premium_call         # Premium for one call
        self.put_premium = premium_put           # Premium for one put
        # Total cost = (2 * call premium) + put premium
        self.total_premium = (2 * self.call_premium) + self.put_premium

    def calculate_payoff(self) -> pd.DataFrame:
        payoffs = []
        for expiration_price in self.expiration_prices:
            # Two calls at the strike
            call_value = max(expiration_price - self.atm_strike, 0)
            total_call_value = 2 * call_value    # Value of TWO calls
            
            # One put at the strike
            put_value = max(self.atm_strike - expiration_price, 0)
            
            # Net payoff = value of 2 calls + value of 1 put - total premium
            net_payoff = total_call_value + put_value - self.total_premium
            
            payoffs.append((
                expiration_price,
                2 * self.call_premium,  # Two calls premium
                self.put_premium,       # Single put premium
                total_call_value,       # Value of 2 calls
                put_value,              # Value of 1 put
                net_payoff
            ))
        return pd.DataFrame(
            payoffs, 
            columns=['Expiration Price', 'Total Call Premium', 'Put Premium', 
                    'Two Calls Value', 'Put Value', 'Net Payoff']
        )
    def calculate_bep(self) -> tuple:
        # Lower BEP: where put profit equals total premium
        lower_bep = self.atm_strike - self.total_premium
        # Upper BEP: where two calls profit equals total premium
        upper_bep = self.atm_strike + (self.total_premium / 2)  # Divide by 2 due to 2 calls
        return lower_bep, upper_bep
    
class LongButterfly(ComplexOptionsStrategies):
    def __init__(self, strike_price_low, strike_price_middle, strike_price_high,
                 premium_low, premium_middle, premium_high,
                 start_price, end_price, step_size):
        super().__init__(start_price, end_price, step_size)
        # Store strikes
        self.long_lower_strike = strike_price_low
        self.short_middle_strike = strike_price_middle
        self.long_upper_strike = strike_price_high
        # Store premiums
        self.lower_premium = premium_low
        self.middle_premium = premium_middle
        self.upper_premium = premium_high
        # Calculate net premium paid
        self.net_premium = (self.lower_premium + self.upper_premium) - (2 * self.middle_premium)

    def calculate_payoff(self) -> pd.DataFrame:
        # First calculate BEPs
        lower_bep = self.long_lower_strike + self.net_premium
        upper_bep = self.long_upper_strike - self.net_premium
        
        # Create expiration price array including BEPs
        all_prices = set(np.arange(self.start_price, self.end_price + self.step_size, self.step_size))
        all_prices.add(lower_bep)  # Add lower BEP
        all_prices.add(upper_bep)  # Add upper BEP
        all_prices.add(self.short_middle_strike)  # Add middle strike for max profit
        expiration_prices = sorted(list(all_prices))
        
        payoffs = []
        for expiration_price in expiration_prices:
            # Long lower call
            lower_call_value = max(expiration_price - self.long_lower_strike, 0)
            # Short TWO middle calls (negative value)
            middle_call_value = -2 * max(expiration_price - self.short_middle_strike, 0)
            # Long upper call
            upper_call_value = max(expiration_price - self.long_upper_strike, 0)
            # Net payoff = sum of values - net premium
            net_payoff = (lower_call_value + middle_call_value + upper_call_value) - self.net_premium
            
            payoffs.append((
                expiration_price,
                self.net_premium,
                lower_call_value,
                middle_call_value,
                upper_call_value,
                net_payoff
            ))
        
        return pd.DataFrame(
            payoffs,
            columns=['Expiration Price', 'Net Premium', 'Lower Call Value', 
                    'Middle Call Value', 'Upper Call Value', 'Net Payoff']
        )
    def calculate_bep(self) -> tuple:
        # Break-even points
        lower_bep = self.long_lower_strike + self.net_premium
        upper_bep = self.long_upper_strike - self.net_premium
        return lower_bep, upper_bep