from app.core.email import send_email
from app.core.enums import TASK_TYPE
from app.shared.schemas.email import EmailPayload

task_handler_func = {
    TASK_TYPE.SEND_EMAIL: {
        "schema": EmailPayload,
        "handler": send_email,
        "waiting_threshold_in_mins": 5,
    }
}
