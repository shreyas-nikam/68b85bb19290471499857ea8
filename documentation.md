id: 68b85bb19290471499857ea8_documentation
summary: Drafting AML Suspicious Activity Reports Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Streamlit Financial Dashboard Codelab

This codelab will guide you through the functionalities of a Streamlit financial dashboard application. This dashboard provides a user-friendly interface for analyzing financial data, performing calculations, and visualizing key metrics. By the end of this codelab, you'll understand how to use the application, customize it, and potentially extend its features. This type of application is important because it democratizes financial analysis, making it accessible to users without extensive programming knowledge.

## Setting Up the Environment
Duration: 00:05

Before diving into the dashboard, ensure you have the necessary libraries installed.  We'll use `streamlit`, `pandas`, `yfinance`, and `plotly`.

Open your terminal and run the following command:

```bash
pip install streamlit pandas yfinance plotly
```

This command installs all the required Python packages to run the application.

## Running the Application
Duration: 00:02

Once the packages are installed, you can run the Streamlit application.  Assuming the Python script is named `app.py`, execute the following command in your terminal:

```bash
streamlit run app.py
```

This command will start the Streamlit server and open the application in your default web browser.

## Understanding the Application Architecture
Duration: 00:10

The application follows a modular structure, leveraging Streamlit's features for interactive elements and data display. Here's a simplified view of the application's workflow:

1.  **User Input:** The user interacts with Streamlit widgets (e.g., text input for ticker symbols, date pickers for date ranges).
2.  **Data Fetching:**  The application uses the `yfinance` library to download historical stock data based on the user's input.
3.  **Data Processing:** `pandas` is used to manipulate and prepare the data for calculations and visualization.
4.  **Calculations:** The application calculates key metrics, such as moving averages and returns.
5.  **Visualization:**  `plotly` creates interactive charts and graphs to visualize the data.
6.  **Display:** Streamlit displays the visualizations and data in a user-friendly format.

## Exploring the Sidebar
Duration: 00:05

The sidebar is the main control panel of the application. Here's a breakdown of its elements:

*   **Ticker Symbol Input:** A text input field where you can enter the stock ticker symbol (e.g., AAPL for Apple, MSFT for Microsoft).
*   **Start and End Date Pickers:**  Date pickers allow you to select the date range for the data you want to analyze.
*   **Moving Average Window Input:**  A number input where you specify the window size for calculating the moving average.

Experiment with different ticker symbols, date ranges, and moving average window sizes to see how they affect the displayed data and charts.

## Fetching and Displaying Stock Data
Duration: 00:10

After entering the ticker symbol and date range, the application fetches historical stock data from Yahoo Finance using the `yfinance` library. This data includes open, high, low, close, adjusted close prices, and volume.

The application then displays this raw data in a Streamlit dataframe. This allows you to quickly inspect the data and verify its accuracy.

```python
# Example of fetching data using yfinance
import yfinance as yf
import streamlit as st
import pandas as pd

def load_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

ticker = st.sidebar.text_input("Enter ticker symbol", "AAPL")
start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End date", value=pd.to_datetime("today"))

df = load_data(ticker, start_date, end_date)

st.subheader('Raw Data')
st.dataframe(df)
```

## Calculating and Displaying Moving Averages
Duration: 00:10

A key feature of the dashboard is the ability to calculate and visualize moving averages.  The moving average is calculated using the following formula:

$$MA_t = \frac{1}{n} \sum_{i=0}^{n-1} P_{t-i}$$

Where:

*   $MA_t$ is the moving average at time $t$
*   $n$ is the window size (number of periods)
*   $P_t$ is the price at time $t$

The `rolling()` method in `pandas` is used to calculate the moving average.  The window size is determined by the input provided in the sidebar.

The application then displays the closing prices and the calculated moving average on a line chart using Plotly. This allows you to visually identify trends and potential buy/sell signals.

```python
# Example of calculating and plotting moving average
import plotly.graph_objects as go

window = st.sidebar.number_input("Moving Average Window", value=20)
df['MA'] = df['Close'].rolling(window=window).mean()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Closing Price'))
fig.add_trace(go.Scatter(x=df.index, y=df['MA'], mode='lines', name=f'Moving Average ({window} days)'))

st.plotly_chart(fig)
```

## Calculating Daily Returns
Duration: 00:05

The dashboard also calculates and displays daily returns.  Daily return is calculated as the percentage change in price from the previous day:

$$Return_t = \frac{P_t - P_{t-1}}{P_{t-1}} * 100$$

Where:

*   $Return_t$ is the daily return at time $t$
*   $P_t$ is the price at time $t$
*   $P_{t-1}$ is the price at time $t-1$

The `pct_change()` method in `pandas` is used to calculate the daily returns. These returns are then multiplied by 100 to express them as percentages. The resulting daily returns are displayed as a line chart, highlighting the volatility of the stock price.

```python
# Example of calculating and plotting daily returns
df['Return'] = df['Close'].pct_change() * 100

fig_return = go.Figure()
fig_return.add_trace(go.Scatter(x=df.index, y=df['Return'], mode='lines', name='Daily Returns'))

st.plotly_chart(fig_return)
```

## Understanding the Code
Duration: 00:15

The Streamlit application is built using Python and several libraries. Here's a breakdown of the key components:

*   **Streamlit (`streamlit as st`):**  Provides the framework for creating the interactive web application. It handles user input, data display, and layout.
*   **pandas (`pandas as pd`):**  A powerful data analysis library used for manipulating and analyzing financial data.  DataFrames are used to store and process the stock data.
*   **yfinance (`yfinance as yf`):** Used to download historical stock data from Yahoo Finance.
*   **plotly (`plotly.graph_objects as go`):**  A charting library for creating interactive and visually appealing charts.

The code is structured into functions to improve readability and maintainability:

*   `load_data(ticker, start_date, end_date)`:  Fetches stock data from Yahoo Finance.
*   Other functions (not explicitly shown in the snippets) might be used for specific calculations or visualizations, contributing to a modular design.

<aside class="positive">
<b>Tip:</b> Breaking down your code into smaller, reusable functions makes it easier to understand, test, and maintain.
</aside>

## Customization and Extension
Duration: 00:20

This dashboard provides a solid foundation for financial analysis.  Here are some ideas for customizing and extending its functionality:

*   **Adding More Technical Indicators:** Implement other technical indicators, such as RSI (Relative Strength Index), MACD (Moving Average Convergence Divergence), and Bollinger Bands.

    ```python
    # Example of calculating RSI
    def calculate_rsi(data, window=14):
        delta = data.diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        roll_up1 = up.ewm(span=window, adjust=False).mean()
        roll_down1 = down.abs().ewm(span=window, adjust=False).mean()
        RS1 = roll_up1 / roll_down1
        RSI1 = 100.0 - (100.0 / (1.0 + RS1))
        return RSI1

    df['RSI'] = calculate_rsi(df['Close'])
    ```

*   **Implementing Portfolio Analysis:** Allow users to input multiple ticker symbols and analyze their portfolio performance.  Calculate portfolio returns, volatility, and Sharpe ratio.
*   **Adding Sentiment Analysis:** Integrate sentiment analysis of news articles or social media data to provide insights into market sentiment.
*   **Adding Machine Learning Models:**  Incorporate machine learning models to predict future stock prices or identify potential trading opportunities.

<aside class="negative">
<b>Warning:</b> Be cautious when using machine learning models for financial prediction.  Financial markets are complex and unpredictable, and past performance is not indicative of future results.
</aside>

## Conclusion
Duration: 00:03

Congratulations! You have successfully navigated this Streamlit financial dashboard codelab. You should now have a good understanding of how the application works, how to use it to analyze financial data, and how to customize and extend its features. Remember to experiment with different parameters and explore the code to further enhance your understanding. This dashboard can be a valuable tool for anyone interested in financial analysis and investment.
