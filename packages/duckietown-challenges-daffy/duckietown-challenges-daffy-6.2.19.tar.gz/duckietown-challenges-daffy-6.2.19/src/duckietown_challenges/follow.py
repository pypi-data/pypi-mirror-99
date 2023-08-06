import datetime
import sys
import time
from collections import defaultdict

import termcolor

from .rest import ServerIsDown
from .rest_methods import dtserver_get_info


from .types import SubmissionID


__all__ = ["follow_submission"]


def follow_submission(token: str, submission_id: SubmissionID):
    step2job_seen = {}
    step2status_seen = defaultdict(lambda: "")

    print("")
    while True:
        try:
            data = dtserver_get_info(token, submission_id)
        except ServerIsDown:
            print(termcolor.colored("Server is down - please wait.", "red"))
            time.sleep(5)
            continue
        except BaseException as e:
            print(termcolor.colored(str(e), "red"))
            time.sleep(5)
            continue
        # print json.dumps(data, indent=4)

        status_details = data["status-details"]
        if status_details is None:
            write_status_line("Not processed yet.")
        else:

            complete = status_details["complete"]
            # result = status_details["result"]
            step2status = status_details["step2status"]
            step2status.pop("START", None)

            step2job = status_details["step2job"]
            for k, v in step2job.items():
                if k not in step2job_seen or step2job_seen[k] != v:
                    step2job_seen[k] = v

                    write_status_line(f'Job "{v}" created for step {k}')

            for k, v in step2status.items():
                if k not in step2status_seen or step2status_seen[k] != v:
                    step2status_seen[k] = v

                    write_status_line(f'Step "{k}" is in state {v}')

            next_steps = status_details["next_steps"]

            # if complete:
            #     msg = 'The submission is complete with result "%s".' % result
            #     print(msg)
            #     break
            cs = []

            if complete:
                cs.append("complete")
            else:
                cs.append("please wait")

            cs.append(f"status: {color_status(status_details['result'])}")

            if step2status:

                for step_name, step_state in step2status.items():
                    cs.append(f"{step_name}: {color_status(step_state)}")

            if next_steps:
                cs.append(f"  In queue: {' '.join(map(str, next_steps))}")

            s = "  ".join(cs)
            write_status_line(s)

        time.sleep(10)


class Storage:
    previous = None


def write_status_line(x):
    if x == Storage.previous:
        sys.stdout.write("\r" + " " * 80 + "\r")
    else:
        sys.stdout.write("\n")
    now = datetime.datetime.now()
    n = termcolor.colored(now.isoformat()[-15:-7], "blue", attrs=["dark"])
    sys.stdout.write(" - " + n + "   " + x)
    sys.stdout.flush()
    Storage.previous = x


def color_status(x: str):
    status2color = {
        "failed": dict(color="red", on_color=None, attrs=None),
        "error": dict(color="red", on_color=None, attrs=None),
        "success": dict(color="green", on_color=None, attrs=None),
        "evaluating": dict(color="blue", on_color=None, attrs=None),
        "aborted": dict(color="cyan", on_color=None, attrs=["dark"]),
        "timeout": dict(color="cyan", on_color=None, attrs=["dark"]),
    }

    if x in status2color:
        return termcolor.colored(x, **status2color[x])
    else:
        return x
