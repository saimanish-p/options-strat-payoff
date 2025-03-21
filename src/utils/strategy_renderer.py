import streamlit as st
import numpy as np
from typing import Type, Union

# Importing validators
from src.utils.validators import StrategyValidator

# Importing formatters
from src.utils.formatters import DataFormatter

# Importing strategy inputs
from src.utils.strategy_inputs import (
    SingleOptionsInputs,
    BullCallSpreadInputs,
    BearPutSpreadInputs,
    LongStraddleInputs,
    LongStrangleInputs,
    StripInputs,
    StrapInputs,
    LongButterflyInputs
)

# Importing base strategies
from src.strategies.base_strategy import (
    LongCall,
    ShortCall,
    LongPut,
    ShortPut
)

# Importing complex strategies
from src.strategies.complex_strategy import (
    BullCallSpread,
    BearPutSpread,
    LongStraddle,
    LongStrangle,
    Strip,
    Strap,
    LongButterfly
)

# Importing payoff plotters
from src.visualisations.payoff_plots import (
    Basic_Payoff_Plotter,
    BullCallSpreadPlotter,
    BearPutSpreadPlotter,
    LongStraddlePlotter,
    LongStranglePlotter,
    StripPlotter,
    StrapPlotter,
    LongButterflyPlotter
)

class StrategyRenderer:

    @staticmethod
    def render_strategy(strategy_class: Type[Union[
        LongCall, 
        ShortCall, 
        LongPut, 
        ShortPut,
        BullCallSpread, 
        BearPutSpread, 
        LongStraddle, 
        LongStrangle, 
        Strip, 
        Strap, 
        LongButterfly
    ]], strategy_name: str):

        # Normalize the strategy name by removing spaces
        normalized_strategy_name = strategy_name.replace(" ", "")

        # Determine if the strategy is a multiple options strategy
        is_multiple_options = normalized_strategy_name in ['BullCallSpread', 'BearPutSpread', 'LongStraddle', 'LongStrangle', 'Strip', 'Strap', 'LongButterfly']
        is_single_options = normalized_strategy_name in ['LongCall', 'ShortCall', 'LongPut', 'ShortPut']
        
        # Get user inputs
        inputs = None

        if is_multiple_options:
            # Manually provide default values for multiple options strategies
            if normalized_strategy_name == 'BullCallSpread':
                inputs = BullCallSpreadInputs(
                    strike_price_low=st.sidebar.number_input("Call 1: Lower Strike Price (ITM)", value=90.0, step=1.0, 
                                                            help="Strike price of the ITM call option you're buying"),
                    strike_price_high=st.sidebar.number_input("Call 2: Higher Strike Price (OTM)", value=110.0, step=1.0,
                                                             help="Strike price of the OTM call option you're selling"),
                    premium_high=st.sidebar.number_input("Call 1: Premium (ITM)", value=15.0, step=1.0,
                                                        help="Premium paid for the ITM call option"),  
                    premium_low=st.sidebar.number_input("Call 2: Premium (OTM)", value=5.0, step=1.0,
                                                       help="Premium received for the OTM call option"),  
                    start_price=st.sidebar.number_input("Start Expiration Price", value=80.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Expiration Price", value=120.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis")
                )
            
            elif normalized_strategy_name == 'BearPutSpread':
                inputs = BearPutSpreadInputs(
                    strike_price_high=st.sidebar.number_input("Long Put Strike (Higher)", value=110.0, step=1.0,
                                                             help="Strike price of the higher put option you're buying"),
                    strike_price_low=st.sidebar.number_input("Short Put Strike (Lower)", value=90.0, step=1.0,
                                                            help="Strike price of the lower put option you're selling"),
                    premium_high=st.sidebar.number_input("Long Put Premium (Higher)", value=15.0, step=1.0,
                                                        help="Premium paid for the higher strike put option"),
                    premium_low=st.sidebar.number_input("Short Put Premium (Lower)", value=5.0, step=1.0,
                                                       help="Premium received for the lower strike put option"),
                    start_price=st.sidebar.number_input("Start Expiration Price", value=80.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Expiration Price", value=120.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis")
                )            
            
            elif normalized_strategy_name == 'LongStraddle':
                inputs = LongStraddleInputs(
                    strike_price=st.sidebar.number_input("Call & Put ATM Strike Price", value=100.0, step=1.0,
                                                        help="Strike price for both the call and put options (typically ATM)"),
                    premium_call=st.sidebar.number_input("Call Option Premium", value=6.0, step=1.0,
                                                        help="Premium paid for the call option"),
                    premium_put=st.sidebar.number_input("Put Option Premium", value=4.0, step=1.0,
                                                       help="Premium paid for the put option"),
                    start_price=st.sidebar.number_input("Start Expiration Price", value=80.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Expiration Price", value=120.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis")
                )            
            
            elif normalized_strategy_name == 'LongStrangle':
                inputs = LongStrangleInputs(
                    strike_price_low=st.sidebar.number_input("OTM Put Strike Price", value=80.0, step=1.0,
                                                           help="Strike price of the OTM put option (lower than current price)"),
                    strike_price_high=st.sidebar.number_input("OTM Call Strike Price", value=100.0, step=1.0,
                                                            help="Strike price of the OTM call option (higher than current price)"),
                    premium_call=st.sidebar.number_input("OTM Call Premium", value=4.0, step=1.0,
                                                        help="Premium paid for the OTM call option"),
                    premium_put=st.sidebar.number_input("OTM Put Premium", value=6.0, step=1.0,
                                                       help="Premium paid for the OTM put option"),
                    start_price=st.sidebar.number_input("Start Expiration Price", value=60.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Expiration Price", value=120.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis")
                )  

            elif normalized_strategy_name == 'Strip':
                inputs = StripInputs(
                    strike_price=st.sidebar.number_input("ATM Strike Price", value=100.0, step=1.0,
                                                        help="Strike price for both the call and puts (typically ATM)"),
                    premium_call=st.sidebar.number_input("Single Call Premium", value=8.0, step=1.0,
                                                        help="Premium paid for the single call option"),
                    premium_put=st.sidebar.number_input("Put Premium", value=6.0, step=1.0,
                                                       help="Premium paid for each put option (you buy 2 puts)"),
                    start_price=st.sidebar.number_input("Start Expiration Price", value=60.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Expiration Price", value=140.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Price Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis"),
                )    

            elif normalized_strategy_name == 'Strap':
                inputs = StrapInputs(
                    strike_price=st.sidebar.number_input("ATM Strike Price", value=100.0, step=1.0,
                                                        help="Strike price for both the calls and put (typically ATM)"),
                    premium_call=st.sidebar.number_input("Single Call Premium", value=11.0, step=1.0,
                                                        help="Premium paid for each call option (you buy 2 calls)"),
                    premium_put=st.sidebar.number_input("Put Premium", value=8.0, step=1.0,
                                                       help="Premium paid for the single put option"),
                    start_price=st.sidebar.number_input("Start Expiration Price", value=60.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Expiration Price", value=140.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis"),
                )     

            elif normalized_strategy_name == 'LongButterfly':
                inputs = LongButterflyInputs(
                    strike_price_low=st.sidebar.number_input("Lower Strike (ITM)", value=120.0, step=1.0,
                                                           help="Lower strike price - buy 1 ITM call"),
                    strike_price_middle=st.sidebar.number_input("Middle Strike (ATM)", value=125.0, step=1.0,
                                                              help="Middle strike price - sell 2 ATM calls"),
                    strike_price_high=st.sidebar.number_input("Upper Strike (OTM)", value=130.0, step=1.0,
                                                            help="Upper strike price - buy 1 OTM call"),
                    premium_low=st.sidebar.number_input("ITM Call Premium", value=3.0, step=1.0,
                                                       help="Premium paid for the ITM call option"),
                    premium_middle=st.sidebar.number_input("ATM Call Premium", value=4.0, step=1.0,
                                                         help="Premium received for each ATM call option (you sell 2)"),
                    premium_high=st.sidebar.number_input("OTM Call Premium", value=6.0, step=1.0,
                                                        help="Premium paid for the OTM call option"),
                    start_price=st.sidebar.number_input("Start Expiration Price", value=90.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Expiration Price", value=160.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis")
                )            
            else:
                st.error("Unknown strategy selected.")
                return
        
        if is_single_options:

            if normalized_strategy_name == 'LongCall':
                inputs = SingleOptionsInputs(
                    strike_price=st.sidebar.number_input("Strike Price", value=100.0, step=1.0,
                                                        help="Price at which you can buy the underlying asset"),
                    premium=st.sidebar.number_input("Premium", value=5.0, step=0.1,
                                                   help="Price paid for the call option"),
                    start_price=st.sidebar.number_input("Start Price", value=60.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Price", value=140.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis")
                )
            elif normalized_strategy_name == 'ShortCall':
                inputs = SingleOptionsInputs(
                    strike_price=st.sidebar.number_input("Strike Price", value=100.0, step=1.0,
                                                        help="Price at which you must sell the underlying asset if option is exercised"),
                    premium=st.sidebar.number_input("Premium", value=5.0, step=0.1,
                                                   help="Price received for selling the call option"),
                    start_price=st.sidebar.number_input("Start Price", value=60.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Price", value=140.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis")
                )
            elif normalized_strategy_name == 'LongPut':
                inputs = SingleOptionsInputs(
                    strike_price=st.sidebar.number_input("Strike Price", value=100.0, step=1.0,
                                                        help="Price at which you can sell the underlying asset"),
                    premium=st.sidebar.number_input("Premium", value=5.0, step=0.1,
                                                   help="Price paid for the put option"),
                    start_price=st.sidebar.number_input("Start Price", value=60.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Price", value=140.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis")
                )
            elif normalized_strategy_name == 'ShortPut':
                inputs = SingleOptionsInputs(
                    strike_price=st.sidebar.number_input("Strike Price", value=100.0, step=1.0,
                                                        help="Price at which you must buy the underlying asset if option is exercised"),
                    premium=st.sidebar.number_input("Premium", value=5.0, step=0.1,
                                                   help="Price received for selling the put option"),
                    start_price=st.sidebar.number_input("Start Price", value=60.0, step=1.0,
                                                       help="Lower bound of stock price range for analysis"),
                    end_price=st.sidebar.number_input("End Price", value=140.0, step=1.0,
                                                     help="Upper bound of stock price range for analysis"),
                    step_size=st.sidebar.number_input("Step Size", value=5.0, step=1.0,
                                                     help="Increment between price points in the analysis")
                )

            else:
                st.error("Unknown strategy selected.")
                return
                
        # Error handling for unknown strategies
        if inputs is None:
            st.error("Unknown strategy selected.")
            return

        # Validate inputs
        if is_multiple_options:
            if normalized_strategy_name == 'BullCallSpread':
                validation_result = StrategyValidator.validate_bull_call_spread(inputs)
            elif normalized_strategy_name == 'BearPutSpread':
                validation_result = StrategyValidator.validate_bear_put_spread(inputs)
            elif normalized_strategy_name == 'LongStraddle':
                validation_result = StrategyValidator.validate_long_straddle(inputs)
            elif normalized_strategy_name == 'LongStrangle':
                validation_result = StrategyValidator.validate_long_strangle(inputs)
            elif normalized_strategy_name == 'Strip':
                validation_result = StrategyValidator.validate_strip(inputs)
            elif normalized_strategy_name == 'Strap':
                validation_result = StrategyValidator.validate_strap(inputs)
            elif normalized_strategy_name == 'LongButterfly':
                validation_result = StrategyValidator.validate_long_butterfly(inputs)
            else:
                st.error("Unknown strategy selected.")
                return
        else:
            validation_result = StrategyValidator.validate_basic_inputs(inputs)

        if not validation_result.is_valid:
            st.error(validation_result.message)
            return
        elif validation_result.severity == "warning":
            st.warning(validation_result.message)

        try:
            strategy = strategy_class(**inputs.__dict__)  # Unpack the dataclass to pass as keyword arguments
        except TypeError as e:
            st.error(f"Error creating strategy instance: {e}")
            return
    
        # After calculating results
        payoff_data = strategy.calculate_payoff()  # Ensure this includes the new Total Premium column
        # Get formatted data and dimensions
        formatted_df, height, width = DataFormatter.format_payoff_table(payoff_data, strategy_name)
        # Display the table with calculated dimensions
        st.subheader(f"{strategy_name} - Net-Payoff Table")
        st.dataframe(
            formatted_df,
            height=height,
            width=width
        )

        # Display payoff plot
        st.subheader(f"{strategy_name} - Net-Payoff Graph")
        if normalized_strategy_name == 'BullCallSpread':
            fig, _ = BullCallSpreadPlotter.create_plot(strategy, normalized_strategy_name, figsize=(10, 5))
        elif normalized_strategy_name == 'BearPutSpread':
            fig, _ = BearPutSpreadPlotter.create_plot(strategy, normalized_strategy_name, figsize=(10, 5))
        elif normalized_strategy_name == 'LongStraddle':
            fig, _ = LongStraddlePlotter.create_plot(strategy, normalized_strategy_name, figsize=(10, 5))
        elif normalized_strategy_name == 'LongStrangle':
            fig, _ = LongStranglePlotter.create_plot(strategy, normalized_strategy_name, figsize=(10, 5))
        elif normalized_strategy_name == 'Strip':
            fig, _ = StripPlotter.create_plot(strategy, normalized_strategy_name, figsize=(10, 5))
        elif normalized_strategy_name == 'Strap':
            fig, _ = StrapPlotter.create_plot(strategy, normalized_strategy_name, figsize=(10, 5))
        elif normalized_strategy_name == 'LongButterfly':
            fig, _ = LongButterflyPlotter.create_plot(strategy, normalized_strategy_name, figsize=(10, 5))
        else:
            fig, _ = Basic_Payoff_Plotter.create_basic_payoff_plot(strategy, normalized_strategy_name, figsize=(10, 5))

        st.pyplot(fig)