import json
from importlib import resources
from io import IOBase
from pathlib import Path
from typing import Union, Dict, Final, List, Optional
from urllib.request import urlretrieve, urlopen

import auto_phylo
from auto_phylo.pipeliner.model.Command import Command
from auto_phylo.pipeliner.model.Commands import Commands

CACHE_PATH: Final[Path] = Path.home() / ".auto-phylo"


def load_commands(custom_commands_paths: Optional[Dict[str, Union[str, Path, IOBase]]] = None) -> List[Commands]:
    commands = {**_load_built_in_commands(), **_load_cached_commands()}

    if custom_commands_paths is not None:
        commands = {**commands, **_load_commands_by_version(custom_commands_paths)}

    return list(commands for _, commands in sorted(commands.items()))


def load_default_commands() -> Commands:
    return _load_built_in_commands()["v2.0.0"]


def check_for_new_versions() -> None:
    with urlopen("https://api.github.com/repos/pegi3s/auto-phylo/tags") as tags_url:
        tags = json.loads(tags_url.read())

        for tag in tags:
            version = tag["name"]

            if version not in ("v1.0.0", "v2.0.0"):
                version_path = CACHE_PATH / version
                version_path.mkdir(parents=True, exist_ok=True)

                commands_path = version_path / "commands.json"
                if not commands_path.is_file():
                    urlretrieve(f"https://raw.githubusercontent.com/pegi3s/auto-phylo/{version}/commands.json",
                                commands_path)


def _load_built_in_commands() -> Dict[str, Commands]:
    return _load_commands_by_version({"v2.0.0": "commands.json"})


def _load_cached_commands() -> Dict[str, Commands]:
    return _load_commands_by_version({
        version_path.name: version_path / "commands.json"
        for version_path in CACHE_PATH.iterdir()
        if version_path.is_dir() and version_path.name.startswith("v")
    })


def _load_commands_by_version(commands_paths: Dict[str, Union[str, Path, IOBase]]) -> Dict[str, Commands]:
    commands_by_version: Dict[str, Commands] = {}

    for version, commands_path in commands_paths.items():
        if isinstance(commands_path, str):
            commands_file = resources.open_text(auto_phylo, commands_path, "utf-8")
        elif isinstance(commands_path, Path):
            commands_file = open(commands_path, encoding="utf-8")
        elif isinstance(commands_path, IOBase):
            commands_file = commands_path  # type: ignore
        else:
            raise ValueError("Invalid commands_file type")

        with commands_file:
            commands = json.load(commands_file)

        commands_by_version[version] = Commands(version, [Command(**data) for data in commands])

    return commands_by_version
