
import time

from app.evaluation.metrics import (
    EvaluationTracker
)


tracker = EvaluationTracker()


# -----------------------------------
# INTENT EXTRACTION
# -----------------------------------

intent_stage = tracker.start_stage(
    "intent_extraction"
)

time.sleep(1)

tracker.end_stage(
    intent_stage
)


# -----------------------------------
# SCHEMA GENERATION
# -----------------------------------

schema_stage = tracker.start_stage(
    "schema_generation"
)

time.sleep(2)

tracker.end_stage(
    schema_stage
)


# -----------------------------------
# VALIDATION
# -----------------------------------

tracker.add_validation_errors(3)

tracker.add_repairs(2)

tracker.add_cost(0.0025)


# -----------------------------------
# FINAL REPORT
# -----------------------------------

report = tracker.generate_report()

print("\nEVALUATION REPORT\n")

print(report)

