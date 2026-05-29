
from app.logging.trace_logger import (
    TraceLogger
)


logger = TraceLogger()


# -----------------------------------
# PIPELINE EVENTS
# -----------------------------------

logger.log(

    stage="intent_extraction",

    status="started"
)

logger.log(

    stage="intent_extraction",

    status="completed",

    metadata={

        "provider":
            "groq",

        "latency":
            1.2
    }
)

logger.log(

    stage="validation",

    status="completed",

    metadata={

        "errors_found":
            2
    }
)


# -----------------------------------
# FINAL OUTPUT
# -----------------------------------

logs = logger.get_logs()

print("\nTRACE LOGS\n")

print(logs)

