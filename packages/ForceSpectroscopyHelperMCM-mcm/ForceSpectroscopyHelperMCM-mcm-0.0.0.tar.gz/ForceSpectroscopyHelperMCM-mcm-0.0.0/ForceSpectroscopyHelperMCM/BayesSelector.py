import os
from ForceSpectroscopyHelperMCM import *

import numpy as np


class ResultParamater:
    def __init__(self, a, b, c, d, z0, a_range, b_range, c_range, rscore=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.z0 = z0
        self.a_range = a_range
        self.b_range = b_range
        self.c_range = c_range
        self.rscore = rscore

    @property
    def average_rscore(self):
        return self.get_average_rscore(self.rscore)

    @staticmethod
    def get_average_rscore(rscore_dict):
        array = [*rscore_dict.values()][0:3]
        return np.average(array)


def __find_all_bayes_file(directory, **kwargs):
    result = {}
    files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    for file in files:
        if utility.IsBayesianSaveResultFile(os.path.join(directory + file)):
            data = BayesData(os.path.join(directory + file))

            if "fileName" in kwargs and kwargs["fileName"] is not None and kwargs["fileName"] != data.source_file_name:
                continue
            if "index" in kwargs and str(kwargs["index"]) is not None and str(kwargs["index"]) != data.index:
                continue
            if "z0" in kwargs and kwargs["z0"] is not None and int(kwargs["z0"]) != data.z0:
                continue
            if "chain" in kwargs and kwargs["chain"] is not None and int(kwargs["chain"]) != data.chainIndex:
                continue

            if data.name in result:
                result[data.name].append(data)
            else:
                result[data.name] = [data]

    return result


def select(directory, fileName, index=None, z0=None, chain=None):
    """
        find all bayes result in a directory fitted the given condition

        condition will be applied if it is not None

        return the dictionary, key: bayes.name, value: array of bayes data by chain
    """
    return __find_all_bayes_file(directory, fileName=fileName, index=index, z0=z0, chain=chain)


def select_result_param(directory, fileName, percentage_limit, index=None, z0=None):
    bayes_datas = select(directory, fileName=fileName, index=index, z0=z0)
    result = []
    for it in bayes_datas.values():
        a = np.asarray(it[0].trace_data["a"])
        b = np.asarray(it[0].trace_data["b"])
        c = np.asarray(it[0].trace_data["c"])

        rscore_dict = None
        # print(it[0].name, it[0].z0)
        if len(it) == 2:
            # print(two_bayesData_verification(it[0], it[1]))
            rscore_dict = two_bayesData_verification(it[0], it[1])

        result.append(ResultParamater(it[0].a, it[0].b, it[0].c, it[0].d, it[0].z0,
                                      np.percentile(a, q=percentage_limit), np.percentile(b, q=percentage_limit),
                                      np.percentile(c, q=percentage_limit), rscore_dict))

    return result


def two_bayesData_verification(bayes1: BayesData, bayes2: BayesData):
    result = {}
    result["a"] = BayesianUtility.CalcRhat([bayes1.trace_data["a"], bayes2.trace_data["a"]])
    result["b"] = BayesianUtility.CalcRhat([bayes1.trace_data["b"], bayes2.trace_data["b"]])
    result["c"] = BayesianUtility.CalcRhat([bayes1.trace_data["c"], bayes2.trace_data["c"]])
    result["d"] = BayesianUtility.CalcRhat([bayes1.trace_data["d"], bayes2.trace_data["d"]])

    result["sigma"] = BayesianUtility.CalcRhat([bayes1.trace_data["sigma"], bayes2.trace_data["sigma"]])
    return result


def bayesData_verification(bayes_array):
    result = {}
    length = len(bayes_array)
    if length < 2:
        raise ValueError('bayes datas count should be over 2')
    for i in range(0, length):
        for j in range(0, i):
            result[(i, j)] = two_bayesData_verification(bayes_array[i], bayes_array[j])
    return result


def average_result(result: dict):
    ave = np.zeros(5)
    length = len(result.keys())
    for v in result.values():
        ave += [v["a"], v["b"], v["c"], v["d"], v["sigma"]]
    return ave / length


def result_verification(bayes_array):
    result = {}
    nChain = len(bayes_array)
    if nChain < 2:
        raise ValueError('bayes datas count should be over 2')

    for i in range(0, nChain):
        for j in range(i+1, nChain):
            rscore_dict = two_bayesData_verification(bayes_array[i], bayes_array[j])
            result[(i, j, ResultParamater.get_average_rscore(rscore_dict))] = rscore_dict

    return result


def select_best_result_from_verification(bayes_array):
    """
        Select the best

        :return BayesData
    """
    length = len(bayes_array)
    if length < 2:
        raise ValueError('bayes datas count should be over 2')

    best_cost = 999
    best_data = bayes_array[0]

    for data in bayes_array:
        cost = 0
        for data1 in bayes_array:
            if data is data1:
                pass
            r = two_bayesData_verification(data, data1)
            cost += r["a"] + r["b"] + r["c"] + r["d"] + r["sigma"]
        if best_cost > cost:
            best_cost = cost
            best_data = data

    return best_data, best_cost/length/5


if __name__ == "__main__":
    # fileName = "MyFile_0020.f.ch1"
    fileName = "Si_H_0041.f.ch1"

    x = []
    rhat_list = []
    for i in range(1, 151):
        result = select("./", fileName=fileName, index=i, z0=None)
        result1 = result_verification(result[[*result.keys()][0]])
        x.append(i)
        rhat_list.append(*result1.keys())
        print(i, *result1.keys())

    # x = np.array(x)
    # y = np.array(rhat_list)[:,2]
    # plt.scatter(x, y)
    # plt.show()
    """
    best_key = (0, 1, 1)
    for it in result1.keys():
        if np.abs(it[2]-1) <= best_key[2]:
            best_key = it

    print(best_key)
    print(result[[*result.keys()][0]][best_key[1]])
    """


