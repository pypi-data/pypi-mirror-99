"""
-*- coding: utf-8 -*-
@Author  : Ora
@Time    : 2020/12/7 8:30 下午
@Software: PyCharm
@File    : _dataframe.py
@E-mail  : victor.xsyang@gmail.com
"""
import collections
from typing import Any
from typing import DefaultDict
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

import opts
from opts._imports import try_import
from opts.trial._state import TrialState

with try_import() as _imports:
    import pandas as pd

if not _imports.is_successful():
    pd = object

def _trials_dataframe(
        experiment: "opts.Experiment", attrs: Tuple[str, ...], multi_index: bool
) -> "pd.DataFrame":
    _imports.check()
    trials = experiment.get_trials(deepcopy=False)

    if not len(trials):
        return pd.DataFrame()

    attrs_to_df_columns: Dict[str, str] = collections.OrderedDict()
    for attr in attrs:
        if attr.startswith("_"):
            df_column = attr[1:]
        else:
            df_column = attr
        attrs_to_df_columns[attr] = df_column

    column_agg: DefaultDict[str, Set] = collections.defaultdict(set)
    non_nested_attr = ""

    def _create_record_and_aggregate_column(
            trial: "opts.trial.FrozenTrial"
    ) -> Dict[Tuple[str, str], Any]:
        record = {}
        for attr, df_column in attrs_to_df_columns.items():
            value = getattr(trial, attr)
            if isinstance(value, TrialState):
                value = str(value).split(".")[-1]
            if isinstance(value, dict):
                for nested_attr, nested_value in value.items():
                    record[(df_column, nested_attr)] = nested_value
                    column_agg[attr].add((df_column, nested_attr))
            else:
                record[(df_column, non_nested_attr)] = value
                column_agg[attr].add((df_column, non_nested_attr))
        return record
    records = list([_create_record_and_aggregate_column(trial) for trial in trials])
    columns: List[Tuple[str, str]] = sum(
        (sorted(column_agg[k]) for k in attrs if k in column_agg), []
    )
    df = pd.DataFrame(records, columns=pd.MultiIndex.from_tuples(columns))
    if not multi_index:
        df.columns = ["_".join(filter(lambda c: c, map(lambda c: str(c), col))) for col in columns]
    return df