# Options Strategy Payoff Calculator

## Overview

This is a Python-based application that allows users to calculate and visualize the payoff profiles for a wide range of options trading strategies. The supported strategies include:

- Long Call
- Short Call
- Long Put
- Short Put
- Bull Call Spread
- Bear Put Spread
- Long Straddle
- Long Strangle
- Strip
- Strap
- Long Butterfly

The application provides a user-friendly interface for inputting the necessary options parameters, and generates detailed payoff tables and charts to help traders and investors better understand the risk and reward characteristics of each strategy.

## Mathematical Formulas

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

## Key Features

1. **Payoff Table Generation**: The application can generate a detailed payoff table for each of the supported options trading strategies, including the expiration price, premium, call/put value, and net payoff.

2. **Payoff Table Formatting**: The payoff table is formatted with intuitive color-coding to highlight profitable and losing scenarios. Positive net payoffs are shown in green, negative net payoffs are shown in red, and breakeven scenarios are shown in a light blue.

3. **Responsive Table Layout**: The application automatically calculates the optimal height and width of the payoff table to ensure it is displayed in a clear and readable format.

4. **Error Handling**: The application includes robust error handling to ensure that it can gracefully handle any issues that may arise during the data processing or payoff calculation steps.

## Contributing

If you would like to contribute to the development of the options strategy payoff calculator, please feel free to clone the repository to your local machine, install the required dependencies, including `numpy`, `pandas`, `matplotlib`, and `streamlit`, make your contribution, and then submit a pull request. You can also use the discussions tab within the repository and raise issues if needed.