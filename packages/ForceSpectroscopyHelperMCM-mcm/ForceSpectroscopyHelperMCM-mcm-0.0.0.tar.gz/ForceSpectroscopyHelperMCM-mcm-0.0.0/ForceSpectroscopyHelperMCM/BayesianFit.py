import pymc3, os, numpy
from enum import Enum
from pymc3 import sample

import matplotlib.pyplot as plt
import ForceSpectroscopyHelper as fsh

from ForceSpectroscopyHelperMCM import *


class BayesianFitParam():
    def __init__(self, name):
        self.work_abs_directory = fsh.default_project_path

        self.name = name.replace(" ", "")
        self.sampler = Sampler.NUTS
        self.sample_count = 5000
        self.tune_count = 1000
        self.chainIndex = 0

    @property
    def Csv_saveResultName(self):
        return self.name + ",Num" + str(self.chainIndex) + BayesianUtility.bayes_file_extension


class BayesianFit(BayesianFitParam):

    def __init__(self, name, **kwargs):
        super(BayesianFit, self).__init__(name)
        self.accept_target = 0.8
        self.max_treedepth = 10
        self.plot_result = True

        if "chainCount" in kwargs:
            self.chainCount = int(kwargs["chainCount"])
        if "tune_count" in kwargs:
            self.tune_count = int(kwargs["tune_count"])
        if "sample_count" in kwargs:
            self.sample_count = int(kwargs["sample_count"])
        if "accept_target" in kwargs:
            self.accept_target = float(kwargs["accept_target"])
        if "max_treedepth" in kwargs:
            self.max_treedepth = int(kwargs["max_treedepth"])
        if "plot_result" in kwargs:
            self.plot_result = kwargs["plot_result"]

    def do_fitting(self, z0, cvt: fsh.BaseConvertor,
                   index, doNorm=False, model=None, trace=None, **kwargs):

        self.chainIndex = self.search_chain_index()
        print(self.Csv_saveResultName)
        numpy.random.seed(114514)

        """
        if index is provided, then run usual fitting about one curve
        
        During None index, trace will start to pick random curve from cvt
        And appendTimes paramater describe the how many times to take curve
        """
        if cvt is not None:
            if "long_range_cutoff" in kwargs:
                cutoff = kwargs["long_range_cutoff"]
                # y_data = theano.shared(np.flipud(cvt.GetYData(index)))
                x_data = cvt.get_x_data(index, offset="auto")[:-cutoff]
                y_data = cvt.get_y_data(index)[:-cutoff]
            else:
                x_data = cvt.get_x_data(index, offset="auto")
                y_data = cvt.get_y_data(index)
        elif "x" in kwargs and "y" in kwargs:
            x_data = kwargs["x"]
            y_data = kwargs["y"]

        else:
            raise ValueError("do_fitting needs a BaseConvertor or x, y data in kwargs")

        if doNorm:
            norm_data = BayesianUtility.normalized(y_data, 1, -1)
        else:
            norm_data = [y_data, -1, 1]

        """
        system can choose your orignal model if "model" argument is not None 
        """
        print("apply model:", model[1])
        trace = self.__run_model(model[0], trace)

        if trace is None:
            return None, None

        """
        At this time, trace should be finnished.
        Then write .bayes save data to the same directory of this script
        For detail of .bayes save data, go to bayesConventor.py
        """

        # save to bayes file
        data = bayesData.BayesData.to_bayesData(trace=trace, bayesianFitParam=self, z0=z0, index=index,
                                                norm_data=norm_data, model_name=model[1])

        # pymc3.forestplot(trace, varnames=["a", "b", "c", "d"])
        pymc3.plot_posterior(trace, var_names=["a", "b", "c", "d", "a0", "sa", "b0", "sb", "c0", "sc", "sigma"])
        plt.savefig(os.path.join(self.work_abs_directory, self.name + ",Num" + str(self.chainIndex) + ".png"))
        plt.close()
        if self.plot_result:
            self.save_plot_result(data, x_data, y_data)

        return trace, data

    # fittingの画像を出力
    def save_plot_result(self, bayes_data, x, y):
        bayesData.Extension.plot_range_result(bayes_data, x, y, show_observed_range=False, show_lr_range=True)
        plt.savefig(os.path.join(self.work_abs_directory, self.name + ",Num" + str(self.chainIndex) + ",fitting" + ".png"))
        plt.clf()

    def __run_model(self, model, trace):
        """
        Only Test at NUTS, It preforms well in NUTS so NUTS implement only
        """
        try:
            with model:
                print(str(self.sampler), str(self.sample_count))
                if self.sampler == Sampler.NUTS:
                    step = pymc3.NUTS(max_treedepth=self.max_treedepth, target_accept=self.accept_target,
                                      step_scale=0.25)
                    trace = sample(self.sample_count, init="jitter+adapt_diag", step=step, tune=self.tune_count, cores=4, chains=1,
                                   discard_tuned_samples=True, trace=trace)

                elif self.sampler == Sampler.SVGD:
                    svgd = pymc3.SVGD(2000)

                    approx = pymc3.fit(n=3000, method=pymc3.SVGD(), model=model,
                                       obj_optimizer=pymc3.sgd(learning_rate=2e-6))

                    trace = approx.sample(self.sample_count)
                elif self.sampler == Sampler.ADVI:
                    approx = pymc3.fit(method=pymc3.ADVI(), n=self.sample_count, model=model,
                                       obj_optimizer=pymc3.adam())
                    trace = approx.sample(self.sample_count)

            return trace

        except:
            import traceback
            traceback.print_exc()
            return None

    def search_chain_index(self):
        result_index = 0
        files = [file for file in os.listdir(self.work_abs_directory)
                 if os.path.isfile(os.path.join(self.work_abs_directory, file))]

        for file in files:
            if BayesianUtility.IsBayesianSaveResultFile(os.path.join(self.work_abs_directory, file)):
                data = bayesData.BayesData(os.path.join(self.work_abs_directory, file))
                # print(data.name)
                # print(self.name)
                if data.name == self.name:
                    if result_index <= data.chainIndex:
                        result_index = data.chainIndex + 1

        return result_index


class Sampler(Enum):
    NUTS = 1
    SVGD = 2
    ADVI = 3
