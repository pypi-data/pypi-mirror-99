# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import getpass
import os
import re
import subprocess
import sys
import textwrap
from typing import Optional, Sequence, Tuple

import attr
import click

import releasetool.filehelpers
import releasetool.git
import releasetool.github
import releasetool.secrets
import releasetool.commands.common


_CHANGELOG_TEMPLATE = """\
# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/DISTRIBUTION NAME/#history

"""


@attr.s(auto_attribs=True, slots=True)
class Context(releasetool.commands.common.GitHubContext):
    last_release_version: Optional[str] = None
    last_release_committish: Optional[str] = None
    release_version: Optional[str] = None
    release_branch: Optional[str] = None
    pull_request: Optional[dict] = None
    monorepo: bool = False  # true only when releasing from google-cloud-python


def determine_package_name(ctx: Context) -> None:
    click.secho("> Figuring out the package name.", fg="cyan")
    if ctx.monorepo:
        ctx.package_name = os.path.basename(os.getcwd())
    else:
        ctx.package_name = subprocess.check_output(
            [sys.executable, "setup.py", "--name"]
        ).decode("utf-8")

    click.secho(f"Looks like we're releasing {ctx.package_name}.")


def find_last_release_tag(
    tags: Sequence[str], package_name: str, monorepo: bool
) -> Optional[Tuple[str, str]]:
    commitish = None
    if monorepo:
        # tags look like storage-1.2.3
        package_names = [package_name, package_name.replace("_", "-")]
        candidates = [tag for tag in tags if tag.rsplit("-")[0] in package_names]

        if candidates:
            commitish = candidates[0]
            version = commitish.rsplit("-").pop()
    else:
        # tags look like v1.2.3 or 1.2.3
        candidates = [tag for tag in tags if re.match(r"v?(\d+\.\d+\.\d+)", tag)]
        if candidates:
            commitish = candidates[0]
            version = commitish.split("v").pop()

    if commitish:
        return commitish, version
    return None


def determine_last_release(ctx: Context) -> None:
    click.secho("> Figuring out what the last release was.", fg="cyan")
    tags = releasetool.git.list_tags()

    candidate = find_last_release_tag(tags, ctx.package_name, ctx.monorepo)
    if candidate is not None:
        ctx.last_release_committish = candidate[0]
        ctx.last_release_version = candidate[1]

    else:
        click.secho(
            f"I couldn't figure out the last release for {ctx.package_name}, "
            "so I'm assuming this is the first release. Can you tell me "
            "which git rev/sha to start the changelog at?",
            fg="yellow",
        )
        ctx.last_release_committish = click.prompt("Committish")
        ctx.last_release_version = "0.0.0"

    click.secho(f"The last release was {ctx.last_release_version}.")


def gather_changes(ctx: Context) -> None:
    click.secho(f"> Gathering changes since {ctx.last_release_version}", fg="cyan")
    ctx.changes = releasetool.git.summary_log(
        from_=ctx.last_release_committish, to="master"
    )
    ctx.changes = [
        ctx.github.link_pull_request(c, ctx.upstream_repo) for c in ctx.changes
    ]
    click.secho(f"Cool, {len(ctx.changes)} changes found.")


def determine_release_version(ctx: Context) -> None:
    click.secho("> Now it's time to pick a release version!", fg="cyan")
    release_notes = textwrap.indent(ctx.release_notes, "\t")
    click.secho(f"Here's the release notes you wrote:\n\n{release_notes}\n")

    parsed_version = [int(x) for x in ctx.last_release_version.split(".")]

    if parsed_version == [0, 0, 0]:
        ctx.release_version = "0.1.0"
        if not click.confirm(f"Release {ctx.release_version}?", default=True):
            version = click.prompt("What version should we release?")
            ctx.release_version = version
        return

    selection = click.prompt(
        "Is this a major, minor, or patch update (or enter the new version " "directly)"
    )
    if selection == "major":
        parsed_version[0] += 1
        parsed_version[1] = 0
        parsed_version[2] = 0
    elif selection == "minor":
        parsed_version[1] += 1
        parsed_version[2] = 0
    elif selection == "patch":
        parsed_version[2] += 1
    else:
        ctx.release_version = selection
        return

    ctx.release_version = "{}.{}.{}".format(*parsed_version)

    click.secho(f"Got it, releasing {ctx.release_version}.")


def create_release_branch(ctx) -> None:
    if ctx.monorepo:
        ctx.release_branch = f"release-{ctx.package_name}-{ctx.release_version}"
    else:
        ctx.release_branch = f"release-v{ctx.release_version}"
    click.secho(f"> Creating branch {ctx.release_branch}", fg="cyan")
    return releasetool.git.checkout_create_branch(ctx.release_branch)


def update_changelog(ctx: Context) -> None:
    changelog_filename = "CHANGELOG.md"
    click.secho(f"> Updating {changelog_filename}.", fg="cyan")

    if not os.path.exists(changelog_filename):
        print(f"{changelog_filename} does not yet exist. Opening it for " "creation.")

        releasetool.filehelpers.open_editor_with_content(
            changelog_filename, _CHANGELOG_TEMPLATE
        )

    changelog_entry = f"## {ctx.release_version}" f"\n\n" f"{ctx.release_notes}" f"\n\n"
    releasetool.filehelpers.insert_before(
        changelog_filename, changelog_entry, r"^## (.+)$|\Z"
    )


def update_setup_py(ctx: Context) -> None:
    click.secho("> Updating setup.py.", fg="cyan")
    releasetool.filehelpers.replace(
        "setup.py",
        r"version\s*=\s*(['\"])(.+?)['\"]",
        f"version = \\g<1>{ctx.release_version}\\g<1>",
    )


def create_release_commit(ctx: Context) -> None:
    """Create a release commit."""
    click.secho("> Comitting changes", fg="cyan")
    if ctx.monorepo:
        commit_msg = f"chore({ctx.package_name}): release {ctx.release_version}"
    else:
        commit_msg = f"chore: release v{ctx.release_version}"
    releasetool.git.commit(["CHANGELOG.md", "setup.py"], commit_msg)


def push_release_branch(ctx: Context) -> None:
    click.secho("> Pushing release branch.", fg="cyan")
    releasetool.git.push(ctx.release_branch)


def create_release_pr(ctx: Context, autorelease: bool = True) -> None:
    click.secho("> Creating release pull request.", fg="cyan")

    if ctx.upstream_repo == ctx.origin_repo:
        head = ctx.release_branch
    else:
        head = f"{ctx.origin_user}:{ctx.release_branch}"

    if ctx.monorepo:
        pr_title = f"chore({ctx.package_name}): release {ctx.release_version}"
    else:
        pr_title = f"chore: Release v{ctx.release_version}"

    ctx.pull_request = ctx.github.create_pull_request(
        ctx.upstream_repo,
        head=head,
        title=pr_title,
        body="This pull request was generated using releasetool.",
    )

    if autorelease:
        ctx.github.add_issue_labels(
            ctx.upstream_repo, ctx.pull_request["number"], ["autorelease: pending"]
        )

    click.secho(f"Pull request is at {ctx.pull_request['html_url']}.")


def start() -> None:
    ctx = Context()

    click.secho(f"o/ Hey, {getpass.getuser()}, let's release some stuff!", fg="magenta")

    releasetool.commands.common.setup_github_context(ctx)

    if "google-cloud-python" in ctx.origin_repo:
        ctx.monorepo = True

    determine_package_name(ctx)
    determine_last_release(ctx)
    gather_changes(ctx)
    releasetool.commands.common.edit_release_notes(ctx)
    determine_release_version(ctx)
    create_release_branch(ctx)
    update_changelog(ctx)
    update_setup_py(ctx)
    create_release_commit(ctx)
    push_release_branch(ctx)
    create_release_pr(ctx)

    click.secho("\\o/ All done!", fg="magenta")
