
import uuid
import datetime


class TraceLogger:

    def __init__(self):

        self.trace_id = str(
            uuid.uuid4()
        )

        self.logs = []

    # -----------------------------------
    # ADD LOG
    # -----------------------------------

    def log(
        self,
        stage,
        status,
        metadata=None
    ):

        entry = {

            "timestamp":
                str(
                    datetime.datetime.utcnow()
                ),

            "trace_id":
                self.trace_id,

            "stage":
                stage,

            "status":
                status,

            "metadata":
                metadata or {}
        }

        self.logs.append(entry)

    # -----------------------------------
    # FETCH LOGS
    # -----------------------------------

    def get_logs(self):

        return {

            "trace_id":
                self.trace_id,

            "entries":
                self.logs
        }

