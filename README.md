# OLAF: an Open Land-use Allocation Framework

![](https://frenchbroadrivermpo.org/wp-content/uploads/2018/06/cropped-FrenchBroadRiverMPO-Los-1.jpg)

This is the FBRMPO version of a Python 3 script designed to serve as a code pattern for building simple and flexible microsimulation-based land use allocation models.  Such models are generally used to predict the spatial distribution of forecasted control totals of various quantities of development activity (such as housing units or square feet of commercial real estate).  Urban planners and transportation engineers use the predictions to run travel forecasting models that estimate traffic on roads and ridership on transit lines; those numbers are used to help prioritize which proposed transportation projects are built and/or to measure the performance of alternative networks with respect to key indicators such as emissions.

## Design Philosophy
There are a wide range of land use models to choose from which are based upon specific theories of urban development promulgated by various economists, planners, and other thinkers; these are implemented with highly complex code that is tightly bound to the theory upon which they are based.  This library seeks to be as theory-agnostic as possible; the only theoretical construct it presupposes is that of multinomial logit location choice, as described by Nobel award-winning economist Daniel McFadden in his seminal 1978 [paper](https://www.semanticscholar.org/paper/Modelling-the-Choice-of-Residential-Location-McFadden/55a63c2a72325a86de9a17814fb6243c132ac19a) "Modeling the Choice of Residential Location".  

In the FBRMPO application, the location-choosing agent is taken to be a housing or commercial real estate developer.  They are assumed to operate across multiple available product types; thus, in addition to choosing a location, they jointly choose which type of land use they wish to develop at that location.  The options available are constrained by build-out capacity assumptions which may vary by forecast scenario.

While both parcel-based and grid-based geographic analysis units were considered for use in this model, ultimately we settled on 2020-vintage U.S. Census Blocks.  This makes our model more compatible with other land use modeling work done at the Land of Sky Regional Council, and also builds upon NCDOT's work to redefine Transportation Analysis Zones as aggregations of 2020-vintage U.S. Census Blocks.  

## User Configuration
A single [YAML](https://yaml.org/)-format configuration file is used to specify the input data (in CSV format).  Examples of the input data and config file are provided.  

## Dependencies
Aside from Python 3, the script requires NumPy, Pandas and PyYAML.  These can be installed using the command:

`pip3 install pandas numpy pyyaml`

It is good practice to create a virtual environment before doing this, e.g.:

`python3 -m venv env && source env/bin/activate`

## Disclaimer
This script is published under an MIT license.  It makes use of Pandas functions which perform arbitrary executions on a dataframe and therefore could possibly present a security vulnerability.  The author assumes no liability whatsoever for any damages incurred by users.
