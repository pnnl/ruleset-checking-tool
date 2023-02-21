# Ruleset Checking Tool

Ruleset Checking Tool for ANSI/ASHRAE/IES Standard 90.1-2019 Appendix G

This package provides a reference implementation of a Ruleset Checking Tool (RCT) in support of ASHRAE Standard 229P.  The RCT is not intended to be a normative part of the proposed standard, so use with Std 229P is optional.  This RCT implementation is specific to ANSI/ASHRAE/IES Standard 90.1-2019 Appendix G and does not support any other rulesets.  Final release of this package is dependent upon acceptance and publication of ASHRAE Standard 229P.

## About ASHRAE 229P

ASHRAE Standard 229P is a proposed standard entitled, "Protocols for Evaluating Ruleset Implementation in Building Performance Modeling Software". To learn more about the title/scope/purpose and status of the proposed standard development visit the standards project committee site at [ASHRAE SPC 229](http://spc229.ashraepcs.org/).

## Introduction
The Ruleset Checking Tool (RCT) is a Python package providing a command line tool for evaluating whether baseline and proposed Building Energy Models (BEM) meet the requirements of ANSI/ASHRAE/IES Standard 90.1-2019 Appendix G.  The tool accepts Ruleset Model Report (RMR) files representing the User, Baseline, and Proposed models as inputs, and generates an output report describing the RMR evalaution.

**This is an early alpha version and is highly unstable!**

**This package will change significantly during the next several versions.**

## ASHRAE Standard 229P Workflows
The RCT can be used for two different workflows within ASHRAE Standard 229P.  The first workflow is the *Project Testing Workflow*.  This workflow is used to evaluate RMR triplets for a design project to determine whether a ruleset is applied correctly in a building energy model.  The second workflow is the *Software Testing Workflow*.  This workflow consists of validation and verification software tests that ensure the ruleset is correctly evaluated by a RCT.

### Project Testing Workflow

A project RMR triplet is evaluated by running the *evaluate* command in the RCT.  The User, Baseline, and Proposed RMR file paths are provided as the input arguments to the *evaluate* command.  The output of this command is a JSON report defining the outcome of the rule evaluation on the provided RMR triplet.

`rct229 evaluate user_rmr.json baseline_rmr.json proposed_rmr.json`  

#### RMR Schema
The RCT data model used by the RCT is based on the [RMR schema](https://github.com/open229/ruleset-model-report-schema).  All RMRs must comply with the version of the RMR schema corresponding to the RCT.  The RMR schema files used by the RCT are located within the [rct229/schema](rct229/schema) directory.  

#### Rule Definition Strategy

The definition of each of the individual rules contained with the RCT are documented in [Rule Definition Strategy](docs/_toc.md) (RDS) documents.  The purpose of the RDS is to act as a bridge between the narrative form of the ruleset document and the logical form of a programming language, allowing non-programmers to evaluate how the rules are implemented in the Python programming language.  The RDS documents provide a description of the specific intrepretation of a rule coded into the RCT.  In addition to the description of the each rule, the RDS describes how data from ruleset tables are handled and defines frequently used functions.  

#### Rule Definition
The core functionality of the RCT is the evaluation of logic defining each rule within a ruleset.  The rules are defined within the RCT by a Rule Definition.  The Rule Definition is a Python class that contains the logic necessary to evaluate the rule within the context of the RMR schema.  The Rule Definition files are are located in the [rct229/rules](rct229/rules) directory.

### Software Testing Workflow

The RCT validation and verification software test suite is run using the *<ADD IN FUTURE>* command.  This command composes RMR triplets for each of the Rule Tests and then evaluates each RMR triplet for the corresponding Rule Definition using the same rule engine as the Project Testing Workflow.  A report is provided that details any Rule Tests that provided unexpected results.

#### Rule Tests
The test cases for the Software Testing Workflow are defined in the Rule Test JSON files.  These files are located in the [rct229/ruletest_engine/ruletest_jsons](rct229/ruletest_engine/ruletest_jsons) directory.  The Rule Tests are contained within JSON files that define the related Rule Definition, the RMR transformation to apply, and the expected outcome of the test evaluation.  The JSON files can be generated using an Excel spreadsheet and Python scripts.  This process is described in the [Rule Test JSON Generation Guide](rct229/ruletest_engine/Ruletest_JSON_Generation_Guide.md).

## Developing the RCT

### Commands
The following provides some useful commands as you get started developing the RCT package.

This package is developed using Pipenv to manage packages during the build process.  First, make sure Pipenv is installed on your system using the following commands. Any new dependencies that are added to the package must be included in the Pipfile.  The package is currently being developed for Python 3.7.  This version of Python must be installed on your machine for Pipenv to work properly.

Install `pipenv` using `pip`
`pip install pipenv`

Now tests can be run by first installing dependencies and then running pytest.
1. `pipenv install --dev`
2. `pipenv run pytest`
    - To see a coverage report, use `pipenv run pytest --cov`
    - To have pytest watch for file changes, use `pipenv run ptw`

You can also package with pipenv to test the CLI tool.
1. `pipenv install '-e .'`
2. `pipenv run rct229 -evaluate`

Run with example ASHRAE 90.1 2019 RMDs.
1. `pipenv run rct229 evaluate -rs ashrae9012019 examples\user_rmr.json examples\baseline_rmr.json examples\proposed_rmr.json`


### Developer Notes

#### Branch and Pull Request naming convention:
The branch or PR name should have the form:
```
CODE/INITIALS/DESCRIPTIVE_NAME
```

CODE is one of the following:
- RCT:  for generic, high-level changes to the ruleset checking tool. Examples include updates to README.md, and the schema files
- RDS:  for changes related to the RDS files
- RS:  for changes to the ruleset code (the actual rules)
- RT:  for changes to the rule test engine

INIITIALS refers to the initials of the owner of the branch or PR.

#### Commit procedure:
Before committing changes you should run the following commands from the `ruleset-checking-tool` directory.
1. `pipenv run isort .` to sort imports according to PEP8 https://www.python.org/dev/peps/pep-0008/
2. `pipenv run black .` to otherwise format code according to PEP8
3. `pipenv run pytest --cov` to run all unit tests for functions.
4. `pipenv run rct229 test` to run rule definition tests.
   1. use `-rs ashrae9012019` to run all 90.1 2019 rule definition tests.

#### Mocking functions for pytests:
- For an explanation of how to specify `<module>` in `patch("<module>.<imported_thing>")` see: https://medium.com/@durgaswaroop/writing-better-tests-in-python-with-pytest-mock-part-2-92b828e1453c

#### Profiling:
- To profile a file: `pipenv run pyinstrument --renderer=html path_to_file`
- To profile the RCT command line: `pipenv run pyinstrument --renderer=html rct229/cli.py  evaluate examples/proposed_model.rmd examples/baseline_model.rmd examples/proposed_model.rmd`
- Note: Aborting the run with Ctrl C will cause the profiler to output the profile up to the abort.
- For detailed info on pyinstrument: https://pyinstrument.readthedocs.io/en/latest/home.html

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
