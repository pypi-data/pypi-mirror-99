import pymc3
from pymc3 import Normal, Uniform, Model
from pymc3.distributions import Interpolated
from ForceSpectroscopyHelperMCM.Utils.ConsoleColor import color
from ForceSpectroscopyHelperMCM import BayesianUtility

from enum import Enum
import numpy as np
from scipy import stats


class ModelEnum(Enum):
    df = "df"
    f = "f"
    legacy_f = "legacy_f"
    legacy_df = "legacy_df"
    static_f = "static_f"
    test_df = "test_df"

    @staticmethod
    def get_model(model):
        if model == ModelEnum.df or model == ModelEnum.f or model == ModelEnum.static_f or model == ModelEnum.test_df:
            return BayesianUtility.f
        if model == ModelEnum.legacy_df or model == ModelEnum.legacy_f:
            return BayesianUtility.f_legacy

    @staticmethod
    def value_of(str_value: str):
        s = str_value.split(".")
        s = s[len(s)-1]
        for it in ModelEnum:
            if it.value == s:
                return it
        raise ValueError("{} can not be convert to enum".format(str_value))


"""
    Here are implement models
"""


def df_model(x, y, z0, limit_d=(0.5, 1.5), param_type="normal", **kwargs):
    """
        a model include one curve of df
        usually used in analyzing short-range fitting with correct z0
    """
    m = ModelEnum.df
    with Model() as model:
        print(color.Log + "Creating model" + color.End)
        if param_type == "normal":
            a0, b0, c0, d = __build_normal_param(limit_d, **kwargs)
        elif param_type == "uniform":
            a0, b0, c0, d = __build_uniform_param(limit_d, **kwargs)
        else:
            raise ValueError("could not find param_type name", param_type)

        s_a = pymc3.HalfCauchy("sa", beta=0.8)
        s_b = pymc3.HalfCauchy("sb", beta=0.5)
        s_c = pymc3.HalfCauchy("sc", beta=0.5)

        a = pymc3.Normal("a", mu=a0, sd=s_a)
        b = pymc3.Normal("b", mu=b0, sd=s_b)
        c = pymc3.Normal("c", mu=c0, sd=s_c)

        f_lr = pymc3.Deterministic("mu", ModelEnum.get_model(m)(x[z0:], a, b, c, d))
        pymc3.Deterministic("mu-all", ModelEnum.get_model(m)(x, a, b, c, d))

        ep_sigma = pymc3.HalfCauchy("sigma", beta=3)
        # ep_sigma = pymc3.Gamma("sigma", alpha=0.015, beta=1)
        # pymc3.StudentT("y", nu=25, mu=f_lr, sd=ep_sigma, observed=y[z0:])
        pymc3.Normal("y", mu=f_lr, sd=ep_sigma, observed=y[z0:])

        return [model, m]


def static_tipbody_force_model(x, y, z0, d_value, **kwargs):
    """
        for a model of tip body phiscal model, "d" argument is usualy from 1~2
        usually used in analyzing short-range fitting with correct z0
    """
    m = ModelEnum.static_f
    with Model() as model:
        if "a" in kwargs:
            a0 = Uniform("a0", upper=kwargs["a"] + 1, lower=kwargs["a"] - 1)
        else:
            a0 = Uniform("a0", upper=1.0, lower=-1)

        if "b" in kwargs:
            b0 = Normal("b0", mu=kwargs["b"], sd=0.1)
        else:
            b0 = Uniform("b0", upper=15.0, lower=0)

        if "c" in kwargs:
            c0 = Normal("c0", mu=kwargs["c"], sd=0.1)
        else:
            c0 = Uniform("c0", upper=5.0, lower=0)

        print(color.Log + "Creating model" + color.End)
        s_a = pymc3.HalfCauchy("sa", beta=0.1)
        s_b = pymc3.HalfCauchy("sb", beta=0.1)
        s_c = pymc3.HalfCauchy("sc", beta=0.1)
        d = pymc3.Uniform("d", d_value, d_value+0.01)

        a = pymc3.Normal("a", mu=a0, sd=s_a)
        b = pymc3.Normal("b", mu=b0, sd=s_b)
        c = pymc3.Normal("c", mu=c0, sd=s_c)

        f_lr = pymc3.Deterministic("mu", ModelEnum.get_model(m)(x[z0:], a, b, c, d_value))
        pymc3.Deterministic("mu-all", ModelEnum.get_model(m)(x, a, b, c, d_value))

        ep_sigma = pymc3.HalfCauchy("sigma", beta=1)
        # ep_sigma = pymc3.Gamma("sigma", alpha=0.015, beta=1)
        pymc3.Normal("y", mu=f_lr, sd=ep_sigma, observed=y[z0:])
        return [model, m]


def f_model(x, y, z0, limit_d=(1.0, 2.0), param_type="normal", **kwargs):
    m = ModelEnum.f
    with Model() as model:
        print(color.Log + "Creating model" + color.End)
        if param_type == "normal":
            a0, b0, c0, d = __build_normal_param(limit_d, **kwargs)
        elif param_type == "uniform":
            a0, b0, c0, d = __build_uniform_param(limit_d, **kwargs)
        else:
            raise ValueError("could not find param_type name", param_type)
        s_a = pymc3.HalfCauchy("sa", beta=0.5)
        s_b = pymc3.HalfCauchy("sb", beta=0.5)
        s_c = pymc3.HalfCauchy("sc", beta=0.5)

        a = pymc3.Normal("a", mu=a0, sd=s_a)
        b = pymc3.Normal("b", mu=b0, sd=s_b)
        c = pymc3.Normal("c", mu=c0, sd=s_c)

        f_lr = pymc3.Deterministic("mu", ModelEnum.get_model(m)(x[z0:], a, b, c, d))
        pymc3.Deterministic("mu-all", ModelEnum.get_model(m)(x, a, b, c, d))

        ep_sigma = pymc3.HalfCauchy("sigma", beta=3)
        pymc3.StudentT("y", nu=25, mu=f_lr, sd=ep_sigma, observed=y[z0:])

        return [model, m]


def test_df_model(x, y, z0, limit_d=(0.5,1.5), param_type="normal", **kwargs):
    m = ModelEnum.test_df
    with Model() as model:
        print(color.Log + "Creating model" + color.End)
        if param_type == "normal":
            a0, b0, c0, d = __build_normal_param(limit_d, **kwargs)
        elif param_type == "uniform":
            a0, b0, c0, d = __build_uniform_param(limit_d, **kwargs)
        else:
            raise ValueError("could not find param_type name", param_type)

        s_a = pymc3.HalfCauchy("sa", beta=0.8)
        s_b = pymc3.HalfCauchy("sb", beta=0.5)
        s_c = pymc3.HalfCauchy("sc", beta=0.5)

        a = pymc3.Normal("a", mu=a0, sd=s_a)
        b = pymc3.Normal("b", mu=b0, sd=s_b)
        c = pymc3.Normal("c", mu=c0, sd=s_c)

        z0 = pymc3.Normal("z0", mu=z0, sd=5)

        f_lr = pymc3.Deterministic("mu", ModelEnum.get_model(m)(x[z0:], a, b, c, d))
        pymc3.Deterministic("mu-all", ModelEnum.get_model(m)(x, a, b, c, d))

        ep_sigma = pymc3.HalfCauchy("sigma", beta=3)
        # ep_sigma = pymc3.Gamma("sigma", alpha=0.015, beta=1)
        # pymc3.StudentT("y", nu=25, mu=f_lr, sd=ep_sigma, observed=y[z0:])
        pymc3.Normal("y", mu=f_lr, sd=ep_sigma, observed=y[z0:])

        return [model, m]


def legacy_df_model(x, y, z0, limit_d=(0.5, 1.5), param_type="normal", **kwargs):
    m = ModelEnum.legacy_df
    with Model() as model:
        print(color.Log + "Creating model" + color.End)
        if param_type == "normal":
            a0, b0, c0, d = __build_normal_param(limit_d, **kwargs)
        elif param_type == "uniform":
            a0, b0, c0, d = __build_uniform_param(limit_d, **kwargs)
        else:
            raise ValueError("could not find param_type name", param_type)

        s_a = pymc3.HalfCauchy("sa", beta=0.8)
        s_b = pymc3.HalfCauchy("sb", beta=0.5)
        s_c = pymc3.HalfCauchy("sc", beta=0.5)

        a = pymc3.Normal("a", mu=a0, sd=s_a)
        b = pymc3.Normal("b", mu=b0, sd=s_b)
        c = pymc3.Normal("c", mu=c0, sd=s_c)

        f_lr = pymc3.Deterministic("mu", ModelEnum.get_model(m)(x[z0:], a, b, c, d))
        pymc3.Deterministic("mu-all", ModelEnum.get_model(m)(x, a, b, c, d))

        ep_sigma = pymc3.HalfCauchy("sigma", beta=3)
        # ep_sigma = pymc3.Gamma("sigma", alpha=0.015, beta=1)
        # pymc3.StudentT("y", nu=25, mu=f_lr, sd=ep_sigma, observed=y[z0:])
        pymc3.Normal("y", mu=f_lr, sd=ep_sigma, observed=y[z0:])

        return [model, m]


def __build_uniform_param(limit_d=(0.5, 1.5), **kwargs):
    if "a" in kwargs:
        a0 = Uniform("a0", upper=kwargs["a"] * 1.5 + 1, lower=kwargs["a"] * 0.5 - 1)
    else:
        a0 = Uniform("a0", upper=1.0, lower=-1)

    if "b" in kwargs:
        b0 = Uniform("b0", upper=kwargs["b"] * 2, lower=kwargs["b"] * 0.5)
    else:
        b0 = Uniform("b0", upper=15.0, lower=0)

    if "c" in kwargs:
        c0 = Uniform("c0", upper=kwargs["c"] * 2, lower=kwargs["c"] * 0.5)
    else:
        c0 = Uniform("c0", upper=5.0, lower=0)

    d = Uniform("d", upper=limit_d[1], lower=limit_d[0])
    return a0, b0, c0, d


def __build_normal_param(limit_d=(0.5, 1.5), **kwargs):
    if "a" in kwargs:
        a0 = Uniform("a0", upper=kwargs["a"] + 1, lower=kwargs["a"] - 1)
    else:
        a0 = Uniform("a0", upper=1.0, lower=-1)

    if "b" in kwargs:
        b0 = Normal("b0", mu=kwargs["b"], sd=0.1)
    else:
        b0 = Uniform("b0", upper=30.0, lower=0)

    if "c" in kwargs:
        c0 = Normal("c0", mu=kwargs["c"], sd=0.1)
    else:
        c0 = Uniform("c0", upper=10.0, lower=0)

    if "d" in kwargs:
        d = Normal("d", mu=kwargs["d"], sd=0.1)
    else:
        d = Uniform("d", upper=limit_d[1], lower=limit_d[0])

    return a0, b0, c0, d


def from_posterior(param, samples):
    smin, smax = np.min(samples), np.max(samples)
    width = smax - smin
    x = np.linspace(smin, smax, 100)
    y = stats.gaussian_kde(samples)(x)

    # what was never sampled should have a small probability but not 0,
    # so we'll extend the domain and use linear approximation of density on it
    x = np.concatenate([[x[0] - 3 * width], x, [x[-1] + 3 * width]])
    y = np.concatenate([[0], y, [0]])
    return Interpolated(param, x, y)


def model_from_trace(x, y, z0, trace):
    m = ModelEnum.legacy_df
    with Model() as model:
        print(color.Log + "Creating model" + color.End)

        s_a = pymc3.HalfCauchy("sa", beta=0.8)
        s_b = pymc3.HalfCauchy("sb", beta=0.5)
        s_c = pymc3.HalfCauchy("sc", beta=0.5)

        a0 = Uniform("a0", upper=1.0, lower=-1)
        b0 = Uniform("b0", upper=15.0, lower=0)
        c0 = Uniform("c0", upper=5.0, lower=0)
        d = from_posterior("d", trace["d"])

        a = pymc3.Normal("a", mu=a0, sd=s_a)
        b = pymc3.Normal("b", mu=b0, sd=s_b)
        c = pymc3.Normal("c", mu=c0, sd=s_c)

        f_lr = pymc3.Deterministic("mu", ModelEnum.get_model(m)(x[z0:], a, b, c, d))
        pymc3.Deterministic("mu-all", ModelEnum.get_model(m)(x, a, b, c, d))

        ep_sigma = pymc3.HalfCauchy("sigma", beta=3)
        # ep_sigma = pymc3.Gamma("sigma", alpha=0.015, beta=1)
        # pymc3.StudentT("y", nu=25, mu=f_lr, sd=ep_sigma, observed=y[z0:])
        pymc3.Normal("y", mu=f_lr, sd=ep_sigma, observed=y[z0:])

        return [model, m]