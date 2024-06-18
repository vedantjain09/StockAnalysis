# Stock Analysis Web Application

## Description
This web application, developed for ITP-216 Applied Python, allows users to analyze stock price fluctuations over time and predict future prices using a linear regression model. The application is built with Flask and utilizes libraries like pandas, matplotlib, and scikit-learn for data manipulation, visualization, and predictive modeling.

## Usage
1. **Start Program**: Run app.py and access the web application via http://127.0.0.1:3800/ in your web browser. It may take a few moments to load.
2. **Select a Stock**: Use the dropdown menu on the home page to select a stock for analysis. If you onl
3. **View Stock Data**: After selecting a stock, the historical price data for that stock will be displayed as a graph on the same page.
4. **Predict Future Prices**: Enter a future date in the provided input field to receive a predicted price based on historical data through a machine learning model.

## Features
- **Stock Selection**: Users can choose from a list of available stocks loaded from CSV files on the server.
- **Data Visualization**: Displays graphical representation of historical stock prices using matplotlib.
- **Price Prediction**: Utilizes a linear regression model from scikit-learn to predict future stock prices based on user-provided future dates.
- **Dynamic Data Loading**: Stock data is dynamically loaded and processed using pandas, allowing for updates and changes without needing to restart the server.
- **Responsive Design**: The web application is designed to be responsive, making it accessible from various devices including tablets and smartphones.

## Project Structure
- `app.py`: Contains the main server logic, route definitions, and Flask application configuration.
- `templates/`: This directory contains the HTML templates for rendering the web pages. It includes:
  - `home.html`: The main page template that displays the stock selection dropdown, the graph, and the prediction form.
- `stocks/`: Contains CSV files, each representing historical data for different stocks labelled by their ticker. This is where new stock data files can be added for analysis.
- `README.md`: Provides an overview of the project, installation instructions, usage details, and other relevant information.

## Installation and Setup
- Ensure Python 3.7+ and pip are installed.
- Install required Python packages:
  ```bash
  pip install Flask pandas matplotlib scikit-learn