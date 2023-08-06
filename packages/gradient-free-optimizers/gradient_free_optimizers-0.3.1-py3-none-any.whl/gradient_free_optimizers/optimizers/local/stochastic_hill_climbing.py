# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import random
import numpy as np

from . import HillClimbingOptimizer
from ...search import Search


class StochasticHillClimbingOptimizer(HillClimbingOptimizer, Search):
    def __init__(
        self,
        search_space,
        initialize={"grid": 4, "random": 2, "vertices": 4},
        epsilon=0.05,
        distribution="normal",
        n_neighbours=3,
        p_accept=0.1,
        norm_factor=1,
        rand_rest_p=0.03,
    ):
        super().__init__(search_space, initialize, epsilon, distribution, n_neighbours)
        self.p_accept = p_accept
        self.norm_factor = norm_factor
        self.rand_rest_p = rand_rest_p

        if self.norm_factor == "adaptive":
            self._accept = self._accept_adapt
            self.diff_max = 0
        else:
            self._accept = self._accept_default

    def _consider(self, p_accept):
        rand = random.uniform(0, self.p_accept)

        if rand > p_accept:
            self._new2current()

    def _score_norm_default(self):
        denom = self.score_current + self.score_new

        if denom == 0:
            return 1
        elif abs(denom) == np.inf:
            return 0
        else:
            return self.norm_factor * (self.score_current - self.score_new) / denom

    def _score_norm_adapt(self):
        diff = abs(self.score_current - self.score_new)
        if self.diff_max < diff:
            self.diff_max = diff

        denom = self.diff_max + diff

        if denom == 0:
            return 1
        elif abs(denom) == np.inf:
            return 0
        else:
            return abs(self.diff_max - diff) / denom

    def _accept_default(self):
        return np.exp(-self._score_norm_default())

    def _accept_adapt(self):
        return self._score_norm_adapt()

    def _transition(self, score_new):
        if score_new <= self.score_current:
            p_accept = self._accept()
            self._consider(p_accept)

    def evaluate(self, score_new):
        HillClimbingOptimizer.evaluate(self, score_new)

        # self._evaluate_new2current(score_new)
        self._transition(score_new)
        # self._evaluate_current2best()
