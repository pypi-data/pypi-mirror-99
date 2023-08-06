import json
import numpy as np
import os

from typing import List, Dict
from teradataml.analytics.valib import *
from teradataml import configure
from teradataml.dataframe.dataframe import DataFrame

configure.val_install_location = os.environ.get("AOA_VAL_DB", "VAL")


class _NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(_NpEncoder, self).default(obj)


def record_stats(df: DataFrame,
                 features: List,
                 predictors: List,
                 categorical: List,
                 category_labels: Dict,
                 category_ordinals: Dict = {},
                 importance: Dict = {},
                 bins=10):
    """

    example usage:
        pima = DataFrame("PIMA_TRAIN")

        record_stats(pima,
                   features=["TwoHourSerIns", "Age"],
                   predictors=["HasDiabetes"],
                   categorical=["HasDiabetes"],
                   importance={"Age": 0.9, "TwoHourSerIns": 0.1},
                   category_labels={"HasDiabetes": {0: "false", 1: "true"}})

    :param df:
    :param features:
    :param predictors:
    :param categorical:
    :param category_labels:
    :param category_ordinals:
    :param importance:
    :param bins:
    :return:
    """
    if not isinstance(df, DataFrame):
        raise ValueError("We only support teradataml DataFrame currently")

    if not all(k in category_labels for k in categorical):
        raise ValueError("You must specify a category_label for each categorical variable")

    total_rows = df.shape[0]

    continuous_vars = (set(features) | set(predictors)) - set(categorical)

    if len(continuous_vars) > 0:
        hist = valib.Histogram(data=df, columns=','.join(continuous_vars), bins=bins)
        hist = hist.result.to_pandas().reset_index()

        stats = valib.Statistics(data=df, columns=','.join(continuous_vars), stats_options="all")
        stats = stats.result.to_pandas().reset_index()

    if len(categorical) > 0:
        frequencies = valib.Frequency(data=df, columns=','.join(categorical))
        frequencies = frequencies.result.to_pandas().reset_index()

    data_struct = {
        "num_rows": total_rows,
        "features": {},
        "predictors": {}
    }

    def strip_key_x(d: Dict):
        return {k[1:]: v for k, v in d.items()}

    def add_var_metadata(var):
        if var in continuous_vars:
            var_hist = hist[hist.xcol == var].sort_values(by=['xbin'])

            bin_edges = [var_hist.xbeg.tolist()[0]]+var_hist.xend.tolist()
            bin_values = var_hist.xcnt

            stats_values = stats[stats.xcol == var].drop(["xdb", "xtbl", "xcol"], axis=1).to_dict(orient='records')[0]

            data_struct["features"][var] = {
                "type": "continuous",
                "statistics": strip_key_x(stats_values),
            }
            data_struct["features"][var]["statistics"]["histogram"] = {
                "edges": bin_edges,
                "values": bin_values.tolist()
            }

            if var in importance:
                data_struct["features"][var]["importance"] = importance[var]

        else:
            data_struct["predictors"][var] = {
                "type": "categorical",
                "category_labels": category_labels[var],
                "ordinal": category_ordinals.get(var, False),
                "statistics": {
                    "frequency": frequencies[frequencies.xcol == var][["xval", "xcnt"]].set_index("xval").T.to_dict(orient='records')[0]
                }
            }

            if var in importance:
                data_struct["predictors"][var]["importance"] = importance[var]

    for var in features:
        add_var_metadata(var)

    for var in predictors:
        add_var_metadata(var)

    with open("artifacts/output/data_stats.json", 'w+') as f:
        json.dump(data_struct, f, indent=2, cls=_NpEncoder)
