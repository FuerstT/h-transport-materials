import h_transport_materials as htm
from h_transport_materials.conversion import atmn_to_Pan
from h_transport_materials.property import Diffusivity, Solubility
from h_transport_materials import k_B, Rg, avogadro_nb
from pathlib import Path

import numpy as np

atm_to_Pa = 101325  # Pa/atm

molar_mass_li = 0.06941  # kg/mol
molar_mass_Pb = 0.2072  # kg/mol
rho_lipb = 10163.197  # kg/m3  at 300K


def molar_mass_lipb(nb_li: int, nb_pb: int):
    """Returns the molar mass (kg/mol) of a LiPb compound

    Args:
        nb_li (int): the number of Li atoms
        nb_pb (int): the number of Pb atoms

    Returns:
        float: the molar mass in kg/mol
    """

    return nb_pb * molar_mass_Pb + nb_li * molar_mass_li


def atom_density_lipb(nb_li: int, nb_pb: int):
    """Returns the atomic density (in m-3) of a LiPb compound

    Args:
        nb_li (int): the number of Li atoms
        nb_pb (int): the number of Pb atoms

    Returns:
        float: the atomic density in m-3
    """
    return (rho_lipb * avogadro_nb) / molar_mass_lipb(nb_li, nb_pb)


wu_solubility = Solubility(
    S_0=6.33e-07 * atom_density_lipb(nb_li=17, nb_pb=83),
    E_S=0,
    range=(850, 1040),
    source="wu_solubility_1983",
    name="D Wu (1983)",
    isotope="D",
    units="m-3 Pa-1/2",
)


chan_solubility = Solubility(
    S_0=4.7e-07 * atom_density_lipb(nb_li=17, nb_pb=1),
    E_S=9000 * k_B / Rg,
    range=(573, 773),
    source="chan_thermodynamic_1984",
    name="H Chan (1984)",
    isotope="H",
    units="m-3 Pa-1/2",
    note="extrapolated to Pb-17Li",
)


S_0_katsuta = 2.9e3  # atm^0.5  / at.fr.
S_0_katsuta = atmn_to_Pan(S_0_katsuta, n=0.5)  # Pa^0.5 / at.fr.
S_0_katsuta = 1 / S_0_katsuta  # at.fr. / Pa^0.5
S_0_katsuta *= atom_density_lipb(nb_li=17, nb_pb=83)

katsuta_solubility = Solubility(
    S_0=S_0_katsuta,
    E_S=0,
    range=(573, 723),
    source="katsuta_hydrogen_1985",
    name="H Katsuta (1985)",
    isotope="H",
    units="m-3 Pa-1/2",
)


fauvet_diffusivity = Diffusivity(
    D_0=1.5e-09,
    E_D=0,
    range=(722, 724),  # TODO should be 723 link to issue #37
    source="fauvet_hydrogen_1988",
    name="H Fauvet (1988)",
    isotope="H",
    note="Fauvet gives the value for 723 K only",
)
fauvet_solubility = Solubility(
    S_0=2.7e-08 * atom_density_lipb(nb_li=17, nb_pb=83),
    E_S=0,
    range=(722, 724),  # TODO should be 723 link to issue #37
    source="fauvet_hydrogen_1988",
    name="H Fauvet (1988)",
    isotope="H",
    units="m-3 Pa-1/2",
    note="Fauvet gives the value for 723 K only",
)


schumacher_solubility_data = np.genfromtxt(
    str(Path(__file__).parent) + "/schumacher_1990/solubility.csv",
    delimiter=",",
)

schumacher_solubility_data_T = schumacher_solubility_data[:, 0]  # 1000K-1
schumacher_solubility_data_T = 1000 / schumacher_solubility_data_T  # K

schumacher_solubility_data_y = schumacher_solubility_data[:, 1]  # ln(Ks/sqrt(bar))
schumacher_solubility_data_y *= (
    -1
)  # -ln(Ks/sqrt(bar)) = ln(sqrt(bar)/Ks) = ln(solubility * sqrt(bar))
schumacher_solubility_data_y = np.exp(
    schumacher_solubility_data_y
)  # solubility * sqrt(bar)

schumacher_solubility_data_y *= 1 / ((1e5) ** 0.5)  # solubility (at.fr Pa-1/2)
schumacher_solubility_data_y *= atom_density_lipb(nb_li=1, nb_pb=1)

schumacher_solubility = Solubility(
    data_T=schumacher_solubility_data_T,
    data_y=schumacher_solubility_data_y,
    source="schumacher_hydrogen_1990",
    name="H Schumacher (1990)",
    isotope="H",
    units="m-3 Pa-1/2",
    note="in the review of E.Mas de les Valls there's a mistake in the conversion and"
    + "the activation energy of solubility should be positive"
    + "We decided to refit Schumacher's data",
)


reiter_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/reiter_1991/diffusivity.csv",
    delimiter=",",
)

reiter_difusivity_data_H = reiter_diffusivity_data[2:, 2:]

reiter_difusivity_data_H_T = reiter_difusivity_data_H[:, 0]  # 1000/K
reiter_difusivity_data_H_T = 1000 / reiter_difusivity_data_H_T  # K

reiter_diffusivity_h = Diffusivity(
    data_T=reiter_difusivity_data_H_T,
    data_y=reiter_difusivity_data_H[:, 1],
    range=(508, 700),
    source="reiter_solubility_1991",
    name="H Reiter (1991)",
    isotope="H",
)

reiter_difusivity_data_D = reiter_diffusivity_data[2:, :2]

reiter_difusivity_data_D_T = reiter_difusivity_data_D[:, 0]  # 1000/K
reiter_difusivity_data_D_T = 1000 / reiter_difusivity_data_D_T  # K

reiter_diffusivity_d = Diffusivity(
    data_T=reiter_difusivity_data_D_T,
    data_y=reiter_difusivity_data_D[:, 1],
    range=(508, 700),
    source="reiter_solubility_1991",
    name="D Reiter (1991)",
    isotope="D",
)


reiter_solubility_data = np.genfromtxt(
    str(Path(__file__).parent) + "/reiter_1991/solubility.csv",
    delimiter=",",
)

reiter_solubility_data_H = reiter_solubility_data[2:, :2]
reiter_solubility_data_H_T = reiter_solubility_data_H[:, 0]  # 1000/K
reiter_solubility_data_H_T = 1000 / reiter_solubility_data_H_T  # K

reiter_solubility_data_H_y = reiter_solubility_data_H[:, 1]  # at.fr. Pa-1/2
reiter_solubility_data_H_y *= atom_density_lipb(nb_li=17, nb_pb=1)  # m-3 Pa-1/2

reiter_solubility_h = Solubility(
    data_T=reiter_solubility_data_H_T,
    data_y=reiter_solubility_data_H_y,
    range=(508, 700),
    source="reiter_solubility_1991",
    name="H Reiter (1991)",
    isotope="H",
    units="m-3 Pa-1/2",
)

reiter_solubility_data_D = reiter_solubility_data[2:, 2:]
reiter_solubility_data_D_T = reiter_solubility_data_D[:, 0]  # 1000/K
reiter_solubility_data_D_T = 1000 / reiter_solubility_data_D_T  # K

reiter_solubility_data_D_y = reiter_solubility_data_D[:, 1]  # at.fr. Pa-1/2
reiter_solubility_data_D_y *= atom_density_lipb(nb_li=17, nb_pb=1)  # m-3 Pa-1/2

reiter_solubility_d = Solubility(
    data_T=reiter_solubility_data_D_T[np.isfinite(reiter_solubility_data_D_T)],
    data_y=reiter_solubility_data_D_y[np.isfinite(reiter_solubility_data_D_y)],
    range=(508, 700),
    source="reiter_solubility_1991",
    name="D Reiter (1991)",
    isotope="D",
    units="m-3 Pa-1/2",
)

reiter_solubility_t = Solubility(
    S_0=2.32e-08 * atom_density_lipb(nb_li=17, nb_pb=1),
    E_S=1350 * k_B / Rg,
    range=(508, 700),
    source="reiter_solubility_1991",
    name="T Reiter (1991)",
    isotope="T",
    units="m-3 Pa-1/2",
)


data_aiello = np.genfromtxt(
    str(Path(__file__).parent) + "/aiello_2006/solubility_data.csv",
    delimiter=",",
)
data_T_aiello = data_aiello[:, 0]  # 1000/K
data_T_aiello = 1000 / data_T_aiello  # K
data_y_aiello = data_aiello[:, 1]  # mol m-3 Pa-1/2
data_y_aiello *= avogadro_nb  # m-3 Pa-1/2

aiello_solubility = Solubility(
    data_T=data_T_aiello,
    data_y=data_y_aiello,
    range=(600, 900),
    source="aiello_determination_2006",
    name="H Aiello (2006)",
    isotope="H",
    units="m-3 Pa-1/2",
)


shibuya_diffusivity = Diffusivity(
    data_T=np.array([300, 400, 500]) + 273.15,
    data_y=np.array([6.6e-6, 7.8e-6, 9.5e-6]) * 1e-4,
    source="shibuya_isothermal_1987",
    name="T Shibuya (1987)",
    isotope="T",
)

terai_diffusivity = Diffusivity(
    D_0=2.50e-07,
    E_D=27000 * k_B / Rg,
    range=(573, 973),
    source="terai_diffusion_1992",
    name="T Terai (1987)",
    isotope="T",
)

alberro_solubility = Solubility(
    S_0=8.64e-3 * avogadro_nb,
    E_S=9000 * k_B / Rg,
    range=(523, 922),
    source="alberro_experimental_2015",
    name="H Alberro (2015)",
    isotope="H",
    units="m-3 Pa-1/2",
)


properties = [
    fauvet_diffusivity,
    reiter_diffusivity_h,
    reiter_diffusivity_d,
    shibuya_diffusivity,
    terai_diffusivity,
    wu_solubility,
    chan_solubility,
    katsuta_solubility,
    fauvet_solubility,
    schumacher_solubility,
    reiter_solubility_h,
    reiter_solubility_d,
    reiter_solubility_t,
    aiello_solubility,
    alberro_solubility,
]

for prop in properties:
    prop.material = "lipb"

htm.database += properties
