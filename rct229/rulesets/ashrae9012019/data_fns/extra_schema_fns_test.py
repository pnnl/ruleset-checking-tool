from rct229.rulesets.ashrae9012019.data_fns.extra_schema_fns import compare_proposed_with_user, EXTRA_SCHEMA
from rct229.utils.json_utils import load_json

proposed = load_json("C:\\Users\\xuwe123\\Documents\\GitHub\\ruleset-checking-tool\\examples\\chicago_demo\\proposed_model.json")
user = load_json("C:\\Users\\xuwe123\\Documents\\GitHub\\ruleset-checking-tool\\examples\\chicago_demo\\user_model.json")
error_msg_list = []

outcome = compare_proposed_with_user(proposed, user, error_msg_list, "$", EXTRA_SCHEMA["RulesetProjectDescription"]["Data Elements"], True)
print(error_msg_list)
print(outcome)
