import matplotlib.pyplot as plt
from typing import Tuple

class Basic_Payoff_Plotter:
    @staticmethod
    def create_basic_payoff_plot(strategy_obj, title: str, figsize=(10, 5)) -> Tuple[plt.Figure, plt.Axes]:

        # Get data
        payoff_data = strategy_obj.calculate_payoff()
        bep = strategy_obj.calculate_bep()  # This may need to handle multiple BEPs
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Main payoff line
        ax.plot(payoff_data['Expiration Price'], 
                payoff_data['Net Payoff'], 
                label='Net Payoff',
                color='blue',
                linewidth=2)
        
        # Zero reference line (subtle)
        ax.axhline(y=0, 
                  color='red', 
                  linestyle='--', 
                  alpha=0.3)
        
        # Handle single break-even point
        if not isinstance(bep, tuple):  # Single BEP
            bep_index = (payoff_data['Expiration Price'] - bep).abs().idxmin()
            bep_x = payoff_data['Expiration Price'].iloc[bep_index]
            bep_y = payoff_data['Net Payoff'].iloc[bep_index]
            ax.plot(bep_x, bep_y, 'go', markersize=8)  # 'go' for green circle
            ax.annotate('BEP',
                        xy=(bep_x, bep_y),
                        xytext=(bep_x + 2, bep_y - 6),  # Adjust the position of the text
                        arrowprops=dict(facecolor='black', arrowstyle='->'),
                        fontsize=10,
                        color='green')
        
        # Profit/Loss regions (very subtle)
        ax.fill_between(payoff_data['Expiration Price'], 
                       payoff_data['Net Payoff'], 
                       0, 
                       where=(payoff_data['Net Payoff'] >= 0),
                       color='green', 
                       alpha=0.10)
        ax.fill_between(payoff_data['Expiration Price'], 
                       payoff_data['Net Payoff'], 
                       0, 
                       where=(payoff_data['Net Payoff'] <= 0),
                       color='red', 
                       alpha=0.10)
        
        # Styling
        ax.set_title(title, pad=20)
        ax.set_xlabel('Stock Price at Expiration')
        ax.set_ylabel('Profit/Loss')
        ax.grid(True, alpha=0.3)  # More subtle grid
        
        plt.tight_layout()
        return fig, ax  # Return only figure and axes

class ComplexPayoffPlotter(Basic_Payoff_Plotter):
    @staticmethod
    def create_complex_payoff_plot(strategy_obj, title: str, figsize=(10, 5)) -> Tuple[plt.Figure, plt.Axes]:

        fig, ax = Basic_Payoff_Plotter.create_basic_payoff_plot(strategy_obj, title, figsize)
        
        # Get data
        payoff_data = strategy_obj.calculate_payoff()
        bep = strategy_obj.calculate_bep()  # This may need to handle multiple BEPs
        
        # Handle multiple break-even points
        if isinstance(bep, tuple):  # If there are multiple BEPs
            # Calculate y-range of the plot
            y_min, y_max = ax.get_ylim()
            y_range = y_max - y_min
            
            for i, be in enumerate(bep):
                bep_index = (payoff_data['Expiration Price'] - be).abs().idxmin()
                bep_x = payoff_data['Expiration Price'].iloc[bep_index]
                bep_y = payoff_data['Net Payoff'].iloc[bep_index]
                ax.plot(bep_x, bep_y, 'go', markersize=8)  # 'go' for green circle
                # For first BEP (left side), offset text to the left
                if i == 0:
                    x_offset = -2
                    y_offset = -0.2 * y_range
                    alignment = 'right'
                # For second BEP (right side), offset text to the right
                else:
                    x_offset = 2
                    y_offset = -0.2 * y_range
                    alignment = 'left'
                ax.annotate('BEP',
                            xy=(bep_x, bep_y),
                            xytext=(bep_x + x_offset, bep_y + y_offset),
                            arrowprops=dict(
                                facecolor='black',
                                arrowstyle='->',
                                connectionstyle='arc3,rad=0.2'
                            ),
                            fontsize=10,
                            color='green',
                            horizontalalignment=alignment,
                            verticalalignment='top'
                )
        return fig, ax
        
class BullCallSpreadPlotter(ComplexPayoffPlotter):
    @staticmethod
    def create_plot(strategy_obj, title: str, figsize=(10, 5)) -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = ComplexPayoffPlotter.create_complex_payoff_plot(strategy_obj, title, figsize)
        
        # Get the actual payoff values for y-axis range
        payoff_data = strategy_obj.calculate_payoff()
        max_profit = payoff_data['Net Payoff'].max()
        max_loss = payoff_data['Net Payoff'].min()
        
        # Add some padding (e.g., 10%) to the y-axis range for better visualization
        y_padding = (max_profit - max_loss) * 0.1
        y_min = max_loss - y_padding
        y_max = max_profit + y_padding

        # Set y-axis limits explicitly
        ax.set_ylim(y_min, y_max)
        return fig, ax

class BearPutSpreadPlotter(ComplexPayoffPlotter):
    @staticmethod
    def create_plot(strategy_obj, title: str, figsize=(10, 5)) -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = ComplexPayoffPlotter.create_complex_payoff_plot(strategy_obj, title, figsize)
        
        # Get the actual payoff values for y-axis range
        payoff_data = strategy_obj.calculate_payoff()
        max_profit = payoff_data['Net Payoff'].max()
        max_loss = payoff_data['Net Payoff'].min()
        
        # Add padding for better visualization
        y_padding = (max_profit - max_loss) * 0.1
        y_min = max_loss - y_padding
        y_max = max_profit + y_padding
                
        # Set y-axis limits
        ax.set_ylim(y_min, y_max)
        return fig, ax
        
class LongStraddlePlotter(ComplexPayoffPlotter):
    @staticmethod
    def create_plot(strategy_obj, title: str, figsize=(10, 5)) -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = ComplexPayoffPlotter.create_complex_payoff_plot(strategy_obj, title, figsize)
        
        # Get the actual payoff values for y-axis range
        payoff_data = strategy_obj.calculate_payoff()
        max_profit = payoff_data['Net Payoff'].max()
        max_loss = payoff_data['Net Payoff'].min()
        
        # Add some padding for better visualization
        y_padding = (max_profit - max_loss) * 0.1
        y_min = max_loss - y_padding
        y_max = max_profit + y_padding
        
        # Set y-axis limits
        ax.set_ylim(y_min, y_max)
        return fig, ax
    
class LongStranglePlotter(ComplexPayoffPlotter):
    @staticmethod
    def create_plot(strategy_obj, title: str, figsize=(10, 5)) -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = ComplexPayoffPlotter.create_complex_payoff_plot(strategy_obj, title, figsize)
        
        # Get the actual payoff values for y-axis range
        payoff_data = strategy_obj.calculate_payoff()
        max_profit = payoff_data['Net Payoff'].max()
        max_loss = payoff_data['Net Payoff'].min()
        
        # Add some padding for better visualization
        y_padding = (max_profit - max_loss) * 0.1
        y_min = max_loss - y_padding
        y_max = max_profit + y_padding
        
        # Set y-axis limits
        ax.set_ylim(y_min, y_max)
        return fig, ax
    
class StripPlotter(ComplexPayoffPlotter):
    @staticmethod
    def create_plot(strategy_obj, title: str, figsize=(10, 5)) -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = ComplexPayoffPlotter.create_complex_payoff_plot(strategy_obj, title, figsize)
        
        # Get the actual payoff values for y-axis range
        payoff_data = strategy_obj.calculate_payoff()
        max_profit = payoff_data['Net Payoff'].max()
        max_loss = payoff_data['Net Payoff'].min()
        
        # Add some padding for better visualization
        y_padding = (max_profit - max_loss) * 0.1
        y_min = max_loss - y_padding
        y_max = max_profit + y_padding
        
        # Set y-axis limits
        ax.set_ylim(y_min, y_max)
        return fig, ax

class StrapPlotter(ComplexPayoffPlotter):
    @staticmethod
    def create_plot(strategy_obj, title: str, figsize=(10, 5)) -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = ComplexPayoffPlotter.create_complex_payoff_plot(strategy_obj, title, figsize)
        
        # Get the actual payoff values for y-axis range
        payoff_data = strategy_obj.calculate_payoff()
        max_profit = payoff_data['Net Payoff'].max()
        max_loss = payoff_data['Net Payoff'].min()
        
        # Add some padding for better visualization
        y_padding = (max_profit - max_loss) * 0.1
        y_min = max_loss - y_padding
        y_max = max_profit + y_padding
        
        # Set y-axis limits
        ax.set_ylim(y_min, y_max)
        return fig, ax

class LongButterflyPlotter(ComplexPayoffPlotter):
    @staticmethod
    def create_plot(strategy_obj, title: str, figsize=(10, 5)) -> Tuple[plt.Figure, plt.Axes]:
        fig, ax = ComplexPayoffPlotter.create_complex_payoff_plot(strategy_obj, title, figsize)
        
        # Get the actual payoff values for y-axis range
        payoff_data = strategy_obj.calculate_payoff()
        max_profit = payoff_data['Net Payoff'].max()
        max_loss = payoff_data['Net Payoff'].min()
        
        # Add some padding for better visualization
        y_padding = (max_profit - max_loss) * 0.1
        y_min = max_loss - y_padding
        y_max = max_profit + y_padding
        
        # Set y-axis limits
        ax.set_ylim(y_min, y_max)
        return fig, ax
