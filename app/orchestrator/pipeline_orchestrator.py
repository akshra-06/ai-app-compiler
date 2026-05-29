
import asyncio

from app.logging.trace_logger import (
    TraceLogger
)

from app.evaluation.metrics import (
    EvaluationTracker
)

from app.clarification.clarification_engine import (
    run_clarification_pipeline
)

from app.validation.appspec_validator import (
    validate_appspec
)

from app.repair.repair_engine import (
    repair_appspec
)


class PipelineOrchestrator:

    def __init__(self):

        self.logger = TraceLogger()

        self.evaluator = (
            EvaluationTracker()
        )

    # -----------------------------------
    # MAIN PIPELINE
    # -----------------------------------

    async def execute_pipeline(

        self,

        intent,

        data_schema,

        app_spec
    ):

        pipeline_result = {}

        # ===================================
        # CLARIFICATION
        # ===================================

        clarification_stage = (
            self.evaluator.start_stage(
                "clarification"
            )
        )

        self.logger.log(

            stage="clarification",

            status="started"
        )

        clarification_result = (
            run_clarification_pipeline(
                intent
            )
        )

        self.logger.log(

            stage="clarification",

            status="completed"
        )

        self.evaluator.end_stage(
            clarification_stage
        )

        pipeline_result[
            "clarification"
        ] = clarification_result

        await asyncio.sleep(1)

        # ===================================
        # VALIDATION
        # ===================================

        validation_stage = (
            self.evaluator.start_stage(
                "validation"
            )
        )

        self.logger.log(

            stage="validation",

            status="started"
        )

        validation_errors = (
            validate_appspec(

                data_schema,

                app_spec
            )
        )

        self.logger.log(

            stage="validation",

            status="completed",

            metadata={

                "errors":
                    len(
                        validation_errors
                    )
            }
        )

        self.evaluator.add_validation_errors(

            len(validation_errors)
        )

        self.evaluator.end_stage(
            validation_stage
        )

        pipeline_result[
            "validation_errors"
        ] = validation_errors

        await asyncio.sleep(1)

        # ===================================
        # REPAIR
        # ===================================

        repair_stage = (
            self.evaluator.start_stage(
                "repair"
            )
        )

        self.logger.log(

            stage="repair",

            status="started"
        )

        repair_result = (
            repair_appspec(

                data_schema,

                app_spec,

                validation_errors
            )
        )

        self.logger.log(

            stage="repair",

            status="completed",

            metadata={

                "repairs":
                    len(
                        repair_result[
                            "repair_log"
                        ]
                    )
            }
        )

        self.evaluator.add_repairs(

            len(
                repair_result[
                    "repair_log"
                ]
            )
        )

        self.evaluator.end_stage(
            repair_stage
        )

        pipeline_result[
            "repair_result"
        ] = repair_result

        await asyncio.sleep(1)

        # ===================================
        # FINAL REPORTS
        # ===================================

        pipeline_result[
            "evaluation_report"
        ] = (
            self.evaluator.generate_report()
        )

        pipeline_result[
            "trace_logs"
        ] = (
            self.logger.get_logs()
        )

        return pipeline_result

