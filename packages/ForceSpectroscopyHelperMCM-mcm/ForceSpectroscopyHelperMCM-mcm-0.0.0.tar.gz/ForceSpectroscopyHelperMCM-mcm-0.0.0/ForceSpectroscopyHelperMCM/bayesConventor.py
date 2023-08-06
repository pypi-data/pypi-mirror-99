import matplotlib.pyplot as plt
import ForceSpectroscopyHelperMCM as mcm
from ForceSpectroscopyHelper.converter import *
import ForceSpectroscopyHelper as fsh



class BayesianConventor:

    def __init__(self, cvt: StandardConvertor, file_directory: str = None):
        self.data_dict = {}
        self.cvt = cvt

        self.curve_count = 1024

        if file_directory is not None:
            n = 0
            m = 0
            files = [file for file in os.listdir(file_directory) if os.path.isfile(os.path.join(file_directory, file))]
            for file in files:
                if mcm.utility.IsBayesianSaveResultFile(file_directory + file):
                    data = mcm.BayesData(file_directory + file)
                    if int(data.index) not in self.data_dict.keys():
                        # self.data_dict[int(data.index)] = bayes_module.Extension.get_best_data(file.split(",")[0], file_directory, index=int(data.index))
                        self.data_dict[int(data.index)] = data
                        m += 1
                    n += 1
                    # print(n)
            print("convertor load", m, "files from", file_directory, "the total files are", n)

    def get_sigma_array(self):
        a = []
        for i in range(1, self.curve_count + 1):
            if i in self.data_dict:
                param, sigma = mcm.Extension.convert_real_param(self.data_dict[i])
                a.append([i, sigma])
        return np.array(a)

    def to_lr_map(self, percent=0.5):
        matrix = []
        x = self.cvt.get_x_data(1)
        for i in range(1, self.curve_count + 1):
            print(i, "/", self.curve_count)
            if i in self.data_dict:
                param, sigma = mcm.Extension.convert_real_param(self.data_dict[i], percent)
                array = np.array(self.data_dict[i].f_equation(x, param[0], param[1], param[2], param[3]))
            else:
                array = np.array([0] * 1024)
            matrix = np.concatenate([matrix, array])

        return np.flipud(np.reshape(matrix, (self.curve_count, 1024), order='F'))

    def to_sr_map(self, percent=0.5):
        lr = self.to_lr_map(percent)
        raw_data = np.flipud(np.array(self.cvt.reconstruct_map()))
        return raw_data - lr

    def to_f_sr_map(self, measure_param:fsh.measurement_param, percent=0.5, window_size = 51):
        matrix = []
        raw_data = np.array(self.cvt.reconstruct_map())
        x = self.cvt.get_x_data(1)
        for i in range(1, self.curve_count + 1):
            print(i, "/", self.curve_count)
            if i in self.data_dict:
                param, sigma = mcm.Extension.convert_real_param(self.data_dict[i], percent)
                array = raw_data[:,i-1] - np.array(self.data_dict[i].f_equation(x, param[0], param[1], param[2], param[3]))
                array = fsh.formula.average_smooth(array, 5)
                array = fsh.formula.CalcForceCurveMatrix(array, measure_param)[2:]
                array = fsh.formula.savitzky_golay_fliter(array,  window_size)
            else:
                array = np.array([0] * 1022)
            matrix = np.concatenate([matrix, array])

        return np.flipud(np.reshape(matrix, (1022, self.curve_count), order='F'))

    def plot(self, index):
        if index not in self.data_dict:
            print("No file exsit in index:", index)
            return
        x = np.flipud(self.cvt.get_x_data())
        y = np.flipud(self.cvt.get_y_data(self.data_dict[index].index))
        self.plot_data(self.data_dict[index], x, y)

    @staticmethod
    def plot_data(bayesData, x, y):
        bayesData.plot_curve(x, y)
        plt.show()

    def plot_path(self, path, index):
        csv = mcm.BayesData(path)
        x = np.flipud(self.cvt.get_x_data())
        y = np.flipud(self.cvt.get_y_data(index))
        self.plot_data(csv, x, y)


if __name__ == "__main__":
    cvt = StandardConvertor(I=1024, Width=10, fileName="MyFile_0020.f.ch1.csv")
    # data_path = default_project_path + "Force_0020.f.ch1,44,200,Num0.bayes"
    # data = BayesData(data_path)
    # data2 = BayesData(default_project_path + "Force_0020.f.ch1,251,360,Num1.bayes")
    # print(BayesianUtility.CalcRhat(np.asarray(data.trace_data["a"]), np.asarray(data2.trace_data["a"])))

    bayes_cvt = BayesianConventor(cvt, fsh.default_project_path + "Scripts/SiMapping/Data/")



