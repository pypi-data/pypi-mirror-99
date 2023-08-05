# -*- coding: utf-8 -*-

from attr import attrs, attrib
import concurrent.futures
import json
import queue
import os
import random
import re
import sys
import time
import traceback
import tuxsuite.exceptions
import tuxsuite.requests
from tuxsuite.version import __version__
import uuid


# We will poll for status change for an average duration of 180 minutes
state_timeout = 10800  # 60 * 180
delay_status_update = int(os.getenv("TUXSUITE_DELAY_STATUS_UPDATE", "29")) + 1


def post_request(url, headers, request):
    response = tuxsuite.requests.post(url, data=json.dumps(request), headers=headers)
    if response.ok:
        return json.loads(response.text)
    else:
        if response.status_code == 400:
            response_data = json.loads(response.text)
            raise tuxsuite.exceptions.BadRequest(
                f"{response_data.get('status_message')}"
            )
        else:
            response.raise_for_status()


def get_request(url, headers):
    response = tuxsuite.requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        response.raise_for_status()  # Some unexpected status that's not caught


class HeadersMixin:
    @property
    def headers(self):
        return {
            "User-Agent": "tuxsuite/{}".format(__version__),
            "Content-Type": "application/json",
            "Authorization": self.token,
        }


@attrs(kw_only=True)
class BuildState:
    build = attrib()
    state = attrib()
    status = attrib(default=None)
    message = attrib()
    warnings = attrib(default=0)
    errors = attrib(default=0)
    icon = attrib()
    cli_color = attrib()
    final = attrib(default=False)


@attrs(kw_only=True)
class Build(HeadersMixin):
    git_repo = attrib()
    git_ref = attrib(default=None)
    git_sha = attrib(default=None)
    target_arch = attrib()
    kconfig = attrib()
    toolchain = attrib()
    token = attrib()
    kbapi_url = attrib()
    tuxapi_url = attrib()
    group = attrib()
    project = attrib()
    environment = attrib(default={})
    targets = attrib(default=[])
    make_variables = attrib(default={})
    kernel_image = attrib(default=None)

    build_data = attrib(default=None)
    build_key = attrib(default=None)
    build_name = attrib(default=None)
    status = attrib(default={})

    def __attrs_post_init__(self):
        if isinstance(self.kconfig, str):
            self.kconfig = [self.kconfig]
        self.verify_build_parameters()
        self.client_token = str(uuid.uuid4())

    def __str__(self):
        git_short_log = self.status.get("git_short_log", "")

        if len(self.kconfig) > 1:
            kconfig = f"{self.kconfig[0]}+{len(self.kconfig)-1}"
        else:
            kconfig = self.kconfig[0]
        return "{} {} ({}) with {} @ {}".format(
            git_short_log,
            self.target_arch,
            kconfig,
            self.toolchain,
            self.build_data,
        )

    @staticmethod
    def is_supported_git_url(url):
        """
        Check that the git url provided is valid (namely, that it's not an ssh
        url)
        """
        return re.match(r"^(git://|https?://).*$", url) is not None

    def generate_build_request(self):
        """ return a build data in a python dict """
        build_entry = {}
        build_entry["client_token"] = self.client_token
        build_entry["git_repo"] = self.git_repo
        if self.git_ref:
            build_entry["git_ref"] = self.git_ref
        if self.git_sha:
            build_entry["git_sha"] = self.git_sha
        build_entry["target_arch"] = self.target_arch
        build_entry["toolchain"] = self.toolchain
        build_entry["kconfig"] = self.kconfig
        build_entry["environment"] = dict(self.environment)
        build_entry["targets"] = self.targets
        build_entry["make_variables"] = self.make_variables
        if self.kernel_image:
            build_entry["kernel_image"] = self.kernel_image
        if self.build_name:
            build_entry["build_name"] = self.build_name
        return build_entry

    def verify_build_parameters(self):
        """ Pre-check the build arguments """
        assert self.git_repo, "git_repo is mandatory"
        assert self.is_supported_git_url(
            self.git_repo
        ), "git url must be in the form of git:// or http:// or https://"
        assert (self.git_ref and not self.git_sha) or (
            self.git_sha and not self.git_ref
        ), "Either a git_ref or a git_sha is required"
        assert self.target_arch is not None, "target_arch is mandatory"
        assert self.kconfig, "kconfig is mandatory"
        assert self.toolchain, "toolchain is mandatory"
        assert self.headers is not None, "headers is mandatory"

    def build(self):
        """ Submit the build request """
        data = []
        data.append(self.generate_build_request())
        url = self.kbapi_url + "/build"
        json_data = post_request(url, self.headers, data)
        self.build_data = json_data[0]["download_url"]
        self.build_key = json_data[0]["build_key"]

    def get_status(self):
        """ Fetches the build status and updates the values inside the build object"""
        url = self.kbapi_url + "/status/" + self.build_key
        self.status = get_request(url, self.headers)

    def watch(self):
        """
        Wait for the build to finish. Whenever the state changes, yielding the
        new state).

        Will timeout after `state_timeout` seconds.
        """
        attempts = 1
        max_attempts = 3
        waiting_states = {
            "queued": BuildState(
                build=self,
                state="queued",
                message="Queued",
                icon="⏳",
                cli_color="white",
            ),
            "provisioning": BuildState(
                build=self,
                state="provisioning",
                message="Provisioning",
                icon="⚙️ ",
                cli_color="white",
            ),
            "building": BuildState(
                build=self,
                state="building",
                message="Building",
                icon="🚀",
                cli_color="cyan",
            ),
        }
        final_states = ["complete", "error"]
        timeout = time.time() + state_timeout
        previous_state = None
        while True:
            self.get_status()
            state = self.status["tuxbuild_status"]
            if state != previous_state:
                if state in waiting_states:
                    yield waiting_states[state]
                elif state == "error" and attempts < max_attempts:
                    attempts += 1
                    message = self.status.get("status_message", "infrastructure error")
                    yield BuildState(
                        build=self,
                        state=self.status["tuxbuild_status"],
                        message=message
                        + f" - retrying (attempt {attempts}/{max_attempts})",
                        icon="🔧",
                        cli_color="yellow",
                    )
                    self.build()
                elif state in final_states:
                    break
                else:
                    # unknown state
                    yield BuildState(
                        build=self,
                        state=state,
                        message=self.status.get("status_message", state),
                        icon="🎰",
                        cli_color="yellow",
                    )
            elif time.time() >= timeout:
                raise tuxsuite.exceptions.Timeout(
                    f"Build timed out after {state_timeout/60} minutes; abandoning"
                )
            delay = random.randrange(delay_status_update)
            time.sleep(delay)
            previous_state = state

        errors = 0
        warnings = 0
        state = self.status["tuxbuild_status"]
        status = self.status["build_status"]

        if status == "pass":
            warnings = self.status["warnings_count"]
            if warnings == 0:
                icon = "🎉"
                message = "Pass"
                cli_color = "green"
            else:
                icon = "👾"
                cli_color = "yellow"
                if warnings == 1:
                    message = "Pass (1 warning)"
                else:
                    message = "Pass ({} warnings)".format(warnings)
        elif status == "fail":
            icon = "👹"
            cli_color = "bright_red"
            errors = self.status["errors_count"]
            if errors == 1:
                message = "Fail (1 error)"
            else:
                message = "Fail ({} errors)".format(errors)
            error_message = self.status.get("status_message")
            if error_message:
                message += f" with status message '{error_message}'"
        else:
            icon = "🔧"
            cli_color = "bright_red"
            message = self.status["status_message"]

        finished = BuildState(
            build=self,
            state=state,
            status=status,
            final=True,
            message=message,
            icon=icon,
            cli_color=cli_color,
            warnings=warnings,
            errors=errors,
        )
        yield finished

    def wait(self):
        state = None
        for s in self.watch():
            state = s
        return state

    def _get_field(self, field):
        """ Retrieve an individual field from status.json """
        self.get_status()
        return self.status.get(field, None)

    @property
    def warnings_count(self):
        """ Get the warnings_count for the build """
        return int(self._get_field("warnings_count"))

    @property
    def errors_count(self):
        """ Get the errors_count for the build """
        return int(self._get_field("errors_count"))

    @property
    def tuxbuild_status(self):
        """ Get the tuxbuild_status for the build """
        return self._get_field("tuxbuild_status")

    @property
    def build_status(self):
        """ Get the build_status for the build """
        return self._get_field("build_status")

    @property
    def status_message(self):
        """ Get the build_status for the build """
        return self._get_field("status_message")


class BuildSet(HeadersMixin):
    def __init__(self, builds, **kwargs):
        self.builds = []
        for item in builds:
            data = kwargs.copy()
            data.update(item)
            self.builds.append(Build(**data))
        self.token = kwargs["token"]
        self.kbapi_url = kwargs["kbapi_url"]

    def build(self):
        """ Submit the build request """

        data = []
        url = self.kbapi_url + "/build"
        for build_object in self.builds:
            data.append(build_object.generate_build_request())
        json_data = post_request(url, self.headers, data)

        builds_by_client_token = {b.client_token: b for b in self.builds}
        for build_config in json_data:
            build = builds_by_client_token[build_config["client_token"]]
            build.build_data = build_config["download_url"]
            build.build_key = build_config["build_key"]

    def __watch_build__(self, build, results):
        for state in build.watch():
            results.put(state)

    def watch(self):
        results = queue.Queue()
        n = len(self.builds)

        with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
            futures = {}
            for build in self.builds:
                f = executor.submit(self.__watch_build__, build, results)
                futures[build.build_key] = f

            finished = 0
            while finished < n:
                try:
                    state = results.get(timeout=60)
                except queue.Empty:
                    if all([f.done() for f in futures.values()]):
                        # Something went wrong: all threads finished but we
                        # don't have enough final states yet.
                        # Report any exceptions and don't wait forever
                        for build, f in futures.items():
                            exc = f.exception()
                            if exc:
                                tb = "".join(traceback.format_tb(exc.__traceback__))
                                print(
                                    f"ERROR for build {build}: {exc}\n{tb}",
                                    file=sys.stderr,
                                )
                        break
                else:
                    yield state
                    if state.final:
                        finished += 1

    def wait(self):
        states = []
        for s in self.watch():
            if s.final:
                states.append(s)
        return states

    @property
    def status_list(self):
        """ Return a list of build status dictionaries """
        return [build.status for build in self.builds]


@attrs(kw_only=True)
class Test(HeadersMixin):
    token = attrib()
    kbapi_url = attrib()
    tuxapi_url = attrib()
    group = attrib()
    project = attrib()
    device = attrib()
    kernel = attrib()
    tests = attrib(default=[])
    uid = attrib(default=None)

    def __str__(self):
        tests = "[" + ", ".join(["boot"] + self.tests) + "]"
        url = self.tuxapi_url + "/v1/groups/{}/projects/{}/tests/{}".format(
            self.group, self.project, self.uid
        )
        return "{} {} @ {}".format(tests, self.device, url)

    def test(self):
        url = self.tuxapi_url + "/v1/groups/{}/projects/{}/tests".format(
            self.group, self.project
        )
        data = {"device": self.device, "kernel": self.kernel}
        if self.tests:
            data["tests"] = self.tests
        data = post_request(url, self.headers, data)
        self.uid = data["uid"]

    def get(self):
        url = self.tuxapi_url + "/v1/groups/{}/projects/{}/tests/{}".format(
            self.group, self.project, self.uid
        )
        return get_request(url, self.headers)

    def watch(self):
        waiting_states = {
            "provisioning": BuildState(
                build=self,
                state="provisioning",
                message="Provisioning",
                icon="⚙️ ",
                cli_color="white",
            ),
            "running": BuildState(
                build=self,
                state="running",
                message="Running",
                icon="🚀",
                cli_color="cyan",
            ),
        }

        previous_state = None
        while True:
            data = self.get()
            state = data["state"]
            if state != previous_state:
                if state in waiting_states:
                    yield waiting_states[state]
                elif state == "finished":
                    break
                else:
                    assert 0
            delay = random.randrange(delay_status_update)
            time.sleep(delay)
            previous_state = state

        errors = 0
        result = data["result"]
        if result == "pass":
            icon = "🎉"
            message = "Pass"
            cli_color = "green"
        elif result == "fail":
            icon = "👹"
            cli_color = "bright_red"
            errors = [
                name for name in data["results"] if data["results"][name] == "fail"
            ]
            message = "Fail ({})".format(", ".join(errors))
            errors = len(errors)
        else:
            icon = "🔧"
            cli_color = "bright_red"
            message = "TuxTest error"

        finished = BuildState(
            build=self,
            state=state,
            status=result,
            final=True,
            message=message,
            icon=icon,
            cli_color=cli_color,
            errors=errors,
        )
        yield finished
