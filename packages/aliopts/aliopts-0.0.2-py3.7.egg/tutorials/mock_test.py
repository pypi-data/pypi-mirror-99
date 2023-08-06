"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2021/1/11 10:54 上午
@Software: PyCharm
@File    : mock_test.py
@E-mail  : victor.xsyang@gmail.com
"""
import opts
import sys

def objective(trial):
    x = trial.suggest_uniform('x', -10, 10)
    return (x - 2) ** 2


if __name__ == '__main__':
    experiment = opts.create_experiment()
    experiment.optimize(objective, n_trials=10)
    sys.exit(0)
    print(experiment.best_params)
    print(experiment.best_value)
