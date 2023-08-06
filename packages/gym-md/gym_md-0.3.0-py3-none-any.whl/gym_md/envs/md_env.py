"""md-env module."""
from collections import defaultdict
from typing import DefaultDict, Final, List, Tuple

import gym
import numpy
from PIL import Image

from gym_md.envs.agent.actioner import Actions
from gym_md.envs.agent.agent import Agent
from gym_md.envs.grid import Grid
from gym_md.envs.renderer.renderer import Renderer
from gym_md.envs.setting import Setting


class MdEnvBase(gym.Env):
    """gym-mdの基底クラス.

    MdEnvBaseを継承する．
    継承したクラスはstage_nameを渡して，各ステージを作成する.
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self, stage_name: str):
        self.stage_name: Final[str] = stage_name
        self.setting: Final[Setting] = Setting(self.stage_name)
        self.grid: Grid = Grid(self.stage_name, self.setting)
        self.agent: Agent = Agent(self.grid, self.setting)
        self.renderer: Final[Renderer] = Renderer(self.grid, self.agent, self.setting)
        self.info: DefaultDict[str, int] = defaultdict(int)
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(7,))
        self.observation_space = gym.spaces.Box(
            low=0, high=30, shape=(8,), dtype=numpy.int32
        )

    def reset(self) -> List[int]:
        """環境をリセットする."""
        self.grid.reset()
        self.agent.reset()
        self.info = defaultdict(int)
        return self._get_observation()

    def step(
        self, actions: Actions
    ) -> Tuple[List[int], int, bool, DefaultDict[str, int]]:
        """エージェントが1ステップ行動する.

        Attributes
        ----------
        actions: Actions
            list of int
            各行動の値を入力する

        Notes
        -----
        行動列をすべて入力としている
        これはある行動をしようとしてもそのマスがない場合があるため
        その場合は次に大きい値の行動を代わりに行う．

        Returns
        -------
        Tuple of (list of int, int, bool, dict)
        """
        action: Final[str] = self.agent.select_action(actions)
        self.agent.take_action(action)
        reward: int = self._get_reward()
        done: bool = self._is_done()
        observation: List[int] = self._get_observation()
        self.info = self._get_info(self.info, action)
        self._update_grid()
        return observation, reward, done, self.info

    def render(self, mode="human") -> Image:
        """画像の描画を行う.

        Notes
        -----
        画像自体も取得できるため，保存も可能.

        Returns
        -------
        Image
        """
        return self.renderer.render(mode=mode)

    def generate(self, mode="human") -> Image:
        """画像を生成する.

        Notes
        -----
        画像の保存などの処理はgym外で行う.

        Returns
        -------
        Image
        """
        return self.renderer.generate(mode=mode)

    def close(self) -> None:
        """環境を閉じる.

        Returns
        -------
        None
        """
        self.reset()

    def _get_reward(self) -> int:
        """報酬を計算する.

        Returns
        -------
        int
            報酬

        """
        R = self.setting.REWARDS
        C = self.setting.CHARACTER_TO_NUM
        ret: int = -R["TURN"]
        y, x = self.agent.y, self.agent.x
        if self.agent.hp <= 0:
            return ret + R["DEAD"]
        if self.grid[y, x] == C["T"]:
            ret += R["TREASURE"]
        if self.grid[y, x] == C["E"]:
            ret += R["EXIT"]
        if self.grid[y, x] == C["M"]:
            ret += R["KILL"]
        if self.grid[y, x] == C["P"]:
            ret += R["PORTION"]
        return ret

    def _get_info(
        self, info: DefaultDict[str, int], action: str
    ) -> DefaultDict[str, int]:
        """プレイデータの取得.

        Notes
        -----
        内部で情報を**更新しない**ことに注意．

        Returns
        -------
        defaultdict of (str, int)
        """
        y, x = self.agent.y, self.agent.x
        info[action] += 1
        info[self.setting.NUM_TO_CHARACTER[self.grid[y, x]]] += 1
        return info

    def _get_observation(self) -> List[int]:
        """環境の観測を取得する.

        Returns
        -------
        list of int
            エージェントにわたす距離の配列 (len: 8)
        """
        sd, _ = self.agent.path.get_distance_and_prev(
            y=self.agent.y, x=self.agent.x, safe=True
        )
        ud, _ = self.agent.path.get_distance_and_prev(
            y=self.agent.y, x=self.agent.x, safe=False
        )
        sd = self.agent.path.get_nearest_distance(sd)
        ud = self.agent.path.get_nearest_distance(ud)
        ret = [
            ud["M"],
            ud["T"],
            sd["T"],
            ud["P"],
            sd["P"],
            ud["E"],
            sd["E"],
            self.agent.hp,
        ]
        return ret

    def _is_done(self) -> bool:
        """ゲームが終了しているか.

        Returns
        -------
        bool
        """
        y, x = self.agent.y, self.agent.x
        if self.agent.hp <= 0:
            return True
        if self.grid[y, x] == self.setting.CHARACTER_TO_NUM["E"]:
            return True
        return False

    def _update_grid(self) -> None:
        """グリッドの状態を更新する.

        Notes
        -----
        メソッド内でグリッドの状態を**直接更新している**ことに注意．

        Returns
        -------
        None
        """
        y, x = self.agent.y, self.agent.x
        C = self.setting.CHARACTER_TO_NUM
        if self.agent.hp <= 0:
            return
        if self.grid[y, x] in [C["P"], C["M"], C["T"]]:
            self.grid[y, x] = C["."]


class TestMdEnv(MdEnvBase):
    """TestMdEnv Class."""

    def __init__(self):
        stage_name: Final[str] = "test"
        super(TestMdEnv, self).__init__(stage_name=stage_name)


class EdgeMdEnv(MdEnvBase):
    """EdgeMdEnv Class."""

    def __init__(self):
        stage_name: Final[str] = "edge"
        super(EdgeMdEnv, self).__init__(stage_name=stage_name)


class HardMdEnv(MdEnvBase):
    """HardMdEnv Class."""

    def __init__(self):
        stage_name: Final[str] = "hard"
        super(HardMdEnv, self).__init__(stage_name=stage_name)


class Random1MdEnv(MdEnvBase):
    """Random1Env Class."""

    def __init__(self):
        stage_name: Final[str] = "random_1"
        super(Random1MdEnv, self).__init__(stage_name=stage_name)


class Random2MdEnv(MdEnvBase):
    """Random1Env Class."""

    def __init__(self):
        stage_name: Final[str] = "random_2"
        super(Random2MdEnv, self).__init__(stage_name=stage_name)


class Gene1MdEnv(MdEnvBase):
    """Random1Env Class."""

    def __init__(self):
        stage_name: Final[str] = "gene_1"
        super(Gene1MdEnv, self).__init__(stage_name=stage_name)


class Gene2MdEnv(MdEnvBase):
    """Random1Env Class."""

    def __init__(self):
        stage_name: Final[str] = "gene_2"
        super(Gene2MdEnv, self).__init__(stage_name=stage_name)
