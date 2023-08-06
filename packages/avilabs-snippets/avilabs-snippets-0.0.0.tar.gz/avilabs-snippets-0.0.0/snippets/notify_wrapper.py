from traceback import print_exception
import sys
import io
import requests
import psutil
from functools import wraps


def slack_notify(auth_token, channel_id):
    def notify(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            output = io.StringIO()
            try:
                func(*args, **kwargs)
                send_slack_msg(auth_token, channel_id)
            except:  # noqa: E722
                exc_type, exc_val, tb = sys.exc_info()
                print_exception(exc_type, exc_val, tb, limit=1, file=output)
                send_slack_msg(auth_token, channel_id, output.getvalue(), success=False)
                raise

        return wrapper

    return notify


def send_slack_msg(auth_token, channel_id, msg="", success=True):
    url = "https://slack.com/api/chat.postMessage"
    auth = {"Authorization": f"Bearer {auth_token}"}

    proc_name = " ".join(psutil.Process().cmdline()[1:])

    if success:
        msg = f"Your job {proc_name} succeeded! :tada:\n{msg}"
    else:
        msg = f"Your job {proc_name} failed! :collision:\n```{msg}```"

    payload = {"channel": channel_id, "text": msg}
    resp = requests.post(url, headers=auth, json=payload)
    if resp.ok:
        print("Slack message sent.")
    else:
        print("Unable to send Slack message.")


# Example usage
@slack_notify("YOUR_AUTH_TOKEN", "YOUR_CHANNEL_ID")
def my_long_running_job(arg1):
    pass
