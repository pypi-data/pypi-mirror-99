# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geojson_modelica_translator',
 'geojson_modelica_translator.geojson',
 'geojson_modelica_translator.model_connectors',
 'geojson_modelica_translator.model_connectors.couplings',
 'geojson_modelica_translator.model_connectors.districts',
 'geojson_modelica_translator.model_connectors.energy_transfer_systems',
 'geojson_modelica_translator.model_connectors.load_connectors',
 'geojson_modelica_translator.model_connectors.networks',
 'geojson_modelica_translator.model_connectors.plants',
 'geojson_modelica_translator.modelica',
 'geojson_modelica_translator.modelica.lib',
 'geojson_modelica_translator.modelica.lib.runner',
 'geojson_modelica_translator.system_parameters',
 'management']

package_data = \
{'': ['*'],
 'geojson_modelica_translator.geojson': ['data/schemas/*'],
 'geojson_modelica_translator.model_connectors.couplings': ['templates/CoolingIndirect_Network2Pipe/*',
                                                            'templates/CoolingIndirect_NetworkChilledWaterStub/*',
                                                            'templates/HeatingIndirect_Network2Pipe/*',
                                                            'templates/HeatingIndirect_NetworkHeatedWaterStub/*',
                                                            'templates/Network2Pipe_CoolingPlant/*',
                                                            'templates/Network2Pipe_HeatingPlant/*',
                                                            'templates/Spawn_EtsColdWaterStub/*',
                                                            'templates/Spawn_EtsHotWaterStub/*',
                                                            'templates/Teaser_EtsColdWaterStub/*',
                                                            'templates/Teaser_EtsHotWaterStub/*',
                                                            'templates/TimeSeriesMFT_CoolingIndirect/*',
                                                            'templates/TimeSeriesMFT_HeatingIndirect/*',
                                                            'templates/TimeSeries_CoolingIndirect/*',
                                                            'templates/TimeSeries_EtsColdWaterStub/*',
                                                            'templates/TimeSeries_EtsHotWaterStub/*',
                                                            'templates/TimeSeries_HeatingIndirect/*'],
 'geojson_modelica_translator.model_connectors.districts': ['templates/*'],
 'geojson_modelica_translator.model_connectors.energy_transfer_systems': ['templates/*'],
 'geojson_modelica_translator.model_connectors.load_connectors': ['templates/*'],
 'geojson_modelica_translator.model_connectors.networks': ['templates/*'],
 'geojson_modelica_translator.model_connectors.plants': ['templates/*'],
 'geojson_modelica_translator.modelica': ['model_connectors/templates/*',
                                          'templates/*']}

install_requires = \
['BuildingsPy==2.1.0',
 'click==7.1.2',
 'geojson==2.5.0',
 'jsonpath-ng==1.5.2',
 'jsonschema==3.2.0',
 'modelica-builder==0.1.1',
 'requests==2.25.1',
 'teaser==0.7.5']

entry_points = \
{'console_scripts': ['format_modelica_files = '
                     'management.format_modelica_files:fmt_modelica_files',
                     'uo_des = management.uo_des:cli',
                     'update_licenses = '
                     'management.update_licenses:update_licenses',
                     'update_schemas = '
                     'management.update_schemas:update_schemas']}

setup_kwargs = {
    'name': 'geojson-modelica-translator',
    'version': '0.2.2',
    'description': 'Package for converting GeoJSON to Modelica models for Urban Scale Analyses.',
    'long_description': 'GeoJSON Modelica Translator (GMT)\n---------------------------------\n\n.. image:: https://github.com/urbanopt/geojson-modelica-translator/actions/workflows/ci.yml/badge.svg?branch=develop\n    :target: https://github.com/urbanopt/geojson-modelica-translator/actions/workflows/ci.yml\n\n.. image:: https://coveralls.io/repos/github/urbanopt/geojson-modelica-translator/badge.svg?branch=develop\n    :target: https://coveralls.io/github/urbanopt/geojson-modelica-translator?branch=develop\n\n.. image:: https://badge.fury.io/py/GeoJSON-Modelica-Translator.svg\n    :target: https://pypi.org/project/GeoJSON-Modelica-Translator/\n\nDescription\n-----------\n\nThe GeoJSON Modelica Translator (GMT) is a one-way trip from GeoJSON in combination with a well-defined instance of the system parameters schema to a Modelica package with multiple buildings loads, energy transfer stations, distribution networks, and central plants. The project will eventually allow multiple paths to build up different district heating and cooling system topologies; however, the initial implementation is limited to 1GDH and 4GDHC.\n\nThe project is motivated by the need to easily evaluate district energy systems. The goal is to eventually cover the various generations of heating and cooling systems as shown in the figure below. The need to move towards 5GDHC systems results in higher efficiencies and greater access to additional waste-heat sources.\n\n.. image:: https://raw.githubusercontent.com/urbanopt/geojson-modelica-translator/develop/docs/images/des-generations.png\n\nGetting Started\n---------------\n\nIt is possible to test the GeoJSON to Modelica Translator (GMT) by simpling installing the Python package and running the\ncommand line interface (CLI) with results from and URBANopt SDK set of results. However, to fully leverage the\nfunctionality of this package (e.g., running simulations), then you must also install the Modelica Buildings\nlibrary (MBL) and Docker. Instructions for installing and configuring the MBL and Docker are available\n`here <docs/getting_started.rst>`_\n\nTo simply scaffold out a Modelica package that can be inspected in a Modelica environment (e.g., Dymola) then\nrun the following code below up to the point of run-model. The example generates a complete 4th Generation District\nHeating and Cooling (4GDHC) system with time series loads that were generated from the URBANopt SDK using\nOpenStudio/EnergyPlus simulations.\n\n.. code-block:: bash\n\n    pip install geojson-modelica-translator\n\n    # from the simulation results within a checkout of this repository\n    # in the ./tests/management/data/sdk_project_scraps path.\n\n    # generate the system parameter from the results of the URBANopt SDK and OpenStudio Simulations\n    uo_des build-sys-param sys_param.json baseline_scenario.csv example_project.json\n\n    # create the modelica package (requires installation of the MBL)\n    uo_des create-model sys_param.json\n\n    # test running the new Modelica package (requires installation of Docker)\n    uo_des run-model model_from_sdk\n\nMore example projects are available in an accompanying\n`example repository <https://github.com/urbanopt/geojson-modelica-translator-examples>`_.\n\nArchitecture Overview\n---------------------\n\nThe GMT is designed to enable "easy" swapping of building loads, district systems, and newtork topologies. Some\nof these functionalities are more developed than others, for instance swapping building loads between Spawn and\nRC models (using TEASER) is fleshed out; however, swapping between a first and fifth generation heating system has\nyet to be fully implemented.\n\nThe diagram below is meant to illustrate the future proposed interconnectivity and functionality of the\nGMT project.\n\n.. image:: https://raw.githubusercontent.com/urbanopt/geojson-modelica-translator/develop/docs/images/des-connections.png\n\nThere are various models that exist in the GMT and are described in the subsections below. See the more `comprehensive\ndocumentation on the GMT <https://docs.urbanopt.net/geojson-modelica-translator/>`_ or the `documentation on\nURBANopt SDK  <https://docs.urbanopt.net/>`_.\n\nGeoJSON and System Parameter Files\n++++++++++++++++++++++++++++++++++\n\nThis module manages the connection to the GeoJSON file including any calculations that are needed. Calculations\ncan include distance calculations, number of buildings, number of connections, etc.\n\nThe GeoJSON model should include checks for ensuring the accuracy of the area calculations, non-overlapping building\nareas and coordinates, and various others.\n\nLoad Model Connectors\n+++++++++++++++++++++\n\nThe Model Connectors are libraries that are used to connect between the data that exist in the GeoJSON with a\nmodel-based engine for calculating loads (and potentially energy consumption). Examples includes, TEASER,\nData-Driven Model (DDM), CSV, Spawn, etc.\n\nSimulation Mapper Class / Translator\n++++++++++++++++++++++++++++++++++++\n\nThe Simulation Mapper Class can operate at mulitple levels:\n\n1. The GeoJSON level -- input: geojson, output: geojson+\n2. The Load Model Connection -- input: geojson+, output: multiple files related to building load models (spawn, rom, csv)\n3. The Translation to Modelica -- input: custom format, output: .mo (example inputs: geojson+, system design parameters). The translators are implicit to the load model connectors as each load model requires different paramters to calculate the loads.\n\nIn some cases, the Level 3 case (translation to Modelica) is a blackbox method (e.g. TEASER) which prevents a\nsimulation mapper class from existing at that level.\n',
    'author': 'URBANopt DES Team',
    'author_email': 'nicholas.long@nrel.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.urbanopt.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
