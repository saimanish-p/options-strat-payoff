import streamlit as st
from typing import Dict, Type, Union
import sys
from pathlib import Path

# Add the project root to the Python path
file_path = Path(__file__).parent.resolve()
sys.path.append(str(file_path))

# Import strategies
from src.strategies.base_strategy import LongCall, ShortCall, LongPut, ShortPut
from src.strategies.complex_strategy import (
    BullCallSpread,
    BearPutSpread,
    LongStraddle,
    LongStrangle,
    Strip,
    Strap,
    LongButterfly
)

from src.utils.strategy_renderer import StrategyRenderer
from src.visualisations.styling import render_header

# Strategy mapping
STRATEGY_MAP: Dict[str, Type[Union[LongCall, ShortCall, LongPut, ShortPut, BullCallSpread, BearPutSpread, LongStraddle, LongStrangle, Strip, Strap, LongButterfly]]] = {
    "Long Call": LongCall,
    "Short Call": ShortCall,
    "Long Put": LongPut,
    "Short Put": ShortPut,
    "Bull Call Spread": BullCallSpread,
    "Bear Put Spread": BearPutSpread,
    "Long Straddle": LongStraddle,
    "Long Strangle": LongStrangle,
    "Strip": Strip,
    "Strap": Strap,
    "Long Butterfly": LongButterfly
}

def main():
    # Set page config
    st.set_page_config(
        page_title="Options Strategy Payoff Calculator",
        page_icon="📈",
        layout="wide"
    )

    render_header()
    
    # Strategy selection
    strategy_name = st.sidebar.selectbox(
        "Select Strategy",
        options=list(STRATEGY_MAP.keys())
    )
    
    # Get strategy class
    strategy_class = STRATEGY_MAP[strategy_name]
    
    # Render strategy analysis
    StrategyRenderer.render_strategy(strategy_class, strategy_name)

if __name__ == "__main__":
    main()