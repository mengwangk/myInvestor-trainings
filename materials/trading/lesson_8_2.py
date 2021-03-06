"""
Convex problem - a real-valued function f(x) defined on an interval is called convex
if the line segment between any two points on the graph of the function lies above the graph ..

Parameterized model - f(x) = c0x + c1

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo


def error(line, data):  # error function
    """Compute error between given line model and observed data

    Parameters
    ----------
    line: tuple/list/array (C0, C1) where C0 is slope and C1 is Y-intercept
    data: 2D array where each row is a point (x,y)

    Returns error as single real value
    """
    # Metric: Sum of squared Y-axis differences = Point Y  - C0X + C1
    err = np.sum((data[:, 1] - (line[0] * data[:, 0] + line[1])) ** 2)
    return err


def fit_line(data, error_func):
    """Fit a line to a given data, using a supplied error function

    Parameters
    ----------
    data: 2D array where each row is a point (X0, Y)
    error_func: function that computes the error between a line and observed data

    Return line that minimizes the error function.
    """

    # Generate initial guess for the line model
    l = np.float32([0, np.mean(data[:, 1])])  # slope = 0, intercept = mean(y values...

    print("Initial guess", l)

    # Plot initial guess (optional)
    x_ends = np.float32([-5, 5])
    plt.plot(x_ends, l[0] * x_ends + l[1], 'm--', linewidth=2.0, label = 'Initial guess')

    # Call optimizer to minimize error function
    result = spo.minimize(error_func, l,  args=(data,), method='SLSQP', options={'disp': True})
    return result.x


def test_run():
    # Define original line
    l_orig = np.float32([4, 2])
    print("Original line: C0 = {}, C1 = {}".format(l_orig[0], l_orig[1]))
    Xorig = np.linspace(0, 10, 21)
    Yorig = l_orig[0] * Xorig + l_orig[1]
    plt.plot(Xorig, Yorig, 'b--', linewidth=2.0, label='Original line')

    # Generate noisy data points
    noise_sigma = 3.0
    noise = np.random.normal(0, noise_sigma, Yorig.shape)

    print("Xorig", Xorig)
    print("Yorig", Yorig)
    print("noise", noise)

    data = np.asanyarray([Xorig, Yorig + noise]).T

    print("data", data)

    plt.plot(data[:, 0], data[:, 1], 'go', label='Data points')

    # Try to fit a line to this data
    l_fit = fit_line(data, error)
    print("Fitted line: C0 = {}, C1 = {}".format(l_fit[0], l_fit[1]))
    plt.plot(data[:, 0], l_fit[0] * data[:, 0] + l_fit[1], 'r--', linewidth=2.0, label='Fitted line')

    # Add a legend and show plot
    plt.title("Optimizer")
    plt.show()


if __name__ == "__main__":
    test_run()
