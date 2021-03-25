# Ruleset Checking Tool

Ruleset Checking Tool for ANSI/ASHRAE/IES Standard 90.1-2019 Appendix G

This package provides a reference implementation of a Ruleset Checking Tool (RCT) in support of ASHRAE Standard 229P.  The RCT is not intended to be a normative part of the proposed standard, so use with Std 229P is optional.  This RCT implementation is specific to ANSI/ASHRAE/IES Standard 90.1-2019 Appendix G and does not support any other rulesets.  Final release of this package is dependent upon acceptance and publication of ASHRAE Standard 229P.

## About ASHRAE 229P

ASHRAE Standard 229P is a proposed standard entitled, "Protocols for Evaluating Ruleset Implementation in Building Performance Modeling Software". To learn more about the title/scope/purpose and status of the proposed standard development visit the standards project committee site at [ASHRAE SPC 229](http://spc229.ashraepcs.org/).

## Introduction
The Ruleset Checking Tool is a Python package providing a command line tool for evaluating whether baseline and proposed Building Energy Models (BEM) meet the requirements of ANSI/ASHRAE/IES Standard 90.1-2019 Appendix G.  The tool accepts Ruleset Model Report (RMR) files representing the User, Baseline, and Proposed models as inputs, and generates an output report describing the RMR evalaution.

**This is an early alpha version and is highly unstable!**

**This package will change significantly during the next several versions.**

## Commands
The following provides some useful commands as you get started using the package.

This package is developed using Pipenv to manage packages during the build process.  First, make sure Pipenv is installed on your system using the following commands. Any new dependencies that are added to the package must be included in the Pipfile.

Install `pipenv` using `pip`
`pip install pipenv`

Now tests can be run by first installing dependencies and then running pytest.
1. `pipenv install --dev`
2. `pipenv run pytest`

You can also package with pipenv to test the CLI tool.
1. `pipenv install '-e .'`
2. `pipenv run rct229`

Run with example RMRs
1. `pipenv run rct229 evaluate examples\user_rmr.json examples\baseline_rmr.json examples\proposed_rmr.json`

## Developer Best Practices

#### Unit Testing
- Pytest is used for unit testing: https://docs.pytest.org/en/stable/contents.html
- A test file should have the same name as the corresponding code file with "_test" appended before the extension.
- Keep the test file in the same directory as the code file.
- The above two bullets act to keep the code file and the test file next to each other in the directory listing.
- Test function names are verbose to be descriptive and should follow the pattern `test__function_name__case_description()`.
- To run all tests, execute the command `pipenv run pytest` from the project root folder.


## Disclaimer Notice      
This material was prepared as an account of work sponsored by an agency of the United States Government.  Neither the United States Government nor the United States Department of Energy, nor Battelle, nor any of their employees, nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe privately owned rights.
Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof, or Battelle Memorial Institute. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

<div align="center">
<pre style="align-text:center">
PACIFIC NORTHWEST NATIONAL LABORATORY
operated by
BATTELLE
for the
UNITED STATES DEPARTMENT OF ENERGY
under Contract DE-AC05-76RL01830
</pre>
</div>
