import pandas as pd

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

        # Add a Total Premium column based on the strategy type
        if strategy_name in ['bull_call_spread', 'bear_put_spread']:
            formatted_df['Total Premium'] = formatted_df['Call 1: Premium'] + formatted_df['Call 2: Premium']
        elif strategy_name in ['long_straddle', 'long_strangle']:
            formatted_df['Total Premium'] = formatted_df['Call Premium'] + formatted_df['Put Premium']
        elif strategy_name == 'long_butterfly':
            formatted_df['Total Premium'] = (formatted_df['Lower Call Value'] +
                                              formatted_df['Upper Call Value'] -
                                              formatted_df['Middle Call Value'])

        # Highlight based on net payoff
        def highlight_rows(row):
            return ['background-color: rgba(0, 255, 0, 0.2)' if row['Net Payoff'] > 0 else
                    'background-color: rgba(255, 0, 0, 0.2)' if row['Net Payoff'] < 0 else
                    'background-color: rgba(173, 216, 230, 0.2)' for _ in row]
        # Apply the highlighting
        styled_df = formatted_df.style.apply(highlight_rows, axis=1)

        height, width = DataFormatter.calculate_table_dimensions(formatted_df)

        return styled_df, height, width