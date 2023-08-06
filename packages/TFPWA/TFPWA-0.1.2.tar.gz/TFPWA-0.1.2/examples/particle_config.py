"""
Examples for config.yml file
----------------------------

Configuration file `config.yml` use YAML (https://yaml.org) format to describe decay process.

The main parts of config.yml is `decay` and `particle`.

The `decay` part describe the particle (or an id of a list of particle)
decay into which particles, it can be a list of a list of list.
A list means that there is ony one decay mode, A list of list is the list of possible decay mode.
The list item can be the particle name (or a dict to describe the decay parameters).
All name should appear in `particle` part.

The `particle` part describe the parameters of particles.
There are two special parts `$top` and `$finals` describe the top and finals particles.
The other parts are lists of particle name or dicts of particle parameters.
The list is the same type particle in decay part.
The dict is the parameters of the particle name.
"""

config_str = """

decay:
    A:
       - [R1, B]
       - [R2, C]
       - [R3, D]
    R1: [C, D]
    R2: [B, D]
    R3: [B, C]

particle:
    $top:
       A: { mass: 1.86, J: 0, P: -1}
    $finals:
       B: { mass: 0.494, J: 0, P: -1}
       C: { mass: 0.139, J: 0, P: -1}
       D: { mass: 0.139, J: 0, P: -1}
    R1: [ R1_a, R1_b ]
    R1_a: { mass: 0.7, width: 0.05, J: 1, P: -1}
    R1_b: { mass: 0.5, width: 0.05, J: 0, P: +1}
    R2: { mass: 0.824, width: 0.05, J: 0, P: +1}
    R3: { mass: 0.824, width: 0.05, J: 0, P: +1}

"""

# %%
# The config file can be loaded by `yaml` library.
#

import matplotlib.pyplot as plt
import yaml

from tf_pwa.config_loader import ConfigLoader
from tf_pwa.histogram import Hist1D

config = ConfigLoader(yaml.full_load(config_str))

# %%
# We set parameters to a blance value. And we can generate some toy data and calclute the weights
#

input_params = {
    "A->R1_a.BR1_a->C.D_total_0r": 6.0,
    "A->R1_b.BR1_b->C.D_total_0r": 1.0,
    "A->R2.CR2->B.D_total_0r": 2.0,
    "A->R3.DR3->B.C_total_0r": 1.0,
}
config.set_params(input_params)

data = config.generate_toy(1000)
phsp = config.generate_phsp(10000)

# You can also fit the data fit to the data
fit_result = config.fit([data], [phsp])
err = config.get_params_error(fit_result, [data], [phsp])

# %%
# we can see that thre fit results consistant with inputs, the first one is fixed.

for var in input_params:
    print(
        f"in: {input_params[var]} => out: {fit_result.params[var]} +/- {err.get(var, 0.)}"
    )

# %%
# We can use the amplitude to plot the fit results

amp = config.get_amplitude()
weight = amp(phsp)
partial_weight = amp.partial_weight(phsp)

# %%
# We can plot the data, Hist1D include some plot method base on matplotlib.

data_hist = Hist1D.histogram(
    data.get_mass("(C, D)"), bins=60, range=(0.25, 1.45)
)

mass_phsp = phsp.get_mass("(C, D)")
phsp_hist = Hist1D.histogram(
    mass_phsp, weights=weight, bins=60, range=(0.25, 1.45)
)
scale = phsp_hist.scale_to(data_hist)

pw_hist = []
for w in partial_weight:
    # here we used more bins for a smooth plot
    hist = Hist1D.histogram(
        mass_phsp, weights=w, bins=60 * 2, range=(0.25, 1.45)
    )
    pw_hist.append(scale * hist * 2)

# %%
# Then we can plot the histogram into matplotlib

for hist, dec in zip(pw_hist, config.get_decay()):
    hist.draw_kde(label=str(dec))
phsp_hist.draw(label="total amplitude")
data_hist.draw_error(label="toy data", color="black")

plt.legend()
plt.ylim((0, None))
plt.xlabel("M(CD)/ GeV")
plt.ylabel("Events/ 20 MeV")
plt.show()
