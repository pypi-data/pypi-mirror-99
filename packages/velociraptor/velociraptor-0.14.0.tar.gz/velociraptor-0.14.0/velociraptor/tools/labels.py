"""
Tools for generating labels from catalogue datasets.
"""

import unyt
import re


def get_full_label(dataset: unyt.unyt_array):
    """
    Get the full label for one of our VelociraptorCatalogue datasets.
    This will get the automatically generated name and concatenate
    it with the _current_ untis for that dataset.
    """

    unit_tex = dataset.units.latex_representation()

    full_label = f"{dataset.name} $\\left[{unit_tex}\\right]$"

    return full_label


def get_mass_function_label_no_units(mass_function_sub_label: str):
    """
    Gets a fancy mass-function label such as:

    d$n(M_*)$/d$\log_{10}M_*$ [Mpc$^{-3}$]

    (this would be for an input of "*" and unyt.Mpc**3).
    """

    output = (
        fr"d$n(M_{mass_function_sub_label})$/d$\log_{{10}}M_{mass_function_sub_label}$"
    )

    return output


def get_mass_function_label(
    mass_function_sub_label: str, mass_function_units: unyt.Unit
):
    """
    Gets a fancy mass-function label such as:

    d$n(M_*)$/d$\log_{10}M_*$ [Mpc$^{-3}$]

    (this would be for an input of "*" and unyt.Mpc**3).
    """

    unit_repr = mass_function_units.latex_representation()
    mass_func_label = get_mass_function_label_no_units(mass_function_sub_label)

    output = fr"{mass_func_label} $\left[{unit_repr}\right]$"

    return output
