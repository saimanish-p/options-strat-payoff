# src/utils/validators.py
from dataclasses import dataclass
from .strategy_inputs import (
    SingleOptionsInputs,
    BullCallSpreadInputs,
    BearPutSpreadInputs,
    LongStraddleInputs,
    LongStrangleInputs,
    StripInputs,
    StrapInputs,
    LongButterflyInputs
)

@dataclass
class ValidationResult:
    is_valid: bool
    message: str
    severity: str  # e.g., "error", "warning"

class StrategyValidator:
    @staticmethod
    def validate_bull_call_spread(inputs: BullCallSpreadInputs) -> ValidationResult:
        if inputs.strike_price_low >= inputs.strike_price_high:
            return ValidationResult(False, "Call 1 Strike Price (Lower) must be less than Call 2 Strike Price (Higher)", "error")
        if inputs.premium_low >= inputs.premium_high:
            return ValidationResult(False, "Call 2 Premium (Lower) must be less than Call 1 Premium (Higher)", "error")
        if inputs.start_price >= inputs.strike_price_low:
            return ValidationResult(False, "Start Price must be less than Call 1 Strike Price (Lower)", "error")
        if inputs.end_price <= inputs.strike_price_high:
            return ValidationResult(False, "End Price must be greater than Call 2 Strike Price (Higher)", "error")
        return ValidationResult(True, "", "")

    @staticmethod
    def validate_bear_put_spread(inputs: BearPutSpreadInputs) -> ValidationResult:
        if inputs.strike_price_low >= inputs.strike_price_high:
            return ValidationResult(False, 
                "Lower Strike (Short Put) must be less than Higher Strike (Long Put)","error")
        if inputs.premium_low >= inputs.premium_high:
            return ValidationResult(False, 
                "Short Put Premium must be less than Long Put Premium","error")
        if inputs.start_price >= inputs.strike_price_high:
            return ValidationResult(False, 
                "Start Price must be less than Higher Strike Price","error")
        if inputs.end_price <= inputs.strike_price_low:
            return ValidationResult(False, 
                "End Price must be greater than Lower Strike Price","error")
        return ValidationResult(True, "", "")

    @staticmethod
    def validate_long_straddle(inputs: LongStraddleInputs) -> ValidationResult:
        if inputs.premium_call <= 0:
            return ValidationResult(False, "Call Premium must be positive", "error")
        if inputs.premium_put <= 0:
            return ValidationResult(False, "Put Premium must be positive", "error")
        if inputs.start_price >= inputs.strike_price - (inputs.premium_call + inputs.premium_put):
            return ValidationResult(False, "Start Price should be below lower break-even point", "error")
        if inputs.end_price <= inputs.strike_price + (inputs.premium_call + inputs.premium_put):
            return ValidationResult(False, "End Price should be above upper break-even point", "error")
        return ValidationResult(True, "", "")

    @staticmethod
    def validate_long_strangle(inputs: LongStrangleInputs) -> ValidationResult:
        if inputs.strike_price_low >= inputs.strike_price_high:
            return ValidationResult(False, "Put Strike must be less than Call Strike", "error")
        if inputs.premium_call <= 0:
            return ValidationResult(False, "Call Premium must be positive", "error")
        if inputs.premium_put <= 0:
            return ValidationResult(False, "Put Premium must be positive", "error")
        total_premium = inputs.premium_call + inputs.premium_put
        if inputs.start_price >= inputs.strike_price_low - total_premium:
            return ValidationResult(False, "Start Price should be below lower break-even point", "error")
        if inputs.end_price <= inputs.strike_price_high + total_premium:
            return ValidationResult(False, "End Price should be above upper break-even point", "error")
        return ValidationResult(True, "", "")

    @staticmethod
    def validate_strip(inputs: StripInputs) -> ValidationResult:
        if inputs.premium_call <= 0:
            return ValidationResult(False, "Call Premium must be positive", "error")
        if inputs.premium_put <= 0:
            return ValidationResult(False, "Put Premium must be positive", "error")
        
        total_premium = (2 * inputs.premium_call) + inputs.premium_put
        lower_bep = inputs.strike_price - total_premium
        upper_bep = inputs.strike_price + (total_premium / 2)
        
        if inputs.start_price >= lower_bep:
            return ValidationResult(False, "Start Price should be below lower break-even point", "error")
        if inputs.end_price <= upper_bep:
            return ValidationResult(False, "End Price should be above upper break-even point", "error")
        return ValidationResult(True, "", "")

    @staticmethod
    def validate_strap(inputs: StrapInputs) -> ValidationResult:
        if inputs.premium_call <= 0:
            return ValidationResult(False, "Call Premium must be positive", "error")
        if inputs.premium_put <= 0:
            return ValidationResult(False, "Put Premium must be positive", "error")
        
        total_premium = (2 * inputs.premium_call) + inputs.premium_put
        lower_bep = inputs.strike_price - total_premium
        upper_bep = inputs.strike_price + (total_premium / 2)
        
        if inputs.start_price >= lower_bep:
            return ValidationResult(False, "Start Price should be below lower break-even point", "error")
        if inputs.end_price <= upper_bep:
            return ValidationResult(False, "End Price should be above upper break-even point", "error")
        return ValidationResult(True, "", "")

    @staticmethod
    def validate_long_butterfly(inputs: LongButterflyInputs) -> ValidationResult:
        # Check strike price order
        if inputs.strike_price_low >= inputs.strike_price_middle:
            return ValidationResult(False, "Lower strike must be less than middle strike", "error")
        if inputs.strike_price_middle >= inputs.strike_price_high:
            return ValidationResult(False, "Middle strike must be less than upper strike", "error")
            
        # Check equal strike price distances
        lower_diff = inputs.strike_price_middle - inputs.strike_price_low
        upper_diff = inputs.strike_price_high - inputs.strike_price_middle
        if abs(lower_diff - upper_diff) > 0.01:  # Allow small floating point differences
            return ValidationResult(False, "Distance between strikes must be equal", "error")
        
        # Check premium relationships
        if inputs.premium_low >= inputs.premium_middle:
            return ValidationResult(False, "ITM call premium must be less than ATM call premium", "error")
        if inputs.premium_middle >= inputs.premium_high:
            return ValidationResult(False, "ATM call premium must be less than OTM call premium", "error")
        
        # Check price range
        net_premium = (inputs.premium_low + inputs.premium_high) - (2 * inputs.premium_middle)
        if inputs.start_price >= inputs.strike_price_low - net_premium:
            return ValidationResult(False, "Start Price should be below lower break-even point", "error")
        if inputs.end_price <= inputs.strike_price_high + net_premium:
            return ValidationResult(False, "End Price should be above upper break-even point", "error")
            
        return ValidationResult(True, "", "")
    
    @staticmethod
    def validate_basic_inputs(inputs: SingleOptionsInputs) -> ValidationResult:
        if inputs.strike_price <= 0 or inputs.premium <= 0:
            return ValidationResult(False, "Strike Price and Premium must be positive", "error")
        if inputs.start_price >= inputs.strike_price:
            return ValidationResult(False, "Start Price must be less than Strike Price", "error")
        if inputs.end_price <= inputs.strike_price:
            return ValidationResult(False, "End Price must be greater than Strike Price", "error")
        return ValidationResult(True, "", "")