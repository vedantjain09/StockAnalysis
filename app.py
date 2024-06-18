# Vedant Jain, vedantj@usc.edu
# ITP 216, Spring 2024
# Section: 31885
# Final Project
# Description: This program serves as the central file for a Flask-based stock analysis web application,
# containing all the server logic, route definitions, and configurations. It facilitates the loading and
# visualization of stock data, enables user interactions to select stocks and predict future prices, and
# integrates pandas and scikit-learn for data processing and machine learning functionality.

from flask import Flask, request, render_template
import pandas as pd
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)


# Load stock data
def load_stock_data():
    # Set the path to the folder containing the stock files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(base_dir, 'stocks')
    files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    stocks = {}
    for file in files:
        path = os.path.join(data_folder, file)
        ticker = file.split('.')[0]
        df = pd.read_csv(path)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Close'] = df['Close'].fillna(df['Close'].mean())  # Fill NaN values with the mean
        stocks[ticker] = df
    return stocks


stocks = load_stock_data()


@app.route('/', methods=['GET', 'POST'])
def home():
    # Handle both GET and POST requests to the root URL
    error_message = None  # Initialize error message
    plot_url = None
    prediction_message = ""
    future_price_plot_url = ""

    if request.method == 'POST':
        ticker = request.form.get('stock')  # Get the stock ticker from the form
        future_date = request.form.get('date')

        if not ticker or ticker not in stocks:
            error_message = "Please select a valid stock ticker from the dropdown."
        else:
            df = stocks[ticker]

            # Plot historical data
            plt.figure()
            plt.plot(df['Date'], df['Close'], label='Historical Data')
            plt.title(f'Stock Price Fluctuations for {ticker}')
            plt.xlabel('Date')
            plt.ylabel('Closing Price')
            plt.grid(True)

            if future_date:
                # Convert dates into an integer 'Day' column for linear regression
                df['Day'] = (df['Date'] - df['Date'].min()).dt.days
                X = df[['Day']]
                y = df['Close']
                model = LinearRegression()
                model.fit(X, y)
                future_day = (pd.to_datetime(future_date) - df['Date'].min()).days
                future_dates = np.arange(df['Day'].max() + 1, future_day + 1)
                future_prices = model.predict(future_dates.reshape(-1, 1))

                # Plot ML processed predictions
                future_df = pd.DataFrame(
                    {'Date': pd.date_range(start=df['Date'].max() + pd.Timedelta(days=1), periods=len(future_dates))})
                plt.plot(future_df['Date'], future_prices, 'r--', label='Predicted Future Prices')

                prediction = model.predict([[future_day]])
                prediction_message = f"The predicted stock price on {future_date} is ${prediction[0]:.2f}"

            plt.legend()
            img = BytesIO()
            plt.savefig(img, format='png')
            plt.close()
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()  # Encode the image in base64 for HTML embedding

        # Render the home.html template with the required context variables
        return render_template('home.html', stocks=list(stocks.keys()), image=plot_url,
                               prediction_message=prediction_message, stock_selected=ticker,
                               future_price_plot_url=future_price_plot_url, error_message=error_message)

    return render_template('home.html', stocks=list(stocks.keys()), error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True, port=3800)
