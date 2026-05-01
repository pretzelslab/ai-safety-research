# hitl.py
# Human-in-the-loop gate. Called when a step is classified ROGUE.
# Prints the flagged step details and prompts for approve / reject.
# Returns "approved" or "rejected" so the caller can decide what to do next.


def hitl_check(step_result: dict, auto_reject: bool = False) -> str:
    """
    Display the ROGUE alert and ask a human whether to allow the step.

    step_result — the dict returned by check_drift() for this step.
    auto_reject — if True, skip the prompt and always reject (for demo / CI mode).

    Returns "approved" or "rejected".
    """

    print("\n" + "=" * 60)
    print("  [!] HITL GATE FIRED -- ROGUE verdict detected")
    print("=" * 60)
    print(f"  Step     : {step_result['step']}")
    print(f"  Tool     : {step_result['tool']}")
    print(f"  Drift    : {step_result['drift_score']}  (< 0.65 threshold)")
    print(f"  Intent   : {step_result['intent']}")

    flags = step_result.get("regulatory_flags", [])
    if flags:
        print("\n  Regulatory flags triggered:")
        for flag in flags:
            print(f"    [!] {flag}")

    print("=" * 60)

    if auto_reject:
        print("  [auto-reject mode] — step BLOCKED automatically.\n")
        return "rejected"

    while True:
        choice = input("  Allow this step? [y = approve / n = reject]: ").strip().lower()
        if choice in ("y", "yes"):
            print("  Step APPROVED by human reviewer.\n")
            return "approved"
        elif choice in ("n", "no"):
            print("  Step REJECTED by human reviewer. Agent halted.\n")
            return "rejected"
        else:
            print("  Please type y or n.")