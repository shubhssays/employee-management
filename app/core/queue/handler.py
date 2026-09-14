from app.core.email import send_email
from app.core.enums import TASK_TYPE

handler_func = {
    TASK_TYPE.SEND_EMAIL: send_email
}
