import os
import pathlib
from typing import Iterator, List, Sequence, Tuple

from pysen import (
    CommandBase,
    ComponentBase,
    Config,
    PluginBase,
    PluginConfig,
    RunOptions,
)
from pysen.mypy import MypyTarget
from pysen.reporter import Reporter
from pysen.runner_options import PathContext
from pysen.types import TargetName


def mypy_init_check() -> PluginBase:
    return MypyInitCheckPlugin()


class MypyInitCheckPlugin(PluginBase):
    def load(
        self, file_path: pathlib.Path, config: PluginConfig, root: Config
    ) -> Sequence[ComponentBase]:
        if root.lint and root.lint.mypy_targets:
            mypy_targets = root.lint.mypy_targets
        else:
            mypy_targets = []

        return [MypyInitCheckComponent(mypy_targets)]


class MypyInitCheckComponent(ComponentBase):
    def __init__(self, mypy_targets: List[MypyTarget]) -> None:
        self._mypy_targets = mypy_targets

    @property
    def targets(self) -> Sequence[TargetName]:
        return ["lint"]

    def create_command(
        self, target: str, paths: PathContext, options: RunOptions
    ) -> CommandBase:
        return MypyInitCheckCommand(self._mypy_targets)


class MypyInitCheckCommand(CommandBase):
    def __init__(self, mypy_targets: List[MypyTarget]) -> None:
        self._mypy_targets = mypy_targets

    @property
    def name(self) -> str:
        return "mypy_init_check"

    @property
    def has_side_effects(self) -> bool:
        return False

    def __call__(self, reporter: Reporter) -> int:
        targets = set(
            target
            for mypy_target in self._mypy_targets
            for path in mypy_target.paths
            for target in (path.iterdir() if path.is_dir() else (path,))
        )

        sources = set(
            root / file
            for target in targets
            for root, _, files in _walk(target)
            for file in files
            if file.suffix == ".py"
        )

        unreachable_sources = set()
        missing_inits = set()
        for source in sorted(sources):
            if source in targets:
                continue
            reachable = True
            for parent in source.parents:
                init = parent / "__init__.py"
                if not init.is_file():
                    reachable = False
                    missing_inits.add(init)
                if parent in targets:
                    break
            if not reachable:
                unreachable_sources.add(source)

        if len(unreachable_sources) > 0:
            reporter.logger.error("mypy will not check the following sources:")
            reporter.logger.error(
                ", ".join(str(source) for source in sorted(unreachable_sources))
            )
            reporter.logger.error("the following files may be required:")
            reporter.logger.error(
                ", ".join(str(source) for source in sorted(missing_inits))
            )
            return 1
        else:
            return 0


def _walk(
    top: pathlib.Path,
) -> Iterator[Tuple[pathlib.Path, List[pathlib.Path], List[pathlib.Path]]]:
    for root, dirs, files in os.walk(top):
        yield (
            pathlib.Path(root),
            [pathlib.Path(dir) for dir in dirs],
            [pathlib.Path(file) for file in files],
        )
