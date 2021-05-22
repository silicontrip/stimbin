#!/usr/local/bin/python3

from symfit import parameters, variables, sin, cos, Fit
import numpy as np
import matplotlib.pyplot as plt

def fourier_series(x, f, n=0):
    """
    Returns a symbolic fourier series of order `n`.

    :param n: Order of the fourier series.
    :param x: Independent variable
    :param f: Frequency of the fourier series
    """
    # Make the parameter objects for all the terms
    a0, *cos_a = parameters(','.join(['a{}'.format(i) for i in range(0, n + 1)]))
    sin_b = parameters(','.join(['b{}'.format(i) for i in range(1, n + 1)]))
    # Construct the series
    series = a0 + sum(ai * cos(i * f * x) + bi * sin(i * f * x)
                     for i, (ai, bi) in enumerate(zip(cos_a, sin_b), start=1))
    return series

x, y = variables('x, y')
w, = parameters('w')
model_dict = {y: fourier_series(x, f=w, n=5)}
print(model_dict)


# Make step function data

stepv = 8 * np.pi / 4

xdata = np.linspace(-4 * np.pi, 4 * np.pi)
ydata = np.zeros_like(xdata)
ydata[xdata > (-4 * np.pi + stepv) ] = 0.33
ydata[xdata > (-4 * np.pi + 2 * stepv) ] = 0.667
ydata[xdata > (-4 * np.pi + 3 * stepv) ] = 1

#ydata[xdata > (-np.pi + 3 * stepv) ] = 0.3
#ydata[xdata > (-np.pi + 4 * stepv) ] = 0.4
#ydata[xdata > (-np.pi + 5 * stepv) ] = 0.5
#ydata[xdata > (-np.pi + 6 * stepv) ] = 0.6
#ydata[xdata > (-np.pi + 7 * stepv) ] = 0.7
#ydata[xdata > (-np.pi + 8 * stepv) ] = 0.8
#ydata[xdata > (-np.pi + 9 * stepv) ] = 0.9

#ydata[xdata > 0] = 1
# Define a Fit object for this model and data
fit = Fit(model_dict, x=xdata, y=ydata)
fit_result = fit.execute()
print(fit_result)

# Plot the result
plt.plot(xdata, ydata)
plt.plot(xdata, fit.model(x=xdata, **fit_result.params).y, color='green', ls=':')
