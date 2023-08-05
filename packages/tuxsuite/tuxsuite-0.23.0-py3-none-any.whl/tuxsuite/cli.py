# -*- coding: utf-8 -*-

import click
from functools import wraps
import json
import os
import sys
import tuxsuite
import tuxsuite.download
import tuxsuite.exceptions
import tuxsuite.gitutils


from tuxsuite.utils import defaults

info = click.echo


def error(msg):
    raise click.ClickException(msg)


def warning(msg):
    click.echo(msg, err=True)


def no_info(_):
    pass


def quiet_output(quiet):
    global info
    if quiet:
        info = no_info


def wait_for_object(build_object):
    result = True
    for state in build_object.watch():
        msg = click.style(
            f"{state.icon} {state.message}: ", fg=state.cli_color, bold=True
        ) + str(state.build)
        if state.status == "fail" or state.state == "error":
            warning(msg)
            if state.final:
                result = False
        elif state.warnings:
            warning(msg)
        else:
            info(msg)
    return result


def key_value(s):
    if "=" not in s:
        error(f"Key Value pair not valid: {s}")
    parts = s.split("=")
    return (parts[0], "=".join(parts[1:]))


def get_make_targets_vars(targets):
    target_list = []
    make_variables = {}
    if targets:
        key_values = [arg for arg in targets if "=" in arg]
        for kv in key_values:
            if kv.count("=") > 1:
                sys.stderr.write(f"Error: invalid KEY=VALUE: {kv}")
                sys.exit(1)
            make_variables = dict((arg.split("=") for arg in key_values))
        target_list = [arg for arg in targets if "=" not in arg]
    return (target_list, make_variables)


@click.group(name="tuxsuite")
@click.version_option()  # Implement --version
def cli():
    pass


def common_options(required):
    def option(*args, **kwargs):
        kw = kwargs.copy()
        kw["required"] = False
        for a in args:
            if a in required:
                kw["required"] = True
        return click.option(*args, **kw)

    options = [
        option("--git-repo", help="Git repository"),
        option("--git-ref", help="Git reference"),
        option("--git-sha", help="Git commit"),
        option(
            "--git-head",
            default=False,
            is_flag=True,
            help="Build the current git HEAD. Overrrides --git-repo and --git-ref",
        ),
        option(
            "--target-arch",
            help="Target architecture [arc|arm|arm64|i386|mips|parisc|powerpc|riscv|s390|sh|sparc|x86_64]",
        ),
        option(
            "--kernel-image",
            help="Specify custom kernel image that you wish to build",
        ),
        option(
            "--kconfig",
            multiple=True,
            help="Kernel kconfig arguments (may be specified multiple times)",
        ),
        option(
            "--toolchain",
            help="Toolchain [gcc-8|gcc-9|gcc-10|clang-10|clang-11|clang-12|clang-nightly]",
        ),
        option(
            "--build-name",
            help=("User defined string to identify the build"),
        ),
        option(
            "--json-out",
            help="Write json build status out to a named file path",
            type=click.File("w", encoding="utf-8"),
        ),
        option(
            "-d",
            "--download",
            default=False,
            is_flag=True,
            help="Download artifacts after builds finish",
        ),
        option(
            "-o",
            "--output-dir",
            default=".",
            help="Directory where to download artifacts",
        ),
        option(
            "-q",
            "--quiet",
            default=False,
            is_flag=True,
            help="Supress all informational output; prints only the download URL for the build",
        ),
        option(
            "-s",
            "--show-logs",
            default=False,
            is_flag=True,
            help="Prints build logs to stderr in case of warnings or errors",
        ),
        option(
            "-e",
            "--environment",
            type=key_value,
            multiple=True,
            help="Set environment variables for the build. Format: KEY=VALUE",
        ),
    ]

    def wrapper(f):
        f = wraps(f)(process_git_head(f))
        for opt in options:
            f = opt(f)
        return f

    return wrapper


def process_git_head(f):
    def wrapper(**kw):
        git_head = kw["git_head"]
        if git_head:
            try:
                repo, sha = tuxsuite.gitutils.get_git_head()
                kw["git_repo"] = repo
                kw["git_sha"] = sha
            except Exception as e:
                error(e)
        return f(**kw)

    return wrapper


def show_log(build, download, output_dir):
    if not build.warnings_count and not build.errors_count:
        return
    print("📄 Logs for {}:".format(build), file=sys.stderr)
    sys.stderr.flush()
    if download:
        for line in open(os.path.join(output_dir, build.build_key, "build.log")):
            print(line.strip(), file=sys.stderr)
    else:
        tuxsuite.download.download_file(
            os.path.join(build.build_data, "build.log"), sys.stderr.buffer
        )


description = (
    "Positional arguments:\n\n"
    "[KEY=VALUE | target] ...    Make variables to use and targets to build."
    "\n\n"
    "\t\t\t    If no TARGETs are specified, tuxsuite will build "
    f"{' + '.join(defaults.targets)}."
)


@cli.command(help=description, short_help="Run a single build.")
@common_options(required=["--target-arch", "--kconfig", "--toolchain"])
@click.argument("targets", metavar="[VAR=VALUE...] [target ...]", nargs=-1)
def build(
    json_out=None,
    quiet=False,
    show_logs=None,
    git_head=False,
    download=False,
    output_dir=None,
    **build_params,
):
    quiet_output(quiet)

    if "targets" in build_params:
        target_list, make_vars = get_make_targets_vars(build_params["targets"])
        build_params["targets"] = target_list
        build_params["make_variables"] = make_vars

    try:
        build = tuxsuite.Build(**build_params)
    except (AssertionError, tuxsuite.exceptions.TuxSuiteError) as e:
        error(e)
    info(
        "Building Linux Kernel {} at {}".format(
            build.git_repo, build.git_ref or build.git_sha
        )
    )
    try:
        build.build()
    except tuxsuite.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))
    build_result = wait_for_object(build)
    if json_out:
        json_out.write(json.dumps(build.status, sort_keys=True, indent=4))
    if download:
        tuxsuite.download.download(build, output_dir)
    if show_logs:
        show_log(build, download, output_dir)
    if quiet:
        print(build.build_data)
    if not build_result:
        sys.exit(1)


@cli.command(help=description, short_help="Run a set of builds.")
@click.option("--set-name", required=True, help="Set name")
@click.option("--tux-config", help="Path or a web URL to tuxsuite config file")
@click.argument("targets", metavar="[VAR=VALUE...] [target ...]", nargs=-1)
@common_options(required=[])
def build_set(
    tux_config,
    set_name,
    json_out=None,
    quiet=None,
    show_logs=None,
    git_head=False,
    download=False,
    output_dir=None,
    **build_params,
):
    quiet_output(quiet)

    if "targets" in build_params:
        target_list, make_vars = get_make_targets_vars(build_params["targets"])
        build_params["targets"] = target_list
        build_params["make_variables"] = make_vars

    try:
        build_set_config = tuxsuite.config.BuildSetConfig(set_name, tux_config)
        build_set = tuxsuite.BuildSet(build_set_config.entries, **build_params)
    except (AssertionError, tuxsuite.exceptions.TuxSuiteError) as e:
        error(e)

    info("Building Linux Kernel build set {}".format(set_name))

    try:
        build_set.build()
    except tuxsuite.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))

    build_set_result = wait_for_object(build_set)

    if json_out:
        json_out.write(json.dumps(build_set.status_list, sort_keys=True, indent=4))

    if download:
        for build in build_set.builds:
            tuxsuite.download.download(build, output_dir)

    if show_logs:
        for build in build_set.builds:
            show_log(build, download, output_dir)

    if quiet:
        for build in build_set.builds:
            print(build.build_data)

    # If any of the builds did not pass, exit with exit code of 1
    if not build_set_result:
        sys.exit(1)


DEVICES = [
    "qemu-arm",
    "qemu-arm64",
    "qemu-i386",
    "qemu-mips64",
    "qemu-ppc64",
    "qemu-riscv64",
    "qemu-x86_64",
]
TESTS = ["ltp-smoke"]


@cli.command(help="Test a kernel", short_help="Test a kernel")
@click.option("--device", help="Device type", required=True, type=click.Choice(DEVICES))
@click.option("--kernel", help="URL of the kernel to test", required=True, type=str)
@click.option("--tests", help="Comma separated list of tests", type=str, default="")
def test(device, kernel, tests):
    tests = [test for test in tests.split(",") if test]
    invalid_tests = [test for test in tests if test not in TESTS]
    if invalid_tests:
        raise click.ClickException(
            "Invalid tests [{}], only valid tests are: [{}]".format(
                ", ".join(invalid_tests), ", ".join(TESTS)
            )
        )
    info("Testing {} on {} with {}".format(kernel, device, ", ".join(["boot"] + tests)))

    try:
        test = tuxsuite.Test(device=device, kernel=kernel, tests=tests)
    except (AssertionError, tuxsuite.exceptions.TuxSuiteError) as e:
        error(e)

    try:
        test.test()
    except tuxsuite.exceptions.BadRequest as e:
        raise (click.ClickException(str(e)))
    test_result = wait_for_object(test)

    # If the test did not pass, exit with exit code of 1
    if not test_result:
        sys.exit(1)


def main():
    cli.main(prog_name="tuxsuite")
