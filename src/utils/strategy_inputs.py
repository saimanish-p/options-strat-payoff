# src/utils/strategy_inputs.py
from dataclasses import dataclass

# Inputs for Simple Options Strategies
@dataclass
class SingleOptionsInputs:
    strike_price: float
    premium: float
    start_price: float
    end_price: float
    step_size: float

# Inputs for Complex Options Strategies
@dataclass
class BullCallSpreadInputs:
    strike_price_low: float
    strike_price_high: float
    premium_low: float
    premium_high: float
    start_price: float
    end_price: float
    step_size: float

@dataclass
class BearPutSpreadInputs:
    strike_price_high: float
    strike_price_low: float
    premium_high: float
    premium_low: float
    start_price: float
    end_price: float
    step_size: float

@dataclass
class LongStraddleInputs:
    strike_price: float
    premium_call: float
    premium_put: float
    start_price: float
    end_price: float
    step_size: float

@dataclass
class LongStrangleInputs:
    strike_price_low: float
    strike_price_high: float
    premium_call: float
    premium_put: float
    start_price: float
    end_price: float
    step_size: float

@dataclass
class StripInputs:
    strike_price: float
    premium_call: float
    premium_put: float
    start_price: float
    end_price: float
    step_size: float

@dataclass
class StrapInputs:
    strike_price: float
    premium_call: float
    premium_put: float
    start_price: float
    end_price: float
    step_size: float

@dataclass
class LongButterflyInputs:
    strike_price_low: float
    strike_price_middle: float
    strike_price_high: float
    premium_low: float
    premium_middle: float
    premium_high: float
    start_price: float
    end_price: float
    step_size: float