import datetime
import filecmp
import os
import pathlib
import shutil
import subprocess
import tempfile
from typing import List

from cookiecutter.generate import generate_files
from dict_tools.data import NamespaceDict


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.pop_create)


COMPLETION_TEXT = """
Congratulations! You have set up a new project!
This project can be executed by calling the run.py script:
    python3 run.py
This project has been set up with pre-commit hooks for code checks and black.
First set up your source control environment with "git init" or "hg init".
Then enable these checks in your git checkout:
    pip install pre-commit
    pre-commit install
To run pre-commit manually, execute:
    pre-commit run --all-files
Please fork the pop-awesome and open a PR listing your new project \u263A
    https://gitlab.com/saltstack/pop/pop-awesome
"""


def cli(hub):
    hub.pop.config.load(["pop_create"], cli="pop_create")
    directory = pathlib.Path(hub.OPT.pop_create.directory)
    project_name = hub.OPT.pop_create.project_name or directory.name
    clean_name = project_name.replace("-", "_").replace(" ", "_")
    short_dyne_list = sorted(hub.OPT.pop_create.get("dyne", ()))

    if hub.OPT.pop_create.vertical:
        dyne_list = short_dyne_list
    else:
        dyne_list = [clean_name] + short_dyne_list

    ctx = {
        "author": subprocess.getoutput("git config --global user.name"),
        "author_email": subprocess.getoutput("git config --global user.email"),
        "clean_name": clean_name,
        "dyne_list": dyne_list,
        "project_name": project_name,
        "short_dyne_list": short_dyne_list,
        "this_year": str(datetime.datetime.today().year),
    }

    for key, value in hub.OPT.pop_create.items():
        # Don't overwrite any values we already sanitized
        if key in ("project_name", "directory"):
            continue
        ctx[key] = value

    if hub.SUBPARSER:
        subparsers = [hub.SUBPARSER.replace("-", "_")]
    else:
        # No subparser specified, do all the core creators
        # cicd is last because it will run pre-commit on everything
        subparsers = ["seed", "docs", "tests", "cicd"]

    # Decide which copy function to use in the end
    if hub.OPT.pop_create.overwrite_existing:
        copy_function = shutil.copy2
    else:
        copy_function = hub.pop_create.init.copytree

    with tempfile.TemporaryDirectory(prefix="pop-create-") as tempdir:
        hub.pop_create.init.run(
            directory=tempdir,
            subparsers=subparsers,
            root_dir=tempdir,
            **ctx,
        )

        # Copy from temporary directory to target directory
        shutil.copytree(
            src=tempdir, dst=directory, dirs_exist_ok=True, copy_function=copy_function
        )

    # All done!
    print(COMPLETION_TEXT)


def run(
    hub,
    directory: pathlib.Path,
    subparsers: List[str],
    **ctx,
):
    for subparser in subparsers:
        try:
            # Let each subparser create it's own context
            context = NamespaceDict(ctx.copy())
            if "init" in hub.pop_create[subparser]:
                context = hub.pop_create[subparser].init.context(context)

            # Get the input directory
            repo_dir = hub.pop_create[subparser]._dirs[0]

            # Copy the templates from the source to the a temporary directory using the generated context
            generate_files(
                repo_dir=repo_dir,
                context={"cookiecutter": context},
                output_dir=directory,
                # We should be dealing with a temporary directory
                overwrite_if_exists=True,
                skip_if_file_exists=False,
            )
        except IndexError:
            hub.log.error(f"No template under sub {subparser}")


def copytree(hub, src, dst, *, follow_symlinks: bool = True):
    """
    Copy function that skips existing files
    """
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    if os.path.isdir(dst) or os.path.isdir(src):
        return dst
    elif os.path.exists(dst):
        hub.log.debug(f"Skipping target that already exists: {dst}")
        return dst
    hub.log.debug(f"Writing new file: {dst}")
    shutil.copyfile(src, dst, follow_symlinks=follow_symlinks)
    shutil.copystat(src, dst, follow_symlinks=follow_symlinks)
    return dst
