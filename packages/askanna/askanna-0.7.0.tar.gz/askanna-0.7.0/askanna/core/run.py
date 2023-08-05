"""
Core functions for management of runs in AskAnna
This is the class which act as gateway to the API of AskAnna
"""
from typing import List

import click

from askanna import job
from askanna.core import client, exceptions
from askanna.core.dataclasses import RunInfo, Run
from askanna.core.metrics import MetricGateway


class RunGateway:
    def __init__(self, *args, **kwargs):
        self.client = client
        self.run_suuid = None

    def start(self, job_suuid: str = None, data: dict = None) -> Run:

        url = "{}{}/{}/".format(self.client.config.remote, "run", job_suuid)

        r = self.client.post(url, json=data)
        if r.status_code != 200:
            raise exceptions.PostError(
                "{} - Something went wrong while starting a "
                "run: {}".format(r.status_code, r.reason)
            )
        run = Run(**r.json())
        self.run_suuid = run.short_uuid

        return run

    def list(self, query_params: dict = None) -> List[Run]:
        url = "{}{}/".format(
            self.client.config.remote,
            "runinfo",
        )
        r = self.client.get(url, params=query_params)
        if r.status_code != 200:
            raise exceptions.GetError(
                "{} - Something went wrong while retrieving the status "
                "of the run: {}".format(r.status_code, r.reason)
            )
        return [RunInfo(**r) for r in r.json().get("results")]

    def detail(self, suuid: str = None) -> RunInfo:
        """
        Retrieve details on a Run
        The suuid is optional and can be retrieved from `self.run_suuid`
        if the gateway was instantiated with it.

        returns RunInfo
        """
        suuid = suuid or self.run_suuid

        url = "{}{}/{}/".format(self.client.config.remote, "jobrun", suuid)

        r = self.client.get(url)
        if r.status_code != 200:
            raise exceptions.GetError(
                "{} - Something went wrong while retrieving the status "
                "of the run: {}".format(r.status_code, r.reason)
            )

        return RunInfo(**r.json())

    def status(self, suuid: str = None) -> Run:
        suuid = suuid or self.run_suuid

        if not suuid:
            raise exceptions.RunError(
                "There is no run SUUID provided. Did you start a run?"
            )

        url = "{}{}/{}/".format(self.client.config.remote, "status", suuid)

        r = self.client.get(url)
        if r.status_code != 200:
            raise exceptions.GetError(
                "{} - Something went wrong while retrieving the status "
                "of the run: {}".format(r.status_code, r.reason)
            )

        return Run(**r.json())


class RunActionGateway:
    """
    This provides to query runs, using the RunGateway
    the .get() returns eiter
    """

    multiple = False
    run_suuid = None

    def __init__(self):
        self.gateway = RunGateway()

    def start(
        self,
        job_suuid: str = None,
        data: dict = None,
        job_name: str = None,
        project_suuid: str = None,
    ) -> Run:
        if not job_suuid and not job_name:
            raise exceptions.PostError(
                "To start a run we need at least a job SUUID or job name"
            )
        elif not job_suuid:
            job_suuid = job.get_job_by_name(
                job_name=job_name, project_suuid=project_suuid
            ).short_uuid

        run = self.gateway.start(job_suuid=job_suuid, data=data)
        self.run_suuid = run.short_uuid
        return run

    def status(self, suuid: str = None) -> Run:
        suuid = suuid or self.run_suuid
        return self.gateway.status(suuid=suuid)

    def get(self, run, include_metrics=False) -> Run:
        if not run:
            click.echo("Please specify the run SUUID to 'get' a run", err=True)
            return

        runinfo = self.gateway.detail(suuid=run)
        if include_metrics:
            # also fetch the metrics for the runs
            run_suuids = [runinfo.short_uuid]
            query = {"runs": run_suuids}
            mgw = MetricGateway()
            metrics = mgw.list(query_params=query)

            # add the metrics to the runobjects
            # run.metrics
            for metric in metrics:
                if metric.get("run_suuid") == runinfo.short_uuid:
                    runinfo.metrics.append(metric)
        return runinfo


class RunMultipleQueryGateway(RunActionGateway):
    def get_query(self, project: str = None, job: str = None, runs: list = None):
        """
        We return jobs/ metrics from either:
        - project
        - job
        - runs (specific run_suuids)

        When runs is set, this takes precedence over project and job.
        When runs is empty, look at project or job, where job takes precedence
        """
        query = {}
        if runs and len(runs):
            # build comma separated string from runs if more then 1 run
            query = {"runs": ",".join(runs)}
        if project:
            query.update({"project": project})
        if job:
            query.update({"job": job})
        return query

    def get(
        self,
        project: str = None,
        job: str = None,
        runs: list = None,
        limit: int = 100,
        offset: int = 0,
        include_metrics: bool = False,
    ) -> List[Run]:
        query = self.get_query(project, job, runs)
        query.update(
            {
                "limit": limit,
                "offset": offset,
            }
        )
        rgw = RunGateway()
        runs = rgw.list(query_params=query)
        if include_metrics:
            # also fetch the metrics for the runs
            # add the metrics to the runobjects
            mgw = MetricGateway()
            for run in runs:
                metrics = mgw.get(run=run.short_uuid)
                # run.metrics
                run.metrics = metrics

        return runs
