# Options Strategy Payoff Calculator

## Contact info

Email: saimanishprabhakar2020@gmail.com

[Linkedin](https://www.linkedin.com/in/saimanish-prabhakar-3074351a0/)

## About the project

A simple web-app that allows users to calculate and visualize the payoff profiles for a wide range of options trading strategies. 

The supported strategies include: Long Call, Short Call, Long Put, Short Put, Bull Call Spread, Bear Put Spread, Long Straddle, Long Strangle, Strip, Strap, and Long Butterfly. 

The dashboard provides a user-friendly interface for inputting the necessary options parameters for each selected strategy, and generates detailed payoff tables and charts to help users better understand the risk and reward characteristics of each strategy.

## Built with

- <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">

- <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">

- <img src="https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white" alt="Matplotlib">

- <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your_username/options-strat-payoff.git
cd options-strat-payoff
```
### 2. Create Virtual Environment (Optional but Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required libraries
pip install -r requirements.txt

# When done working on the project
deactivate
```
### Alternative: Direct Installation
```bash
# If you prefer not to use a virtual environment, you can directly install dependencies
pip install -r requirements.txt
```
### 3. Change git remote url to avoid accidental pushes to base project
```bash
git remote set-url origin github_username/options-strat-payoff
git remote -v # confirm the changes
```
## Usage

### Video walkthrough of project

Here is a video explaining everything about the concept of the project, its features, and how to get the most out of it. Alternatively, you can read the written step-by-step walkthrough of the project alongside some images below if you can't stand my voice!

*** Video Tutorial - Coming soon ***

### Step-by-Step image walkthorugh of project

Select a strategy from the dropdown list and input relevant parameters pertaining to chosen strategy
![Input Parameters](/images/input_parameters.png)

If you are unsure what the variable represents, please hover over the question mark symbol beside the specific parameter for additional context. 

![Help Functionality](/images/help_functionality_user_parameters.png)

The project contains validators ensuring all parameters inputted by the user are accurate, if you do input values that do not make logical sense, you will be prompted with a message such as the one below seen in the image. 

In this image, the start price (i.e. start expiration price) is greater than the strike price which results in an error as the correct format should be (start exp price < strike price < end exp price).

![Input Error Handling](/images/user_input_error_handling.png)

After all of the parameters have been inputted by the user, you will be presented with a payoff table that displays the expiration price range (start price to end price, incremented by step size), the premium, the value of the option (call/put), and lastly the net-payoff of the strategy. 

The rows of the table are colour coded to represent the moneyness of the strategy depending on the parameters inputted by the user. 

- Green: Strategy is ITM (Where Net-Payoff > 0)
- Light Blue: Break-Even Point of Strategy (Where Net-Payoff = 0)
- Red: Strategy is OTM (Where Net-Payoff < 0)

![Payoff Table](/images/payoff_table.png)

The payoff graph simply visualises the payoff table, highlighting the profit/loss zones using the same green/red colours representing the moneyness of the options / strategy itself. Break-Even Points are highlighted using the text 'BEP' and an arrow pointing to a green marker.

For complex strategies that employ multiple options, multiple BEP markers will be displayed accordingly. 

![Payoff Graph](/images/payoff_graph.png)

And... that is all. 

For those more inclined to learn more about the mathematical expressions behind each options strategy's payoff, you can read the final section of this file which breaks down each formula with labels.

## Contributing

I genuinely hope you find some value from this project, and hope it serves you in your journey towards mastering options and other derivatives. 

If you would like to contribute to the development of the options strategy payoff calculator (always looking to add more strategies to the project), please:

1. Feel free to clone the repository to your local machine (follow the steps in the 'Getting Started' section)
2. Make your contribution, and then submit a pull request.
3. Use the discussions tab within the repository and raise issues if needed.

## Mathematical Expressions

The payoff calculations for each strategy are based on the following mathematical expressions:

### Long Call
$\text{Payoff} = \max(S - K, 0) - c$

where $S$ is the underlying asset price, $K$ is the strike price, and $c$ is the call option premium.

### Short Call
$\text{Payoff} = \min(K - S, 0) + c$

### Long Put
$\text{Payoff} = \max(K - S, 0) - p$

where $p$ is the put option premium.

### Short Put
$\text{Payoff} = \min(S - K, 0) + p$

### Bull Call Spread
$\text{Payoff} = \max(S - K_1, 0) - c_1 - \max(S - K_2, 0) + c_2$

where $K_1$ and $K_2$ are the lower and upper strike prices, and $c_1$ and $c_2$ are the premiums for the lower and upper call options, respectively.

### Bear Put Spread
$\text{Payoff} = \max(K_1 - S, 0) - p_1 - \max(K_2 - S, 0) + p_2$

where $K_1$ and $K_2$ are the lower and upper strike prices, and $p_1$ and $p_2$ are the premiums for the lower and upper put options, respectively.

### Long Straddle
$\text{Payoff} = \max(S - K, 0) - c + \max(K - S, 0) - p$

where $K$ is the strike price, $c$ is the call option premium, and $p$ is the put option premium.

### Long Strangle
$\text{Payoff} = \max(S - K_c, 0) - c + \max(K_p - S, 0) - p$

where $K_c$ and $K_p$ are the call and put strike prices, $c$ is the call option premium, and $p$ is the put option premium.

### Strip
$\text{Payoff} = \max(S - K, 0) - c + 2 \max(K - S, 0) - 2p$

where $K$ is the strike price, $c$ is the call option premium, and $p$ is the put option premium.

### Strap
$\text{Payoff} = 2 \max(S - K, 0) - 2c + \max(K - S, 0) - p$

where $K$ is the strike price, $c$ is the call option premium, and $p$ is the put option premium.

### Long Butterfly
$\text{Payoff} = \max(S - K_1, 0) - c_1 - 2 \max(S - K_2, 0) + 2c_2 + \max(S - K_3, 0) - c_3$

where $K_1$, $K_2$, and $K_3$ are the lower, middle, and upper strike prices, and $c_1$, $c_2$, and $c_3$ are the premiums for the lower, middle, and upper call options, respectively.
