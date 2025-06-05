from rct229.utils.pint_utils import _UNIT_LIST


def test_evaluation_converter(evaluation: dict):
    output_evaluation = {}
    output_evaluation["data_group_id"] = evaluation["id"]
    output_evaluation["message"] = (
        evaluation["message"] if evaluation.get("message") else ""
    )
    output_evaluation["evaluation_outcome"] = (
        evaluation["result"] if evaluation.get("result") else "FAILED"
    )
    output_evaluation["calculated_values"] = (
        calc_vals_converter(evaluation["calculated_values"])
        if evaluation.get("calculated_values")
        else []
    )
    return output_evaluation


def calc_vals_converter(calc_vals):
    """
    Utility function that converts a calc_vals raw output
    to a json compatible dictionary.

    Parameters
    ----------
    calc_vals: dict raw output calc_vals value that contains quantity object.

    Returns
    -------

    """
    calc_vals_dict = []
    for key in calc_vals:
        calc_val = {}
        calc_val["variable"] = key
        value = calc_vals[key]
        if isinstance(value, str):
            numerical_value = value.split(" ", 1)
            if len(numerical_value) > 1 and numerical_value[1] in _UNIT_LIST:
                calc_val["value"] = numerical_value[0]
                calc_val["unit"] = numerical_value[1]
            elif len(numerical_value) > 1 and numerical_value[1] == "R":
                calc_val["value"] = numerical_value[0]
                calc_val["unit"] = "delta F"
            else:
                calc_val["value"] = value
        else:
            calc_val["value"] = str(value)
        calc_vals_dict.append(calc_val)
    return calc_vals_dict


def aggregate_outcomes(outcomes):
    def _count_results(outcomes):
        for outcome in outcomes:
            summary_dict["number_evaluations"] += 1
            result = outcome["result"]
            if type(result) is str:
                if result == "FAILED":
                    summary_dict["number_failed"] += 1
                elif result == "PASSED":
                    summary_dict["number_passed"] += 1
                elif result == "UNDETERMINED":
                    summary_dict["number_undetermined"] += 1
                elif result == "NOT_APPLICABLE":
                    summary_dict["number_not_applicable"] += 1
                elif result == "INVALID_BASELINE_CONTEXT":
                    summary_dict["number_invalid_context"] += 1
            elif type(result) is list:
                summary_dict["number_evaluations"] -= 1
                _count_results(result)
            elif type(result) is dict and any(
                [
                    key.startswith("INVALID_") and key.endswith("_CONTEXT")
                    for key in result
                ]
            ):
                summary_dict["number_invalid_context"] += 1

            else:
                print("result:", result, " result type:", type(result))
                raise ValueError("Unknown result type")

    # Aggregate outcomes
    summary_dict = {
        "number_evaluations": 0,
        "number_passed": 0,
        "number_failed": 0,
        "number_invalid_context": 0,
        "number_undetermined": 0,
        "number_not_applicable": 0,
    }
    _count_results(outcomes)

    return summary_dict
