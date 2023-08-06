import os
import time

import matplotlib
import numpy as np
import pytest
import tensorflow as tf

from tf_pwa import set_random_seed
from tf_pwa.applications import gen_data, gen_mc
from tf_pwa.config_loader import ConfigLoader, MultiConfig
from tf_pwa.experimental import build_amp
from tf_pwa.utils import tuple_table

matplotlib.use("agg")


this_dir = os.path.dirname(os.path.abspath(__file__))


def generate_phspMC(Nmc):
    """Generate PhaseSpace MC of size Nmc and save it as txt file"""
    # masses of mother particle A and daughters BCD
    mA = 4.6
    mB = 2.00698
    mC = 2.01028
    mD = 0.13957
    # a2bcd is a [3*Nmc, 4] array, which are the momenta of BCD in the rest frame of A
    a2bcd = gen_mc(mA, [mB, mC, mD], Nmc)
    return a2bcd


def generate_toy_from_phspMC(Ndata, mc_file, data_file):
    """Generate toy using PhaseSpace MC from mc_file"""
    config = ConfigLoader(f"{this_dir}/config_toy.yml")
    config.set_params(f"{this_dir}/gen_params.json")
    amp = config.get_amplitude()
    data = gen_data(
        amp,
        Ndata=Ndata,
        mcfile=mc_file,
        genfile=data_file,
        particles=config.get_dat_order(),
    )
    return data


@pytest.fixture
def gen_toy():
    set_random_seed(1)
    if not os.path.exists("toy_data"):
        os.mkdir("toy_data")
    phsp = generate_phspMC(10000)
    np.savetxt("toy_data/PHSP.dat", phsp)
    generate_toy_from_phspMC(1000, "toy_data/PHSP.dat", "toy_data/data.dat")
    bg = generate_phspMC(1000)
    data = np.loadtxt("toy_data/data.dat")
    np.savetxt("toy_data/data.dat", np.concatenate([data, bg[:300, :]]))
    np.savetxt("toy_data/bg.dat", bg)
    np.savetxt("toy_data/data_bg_value.dat", np.ones((1000 + 100,)))
    np.savetxt("toy_data/data_eff_value.dat", np.ones((1000 + 100,)))
    np.savetxt("toy_data/phsp_bg_value.dat", np.ones((10000,)))
    np.savetxt("toy_data/phsp_eff_value.dat", np.ones((10000,)))


@pytest.fixture
def toy_config(gen_toy):
    config = ConfigLoader(f"{this_dir}/config_toy.yml")
    config.set_params(f"{this_dir}/exp_params.json")
    return config


def test_build_angle_amplitude(toy_config):
    data = toy_config.get_data("data")
    dec = toy_config.get_amplitude().decay_group
    amp_dict = build_amp.build_angle_amp_matrix(dec, data[0])
    assert len(amp_dict[1]) == 3


@pytest.fixture
def toy_config2(gen_toy, fit_result):
    config = MultiConfig(
        [f"{this_dir}/config_toy.yml", f"{this_dir}/config_toy2.yml"]
    )
    config.set_params(f"{this_dir}/exp2_params.json")
    return config


@pytest.fixture
def fit_result(toy_config):
    return toy_config.fit()


def test_cfit(gen_toy):
    config = ConfigLoader(f"{this_dir}/config_cfit.yml")
    config.set_params(f"{this_dir}/gen_params.json")
    fcn = config.get_fcn()
    fcn({})
    fcn.nll_grad({})


def test_constrains(gen_toy):
    config = ConfigLoader(f"{this_dir}/config_cfit.yml")
    var_name = "A->R_CD.B_g_ls_1r"
    config.config["constrains"]["init_params"] = {var_name: 1.0}

    @config.register_extra_constrains("init_params")
    def float_var(amp, params=None):
        amp.set_params(params)

    config.register_extra_constrains("init_params2", float_var)

    amp = config.get_amplitude()
    assert amp.get_params()[var_name] == 1.0


def test_fit(toy_config, fit_result):
    toy_config.plot_partial_wave(prefix="toy_data/figure", save_root=True)
    toy_config.plot_partial_wave(
        prefix="toy_data/figure", plot_pull=True, single_legend=True
    )
    toy_config.plot_partial_wave(
        prefix="toy_data/figure", smooth=False, bin_scale=1
    )
    toy_config.plot_partial_wave(prefix="toy_data/figure", color_first=False)
    toy_config.get_params_error(fit_result)
    fit_result.save_as("toy_data/final_params.json")
    fit_frac, frac_err = toy_config.cal_fitfractions()
    tuple_table(fit_frac)


def test_cal_chi2(toy_config, fit_result):
    toy_config.cal_chi2(bins=[[2, 2]] * 2, mass=["R_BD", "R_CD"])


def test_cal_signal_yields(toy_config, fit_result):
    toy_config.cal_signal_yields()


def test_fit_combine(toy_config2):
    toy_config2.fit()
    toy_config2.get_params_error()
    print(toy_config2.get_params())
