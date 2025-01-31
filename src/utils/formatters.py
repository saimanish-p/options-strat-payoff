import pandas as pd
import numpy as np

class DataFormatter:
    # Constants for table sizing
    ROW_HEIGHT = 35  
    HEADER_HEIGHT = 40  
    PADDING = 5  
    COLUMN_WIDTH = 180  
    SCROLLBAR_WIDTH = 25  

    @staticmethod
    def calculate_table_dimensions(df: pd.DataFrame) -> tuple:
        # Calculate height based on number of rows
        num_rows = len(df)
        total_height = (num_rows * DataFormatter.ROW_HEIGHT) + DataFormatter.HEADER_HEIGHT + DataFormatter.PADDING

        # Calculate width based on number of columns
        num_columns = len(df.columns)
        total_width = (num_columns * DataFormatter.COLUMN_WIDTH) + DataFormatter.SCROLLBAR_WIDTH

        return total_height, total_width

    @staticmethod
    def format_payoff_table(df: pd.DataFrame, strategy_name: str) -> tuple:
        formatted_df = df.copy()

        numeric_columns = formatted_df.select_dtypes(include=[np.number]).columns
        formatted_df[numeric_columns] = formatted_df[numeric_columns].round(2)

        # Add a Total Premium column based on the strategy type
        if strategy_name in ['bull_call_spread', 'bear_put_spread']:
            formatted_df['Total Premium'] = formatted_df['Premium Low'] + formatted_df['Premium High']

        elif strategy_name in ['long_straddle', 'long_strangle']:
            formatted_df['Total Premium'] = formatted_df['Premium Call'] + formatted_df['Premium Put']

        elif strategy_name == 'long_butterfly':
            formatted_df['Total Premium'] = (formatted_df['Premium Low'] +
                                          formatted_df['Premium Middle'] +
                                          formatted_df['Premium High'])

        height, width = DataFormatter.calculate_table_dimensions(formatted_df)

        return formatted_df, height, width