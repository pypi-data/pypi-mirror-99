"""Miscellaneous tools for marine carbonate chemistry and other such things."""

import string, textwrap
import numpy as np
from . import crm, infrared, molar, spectro, vindta, parameterisations, plot
from .vindta import (
    Dbs,
    read_dbs,
    read_logfile,
    get_logfile_index,
    get_sample_blanks,
    blank_progression,
    centre_and_scale,
    de_centre_and_scale,
    get_session_blanks,
    blank_correction,
    get_blank_corrections,
    get_density,
    get_standard_calibrations,
    get_session_calibrations,
    calibrate_dic,
    plot_session_blanks,
    plot_blanks,
    plot_k_dic,
    plot_dic_offset,
    concat,
    poison_correction,
)
from .plot import get_cluster_profile, cluster_profile
from .parameterisations import aou_GG92

__version__ = "0.0.15"
__author__ = "Humphreys, Matthew P."


lcletter = dict(zip(range(1, 27), string.ascii_lowercase))


def sigfig(x, sf):
    """Return `x` to `sf` significant figures."""
    factor = 10.0 ** np.ceil(np.log10(np.abs(x)))
    return factor * np.around(x / factor, decimals=sf)


def say_hello():
    greeting = textwrap.dedent(
        r"""
        k  Miscellaneous tools for
        o  marine carbonate chemistry
        o  and other such things
        l  
        s  Matthew P. Humphreys
        t  https://mvdh.xyz
        o  
        f  Version {}
        """.format(
            __version__
        )
    )
    print(greeting)


hello = say_hello
