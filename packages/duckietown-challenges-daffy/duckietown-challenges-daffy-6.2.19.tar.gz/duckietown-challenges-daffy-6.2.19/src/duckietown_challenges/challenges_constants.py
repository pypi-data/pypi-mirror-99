# coding=utf-8
from typing import cast, ClassVar

__all__ = ["ChallengesConstants"]

from .types import JobStatusString


class ChallengesConstants:
    # status for evaluation jobs
    STATUS_JOB_TIMEOUT: ClassVar[JobStatusString] = cast(JobStatusString, "timeout")
    STATUS_JOB_EVALUATION: ClassVar[JobStatusString] = cast(JobStatusString, "evaluating")

    # evaluator can report one of these 5
    STATUS_JOB_FAILED: ClassVar[JobStatusString] = cast(JobStatusString, "failed")
    """ The submission failed PERMANENTLY - it crashed, segfault"""

    STATUS_JOB_ERROR: ClassVar[JobStatusString] = cast(JobStatusString, "error")  # evaluation failed
    """ The evaluator failed PERMANENTLY - for example, I gave you an incorrect map. """

    STATUS_JOB_HOST_ERROR: ClassVar[JobStatusString] = cast(JobStatusString, "host-error")
    """
        The environment had a TEMPORARY error - out of memory.
        The current submission is blacklisted for this evaluator, we will retry on a different evaluator.
        (you can always "reset" the job)
    """

    STATUS_JOB_ABORTED: ClassVar[JobStatusString] = cast(JobStatusString, "aborted")
    """
        The evaluation was aborted - the operator had to go to lunch.

        This evaluation is ignored. Just like it didn't happen.

    """

    STATUS_JOB_SUCCESS: ClassVar[JobStatusString] = cast(JobStatusString, "success")
    """ All good """

    ALLOWED_JOB_STATUS = [
        STATUS_JOB_EVALUATION,
        STATUS_JOB_SUCCESS,
        STATUS_JOB_TIMEOUT,
        STATUS_JOB_FAILED,
        STATUS_JOB_ERROR,
        STATUS_JOB_ABORTED,
        STATUS_JOB_HOST_ERROR,
    ]

    # JOB_TIMEOUT_MINUTES = 30
    DTSERVER_ENV_NAME = "DTSERVER"
    DEFAULT_DTSERVER = "https://challenges.duckietown.org/v4"
    DEFAULT_TIMEOUT = 30

    class Endpoints:
        challenge_define = "/challenge-define"
        registry_info = "/api/registry-info"
        user_info = "/api/user-info"
        submissions = "/api/submissions"
        components = "/api/components"
        challenges = "/api/challenges"
        jobs = "/api/jobs"
        take_submission = "/api/take-submission"
        job_heartbeat = "/api/heartbeat"
        auth = "/api/auth"
        reset_submission = "/api/reset-submission"
        bless_submission = "/api/bless-submission"
        change_user_priority = "/api/change-user-priority"
        change_admin_priority = "/api/change-admin-priority"
        reset_job = "/api/reset-job"
        submissions_list = "/api/submissions-list"
        submission_single = "/api/submission-single"
        sub_by_challenges = "/api/sub-by-challenges"

        jobs_by_submission = "/api/jobs-by-submission"
        leaderboards_data = "/api/leaderboardds-data"

    SUBMISSION_CONTAINER_TAG = "SUBMISSION_CONTAINER"
