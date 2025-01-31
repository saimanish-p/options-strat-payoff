import pandas as pd
import numpy as np

class DataFormatter:
    
    @staticmethod
    def format_payoff_table(df: pd.DataFrame, strategy_name: str) -> pd.DataFrame:
        """
        Formats the payoff table for display.
        
        Args:
            df: The DataFrame containing payoff data.
            strategy_name: The name of the strategy to customize formatting if needed.
        
        Returns:
            A formatted DataFrame ready for display.
        """
        # Create a copy to avoid modifying the original DataFrame
        formatted_df = df.copy()
        
        # Round all numeric columns to 2 decimal places
        numeric_columns = formatted_df.select_dtypes(include=[np.number]).columns
        formatted_df[numeric_columns] = formatted_df[numeric_columns].round(2)
        
        # Add a Total Premium column based on the strategy type
        if strategy_name in ['bull_call_spread', 'bear_put_spread']:
            formatted_df['Total Premium'] = formatted_df['Premium Low'] + formatted_df['Premium High']
        
        elif strategy_name in ['long_straddle', 'long_strangle']:
            formatted_df['Total Premium'] = formatted_df['Premium Call'] + formatted_df['Premium Put']
        
        elif strategy_name == 'long_butterfly':
            formatted_df['Total Premium'] = formatted_df['Premium Low'] + formatted_df['Premium Middle'] + formatted_df['Premium High']
        
        # Additional strategies can be added here as needed
        
        # No renaming of existing columns
        return formatted_df