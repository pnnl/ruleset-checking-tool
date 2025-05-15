# Ruletest JSON Generation Guide

## Ruletest JSON Overview and Workflow

This guide will present the process of testing the Test Case Descriptions (TCD) from the TCD spreadsheet against the Ruleset Checking Tool engine. This guide takes readers through the following pipeline for interpretting TCDs, generating their test case RMD JSON, and testing it against the rule test engine. This guide documents the following:

1) Interpretting Test Case Description (TCD) Spreadsheets
2) Understanding the Ruletest JSON Structure
3) The Ruletest JSON Generation Spreadsheet
4) Generating a Ruletest JSON
5) Testing Ruletest JSON Against the ASHRE229.schema.json
6) Testing a Ruletest JSON Against the RCT Engine


## Interpretting Test Case Description (TCD) Spreadsheets 

Test Case Description (TCD) spreadsheets describe scenarios used to test the implementation of Rules. These TCDs exercise the implementation of Rules to ensure they pass or fail as expected under various conditions. The fields required to implement a successful Ruletest JSON are as follows:

* Appendix G Section ID
* Rule ID
* Test ID
* Rule Description
* Expected Test Outcome (pass, fail, non-applicable, undetermined)
* Standard Information:
    * Rule ID
    * Ruleset Reference
    * Rule Description
    * Applicable RMD (e.g., user, baseline, proposed)
    * What the applicable RMD is being compared with (e.g., another RMD, an expected value from a table)
    * Rule dependencies
    * Whether or not a rule is a **mandatory** rule
* All expected attributes for each User, Proposed, and Baseline RMDs

The next section will take a look at an easy example from the *Transformer TCD 201030.xlsx* excel file and describe how to enter these fields into a **Rule Test JSON file**. The Ruleset Checking Tool's (RCT) test engine ingests these JSON files to evaluate the implentation of various rules.

### Understanding the Ruletest JSON Structure

#### Test case decription overview in the JSON

 The first description in the *Transformer TCD 201030.xlsx* excel file is for **Section 15, Rule 1, Test A**. The spreadsheet provides a lot of information, but let's focus only a few of the fields to start:


| App G Section ID | Rule ID | Test ID | Rule Description | Expected Test Outcome |
| ------ | ------ | ------ | ------ | ------ |
| 15 | 1 | a | Number of transformers modeled in User RMD and Baseline RMD are the same | Pass |

These fields provide an overview of the Rule Test and get placed at the beginning of the Rule Test JSON. Here's how they would appear in a Rule Test JSON:

```json
{
    "rule-15-1a": {
        "Section": 15,
        "Rule": 1,
        "Test": "a",
        "description": "Number of transformers modeled in User RMD and Baseline RMD are the same",
        "expected_rule_outcome": "pass"
    }
}
```

These are the important things to note:

* Rule Test JSONs are structured as a series of rule tests distinguished by their section, rule, and test ID combination. The format is `rule-{APPENDIX_G_SECTION_ID}-{RULE_ID}{TEST_ID}`. Our our example above this would be `rule-15-1a` 
* The top level of each rule test requires the `Section`, `Rule`, `Test`, `description`, and `expected_rule_outcome`.
    * NOTE: `expected_rule_outcome` - this field is limited to only 'pass' or 'fail'

#### ASHRAE 229 RMD JSONs in the Rule Test JSON

In the last section we established the overview of the rule test but next let's take a look at writing RMDs into the Rule Test JSON. These RMDs are what get ingested by the RCT test engine and evaluate the capability of the engine's Rules. Going back to the TCD spreadsheet, the fields that describe the User, Proposed, and Baseline RMDs are found in the following columns:

* Attribute Names
* User RMD Value(s)	
* Proposed RMD Value(s)	
* Baseline RMD Value(s)

Here are those fields for `rule-15-1a`. 

| Attribute Values | User RMD Value(s) | Proposed RMD Value(s) | Baseline RMD Value(s)|
| ------ | ------ | ------ | ------ | 
| xfrm:id|Transformer 1| |Transformer 1|
| xfrm:id|Transformer 2| |Transformer 2|
| xfrm:id|Transformer 3| |Transformer 3|

This is where we need to do a bit of interpretation. Based on the rule description and looking through the [ASHRAE229.schema.json](https://github.com/pnnl/ruleset-checking-tool/blob/develop/rct229/schema/ASHRAE229.schema.json) file, we can infer the author is describing three transformers with unique IDs in both the User and Baseline RMD. Using the JSON schema, we can infer this is the JSON we want to write for both the baseline and user RMDs:

```json
 {
    "transformers": [
        {
            "id": "Transformer_1"
        },
        {
            "id": "Transformer_2"
        },
        {
            "id": " Transformer_3"
        }
    ]
```

The next step would be to write this interpretation into a Test JSON. The user, proposed, and baseline RMDs are all injected inside an element called `rmr_transformations`.  This element has 3 keys-- `user`, `proposed`, and `baseline`. For the example above, the completed rule test JSON would appear as follows:

```json
{
 "rule-15-1-a": {
        "Section": 15,
        "Rule": 1,
        "Test": "a",
        "test_description": "Number of transformers modeled in User RMD and Baseline RMR are the same",
        "expected_rule_outcome": "pass",
        "standard": {
            "rule_id": "15-1",
            "ruleset_reference": "-",
            "rule_description": "Number of transformers modeled in User RMR and Baseline RMR are the same",
            "applicable_rmr": "Baseline RMR",
            "rule_assertion": "=",
            "comparison_value": "User RMR",
            "rule_dependency": "none",
            "mandatory_rule": "Yes",
            "schema_version": "0.0.23"
        },
        "rmr_transformations": {
            "user": {
                "id": "ashrae229",
                "ruleset_model_descriptions": [
                    {
                        "id": "RMD 1",
                        "transformers": [
                            {
                                "id": "Transformer_1"
                            },
                            {
                                "id": "Transformer_2"
                            },
                            {
                                "id": "Transformer_3"
                            }
                        ]
                    }
                ]
            },
            "baseline": {
                "id": "ashrae229",
                "ruleset_model_descriptions": [
                    {
                        "id": "RMD 1",
                        "transformers": [
                            {
                                "id": "Transformer_1"
                            },
                            {
                                "id": "Transformer_2"
                            },
                            {
                                "id": "Transformer_3"
                            }
                        ]
                    }
                ]
            }
        }
    }
}
```

Now the example Ruletest JSON we wrote early includes both the `user` and `baseline` elements inside the `rmr_transformations` element as required by the RCT.

## The Ruletest JSON Generation Spreadsheet

Writing out these test JSONs by hand would be tedious and require long refactoring for each schema update. The **Ruletest JSON Spreadsheet**s found in this repository shorten the process of generating and re-generating JSONs. 

Examples of these spreadsheets can be found [here](https://github.com/pnnl/ruleset-checking-tool/tree/develop/rct229/ruletest_engine/ruletest_jsons/ruletest_spreadsheets)



### Ruletest JSON Generation Guide

#### Overview 

This guide will describe the process of generating test JSONs used to test Rules in the Ruleset Checking Tool (RCT). JSON files are generated by spreadsheets developed for each section of the Appendix G's test case descriptions (TCDS) (how should we refer to these?). Each RCT Rule has multiple test case descriptions to exercise different input conditions and tests against expected outcomes. 

These spreadsheets can be found at the `ruletest_engine\ruletest_jsons\ruletest_spreadsheets` directory and generate JSONS using the `ruletest_engine\ruletest_jsons\scripts\excel_to_test_json.py` Python script.

#### Spreadsheet Structure: Columns

Each ruletest spreadsheet is separated into three notable column sections-- 

1. **Keys**: Keys dictate the hierarchy or nested strucutre of the resulting ruletest JSON
2. **Units**: These columns define both the unit type (e.g., area, electric power) and TCD unit for a given row (e.g., ft2, Watts). These are important for translating between units required by the RMD schema and units used by the TCDs and 90.1.
3. **Rule Tests**: The remainder of the columns are each dedicated to rule tests.

keys used to describe JSON paths and the values assigned to them. Both keys and their corresponding JSON path values have some intricacies described here.

##### Keys and Values

Each ruletest spreadsheet utilizes keys to describe the JSON path for a given value. This is best described through example. Let's take a look at an example from the envelope tests. Consider the following in the spreadsheet:

| key1 | key2 | key3 | key4 | rule-5-7a |
| ------ | ------ | ------ | ------ | ------ |
| rmr_transformations | user | buildings | is_new | true |

A key column is specified with the string "*key*" followed by a number. The **four keys** here describe the JSON path. These keys include the following:

- rmr_transformations
- user
- building
- is_new

Their corresponding value for the header `rule-5-7a` is `true`. When ran through the Python script `excel_to_json.py` (see the *Generating a Ruletest JSON* section for details), the resulting JSON would appear as follows:

``` json
{
    "rule-5-7a": {
            "rmr_transformations": {
                "user": {
                    "buildings": {
                        "is_new": "true"
                        }
                    }
                }
            }
}
```

##### Units

Values in Ruletests often have associate with them. Users should specify the units for any quantity in a given ruletest. There are two unit columns (typically follow the *key* columns) in the RCT Ruletest Spreadsheets. NOTE: these columns can and should be left blank if the row does not specify a quantity.

1. **Unit types** - Categorize the value being specify as a string. For instance, floor area could be specifed as *area*. This column is titled "*unit_type*". A full list of existing enumerations can be found [here](https://github.com/pnnl/ruleset-checking-tool/tree/develop/rct229/schema/resources/unit_conventions.json "List of Enumerations").
2. **Units** - The dimensional units describing the value quantity for a given ruletest described in the TCD. Typically these are in IP units. For instance, floor area might be *ft2*. This column is titled "*units*"

Below are some examples:

| unit_type | units |
| ------ | ------ | 
| transformer_capacity | V-A |
| electric_power | W |
| power_density | W/ft2 |
| area | ft2 |

### Spreadsheet Structure: Rows

Ruletest JSON Spreadsheets are split into a few distinct sections:

- **Unique Test ID** -- these three rows specify the Section, Rule, and Test ID for a given ruletest. These are conventionally the top rows in the Ruletest JSON Spreadsheet
- **General Info** -- These rows specify none RMD specific parameters for a given ruletest. This includes information like a description to the test and whether or not it's expected to pass or fail. 
    - *description* - This row describes what's being tested in a given ruletest
    - *expected_rule_outcome* - This row specifies whether a given ruletest is expected to `pass`, `fail`, `not_applicable` or `undetermined`
- **Standard Information** -- This information in this section communicates corresponding ASHRAE Standard 229 information about the test in question
    - *rule_id* - unique combination of a the standard's Section and Rule (e.g., `23-7`)
    - *ruleset_reference* - A reference to where the this rule's information can be found in the standard (e.g., G3.1.3.12)
    - *rule_description* - Description of the standard's rule (e.g., `For baseline systems 6 and 8,  supply air temperature setpoint shall be constant at the design condition`)
    - *applicable_rmr* - the RMD being tested against either another RMD or expected value from a table or standard (`User`, `Baseline`, `Proposed`)
    - *rule_assertion* - an operator describing how the applicable RMD is being compared against the `comparison_value` (e.g., `=`, `>`)
    - *comparison_value* - The value or RMD being compared against the `applicable` RMD (`User`, `Baseline`, `Proposed`)
    - *rule_dependency* - Communicates if another Rule or condition must be met for this Rule to apply
    - *mandatory_rule* - Boolean describing if this rule is a mandatory or "primary" rule
    - *schema_version* - Used to document what version of the ASHRAE 229 JSON schema is being used in a given Ruletest JSON (e.g., `0.0.23`)
- **Template** -- Many ruletest require multiple RMDs with nearly identical JSON structures. This section of rows serves to do define a "template"-- a set of values which are the same for all RMDs in a given ruletest. These rules have their first key (`key1`) equal to *rmr_template* 
    - *user, proposed, baseline* - These three rows, if specified as `true`, will create a copy of the RMD template for the respective RMD (e.g., if the `rmr_template/user` row is set to `true`, a user RMD is generated with the values populated in the `rmr_template/json_template` rows)
    - *rmr_template/json_template* - These rows specify the RMD values used in the RMD template (e.g., `rmr_template/json_template/buildings[0]/id` would specify a building ID for an RMD template)
- **RMD Transformations** -- These rows specify the differences between the three RMD triplets (i.e., user, proposed, and baseline). This is where a user introduces values not specified in the **Template** section. For instance, a `user` and `baseline` RMD might be identical in everything except their transformer's effiency. Their key values would be `rmr_transformations/user/transformers[0]/efficiency` and `rmr_transformations/baseline/transformers[0]/efficiency`.



#### The JSON_PATH Keyword

The example above works well when the JSON path one tries to set is not too long. As the RCT schema evolves, fields can become further and further buried down with very long JSON paths. For these cases, it's often helpful to utilize shorthand expressions using the `JSON_PATH` keyword. You can find `JSON_PATH` shorthand in keys throughout the test document. Let's take a look at an example in the envelope test sheet:

Consider the following-- you want to describe a space's floor area in the user RMD inside the `rmr_transformations` section of the test JSON. Using the conventional approach, this would require laying out a very long JSON path:
| key1 | key2 | key3 | key4 | key5 | key6 | key7 |  key8 | rule-5-7a |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| rmr_transformations | user | buildings | building_segments | thermal_blocks | zones | spaces | floor area | 1000 |

Note how the conventional approach requires a great deal of columns to express. By utilizing a `JSON_PATH`, things become substantially tidier. Consider the following:

| key1 | key2 | key3 | key4 | rule-5-7a |
| ------ | ------ | ------ | ------ | ------ |
| rmr_transformations | user | JSON_PATH: spaces[0] | floor_area | 1000 |

The `JSON_PATH` for `spaces` shortens this down substantially. These shorthand enumerations are described in the `\ruletest_engine\ruletest_jsons\scripts\resources\json_pointer_enumerations.json` JSON file. You'll note that the `spaces` path maps to *'buildings[0]/building_segments[0]/thermal_blocks[0]/zones[0]/spaces'*. The square brackets are described in the following section.

#### Specifying Arrays/Lists: Using Square Brackets

Many elements in the `ASHRAE229.schema.json` require embedding many arrays of dictionaries into each other. The JSON definitions prior to this section work well for fairly "flat" dictionaries but not well for lists of them. 

Let's consider how we'd set IDs for Zones within two distinct ThermalBlocks. The JSON we hope to achieve looks as follows:

``` json
{
    "rule-5-7a": {
    	"rmr_transformations": {
    		"user": {
    			"buildings": [
    				{
    					"building_segments": [
    						{
    							"thermal_blocks": [
    								{
    									"zones": [
    										{
    											"id": "Zone 1"
    										}
    									]
    								},
    								{
    									"zones": [
    										{
    											"id": "Zone 2"
    										}
    									]
    								}
    							]
    						}
    					]
    				}
    			]
    		}
    	}
    }
}
```

Note how there are two separate thermal blocks, each containing their own zone. This is a good example of when you'd need to specify specific array indices. You do this using square brackets:

| key1 | key2 | key3 | key4 | rule-5-7a |
| ------ | ------ | ------ | ------ | ------ |
| rmr_transformations | user | JSON_PATH: zones[0] | id | Zone 1 |
| rmr_transformations | user | JSON_PATH: zones[1] | id | Zone 2 |

Breaking down the interesting parts-- 

* `JSON_PATH:zones` - shorthand for *"buildings[0]/building_segments[0]/thermal_blocks[0]/zones"* Note how even the shorthand has many list indices appended. Those elements are type "array" according to `ASHRAE229.schema.json`
* `[0]` and `[1]` appended after the `JSON_PATH:zones` specify the 1st and 2nd element in the `zones` array/list.
* Lastly, `id` specifies the zone ID for each Zone in `zones`. 





### Generating a Master Ruletest JSON

Users can generate Ruletest JSONs using the Python script `excel_to_json.py` located in the `rct229/ruletest_engine/ruletest_jsons/scripts` directory. Running the script requires setting three parameters:

* **spreadsheet_name** = The name of the Ruletest JSON Generation Spreadsheet describing the Ruletest JSON
    * Example: *'envelope_tests_draft.xlsx'* 
* **json_name** = The name of the resulting Ruletest JSON file.
    * Example: *'envelope_tests.json'* 
* **sheet_name** = The name of the Excel sheet/tab containing key/value definitions
    * Example: *'TCDs'* 

These are all found at the very top of the script under the `USER INPUTS` section. Once defined, running the `excel_to_json.py` file will generate what we call a "**master**" Ruletest JSON. A master Ruletest JSON contains *all* the Ruletests specified in a single spreadsheet. Typically, spreadsheets are defined by their category (e.g., *lighting_tcd_master.xlsx*). This is valuable for testing all of them at once against the ASHRAE229 JSON schema.

### Testing Ruletest JSON Against the ASHRAE229.schema.json

Ruletest JSONs are only valuable for testing if they following the [ASHRAE229.schema.json](https://github.com/pnnl/ruleset-checking-tool/blob/develop/rct229/schema/ASHRAE229.schema.json) schema definition. It's valuable to test any generated Ruletest JSON against this schema to ensure compatibility with the RCT engine. 

The script to test a Ruletest JSON against the `ASHRAE229.schema.json` is located in the `rct229/ruletest_engine/ruletest_jsons/scripts` directory and is called `run_json_schema_validation.py`. Running this script is simple. Simply set the `test_json_name` input at the top of the script to match the ruletest JSON you want to test. That ruletest JSON should be located in the `rct229\ruletest_engine\ruletest_jsons` directory. Once set, simply run the script. The results of the test for validation against the schema will be printed in the console.

### Disaggregating a Master Ruletest JSON

While master JSON (see the *Generating a Master Ruletest JSON* section for definition of a master JSON) is valuable for testing a whole section against the ASHRAE229 JSON schema, it's a lot easier to test against single Section + Rule combinations. The [disaggregate_master_test_json script](https://github.com/pnnl/ruleset-checking-tool/blob/develop/rct229/ruletest_engine/ruletest_jsons/scripts/disaggregate_master_test_json.py) will take the JSON specified in the `json_name` parameter and split it out into section + rule files (e.g., `rule_6_1.json`) in `rct229\ruletest_engine\ruletest_jsons\[SECTION]`directories. Simply specify the master ruletest JSON you want to disaggregate in the python [script](https://github.com/pnnl/ruleset-checking-tool/blob/develop/rct229/ruletest_engine/ruletest_jsons/scripts/disaggregate_master_test_json.py#L6)'s `json_name` and run it. 

*NOTE*: master ruletest JSONs must be placed in the `rct229\ruletest_engine\ruletest_jsons` directory. 

### Testing a Ruletest JSON Against the RCT Engine 

Testing a schema validated Ruletest JSON against the RCT is fairly simple. This is done by executing the `run_section_tests` function in the `ruletest_engine.py` script. This script is found in the `rct229/ruletest_engine` directory. The `run_section_tests` script only requires one input-- the name of the Ruletest JSON to run. An example of using this script can be found in the `run_transformer_tests` function. 

