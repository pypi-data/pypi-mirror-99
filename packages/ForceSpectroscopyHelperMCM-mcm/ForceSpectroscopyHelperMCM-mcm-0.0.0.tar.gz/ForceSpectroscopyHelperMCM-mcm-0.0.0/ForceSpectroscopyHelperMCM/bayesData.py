import pandas as pd
import numpy as np
import os
from io import StringIO
import matplotlib.pyplot as plt
from scipy.stats import norm
import pymc3

import ForceSpectroscopyHelperMCM.Utils.ConsoleColor as color
import ForceSpectroscopyHelperMCM as mcm
import ForceSpectroscopyHelper as fsh
import scipy.stats as stats


"""
    Bayesで出力されたcsvファイルの解析
"""



class BayesData:
    def __init__(self, file_path):
        if not mcm.utility.IsBayesianSaveResultFile(file_path):
            print(color.color.Error + "Error File Type Error!" + color.color.Error, file_path)
            return

        self._file = open(file_path)
        headers = str(self._file.read().split("HeaderEnd")[0]).replace(" ", "").split('\n')
        try:
            self.name = headers[1].replace("csvdata,", "")
            self.source_file_name = headers[1].split(",")[1]
            self.norm_min = float(headers[2].split(",")[1])
            self.norm_delta = float(headers[3].split(",")[1])
            self.index = headers[4].replace("index,", "")
            self.z0 = int(headers[5].split(",")[1])
            self.sample = str(headers[6].split(",")[1])
            self.chainIndex = int(headers[7].split(",")[1])
            self.model_name = mcm.BayesianModel.ModelEnum.value_of(str(headers[8].split(",")[1]))
            self.f_equation = mcm.BayesianModel.ModelEnum.get_model(self.model_name)

            # self.traceDir = headers[8].split(",")[1]
        except:
            import traceback
            traceback.print_exc()

        self._data = open(file_path).read()

    def get_result_param(self, percent):

        param_mat = np.array(self.trace_data)[:, 1:6]
        param_mat = sorted(param_mat, key=lambda x: self.f_equation(0, x[0], x[1], x[2], x[3]))
        # print(param_mat)

        count = int(len(param_mat))
        if count * percent > count - 1:
            param = param_mat[count-1]
        else:
            param = param_mat[int(count * percent)]

        # sigma_mat = np.array(self.trace_data)[:, 5:]
        # sigma = np.percentile(sigma_mat, int(percent * 100))
        return param[:-1], param[4]

    def get_lr_curve(self, x, percent):
        param, sigma = self.get_result_param(percent)
        return self.f_equation(x, *param), sigma


    @property
    def summary_data(self) -> pd.DataFrame:
        data = self._data.split("HeaderEnd")[1].split("SummaryEnd")[0]
        f_io = StringIO(data)
        df = pd.read_csv(f_io, sep=",")
        return df

    @property
    def trace_data(self) -> pd.DataFrame:
        data = self._data.split("SummaryEnd")[1].split("TraceEnd")[0]
        f_io = StringIO(data)
        df = pd.read_csv(f_io, sep=",")
        return df

    @property
    def y_range_data(self) ->pd.DataFrame:
        data = self._data.split("TraceEnd")[1]
        f_io = StringIO(data)
        df = pd.read_csv(f_io, sep=",")
        return df

    @property
    def a(self):
        return self.get_result_param(0.5)[0][0]

    @property
    def b(self):
        return self.get_result_param(0.5)[0][1]

    @property
    def c(self):
        return self.get_result_param(0.5)[0][2]

    @property
    def d(self):
        return self.get_result_param(0.5)[0][3]

    @property
    def a_range(self):
        return np.asarray(self.summary_data)[:, 4][0], np.asarray(self.summary_data)[:, 5][0]

    @property
    def b_range(self):
        return np.asarray(self.summary_data)[:, 4][1], np.asarray(self.summary_data)[:, 5][1]

    @property
    def c_range(self):
        return np.asarray(self.summary_data)[:, 4][2], np.asarray(self.summary_data)[:, 5][2]

    @property
    def d_range(self):
        return np.asarray(self.summary_data)[:, 4][3], np.asarray(self.summary_data)[:, 5][3]

    @property
    def real_a(self):
        return (self.a + 1) * self.norm_delta + self.norm_min

    @property
    def real_b(self):
        return self.b * self.norm_delta

    @property
    def y_range(self):
        return np.array(self.y_range_data)[0, 1:], np.array(self.y_range_data)[1, 1:]

    def __str__(self):
        return "a: " + str(self.a) + " b: " + str(self.b) + " c: " + str(self.c) + " d: " + str(self.d)

    def __repr__(self):
        return "a: " + str(self.a) + " b: " + str(self.b) + " c: " + str(self.c) + " d: " + str(self.d)

    def plot_curve(self, x, y):
        plt.plot(x, y, color="black")
        plt.axhline(0, color='green', linestyle='dashdot')
        plt.axvline(x[self.z0], color='green', linestyle='dashdot')

        plt.plot(x, self.f_equation(x, self.real_a, self.real_b, self.c, self.d), color="red")
        plt.plot(x, y - self.f_equation(x, self.real_a, self.real_b, self.c, self.d))
        plt.tight_layout()
        plt.show()

    @staticmethod
    def to_bayesData(trace, bayesianFitParam, z0, index,
                     norm_data=None, model_name=None, path=None):
        if norm_data is None:
            norm_data = [0, -1, 1]
        summary = pymc3.summary(trace, var_names=["a", "b", "c", "d",
                                                 "a0", "sa", "b0", "sb", "c0", "sc", "sigma"])

        print(summary)
        result_mat = np.asarray(summary)
        # summary save
        df = pd.DataFrame(result_mat,
                         columns=list(summary.columns.values),
                         index=["a", "b", "c", "d", "a0", "sa", "b0", "sb", "c0", "sc", "sigma"])
        df.to_csv(bayesianFitParam.Csv_saveResultName+"_temp1")
        # trace save
        df = pymc3.trace_to_dataframe(trace, varnames=["a", "b", "c", "d", "sigma"])
        df.to_csv(bayesianFitParam.Csv_saveResultName+"_temp2")
        # y-range save
        if trace.nchains == 1:
            # mu = np.array([pymc3.quantiles(trace)["mu-all"][2.5], pymc3.quantiles(trace)["mu-all"][97.5]])
            # eps = np.array(pymc3.quantiles(trace)["sigma"][50], pymc3.quantiles(trace)["sigma"][50])
            # y1, y2 = map(list, zip(*norm.ppf(q=[0.05, 0.95], loc=mu.T, scale=eps)))
            # y1 = pymc3.quantiles(trace)["mu-all"][2.5]
            # y2 = pymc3.quantiles(trace)["mu-all"][97.5]
            y1 = np.array(pymc3.summary(trace, var_names=["mu-all"])["hpd_3%"])
            y2 = np.array(pymc3.summary(trace, var_names=["mu-all"])["hpd_97%"])
            # y3 = norm.ppf(q=0.5, loc=mu.T, scale=eps)
            mu_mat = pd.DataFrame(np.asarray([y1, y2]))
            mu_mat.to_csv(bayesianFitParam.Csv_saveResultName + "_temp3")

        if path is None:
            dir = os.path.join(bayesianFitParam.work_abs_directory, bayesianFitParam.Csv_saveResultName)
        else:
            dir = os.path.join(path, bayesianFitParam.Csv_saveResultName)

        with open(dir, "w") as f:
            f.write("BayesianSaveResultFile" + "\n")
            f.write("csvdata," + bayesianFitParam.name + "\n")
            f.write("min," + str(float(norm_data[1])) + "\n")
            f.write("delta," + str(float(norm_data[2])) + "\n")
            f.write("index," + str(index) + "\n")
            f.write("z0," + str(int(z0)) + "\n")
            f.write("sampler," + str(bayesianFitParam.sampler) + "\n")
            f.write("chainIndex," + str(bayesianFitParam.chainIndex) + "\n")
            if model_name is not None:
                f.write("model," + str(model_name) + "\n")
            # f.write("traceDir," + trace_dir + "\n")
            f.write("HeaderEnd" + "\n")

            f.write(open(bayesianFitParam.Csv_saveResultName+"_temp1").read())
            os.remove(bayesianFitParam.Csv_saveResultName+"_temp1")
            f.write("SummaryEnd" + "\n")
            f.write(open(bayesianFitParam.Csv_saveResultName+"_temp2").read())
            os.remove(bayesianFitParam.Csv_saveResultName+"_temp2")
            f.write("TraceEnd" + "\n")
            if os.path.isfile(bayesianFitParam.Csv_saveResultName+"_temp3"):
                f.write(open(bayesianFitParam.Csv_saveResultName + "_temp3").read())
                os.remove(bayesianFitParam.Csv_saveResultName + "_temp3")

        return BayesData(os.path.join(bayesianFitParam.work_abs_directory, bayesianFitParam.Csv_saveResultName))


class Extension:

    plot_hyper_range = 450

    @staticmethod
    def get_best_data(fileName, data_path, index, z0=None) -> BayesData:
        data_dict = mcm.BayesSelector.select(data_path, fileName=fileName, index=index, z0=z0)
        data = None
        for v in data_dict.values():
            data, _ = mcm.BayesSelector.select_best_result_from_verification(v)
        if data is None:
            raise ValueError("can not find bayes data in path: " + data_path)
        return data

    @staticmethod
    def convert_real_param(bayes_data: BayesData, percentage=0.5):
        param, sigma = bayes_data.get_result_param(percentage)
        param[0] = (param[0] + 1) * bayes_data.norm_delta + bayes_data.norm_min
        param[1] = param[1] * bayes_data.norm_delta
        return param, sigma

    @staticmethod
    def plot_percentage_result(percentage, bayes_data: BayesData, x, y):
        param, eps = Extension.convert_real_param(bayes_data, percentage)

        plt.scatter(x, y, s=3)
        plt.axhline(0, color='green', linestyle='dashdot')
        plt.axvline(x[bayes_data.z0], color='green', linestyle='dashdot')
        f_lr = mcm.BayesianModel.ModelEnum.get_model(bayes_data.model_name)(x, param[0], param[1], param[2], param[3])
        plt.plot(x, f_lr, alpha=0.9, color="black", linewidth=1.0, label="long-range_median")
        plt.plot(x, y - f_lr, alpha=0.9, color="red", linewidth=1.0, label="short-range")

        if Extension.plot_hyper_range < len(x):
            plt.xlim(0, x[Extension.plot_hyper_range])
        plt.legend(fontsize=18)
        plt.tick_params(labelsize=18)

    @staticmethod
    def plot_range_result(bayes_data: BayesData, x, y, show_legend=True, show_observed_range=True, show_lr_range=False,
                          show_short_range=True):
        eps = bayes_data.get_result_param(0.5)[1]

        plt.scatter(x, y, s=3, label="measured data")
        # plt.axhline(0, color='black', linestyle='dashdot')
        plt.axvline(x[bayes_data.z0], color='black', linestyle='dashdot')
        f_lr = bayes_data.f_equation(x, bayes_data.real_a, bayes_data.real_b, bayes_data.c, bayes_data.d)

        mu = np.array([bayes_data.y_range[0], bayes_data.y_range[1]])
        nan_limit = -1
        for index in range(len(mu[0])):
            if np.isnan(mu[0][index]):
                nan_limit = index
            else:
                break
        for index in range(len(mu[1])):
            if np.isnan(mu[1][index]):
                nan_limit = index
            else:
                break

        param1, sigma1 = bayes_data.get_result_param(0.0)
        f1 = bayes_data.f_equation(x, param1[0], param1[1], param1[2], param1[3])
        param2, sigma2 = bayes_data.get_result_param(1.0)
        f2 = bayes_data.f_equation(x, param2[0], param2[1], param2[2], param2[3])

        if show_observed_range:
            y1, y2 = map(list, zip(*norm.ppf(q=[0.03, 0.97], loc=mu.T, scale=eps)))
            plt.fill_between(x, y1=y1, y2=y2, alpha=0.4, color="orange", label="$F_{fit}$ range(bayes inference)")

        # plt.plot(x, y - f_lr, alpha=0.9, color="red", linewidth=1.0, label="short-range")
        if nan_limit == -1:
            if show_lr_range:
                y1, y2 = bayes_data.f_equation(x, *param1), bayes_data.f_equation(x, *param2)
                plt.fill_between(x, y1=y1, y2=y2, alpha=0.4, color="blue", label="long-range")
            if show_short_range:
                plt.fill_between(x, y1=y-f1, y2=y-f2, alpha=0.6, color="red", label="short-range")

            # plt.plot(x, f_lr, alpha=0.9, color="black", linewidth=1.0, label="long-range_median")

        else:
            if show_lr_range:
                y1, y2 = bayes_data.f_equation(x[nan_limit:], *param1), bayes_data.f_equation(x[nan_limit:], *param2)
                plt.fill_between(x[nan_limit:], y1=y1, y2=y2, alpha=0.4, color="blue", label="long-range")
            if show_short_range:
                plt.fill_between(x[nan_limit:], y1=(y-f1)[nan_limit:], y2=(y-f2)[nan_limit:],
                             alpha=0.6, color="red", label="short-range")

            plt.plot(x[nan_limit:], f_lr[nan_limit:], alpha=0.9, color="black", linewidth=1.0, label="long-range_median")

        if Extension.plot_hyper_range < len(x):
            plt.xlim(x[0]-0.5, x[Extension.plot_hyper_range])
        if show_legend:
            plt.legend(fontsize=16)
        plt.tick_params(labelsize=18)

    @staticmethod
    def plot_histogram(datas, label="", color="blue", bin=100, alpha=0.5, figsize=(5, 10)):
        # point = literal_eval(data.index)
        # height_offset = analyzer.topo(fileName)[point[0], point[1]] * 10 ** 10
        axes = mcm.BayesianUtility.build_ax(5, figsize=figsize)
        if not isinstance(datas, list):
            datas = [datas]
            label = [label]
            color = [color]

        a_bins = np.histogram(np.hstack([data.trace_data["a"] for data in datas]), bins=bin)[1]
        b_bins = np.histogram(np.hstack([data.trace_data["b"] for data in datas]), bins=bin)[1]
        c_bins = np.histogram(np.hstack([data.trace_data["c"] for data in datas]), bins=bin)[1]
        d_bins = np.histogram(np.hstack([data.trace_data["d"] for data in datas]), bins=bin)[1]
        sigma_bins = np.histogram(np.hstack([data.trace_data["sigma"] for data in datas]), bins=bin)[1]

        for j, data in enumerate(datas):
            a = np.array(data.trace_data["a"])
            b = np.array(data.trace_data["b"])
            c = np.array(data.trace_data["c"])
            d = np.array(data.trace_data["d"])
            sigma = np.array(data.trace_data["sigma"])

            axes[0].hist(a, bins=a_bins, alpha=alpha, label=label[j], color=color[j])
            axes[0].set_xlabel("$A^\prime$")
            axes[1].hist(b, bins=b_bins, alpha=alpha, label=label[j], color=color[j])
            axes[1].set_xlabel("$B^\prime$")
            axes[2].hist(c, bins=c_bins, alpha=alpha, label=label[j], color=color[j])
            axes[2].set_xlabel("$C^\prime$")
            axes[3].hist(d, bins=d_bins, alpha=alpha, label=label[j], color=color[j])
            axes[3].set_xlabel("$D^\prime$")
            axes[4].hist(sigma, bins=sigma_bins, alpha=alpha, label=label[j], color=color[j])
            axes[4].set_xlabel("sigma")
        return axes

    @staticmethod
    def plot_smooth_histogram(datas, label="", color=None, bin=100, alpha=0.5, figsize=(5, 12)):
        # point = literal_eval(data.index)
        # height_offset = analyzer.topo(fileName)[point[0], point[1]] * 10 ** 10
        axes = mcm.BayesianUtility.build_ax(5, figsize=figsize)
        if not isinstance(datas, list):
            datas = [datas]
            label = [label]
            color = [color]

        a_bins = np.histogram(np.hstack([data.trace_data["a"] for data in datas]), bins=bin)[1]
        b_bins = np.histogram(np.hstack([data.trace_data["b"] for data in datas]), bins=bin)[1]
        c_bins = np.histogram(np.hstack([data.trace_data["c"] for data in datas]), bins=bin)[1]
        d_bins = np.histogram(np.hstack([data.trace_data["d"] for data in datas]), bins=bin)[1]
        sigma_bins = np.histogram(np.hstack([data.trace_data["sigma"] for data in datas]), bins=bin)[1]

        for j, data in enumerate(datas):
            a = np.array(data.trace_data["a"])
            b = np.array(data.trace_data["b"])
            c = np.array(data.trace_data["c"])
            d = np.array(data.trace_data["d"])
            sigma = np.array(data.trace_data["sigma"])

            den_a = stats.gaussian_kde(a)
            den_b = stats.gaussian_kde(b)
            den_c = stats.gaussian_kde(c)
            den_d = stats.gaussian_kde(d)
            n, x, _ = plt.hist(a, bins=a_bins, histtype=u'step', density=True)
            axes[0].plot(x, den_a(x), alpha=alpha, label=label[j], color=color[j])
            axes[0].set_xlabel("$A$[Hz]")
            n, x, _ = plt.hist(b, bins=b_bins, histtype=u'step', density=True)
            axes[1].plot(x, den_b(x), alpha=alpha, label=label[j], color=color[j])
            axes[1].set_xlabel("$B$[Hz/$\AA^D$]")
            n, x, _ = plt.hist(c, bins=c_bins, histtype=u'step', density=True)
            axes[2].plot(x, den_c(x), alpha=alpha, label=label[j], color=color[j])
            axes[2].set_xlabel("$C$[$\AA$]")
            n, x, _ = plt.hist(d, bins=d_bins, histtype=u'step', density=True)
            axes[3].plot(x, den_d(x), alpha=alpha, label=label[j], color=color[j])
            axes[3].set_xlabel("$D$")
            axes[4].hist(sigma, bins=sigma_bins, alpha=alpha, label=label[j], color=color[j])
            axes[4].set_xlabel("sigma")
        return axes

    # @staticmethod
    # def custom_plot_range_result(bayes_data: BayesData, x, y):
    #     plt.style.use('grayscale')
    #     plt.scatter(x[1:], y[1:], label="measured force", c="black", s=20, marker=".", alpha=1)
    #     plt.axvline(x[bayes_data.z0], linestyle='dashdot', c="black", alpha=0.8)
    #     f_lr = bayes_data.f_equation(x, bayes_data.real_a, bayes_data.real_b, bayes_data.c, bayes_data.d)
    #
    #     param1, sigma1 = bayes_data.get_result_param(0.001)
    #     param2, sigma2 = bayes_data.get_result_param(0.999)
    #
    #     y1, y2 = bayes_data.f_equation(x, *param1), bayes_data.f_equation(x, *param2)
    #     plt.fill_between(x, y1=y1, y2=y2, alpha=0.5, label="$\Delta f_{LR}$ inference range")
    #     # plt.plot(x, f_lr, linewidth=1.0, label="$F_{LR}$ median value")
    #     plt.xlim(-0.2, 5)
    #
    #     plt.legend(fontsize=13)
    #     plt.tick_params(labelsize=14)


if __name__ == "__main__":
    fileName = "Si_H_0041.f.ch1"
    data = BayesData(fileName+",51,42,Num0.bayes")
    print(data)
    Extension.plot_hyper_range = 10000
    print(fsh.default_project_path)

    cvt = fsh.PakConvertor(fileName)
    x, y = cvt.get_x_data(point=51), cvt.get_y_data(point=51)
    # x, y = cvt.get_x_data(point=(24,22), offset=None) - 30, cvt.get_y_data(point=(24,22))

    # plt.style.use('grayscale')
    Extension.plot_range_result(data, x, y)
    # Extension.plot_histogram(data)

    # Extension.plot_percentage_result(0.001, data, np.flipud(cvt.GetXData()), np.flipud(cvt.GetYData(50)))
    # Extension.plot_percentage_result(0.999, data, np.flipud(cvt.GetXData()), np.flipud(cvt.GetYData(50)))
    plt.show()
    # plt.savefig("fig_bayes1.png", transparent=True, dpi=300)

