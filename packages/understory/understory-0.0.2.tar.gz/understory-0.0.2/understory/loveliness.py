"""
A background job queue.

Just a bunch of ladybugs doing their thing.

"""

from gevent import monkey; monkey.patch_all()  # noqa

from importlib import import_module
import json
import time
import traceback

import gevent.queue
import kv
import pendulum
from .. import term
from . import agent


main = term.application("loveliness", "job queue")
queue = gevent.queue.PriorityQueue()
worker_count = 20

sqldb = sql.db("")
kvdb = kv.db()


def schedule_jobs(browser):
    """Check all schedules every minute and enqueue any scheduled jobs."""
    # TODO support for days of month, days of week
    while True:  # wait for the start of a new minute
        now = pendulum.now()
        if now.second == 0:
            break
        time.sleep(1)
    for host in get_hosts():
        tx = canopy.contextualize(host)
        jobs = tx.db.select("job_schedules AS sch",
                            join="""job_signatures AS sig ON
                                    sch.job_signature_id = sig.rowid""")
        for job in jobs:
            run = True
            minute = job["minute"]
            hour = job["hour"]
            month = job["month"]
            if minute[:2] == "*/":
                if now.minute % int(minute[2]) == 0:
                    run = True
                else:
                    run = False
            if hour[:2] == "*/":
                if now.hour % int(hour[2]) == 0 and now.minute == 0:
                    run = True
                else:
                    run = False
            if month[:2] == "*/":
                if now.month % int(month[2]) == 0 and now.hour == 0 \
                   and now.minute == 0:
                    run = True
                else:
                    run = False
            if run:
                canopy.enqueue(getattr(import_module(job["module"]),
                                       job["object"]))
    time.sleep(1)


def handle_job(job_identifier, browser):
    """
    handle a freshly dequeued job

    """
    # TODO handle retries
    host, _, job_run_id = job_identifier.partition(":")
    tx = canopy.contextualize(host)
    tx.browser = browser
    job = tx.db.select("job_runs AS r", what="s.rowid, *",
                       join="""job_signatures AS s
                               ON s.rowid = r.job_signature_id""",
                       where="r.id = ?", vals=[job_run_id])[0]
    _module = job["module"]
    _object = job["object"]
    _args = json.loads(job["args"])
    _kwargs = json.loads(job["kwargs"])
    print(f"{host}/{_module}:{_object}",
          *(_args + list(f"{k}={v}" for k, v in _kwargs.items())),
          sep="\n  ", flush=True)
    tx.db.update("job_runs", where="id = ?", vals=[job_run_id],
                 what="started = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')")
    status = 0
    try:
        output = getattr(import_module(_module), _object)(*_args, **_kwargs)
    except Exception as err:
        status = 1
        output = str(err)
        traceback.print_exc()
    tx.db.update("job_runs", vals=[status, output, job_run_id],
                 what="""finished = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'),
                         status = ?, output = ?""", where="id = ?")
    run = tx.db.select("job_runs", where="id = ?", vals=[job_run_id])[0]
    st, rt = run["started"] - run["created"], run["finished"] - run["started"]
    tx.db.update("job_runs", what="start_time = ?, run_time = ?",
                 where="id = ?", vals=[f"{st.seconds}.{st.microseconds}",
                                       f"{rt.seconds}.{rt.microseconds}",
                                       job_run_id])


def run_scheduler(browser):
    while True:
        schedule_jobs(browser)


def run_worker(browser):
    while True:
        priority, job = queue.get()
        handle_job(job, browser)


@main.register()
class JobQueue:
    """Run the job queue."""

    def run(self, stdin, log):
        # TODO capture supervisor's kill signal and make sure to quit browser
        # XXX for host in get_hosts():
        # XXX     # TODO should skip if host doesn't need IMAP!
        # XXX     gevent.spawn(run_imap_idler, host)
        browser = agent.browser()
        gevent.spawn(run_scheduler, browser)
        for _ in range(worker_count):
            gevent.spawn(run_worker, browser)
        try:
            for job in kvdb["queue"].keep_popping():
                queue.put((1, job))  # TODO utilize priority levels
        except KeyboardInterrupt:
            browser.quit()


if __name__ == "__main__":
    main()
