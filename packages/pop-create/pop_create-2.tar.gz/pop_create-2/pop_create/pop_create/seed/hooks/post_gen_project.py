import pathlib

from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    ctx = NamespaceDict({{cookiecutter}})
    root_directory = pathlib.Path.cwd()

    if ctx.vertical:
        script = root_directory / ctx.clean_name / "scripts.py"
        script.unlink(missing_ok=True)

        run = root_directory / "run.py"
        run.unlink(missing_ok=True)

        init = root_directory / ctx.clean_name / ctx.clean_name / "init.py"
        init.unlink(missing_ok=True)

        try:
            non_vertical_dyne = root_directory / ctx.clean_name / ctx.clean_name
            non_vertical_dyne.rmdir()
        except:
            ...
