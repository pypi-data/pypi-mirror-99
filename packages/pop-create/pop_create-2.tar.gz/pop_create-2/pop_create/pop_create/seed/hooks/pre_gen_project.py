import pathlib

from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    ctx = NamespaceDict({{cookiecutter}})
    root_directory = pathlib.Path.cwd()

    for dyne in ctx.dyne_list:
        (root_directory / ctx.clean_name / dyne / "contracts").mkdir(
            parents=True, exist_ok=True
        )
