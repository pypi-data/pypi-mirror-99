"""Docker helpers."""

from enum import Enum
from typing import Dict, Iterator, List, Optional, Sequence, Tuple, cast

from invoke import Context, Result
from pydantic import BaseModel, Field, validator

EnvironmentVar = Dict[str, str]
CommandArgs = Sequence[Tuple[str, ...]]
Volumes = Sequence[Tuple[str, str]]


class UnknownContainer(Exception):
    ...


class DuplicateContainer(Exception):
    ...


default_args = ['--rm']


def create_container(  # noqa: WPS211, WPS231
    c: Context,
    name: str,
    image: str,
    environment: Optional[EnvironmentVar] = None,
    port: Optional[int] = None,
    workdir: Optional[str] = None,
    volumes: Optional[Volumes] = None,
    detach: bool = True,
    additional_args: Optional[List[str]] = None,
    command: Optional[str] = None,
    command_args: Optional[CommandArgs] = None,
    command_args_sep: str = ' ',
):
    environment = environment or {}
    volumes = volumes or []
    additional_args = additional_args or []

    if container_exists(c, name):
        raise DuplicateContainer(name)

    args = default_args.copy()

    args.append(f'--name {name}')

    if detach:
        args.append('-d')
    else:
        args.append('-it')

    if workdir:
        args.append(f'-w {workdir}')

    for volume in volumes:
        args.append(f'-v {volume[0]}:{volume[1]}')

    if port:
        args.append(f'-p {port}:{port}')

    for key, value in environment.items():
        args.append(f'-e {key}="{value}"')

    arg_string = ' '.join(args + additional_args)

    command_to_run = f'docker run {arg_string} {image}'

    if command:
        command_to_run = f'{command_to_run} {command}'

        if command_args:
            for command_arg in command_args:
                command_arg_string = command_args_sep.join(command_arg)
                command_to_run = f'{command_to_run} {command_arg_string}'

    c.run(command_to_run)


def start_container(c: Context, name: str):
    if not container_exists(c, name):
        raise UnknownContainer

    if not container_is_running(c, name):
        c.run(f'docker start {name}')


def stop_container(c: Context, name: str):
    if container_is_running(c, name):
        c.run(f'docker stop {name}')


class DockerState(Enum):
    running = 'running'
    exited = 'exited'


class DockerProcess(BaseModel):
    class Config:
        extra = 'ignore'

    command: str = Field(..., alias='Command')
    identifier: str = Field(..., alias='ID')
    image: str = Field(..., alias='Image')
    state: DockerState = Field(..., alias='State')
    names: List[str] = Field(..., alias='Names')

    @validator('names', pre=True)
    def parse_list(cls, v: object) -> object:  # noqa: N805  # pragma: no cover
        if isinstance(v, str):
            return v.split(',')
        return v


def container_exists(c: Context, name: str) -> bool:
    for container in get_docker_containers(c, only_running=False):
        if name in container.names:
            return True

    return False


def container_is_running(c: Context, name: str) -> bool:
    for container in get_docker_containers(c):
        if name in container.names:
            return container.state == DockerState.running

    return False


def get_docker_containers(c: Context, only_running: bool = True) -> Iterator[DockerProcess]:
    options: List[str] = ["--format '{{json .}}'"]

    if only_running:
        options.append('-a')

    opts = ' '.join(options)
    command = f'docker ps {opts}'

    res = cast(Result, c.run(command, echo=False, hide=True))
    output = cast(str, res.stdout)

    yield from (DockerProcess.parse_raw(line) for line in output.splitlines() if line)
