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
    for key in calc_vals.keys():
        calc_val = dict()
        calc_val["variable"] = key
        calc_val["value"] = str(calc_vals[key])
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
                    for key in result.keys()
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
