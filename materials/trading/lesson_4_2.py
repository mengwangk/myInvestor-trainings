"""Rolling statistics - Bollinger Bands"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}_history.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'GOOG' not in symbols:  # add GOOG for reference, if absent
        symbols.insert(0, 'GOOG')

    for symbol in symbols:
        # Read and join data for each symbol
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date', parse_dates=True,
                              usecols=['Date', 'Adj Close'],
                              na_values=['nan'])
        # Rename Adj Close to the symbol
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'GOOG':
            df = df.dropna(subset=["GOOG"])
        # df = df.join(df_temp, how='inner')

    return df


def plot_data(df, title="Stock Prices"):
    """Plot stock prices"""
    ax = df.plot(title=title, fontsize=2)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()  # Show the plot


def test_run():
    # Define a date range
    dates = pd.date_range('2017-01-01', '2018-01-10')

    # Choose stock symbols to read
    symbols = ['AAPL']

    # Get stock data
    df = get_data(symbols, dates)

    # Plot data, retain matplotlib axis object
    ax = df['AAPL'].plot(title="AAPL Rolling mean", label="Stock")

    # Compute rolling mean using a 20-day window
    rm_stock = pd.Series(df["AAPL"]).rolling(window=20).mean()

    # Add rolling mean to same plot
    rm_stock.plot(label="Rolling mean", ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")
    plt.show()


if __name__ == "__main__":
    test_run()
