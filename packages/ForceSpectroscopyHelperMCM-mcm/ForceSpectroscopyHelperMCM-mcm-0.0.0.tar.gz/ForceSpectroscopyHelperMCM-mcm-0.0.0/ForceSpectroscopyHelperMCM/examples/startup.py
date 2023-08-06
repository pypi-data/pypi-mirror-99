import ForceSpectroscopyHelperMCM as mcm

import errandpy.handy

import ForceSpectroscopyHelper as fsh
import matplotlib.pyplot as plt


"""
Step 1. First, we need to know [z0] and a suitable [a,b,c,d]^1 parameters for long-range force Model.
    we use "errandpy" to estimate the requried parameters mentioned before. 
    and we use "ForceSpectroscopyHelper" to perform data IO and data analysis 

(For someone first time to use ForceSpectroscopyHelper, a gui will popup and please select to root directory of your
python project and your force curve data folder)


^1 One of the NC-AFM long-range force models is F = a - b / (c+x)^d
"""


"""
    This is our example force curve (On Si)
"""
x, y = errandpy.test.get_test_curve()
plt.plot(x, y)
plt.show()

# example si force curve


# estimate z0 and piror [a,b,c,d]
dict = errandpy.handy.extract_short_range(x[1:], y[1:], show_graph=True)

# get z0  a,b,c,d from return value
# z0, a, b, c, d = dict["z0"], dict["a"], dict["b"], dict["c"], dict["d"]
# or get from log file
z0 = errandpy.utility.get_z0FromLogFile("./Outputs/Master@handy_analyze.log")
a, b, c, d = errandpy.utility.get_logFileParamater("./Outputs/Master@handy_analyze.log", normalized_param=False)


"""
    Create Model and Analyzer instance
"""
bayes = mcm.BayesianFit(name="test," + str(0) + "," + str(z0))
model = mcm.BayesianModel.df_model(x, y, z0, limit_d=(0.5, 1.5), param_type="normal")
"""
Note: [cvt] and [index] parameters are for map analyze (includes a lot of data)
in this example, we set a dummy value for these two paramater. 
"""
bayes.do_fitting(z0, cvt=None, x=x, y=y, index=0, model=model, a=a, b=b, c=c, d=d)

"""
    Data Summry
    
    a ".bayes" extension file has been created in the root directory 
    or you can adjust the output by bayes.work_abs_directory = [your path].
    Use "BayesData" class to open it.
"""

data = mcm.BayesData(fsh.default_project_path + "./test,0,61,Num0.bayes")
mcm.Extension.plot_range_result(data, x=x, y=y)
plt.show()

mcm.Extension.plot_histogram(data)
plt.tight_layout()
plt.show()
