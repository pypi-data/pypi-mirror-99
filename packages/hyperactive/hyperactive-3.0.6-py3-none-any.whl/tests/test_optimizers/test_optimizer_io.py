import pytest
import numpy as np

from ._parametrize import optimizers


def objective_function(opt):
    score = -opt["x1"] * opt["x1"]
    return score


def objective_function_m5(opt):
    score = -(opt["x1"] - 5) * (opt["x1"] - 5)
    return score


def objective_function_p5(opt):
    score = -(opt["x1"] + 5) * (opt["x1"] + 5)
    return score


search_space_0 = {"x1": np.arange(-100, 101, 1)}
search_space_1 = {"x1": np.arange(0, 101, 1)}
search_space_2 = {"x1": np.arange(-100, 1, 1)}

search_space_3 = {"x1": np.arange(-10, 11, 0.1)}
search_space_4 = {"x1": np.arange(0, 11, 0.1)}
search_space_5 = {"x1": np.arange(-10, 1, 0.1)}

search_space_6 = {"x1": np.arange(-0.0000000003, 0.0000000003, 0.0000000001)}
search_space_7 = {"x1": np.arange(0, 0.0000000003, 0.0000000001)}
search_space_8 = {"x1": np.arange(-0.0000000003, 0, 0.0000000001)}

objective_para = (
    "objective",
    [
        (objective_function),
        (objective_function_m5),
        (objective_function_p5),
    ],
)

search_space_para = (
    "search_space",
    [
        (search_space_0),
        (search_space_1),
        (search_space_2),
        (search_space_3),
        (search_space_4),
        (search_space_5),
        (search_space_6),
        (search_space_7),
        (search_space_8),
    ],
)


@pytest.mark.parametrize(*objective_para)
@pytest.mark.parametrize(*search_space_para)
@pytest.mark.parametrize(*optimizers)
def test_best_results_0(Optimizer, search_space, objective):
    search_space = search_space
    objective_function = objective

    initialize = {"vertices": 2}

    opt = Optimizer()
    opt.init(search_space, initialize)
    opt.search(objective_function, n_iter=10)

    assert opt.best_score == objective_function(opt.best_para)
