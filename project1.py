# -*- coding: utf-8 -*-
"""
project1.py

Code solves project 1 for E19, numerical methods.
By Evan Greene

The purpose of this project is to estimate pi by various numerical methods. 
"""

import numpy
import time
import matplotlib.pyplot as plt
import math

def mcpi(n):
    """ calculates the value of pi using the monte carlo method
    Does so by generating a n points within [0, 1] x [0, 1], and checking
    to see the proportion of these points that fall within the unit circle.
    This proportion is equal to pi/4
    """

    # generate n pairs of floats, then count the number that are inside the unit circle
    incircle = 0
    for i in range(n):
        point = numpy.random.random(2)
        if point[0] ** 2 + point[1] ** 2 < 1:
            incircle += 1

    # incircle / n should be equal to pi / 4
    pi_est = 4 * float(incircle) / n
    # print pi_est
    return pi_est

def task1():
    """ Estimates the number of guesses required to get an estimate of pi accurate to 10 decimal places"""
    
    places = 4
    pi = numpy.around(numpy.pi, decimals = places)
    print 'pi = {}'.format(pi)
    n = 10
    while True:
        counter = 0
        # run the simulation ten times and average them, then round
        pi_est = 0
        for _ in range(10):
           pi_est += mcpi(n)
        pi_est = pi_est / 10
        pi_est = numpy.around(pi_est, decimals = places)
        print '{} iterations returns pi = {}'.format(n, pi_est)
        if abs(pi_est - pi) < 0.000001: # guard against floating-point curse
            print 'It took {} points to estimate pi to {} places'.format(\
            n, places)
            return n
        else:
            n = n*2

def intpi(n):
    """ Calculates pi by numerical integration. 
    Evaluates the integral from 0 to 1 of (1-x^2) dx, 
    using a simple left Riemann sum, (rectangular integration)
    """
    pi = 0

    delta_x = 1.0/n # step size
    for i in range(n):
        x = delta_x * i 
        pi += delta_x * numpy.sqrt(1 - x**2)

    pi *= 4

    return pi

def task2():
    """ plots the error with respect to the number of steps for the numerical integration
    used in the intpi() function. """
    last_est = 0
    error_list = []
    step_size_list = []
    for n in [10, 50, 100, 500, 1000, 5000] :
        pi_est = intpi(n)
        error = abs(numpy.pi - pi_est)
        error_list.append(error)
        step_size_list.append(1.0/n)
        print 'for n = {}, pi = {}, error = {} %'.format(n, pi_est, error * 100)
        print 'Relative error = {} %'.format(abs(pi_est - last_est)* 100/pi_est)
        last_est = pi_est

    plt.plot(step_size_list, error_list)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Error size')
    plt.xlabel('Step size')
    plt.title('Step size and error')
    plt.show()


def tspi1(n):
    """ calculates pi as pi = 4 * arctan(1) using a taylor series approximation. 
    The approximation is arctan(x) ~ x - x^3/3 + x^5 / 5 - x^7 / 7 ... """
    pi = 0.0
    for i in range(1, 2*n + 1, 2):
        if (i / 2) % 2 == 0:
            pi += 1.0 / i
        else:
            pi -= 1.0 / i
            
    pi *= 4
    return pi

def tspi2(n):
    """ calculates pi as 16 * arctan(1/5) - 4 arctan(1/239) using a taylor series approximation. 
    The approximation is arctan(x) ~ x - x^3/3 + x^5 / 5 - x^7 / 7 ...
    This is the same approximation used in tspi1() """ 
    
    pi = 0.0
    for i in range(1, 2*n + 1, 2):
        if i / 2 % 2 == 0:
            pi += (16 * ((1.0/5)**i) / i) - (4 * ((1.0/239)**i) / i)
        else:
            pi -= (16 * ((1.0/5)**i) / i) - (4 * ((1.0/239)**i) / i)

    return pi

def task3():
    print '\nFirst method'
    last_est = 0
    # error_list = []
    # n_list = []
    for n in range(1, 21):
        pi_est = tspi1(n)
        error = abs(pi_est - numpy.pi) / numpy.pi
        rel_error = abs(pi_est - last_est) / pi_est
        # """
        print '\nn = {}, pi = {}'.format(n, pi_est)
        print 'Approximate relative error-- {} %'.format(rel_error * 100)
        print 'True relative error -- {} %'.format(error * 100 )
        # code to output the numbers in such a way that they can be copied and
        # pasted into LaTeX
        """
        pi_est = numpy.around(pi_est, 6)
        # round to 4 significant digits
        places = 4- int(numpy.floor(math.log10(error)))
        error = numpy.around(error, places)
        rel_error = numpy.around(rel_error, places)
        print '{} & {} & {} & {} \\\ '.format(n, pi_est,error *100, rel_error * 100)
        last_est = pi_est
        """
    print '\nMachin method'
    last_est = 0
    for n in range(1, 21):
        pi_est = tspi2(n)
        error = abs(pi_est - numpy.pi) / numpy.pi
        rel_error = abs(pi_est - last_est) / pi_est
        last_est = pi_est
        # """
        print '\nn = {}, pi = {}'.format(n, pi_est)
        print 'Approximate relative error-- {} %'.format(rel_error * 100)
        print 'True relative error-- {}%'.format(error * 100)


def main():
    print task1()``
    task2()
    task3()

if __name__ == '__main__':
    main()
