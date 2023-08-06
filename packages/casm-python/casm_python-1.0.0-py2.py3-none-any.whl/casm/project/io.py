"""casm.project file io"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from builtins import *

import json
import six
from casm.misc import compat, noindent


def write_eci(proj, eci, fit_details=None, clex=None, verbose=False):
    """Write eci.json

    Arguments
    ---------

    proj: casm.project.Project
        The CASM project

    eci: List[(index, value)]
        List of tuple containing basis function index and coefficient value:

            index (int): linear index of basis function
            value (float): ECI value

    fit_details: Dict
        Description of the fitting method used to generate the ECI, usually as output by `casm.learn.to_json`. It is added to the eci.json file under the attribute `"fit"`.

    clex: casm.project.ClexDescription
        Specifies where to write the ECI. Default value is  `proj.settings.default_clex`.

    """
    dir = proj.dir
    if clex is None:
        clex = proj.settings.default_clex

    # read basis.json
    filename = dir.basis(clex)
    with open(filename, 'r') as f:
        j = json.load(f)

    # edit to add fitting settings
    j["fit"] = fit_details

    # edit to add eci
    for index, value in eci:
        if j["orbits"][index]["linear_orbit_index"] != index:
            msg = "Formatting error in '" + str(filename) + "': "
            msg += " linear_orbit_index mismatch"
            raise Exception(msg)
        j["orbits"][index]["eci"] = value

    # pretty printing -- could be improved
    cspecs_params = j["bspecs"]["cluster_specs"]["params"]
    if "generating_group" in cspecs_params:
        cspecs_params["generating_group"] = noindent.NoIndent(
            cspecs_params["generating_group"])
    for entry in j["orbits"]:
        sites = entry["prototype"]["sites"]
        for i in range(len(sites)):
            sites[i] = noindent.NoIndent(sites[i])
    for site in j["prim"]["basis"]:
        site["coordinate"] = noindent.NoIndent(site["coordinate"])
        site["occupants"] = noindent.NoIndent(site["occupants"])
    for i in range(len(j["prim"]["lattice_vectors"])):
        j["prim"]["lattice_vectors"][i] = noindent.NoIndent(
            j["prim"]["lattice_vectors"][i])

    # write eci.json
    filename = dir.eci(clex)

    if verbose:
        print("Writing:", filename, "\n")
    with open(filename, 'w') as f:
        f.write(json.dumps(j, indent=2, cls=noindent.NoIndentEncoder))

    # refresh proj to reflect new eci
    proj.refresh(clear_clex=True)
