"""
Runs jobs passing a function as an argument. Thread safe.
"""
import time

from delphixpy.v1_10_2 import exceptions
from delphixpy.v1_10_2.web import job
from dxi._lib import util

from . import dlpx_exceptions
from . import dx_logging

VERSION = "v.0.3.004"


def run_job(main_func, dx_obj, engine="default", single_thread=True):
    """
    This method runs the main_func asynchronously against all the
    delphix engines specified
    :param main_func: function to run against the DDP(s).
     In these examples, it's main_workflow().
    :type main_func: function
    :param dx_obj: Delphix session object from config
    :type dx_obj: lib.get_session.GetSession object
    :param engine: name of an engine, all or None
    :type engine: str
    :param single_thread: Run as single thread (True) or
                    multiple threads (False)
    :type single_thread: bool
    """
    threads = []
    # if engine ="all", run against every engine in config_file
    if engine == "all":
        dx_logging.print_info(f"Executing on all Delphix Engines")
        try:
            for delphix_ddp in dx_obj.dlpx_ddps:
                t = main_func(
                    dx_obj.dlpx_ddps[delphix_ddp], dx_obj, single_thread
                )
                threads.append(t)
                # TODO: Revisit threading logic
                # This sleep has been tactically added to prevent errors in the parallel
                # processing of operations across multiple engines
                time.sleep(1)
        except dlpx_exceptions.DlpxException as err:
            dx_logging.print_exception(f"Error encountered in run_job():{err}")
    elif engine == "default":
        try:
            for delphix_ddp in dx_obj.dlpx_ddps.keys():
                if dx_obj.dlpx_ddps[delphix_ddp]["default"] == "True":
                    dx_obj_default = dx_obj
                    dx_obj_default.dlpx_ddps = {
                        delphix_ddp: dx_obj.dlpx_ddps[delphix_ddp]
                    }
                    dx_logging.print_info(
                        "Executing on the default Delphix Engine"
                    )
                    t = main_func(
                        dx_obj.dlpx_ddps[delphix_ddp], dx_obj, single_thread
                    )
                    threads.append(t)
                break
        except TypeError as err:
            raise dlpx_exceptions.DlpxException(f"Error in run_job: {err}")
    else:
        # Test to see if the engine exists in config_file
        try:
            engine_ref = dx_obj.dlpx_ddps[engine]
            t = main_func(engine_ref, dx_obj, single_thread)
            threads.append(t)
            dx_logging.print_info(
                f"Executing on Delphix Engine: "
                f'{engine_ref["hostname"]}'
            )
        except (exceptions.RequestError, KeyError):
            raise dlpx_exceptions.DlpxException(
                f"\nERROR: Delphix Engine {engine} cannot be found. Please "
                f"check your input and try again."
            )
    if engine is None:
        raise dlpx_exceptions.DlpxException(
            f"ERROR: No default Delphix Engine found."
        )
    return threads


def run_job_mt(main_func, dx_obj, engine="default", single_thread=True):
    """
    This method runs the main_func asynchronously against all the
    delphix engines specified
    :param main_func: function to run against the DDP(s).
     In these examples, it's main_workflow().
    :type main_func: function
    :param dx_obj: Delphix session object from config
    :type dx_obj: lib.get_session.GetSession object
    :param engine: name of an engine, all or None
    :type engine: str
    :param single_thread: Run as single thread (True) or
                    multiple threads (False)
    :type single_thread: bool
    """
    threads = []
    # if engine ="all", run against every engine in config_file
    if engine == "all":
        dx_logging.print_info(f"Executing on all Delphix Engines")
        try:
            for delphix_ddp in dx_obj.dlpx_ddps:
                engine_ref = dx_obj.dlpx_ddps[delphix_ddp]
                dx_obj.jobs[engine_ref["ip_address"]] = []
                t = main_func(
                    dx_obj.dlpx_ddps[delphix_ddp], dx_obj, single_thread
                )
                threads.append(t)
                # TODO: Revisit threading logic
                # This sleep has been tactically added to prevent errors in the parallel
                # processing of operations across multiple engines
                time.sleep(2)
        except dlpx_exceptions.DlpxException as err:
            dx_logging.print_exception(
                f"Error encountered in run_job():\n{err}"
            )
            raise err
    elif engine == "default":
        try:
            for delphix_ddp in dx_obj.dlpx_ddps.keys():
                is_default = dx_obj.dlpx_ddps[delphix_ddp]["default"]
                if is_default and is_default.lower() == "true":
                    dx_obj_default = dx_obj
                    dx_obj_default.dlpx_ddps = {
                        delphix_ddp: dx_obj.dlpx_ddps[delphix_ddp]
                    }
                    engine_ref = dx_obj.dlpx_ddps[delphix_ddp]
                    dx_obj.jobs[engine_ref["ip_address"]] = []
                    dx_logging.print_info(
                        f"Executing on the default Delphix Engine"
                    )
                    t = main_func(
                        dx_obj.dlpx_ddps[delphix_ddp], dx_obj, single_thread
                    )
                    threads.append(t)
                    break
        except TypeError as err:
            raise dlpx_exceptions.DlpxException(f"Error in run_job: {err}")
        except (dlpx_exceptions.DlpxException) as e:
            dx_logging.print_exception(f"Error in run_job():\n{e}")
            raise e
    else:
        # Test to see if the engine exists in config_file
        try:
            engine_ref = dx_obj.dlpx_ddps[engine]
            dx_obj.jobs[engine_ref["ip_address"]] = []
            t = main_func(engine_ref, dx_obj, single_thread)
            threads.append(t)
            dx_logging.print_info(
                f"Executing on Delphix Engine: "
                f'{engine_ref["hostname"]}'
            )
        except (exceptions.RequestError, KeyError):
            raise dlpx_exceptions.DlpxException(
                f"\nERROR: Delphix Engine: {engine} cannot be found. Please "
                f"check your input and try again."
            )
        except (dlpx_exceptions.DlpxException) as e:
            dx_logging.print_exception(f"Error in run_job():\n{e}")
            raise e
    if engine is None:
        raise dlpx_exceptions.DlpxException(
            f"ERROR: No default Delphix Engine found."
        )
    return threads


def track_running_jobs(
    engine, dx_obj, poll=10, failures=None, with_progress_bar=True
):
    """
    Retrieves running job state
    :param engine: Dictionary containing info on the DDP (IP, username, etc.)
    :param poll: How long to sleep between querying jobs
    :param dx_obj: Delphix session object from config
    :type dx_obj: lib.get_session.GetSession object
    :type poll: int
    :return:
    """
    # get all the jobs, then inspect them
    if failures is None:
        failures = [False]
    engine_running_jobs = ""
    if engine["ip_address"] in dx_obj.jobs:
        engine_running_jobs = dx_obj.jobs[engine["ip_address"]]
    if not engine_running_jobs:
        dx_logging.print_debug(
            f'No running jobs on engine : {engine["hostname"]}'
        )
    else:
        dx_logging.print_info(
            f'Waiting for jobs on : {engine["hostname"]}'
        )
    while engine_running_jobs:
        for j in engine_running_jobs:
            job_obj = job.get(dx_obj.server_session, j)
            if job_obj.job_state in ["COMPLETED"]:
                # util.show_progress(100, job_obj.reference, with_progress_bar=with_progress_bar)
                engine_running_jobs.remove(j)
                dx_logging.print_info(
                    f'Engine: {engine["hostname"]}: {job_obj.reference} is 100% COMPLETE'
                )
            elif job_obj.job_state in ["CANCELED", "FAILED"]:
                err_msg = extract_failure_message(job_obj)
                engine_running_jobs.remove(j)
                dx_logging.print_info(
                    f'Engine: {engine["hostname"]}: {job_obj.reference} was CANCELLED or FAILED '
                    f"due to an error"
                )
                dx_logging.print_info(f"{err_msg}")
                failures[0] = True
                raise Exception(f"{job_obj.job_id} {job_obj.job_state}")

            elif job_obj.job_state in "RUNNING":
                # util.show_progress(job_obj.percent_complete, job_obj.reference, with_progress_bar=with_progress_bar)
                dx_logging.print_info(
                    f'Engine: {engine["hostname"]}: {job_obj.reference} is RUNNING and {job_obj.percent_complete}% complete '
                )
        if engine_running_jobs:
            time.sleep(poll)


def extract_failure_message(jobobj):
    try:
        events = jobobj.events
        err_event = [event for event in events if event.event_type == "ERROR"]
        if err_event:
            err_msg = f"Error Reason: {err_event[0].message_details} \n Possible Action: {err_event[0].message_action}"
        return err_msg
    except (Exception) as err:
        return


def find_job_state(engine, dx_obj, poll=5):
    """
    Retrieves running job state
    :param engine: Dictionary containing info on the DDP (IP, username, etc.)
    :param poll: How long to sleep between querying jobs
    :param dx_obj: Delphix session object from config
    :type dx_obj: lib.get_session.GetSession object
    :type poll: int
    :return:
    """
    # get all the jobs, then inspect them
    dx_logging.print_debug(f"Checking running jobs state")
    i = 0
    for j in dx_obj.jobs.keys():
        print(len(dx_obj.jobs), j)
        job_obj = job.get(dx_obj.server_session, dx_obj.jobs[j])
        dx_logging.print_debug(
            f'{engine["ip_address"]}: Running job: ' f"{job_obj.job_state}"
        )
        if job_obj.job_state in ["CANCELED", "COMPLETED", "FAILED"]:
            # If the job is in a non-running state, remove it
            # from the running jobs list.
            del dx_obj.jobs[j]
            if len(dx_obj.jobs) == 0:
                break
        elif job_obj.job_state in "RUNNING":
            # If the job is in a running state, increment the
            # running job count.
            i += 1
        dx_logging.print_debug(f'{engine["ip_address"]}: {i} jobs running.')
        # If we have running jobs, pause before repeating the
        # checks.
        if dx_obj.jobs:
            time.sleep(poll)
        else:
            dx_logging.print_debug(f"No jobs running")
            break


def find_job_state_by_jobid(engine, dx_obj, job_id, poll=20):
    """
    Retrieves running job state
    :param engine: Dictionary containing info on the DDP (IP, username, etc.)
    :param poll: How long to sleep between querying jobs
    :param dx_obj: Delphix session object from config
    :type dx_obj: lib.get_session.GetSession object
    :param job_id: Job ID to check the state
    :type poll: int
    :return:
    """
    # get the job object
    job_obj = job.get(dx_obj.server_session, job_id)
    dx_logging.print_debug(job_obj)
    dx_logging.print_debug(f" Waiting for : {job_id} to finish")
    while job_obj.job_state == "RUNNING":
        time.sleep(poll)
        job_obj = job.get(dx_obj.server_session, job_id)
    dx_logging.print_debug(
        f"Job: {job_id} completed with status: {job_obj.job_state}"
    )
    return job_obj.job_state


def time_elapsed(time_start):
    """
    This function calculates the time elapsed since the beginning of the script.
    Call this anywhere you want to note the progress in terms of time
    :param time_start: start time of the script.
    :type time_start: float
    """
    return round((time.time() - time_start) / 60, +1)
