"""renderer module."""
from typing import Final

import matplotlib.pyplot as plt
from PIL import Image

from gym_md.envs.agent.agent import Agent
from gym_md.envs.grid import Grid
from gym_md.envs.renderer.generator import Generator
from gym_md.envs.setting import Setting


class Renderer:
    """Renderer class."""

    def __init__(self, grid: Grid, agent: Agent, setting: Setting):
        self.grid: Final[Grid] = grid
        self.agent: Final[Agent] = agent
        self.generator: Final[Generator] = Generator(grid=grid, agent=agent)
        self.setting: Final[Setting] = setting

    def render(self, mode="human") -> Image:
        """可視化を提供する.

        Parameters
        ----------
        mode: str

        Returns
        -------
        Image or None
        """
        if mode == "human":
            return self._render_human(mode)

    def generate(self, mode="human") -> Image:
        """画像を生成して返す.

        Parameters
        ----------
        mode:str

        Returns
        -------
        Image or None
        """
        if mode == "human":
            return self.generator.generate()

    def _render_human(self, mode="human") -> Image:
        img = self.generate(mode=mode)
        plt.imshow(img)
        plt.pause(self.setting.RENDER_WAIT_TIME)
        plt.clf()
        return img
