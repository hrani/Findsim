""" setup.py : Script for FindSim """
__author__      = "HarshaRani"
__copyright__   = "Copyright 2021 FindSim, NCBS"
__maintainer__  = "HarshaRani"
__email__       = "hrani@ncbs.res.in"

import os
import sys
import setuptools

with open("README.md","r") as fh:
        description = fh.read()

setuptools.setup(
        name="FindSim",
        desctiption="A Framework for Integrating Neuronal Data and Signalling Models",
        version="1.0",
        long_description = description,
        packages = ["FindSim"],
        package_dir= {"FindSim" : "."},
	install_requires = ["pymoose","numpy","mpld3","jsonschema"],
	url ="http://github.com/Bhallalab/FindSim",
	package_data = {"FindSim" : ['*.json','Curated/*.json','models/*']},
	license="GPLv3",
	entry_points = {
		'console_scripts' : ['findSim = FindSim.__main__:run',
				      'findSim_parallel = FindSim.__main__:run_parallel'
				     ]
			},
		)
