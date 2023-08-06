import pytest

from gym_md.envs.grid import Grid
from gym_md.envs.setting import Setting
from gym_md.envs.agent.pather import Pather

NAME: str = 'test'


@pytest.fixture
def make_setting() -> Setting:
    setting: Setting = Setting(stage_name=NAME)
    return setting


@pytest.fixture
def make_grid(make_setting: Setting) -> Grid:
    grid = Grid(stage_name=NAME, setting=make_setting)
    return grid


@pytest.fixture
def make_pather(make_setting: Setting, make_grid: Grid):
    pather = Pather(grid=make_grid, setting=make_setting)
    return pather
