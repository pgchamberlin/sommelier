# Matplotlib

http://matplotlib.org/citing.html

    # import matplotlib libraries
    import matplotlib
    import matplotlib.pyplot as pp

    # import numpy
    import numpy as np

    # step increments
    steps=[250, 500, 750, 1000, 1250, 1500, 1750, 2000]

    # user errors for K=10, steps=250..2000
    ue250=[0.41035, 0.448666, 0.41759, 0.272029, 0.583405, 0.632273, 0.522458, 0.429948, 0.289623, 0.444679, 0.485332, 0.603858, 0.362667, 0.672182, 0.499737, 0.441303, 0.24626, 0.361574]
    ue500=[0.237325, 0.195812, 0.280171, 0.226809, 0.275289, 0.186347, 0.236226, 0.20412, 0.112417, 0.277758, 0.302235, 0.257187, 0.236484, 0.403778, 0.336641, 0.273846, 0.264286, 0.192836] 
    ue750=[0.147782, 0.062828, 0.195698, 0.088028, 0.117261, 0.09805, 0.095253, 0.136114, 0.097403, 0.138187, 0.151195, 0.138232, 0.209939, 0.209339, 0.22658, 0.147829, 0.088503, 0.073736]
    ue1000=[0.090727, 0.053114, 0.114318, 0.032591, 0.093008, 0.026915, 0.062912, 0.03169, 0.041947, 0.078352, 0.10645, 0.066436, 0.123729, 0.07837, 0.200686, 0.074688, 0.044692, 0.055672]
    ue1250=[0.06623, 0.021545, 0.070836, 0.032397, 0.048669, 0.022891, 0.060753, 0.023061, 0.021899, 0.043566, 0.068054, 0.024856, 0.140773, 0.069365, 0.1599, 0.03361, 0.069018, 0.026283]
    ue1500=[0.046634, 0.014417, 0.053432, 0.019819, 0.014974, 0.013522, 0.049975, 0.009694, 0.016849, 0.041106, 0.03978, 0.019441, 0.099819, 0.054469, 0.108243, 0.022368, 0.002719, 0.020151]
    ue1750=[0.034706, 0.016795, 0.034735, 0.023395, 0.013372, 0.031003, 0.01233, 0.00998, 0.011547, 0.046362, 0.040407, 0.01971, 0.063811, 0.037329, 0.111191, 0.019203, 0.007606, 0.018712]
    

    # plot standard deviation of user error for each steps
    # n.b. not using float64 so not max. accuracy
    ue_sds=()
    for ue in (ue250, ue500, ue750, ue1000, ue1250, ue1500, ue1750, ue2000):
        ue_sds += (np.std(ue), )
    pp.plot(steps, list(ue_stds), 'ro')
    pp.show()

    # plot total error
    total_error=[0.451,0.250,0.135,0.0764,0.0558,0.0360,0.0310]
    pp.plot(steps, total_error)
    pp.show()

    # plot time per factorization
    # this plot includes a line of best fit for the data
    # - it appears nicely linear :-)
    times=[0.451,0.250,0.135,0.0764,0.0558,0.0360,0.0310]
    pfit=np.polyfit(steps, times, 1)
    yfit=np.polyval(pfit, steps)
    pp.plot(steps, time, 'bo', steps, yfit, 'k')

    # now to do some curvy plots...
    # first create a linear space between our steps
    # with lots of points in it
    spline_x=np.linspace(steps[0], steps[-1], 250)
    # now generate spline
    from scipy.interpolate import spline
    spline=spline(steps, total_error, spline_x)
    # now plot the graph with the spline over the observed data points
    pp.plot(steps, total_error, 'bo', spline_x, spline, 'k')
    p.show()

    
