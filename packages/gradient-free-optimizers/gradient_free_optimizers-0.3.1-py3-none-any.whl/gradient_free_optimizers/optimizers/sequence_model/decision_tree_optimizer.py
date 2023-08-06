# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


from .exp_imp_based_opt import ExpectedImprovementBasedOptimization
from .surrogate_models import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
)

tree_regressor_dict = {
    "random_forest": RandomForestRegressor(n_estimators=5),
    "extra_tree": ExtraTreesRegressor(n_estimators=5),
    "gradient_boost": GradientBoostingRegressor(n_estimators=5),
}


class DecisionTreeOptimizer(ExpectedImprovementBasedOptimization):
    """Based on the forest-optimizer in the scikit-optimize package"""

    def __init__(
        self,
        search_space,
        initialize={"grid": 4, "random": 2, "vertices": 4},
        tree_regressor="extra_tree",
        xi=0.01,
        warm_start_smbo=None,
        sampling={"random": 1000000},
        warnings=100000000,
        rand_rest_p=0.03,
    ):
        super().__init__(search_space, initialize)
        self.tree_regressor = tree_regressor
        self.regr = tree_regressor_dict[tree_regressor]
        self.xi = xi
        self.warm_start_smbo = warm_start_smbo
        self.sampling = sampling
        self.warnings = warnings
        self.rand_rest_p = rand_rest_p

        self.init_position_combinations()
        self.init_warm_start_smbo()
