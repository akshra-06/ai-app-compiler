
import time


class EvaluationTracker:

    def __init__(self):

        self.stage_metrics = []

        self.total_cost = 0

        self.repair_count = 0

        self.validation_error_count = 0

    # -----------------------------------
    # STAGE TIMER
    # -----------------------------------

    def start_stage(
        self,
        stage_name
    ):

        return {

            "stage":
                stage_name,

            "start":
                time.time()
        }

    def end_stage(
        self,
        tracker
    ):

        end = time.time()

        latency = (
            end - tracker["start"]
        )

        self.stage_metrics.append({

            "stage":
                tracker["stage"],

            "latency_seconds":
                round(latency, 3)
        })

    # -----------------------------------
    # COST TRACKING
    # -----------------------------------

    def add_cost(
        self,
        amount
    ):

        self.total_cost += amount

    # -----------------------------------
    # VALIDATION METRICS
    # -----------------------------------

    def add_validation_errors(
        self,
        count
    ):

        self.validation_error_count += (
            count
        )

    # -----------------------------------
    # REPAIR METRICS
    # -----------------------------------

    def add_repairs(
        self,
        count
    ):

        self.repair_count += count

    # -----------------------------------
    # FINAL REPORT
    # -----------------------------------

    def generate_report(self):

        total_latency = sum(

            metric[
                "latency_seconds"
            ]

            for metric
            in self.stage_metrics
        )

        return {

            "total_latency_seconds":
                round(total_latency, 3),

            "total_cost":
                round(
                    self.total_cost,
                    6
                ),

            "repair_count":
                self.repair_count,

            "validation_error_count":
                self.validation_error_count,

            "stage_metrics":
                self.stage_metrics
        }

