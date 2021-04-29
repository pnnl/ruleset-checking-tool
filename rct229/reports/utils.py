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
                elif result == "MANUAL_CHECK_REQUIRED":
                    summary_dict["number_manual_check_required"] += 1
                elif result.startswith("MISSING_"):
                    summary_dict["number_missing_context"] += 1
                elif result == "NA":
                    summary_dict["number_not_applicable"] += 1
            elif type(result) is list:
                summary_dict["number_evaluations"] -= 1
                _count_results(result)
            else:
                raise ValueError("Unknown result type")

    # Aggregate outcomes
    summary_dict = {
        "number_evaluations": 0,
        "number_passed": 0,
        "number_failed": 0,
        "number_missing_context": 0,
        "number_not_applicable": 0,
        "number_manual_check_required": 0,
    }
    _count_results(outcomes)

    return summary_dict
