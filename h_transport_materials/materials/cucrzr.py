from h_transport_materials import k_B, Rg, avogadro_nb
from h_transport_materials.materials import Material
from h_transport_materials.property import ArheniusProperty

anderl_src = "R. A. Anderl et al. 'Deuterium transport in Cu, CuCrZr, and Cu/Be'. In: Journal of Nuclear Materials 266-269 (Mar. 1999), pp. 761–765"
anderl_recombination = ArheniusProperty(pre_exp=2.9e-14, act_energy=1.92, source=anderl_src, name="Anderl (1999)")

serra_src = "E Serra and A Perujo. 'Hydrogen and deuterium transport and inventory parameters in a Cu–0.65Cr–0.08Zr alloy for fusion reactor applications'. en. In: Journal of Nuclear Materials 258-263 (Oct. 1998), pp. 1028–1032"

# these are the equations given in Serra 1998 but some are wrong (not in agreement with the plotted data)
serra_diffusivity_h_eq = ArheniusProperty(pre_exp=5.7e-7, act_energy=41220*k_B/Rg, source=serra_src, name="H Serra (1998)")
serra_diffusivity_d_eq = ArheniusProperty(pre_exp=4.8e-7, act_energy=40370*k_B/Rg, source=serra_src, name="D Serra (1998)")
serra_diffusivity_T_eq = ArheniusProperty(pre_exp=3.07e-7, act_energy=39120*k_B/Rg, source=serra_src, name="T Serra (1998)")
serra_solubility_h_eq = ArheniusProperty(pre_exp=0.9*avogadro_nb, act_energy=38580*k_B/Rg, source=serra_src, name="H Serra (1998)")
serra_solubility_d_eq = ArheniusProperty(pre_exp=0.71*avogadro_nb, act_energy=37380*k_B/Rg, source=serra_src, name="D Serra (1998)")
serra_solubility_t_eq = ArheniusProperty(pre_exp=0.84*avogadro_nb, act_energy=38540*k_B/Rg, source=serra_src, name="T Serra (1998)")


# these are the fitted values from the experimental points in Serra 1998
from h_transport_materials.fitting import fit_arhenius
import numpy as np

# diffusivity
data_diffusivity_serra = np.genfromtxt("h_transport_materials/materials/cucrzr/serra_diffusivity_1998.csv", delimiter=",", dtype=str)
data_diffusivity_serra_h = data_diffusivity_serra[2:, :2].astype(float)
data_diffusivity_serra_d = data_diffusivity_serra[2:, 2:].astype(float)


D_0, E_D = fit_arhenius(data_diffusivity_serra_h[:, 1], 1000/data_diffusivity_serra_h[:, 0])
serra_diffusivity_h = ArheniusProperty(pre_exp=D_0, act_energy=E_D, source=serra_src, name="H Serra (1998) (refitted)")

D_0, E_D = fit_arhenius(data_diffusivity_serra_d[:, 1], 1000/data_diffusivity_serra_d[:, 0])
serra_diffusivity_d = ArheniusProperty(pre_exp=D_0, act_energy=E_D, source=serra_src, name="D Serra (1998) (refitted)")

# solubility
data_solubility_serra = np.genfromtxt("h_transport_materials/materials/cucrzr/serra_diffusivity_1998.csv", delimiter=",", dtype=str)
data_solubility_serra_h = data_solubility_serra[2:, :2].astype(float)
data_solubility_serra_d = data_solubility_serra[2:, 2:].astype(float)

S_0, E_S = fit_arhenius(data_solubility_serra_h[:, 1]*avogadro_nb, 1000/data_solubility_serra_h[:, 0])
serra_solubility_h = ArheniusProperty(pre_exp=S_0, act_energy=E_S, source=serra_src, name="H Serra (1998) (refitted)")

S_0, E_D = fit_arhenius(data_solubility_serra_d[:, 1]*avogadro_nb, 1000/data_solubility_serra_d[:, 0])
serra_solubility_d = ArheniusProperty(pre_exp=S_0, act_energy=E_S, source=serra_src, name="D Serra (1998) (refitted)")

serra_diffusivity_iter = ArheniusProperty(pre_exp=3.92e-7, act_energy=0.418, source=serra_src, name="T Serra acc. ITER (1998)")

cucrzr = Material(D=serra_diffusivity_h, S=serra_solubility_h, name="cucrzr")
