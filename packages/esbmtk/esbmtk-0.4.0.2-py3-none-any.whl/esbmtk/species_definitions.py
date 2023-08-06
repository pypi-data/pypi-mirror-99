# from pint import UnitRegistry
from numbers import Number
from nptyping import *
from typing import *
from numpy import array, set_printoptions, arange, zeros, interp, mean
from pandas import DataFrame
from copy import deepcopy, copy
from time import process_time

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import logging
import time
import builtins
set_printoptions(precision=4)
# from .utility_functions import *
from .esbmtk import Element, Species

def carbon(model):
    """ Some often used definitions
    
    """

    eh = Element(
        name="Carbon",  # Element Name
        model=model,  # Model handle
        mass_unit="mmol",  # base mass unit
        li_label="C^{12}$S",  # Name of light isotope
        hi_label="C^{13}$S",  # Name of heavy isotope
        d_label= r"$\delta^{13}$C",  # Name of isotope delta
        d_scale="VPDB",  # Isotope scale. End of plot labels
        r=0.0112372,  # VPDB C13/C12 ratio https://www-pub.iaea.org/MTCD/publications/PDF/te_825_prn.pdf
    )

    # add species
    Species(name="CO2", element=eh, display_as = r"CO$_2$" )  # Name & element handle
    Species(name="DIC", element=eh)
    Species(name="OM", element=eh)
    Species(name="CaCO3", element=eh,  display_as= r"CaCO$_3$")
    Species(name="HCO3", element=eh, display_as= r"HCO$_3^-$")
    Species(name="CO3", element=eh, display_as = "CO$_3^{2-}$")
    Species(name="DOC", element=eh)
    Species(name="C", element=eh)
    Species(name="ALK", element=eh)  # Alkalinity
    Species(name="CALK", element=eh) # Carbonate Alkalinity
    Species(name="CA", element=eh) 
    Species(name="TALK", element=eh) # Total Alkalinity
    Species(name="TA", element=eh) 
    Species(name="PALK", element=eh) # Practical Alkalinity
    Species(name="PA", element=eh) 


def sulfur(model):
    eh = Element(
        name="Sulfur",
        model=model,  # model handle
        mass_unit="mmol",  # base mass unit
        li_label="$^{32}$S",  # Name of light isotope
        hi_label="$^{34}$S",  # Name of heavy isotope
        d_label="$\delta^{34}$S",  # Name of isotope delta
        d_scale="VCDT",  # Isotope scale. End of plot labels
        r=0.044162589,  # isotopic abundance ratio for species
    )

    # add species
    Species(name="SO4", element=eh, display_as=r"SO$_{4}^{2-}$")
    Species(name="SO4oxygen", element=eh, display_as=r"SO$_{4}^{2-}{_ox}$")
    Species(name="SO3", element=eh,  display_as=r"SO$_{3}$")
    Species(name="SO2", element=eh, display_as=r"SO$_{2$}")
    Species(name="HS", element=eh, display_as=r"HS$^-$")
    Species(name="H2S", element=eh, display_as=r"H$_{2}$S")
    Species(name="FeS", element=eh)
    Species(name="FeS2", element=eh, display_as=r"FeS$_{2}$") 
    Species(name="S0", element=eh)
    Species(name="S", element=eh)
    Species(name="S2minus", element=eh, display_as=r"S$^{2-}$")

def hydrogen(model):
    eh = Element(
        name="Hydrogen",
        model=model,  # model handle
        mass_unit="mmol",  # base mass unit
        li_label="$^{1$}H",  # Name of light isotope
        hi_label="$^{2}$H",  # Name of heavy isotope
        d_label=r"$\delta^{2}$D",  # Name of isotope delta
        d_scale="VSMOV",  # Isotope scale. End of plot labels  # needs verification
        r=155.601e-6,  # After Groenig, 2000, Tab 40.1
    )

    # add species
    Species(name="Hplus", element=eh, display_as=r"$H^+$")  # Name & element handle
    Species(name="H2O", element=eh, display_as=r"H$_{2}$O")  # Name & element handle
    Species(name="H", element=eh)  # Name & element handle


def oxygen(model):
    eh = Element(
        name="Oxygen",
        model=model,  # model handle
        mass_unit="mmol",  # base mass unit
        li_label="$^{16$}O",  # Name of light isotope
        hi_label="$^{18}$)",  # Name of heavy isotope
        d_label=r"$\delta^{18}$)",  # Name of isotope delta
        d_scale="VSMOV",  # Isotope scale. End of plot labels  # needs verification
        r=2005.201e-6,  # https://nucleus.iaea.org/rpst/documents/vsmow_slap.pdf
    )

    # add species
    Species(name="O", element=eh, display_as="O")
    # Name & element handle
    Species(name="O2", element=eh, display_as=r"O$_{2}$")  # Name & element handle
    Species(name="OH", element=eh, display_as=r"OH$^{-}$")  # Name & element handle


def phosphor(model):
    eh = Element(
        name="Phosphor",
        model=model,  # model handle
        mass_unit="mmol",  # base mass unit
        li_label="None",  # Name of light isotope
        hi_label="None",  # Name of heavy isotope
        d_label="None",  # Name of isotope delta
        d_scale="None",  # Isotope scale. End of plot labels  # needs verification
        r=1,  # isotopic abundance ratio for species # needs verification
    )

    # add species
    Species(name="PO4", element=eh, display_as=r"PO$_{4}$")  # Name & element handle
    Species(name="P", element=eh, display_as=r"P")  # Name & element handle


def nitrogen(model):
    eh = Element(
        name="Nitrogen",
        model=model,  # model handle
        mass_unit="mmol",  # base mass unit
        li_label=r"$^{15$}N",  # Name of light isotope
        hi_label=r"$^{14$}N",  # Name of heavy isotope
        d_label=r"$\delta^{15}$N",  # Name of isotope delta
        d_scale="Air",  # Isotope scale. End of plot labels  # needs verification
        r=3676.5e-6,  # isotopic abundance ratio for species # needs verification
    )

    # add species
    Species(name="N", element=eh, display_as=r"N")
    Species(name="N2", element=eh, display_as=r"N$_{2}$")  # Name & element handle
    Species(name="Nox", element=eh, display_as=r"Nox")  # Name & element handle
    Species(name="NH4", element=eh, display_as=r"NH$_{4}^{+}$")  # Name & element handle
    Species(name="NH3", element=eh, display_as=r"NH$_{3}$")  # Name & element handle


def boron(model):
    eh = Element(
        name="Boron",
        model=model,  # model handle
        mass_unit="mmol",  # base mass unit
        li_label=r"$^{11$}B",  # Name of light isotope
        hi_label=r"$^{10$}B",  # Name of heavy isotope
        d_label=r"$\delta{11}B",  # Name of isotope delta
        d_scale="SRM951",  # Isotope scale. End of plot labels  # needs verification
        r=0.26888,  # isotopic abundance ratio for species # needs verification
    )

    # add species
    Species(name="B", element=eh, display_as=r"B")  # Name & element handle
    Species(name="BOH3", element=eh, display_as=r"B(OH)$_{3}$")  # Boric Acid
    Species(name="BOH4", element=eh, display_as=r"B(OH)$_{4}^{-}$")  # Borate
