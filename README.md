<table>
   <tr>
      <td>Latest Release</td>
      <td>
         <a href="https://pypi.org/project/ruleset-checking-tool/"/>
         <img src="https://badge.fury.io/py/ruleset-checking-tool.svg"/>
      </td>
   </tr>
   <tr>
      <td>License</td>
      <td>
         <a href="https://github.com/pnnl/ruleset-checking-tool/blob/master/LICENSE"/>
         <img src="https://img.shields.io/badge/License-MIT-yellow.svg"/>
      </td>
   </tr>
   <tr>
      <td>Test</td>
      <td>
         <img src="https://github.com/pnnl/ruleset-checking-tool/actions/workflows/python-app.yml/badge.svg">
      </td>
   </tr>
</table>

# Ruleset Checking Tool

Ruleset Checking Tool for ANSI/ASHRAE/IES Standard 90.1-2019 Appendix G

This package provides a reference implementation of a Ruleset Checking Tool (RCT) in support of ASHRAE Standard 229P.  The RCT is not intended to be a normative part of the proposed standard, so use with Std 229P is optional.  This RCT implementation is specific to ANSI/ASHRAE/IES Standard 90.1-2019 Appendix G and does not support any other rulesets.  Final release of this package is dependent upon acceptance and publication of ASHRAE Standard 229P.

## Install it from PyPI

```bash
pip install ruleset-checking-tool
```

## Usage

```py
from rct229.web_application import run_project_evaluation as run
from rct229.utils.file import deserialize_rpd_file

user_rpd_path = "../examples/chicago_demo/user_model.json"
proposed_rpd_path = "../examples/chicago_demo/proposed_model.json"
baseline_rpd_path = "../examples/chicago_demo/baseline_model.json"

user_rpd = None
proposed_rpd = None
baseline_rpd = None
try:
    user_rpd = deserialize_rpd_file(user_rpd_path)
except:
    print(f"{user_rpd_path} is not a valid JSON file")

try:
    proposed_rpd = deserialize_rpd_file(proposed_rpd_path)
except:
    print(f"{proposed_rpd_path} is not a valid JSON file")
    
try:
    baseline_rpd = deserialize_rpd_file(baseline_rpd_path)
except:
    print(f"{baseline_rpd_path} is not a valid JSON file")


run([user_rpd, proposed_rpd, baseline_rpd], "ashrae9012019", ["ASHRAE9012019DetailReport"], saving_dir="./")
```

You can also call evaluation functions from its command line tool. Example is given below:

```bash
rct229 evaluate -rs ashrae9012019 -f examples\chicago_demo\baseline_model.json -f examples\chicago_demo\proposed_model.json -f examples\chicago_demo\user_model.json -r ASHRAE9012019DetailReport
```

## About ASHRAE 229P

ASHRAE Standard 229P is a proposed standard entitled, "Protocols for Evaluating Ruleset Implementation in Building Performance Modeling Software". To learn more about the title/scope/purpose and status of the proposed standard development visit the standards project committee site at [ASHRAE SPC 229](https://tpc.ashrae.org/?cmtKey=9ffa4db6-eebe-4418-a8c4-d0c220603735).

## Introduction
The Ruleset Checking Tool (RCT) is a Python package providing a command line tool for evaluating whether the Building Energy Models (BEM) meet the requirements of a ruleset. Current available ruleset includes ANSI/ASHRAE/IES Standard 90.1-2019 Appendix G (`ashrae9012019`).  The tool accepts Ruleset Project Description (RPD) files as inputs, and generates output reports describing the RPD evaluation.


## ASHRAE Standard 229P Workflows
The RCT can be used for two different workflows within ASHRAE Standard 229P.  The first workflow is the *Project Testing Workflow*.  This workflow is used to evaluate RMD triplets for a design project to determine whether a ruleset is applied correctly in a building energy model.  The second workflow is the *Software Testing Workflow*.  This workflow consists of validation and verification software tests that ensure the ruleset is correctly evaluated by a RCT.

### Project Testing Workflow
A project RPD is evaluated by running the *evaluate* command in the RCT.  RPD file paths are provided as the input arguments to the *evaluate* command.  The output of this command is a JSON report defining the outcome of the rule evaluation.

`rct229 evaluate -f user_rmr.json -f baseline_rmr.json -f proposed_rmr.json -rs ashrae9012019`

#### RPD Schema
The RCT data model used by the RCT is based on the [RPD schema](https://github.com/open229/ruleset-model-report-schema).  All RPDS must comply with the version of the Ruleset evaluation schema (RES) corresponding to the RCT.  The RES files used by the RCT are located within the [rct229/schema](rct229/schema) directory.  

#### Rule Definition Strategy

The definition of each of the individual rules contained with the RCT are documented in [Rule Definition Strategy](docs/_toc.md) (RDS) documents.  The purpose of the RDS is to act as a bridge between the narrative form of the ruleset document and the logical form of a programming language, allowing non-programmers to evaluate how the rules are implemented in the Python programming language.  The RDS documents provide a description of the specific interpretation of a rule coded into the RCT.  In addition to the description of each rule, the RDS describes how data from ruleset tables are handled and defines frequently used functions.  

#### Rule Definition

The core functionality of the RCT is the evaluation of logic defining each rule within a ruleset.  The rules are defined within the RCT by a Rule Definition.  The Rule Definition is a Python class that contains the logic necessary to evaluate the rule within the context of the RES.  The Rule Definition files are located in the [rct229/rules](rct229/rules) directory.

### Software Testing Workflow

The RCT validation and verification software test suite is run using the `test` command.  This command composes a set of RPDs for each of the Rule Tests and then evaluates each RPD set for the corresponding Rule Definition using the same rule engine as the Project Testing Workflow.  A report is provided that details any Rule Tests that provided unexpected results.

#### Rule Tests
The test cases for the Software Testing Workflow are defined in the Rule Test JSON files.  These files are located in the [rct229/ruletest_engine/ruletest_jsons](rct229/ruletest_engine/ruletest_jsons) directory.  The Rule Tests are contained within JSON files that define the related Rule Definition, the RPD transformation to apply, and the expected outcome of the test evaluation.  The JSON files can be generated using an Excel spreadsheet and Python scripts.  This process is described in the [Rule Test JSON Generation Guide](rct229/ruletest_engine/Ruletest_JSON_Generation_Guide.md).

## Developing the RCT

### Commands
The following provides some useful commands as you get started developing the RCT package.

This package is developed using Poetry to manage packages during the build process.  First, follow the instruction from [poetry](https://python-poetry.org/docs/) to install the package.
Any new dependencies that are added to the package must be included in the pyproject.toml. The package is currently being developed for Python 3.10. This version of Python must be installed on your machine for Poetry to work properly.

Now tests can be run by first installing dependencies and then running pytest.
1. `poetry install`
2. `poetry run pytest`
    - To see a coverage report, use `poetry run pytest --cov`
    - To have pytest watch for file changes, use `poetry run ptw`

You can also package with poetry to test the CLI tool.
2. `poetry run rct229 test`

Run with example ASHRAE 90.1 2019 RPDs.
1. `poetry run rct229 evaluate -rs ashrae9012019 -f examples\chicago_demo\baseline_model.json -f examples\chicago_demo\proposed_model.json -f examples\chicago_demo\user_model.json -r ASHRAE9012019_DETAIL`


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
1. `poetry run isort .` to sort imports according to PEP8 https://www.python.org/dev/peps/pep-0008/
2. `poetry run black .` to otherwise format code according to PEP8
3. `poetry run pytest --cov` to run all unit tests for functions.
4. `poetry run rct229 test` to run rule definition tests.
   1. use `-rs ashrae9012019` to run all 90.1 2019 rule definition tests.

#### Mocking functions for pytests:
- For an explanation of how to specify `<module>` in `patch("<module>.<imported_thing>")` see: https://medium.com/@durgaswaroop/writing-better-tests-in-python-with-pytest-mock-part-2-92b828e1453c

#### Profiling:
- To profile a file: `poetry run pyinstrument --renderer=html path_to_file`
- To profile the RCT command line: `poetry run pyinstrument --renderer=html rct229/cli.py  evaluate examples/proposed_model.rmd examples/baseline_model.rmd examples/proposed_model.rmd`
- Note: Aborting the run with Ctrl C will cause the profiler to output the profile up to the abort.
- For detailed info on pyinstrument: https://pyinstrument.readthedocs.io/en/latest/home.html

#### Rule numbering procedure:
- For adding a new rule:
  1. Generate a unique rule ID for the new rule using the `generate_unique_rule_id()` function in the `rct229/utils/generate_unique_rule_id.py` file.
  2. Add a new item to the `rules_dict` in the rulset's `rct229/rulesets/<RULESET>/__init__.py` file with the unique rule ID and desired rule section and number.
  3. Create the new rule module in the ruleset directory following the typical procedure, but using the unique rule ID as the rule's class name.
  ```python
        class PRM9012019Rule86h31(RuleDefinitionBase):
  ```
  
- For renumbering a rule to remain in the same section:
  1. Adjust the `rules_dict` in the rulset's `rct229/rulesets/<RULESET>/__init__.py` file.
  2. Run the `renumber_rules()` function in the `rct229/rulesets/ruleset_functions.py` file.
  3. Update the rule number in the RDS file.

- For renumbering a rule to move to a different section:
  1. Adjust the `rules_dict` in the rulset's `rct229/rulesets/<RULESET>/__init__.py` file.
  2. Transfer the Rule and TCD info between the affected TCD Excel Spreadsheets
  3. Regenerate the affected Master Test JSON files
  4. Run the `renumber_rules()` function in the `rct229/rulesets/ruleset_functions.py` file.
  5. Update the rule number in the RDS file.
  >  Replace `<RULESET>` with the appropriate ruleset name (e.g., `ashrae9012019`).

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
