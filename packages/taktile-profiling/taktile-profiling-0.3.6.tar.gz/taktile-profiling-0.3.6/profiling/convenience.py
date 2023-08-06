import json
import logging
import os
from typing import Callable, Dict, List

import pandas
from fastapi.encoders import jsonable_encoder

from .accuracy import calibration, largest_errors, metrics
from .dependence import partialdep
from .expectations import condexp
from .importance import varimp
from .shap import ShapExplainer
from .utils import create_description, df_to_dict, input_schema_to_pandas

BASE_RESULTS_PATH = os.environ.get("BASE_RESULTS_PATH", "results")


def mkdir(endpoint_name, spec_path=""):
    folder = os.path.join(BASE_RESULTS_PATH, endpoint_name, spec_path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def create_shapley_schema(
    func: Callable,
    x: pandas.DataFrame,
    endpoint_name: str,
    profile_columns: List[str],
    explain_input_example: List[Dict],
):
    """Create shapley schema for endpoint"""

    explainer = ShapExplainer(func=func, x=x, profile_columns=profile_columns)
    folder = mkdir(endpoint_name=endpoint_name)

    input_descriptions = [create_description(x[col]) for col in profile_columns]
    logging.info("Shapley - Creating schema")
    fname = "schema.json"
    fpath = os.path.join(folder, fname)
    example = x[profile_columns].head(1)

    data = create_explainer_schema(
        explainer_schema_example=example,
        explainer=explainer,
        input_descriptions=input_descriptions,
        explain_input_example=explain_input_example,
    )
    with open(fpath, "w") as f:
        json.dump(jsonable_encoder(data), f)


def create_explainer_schema(
    explainer_schema_example: pandas.DataFrame,
    explainer: ShapExplainer,
    input_descriptions: List[Dict],
    explain_input_example: List[Dict],
) -> Dict:
    """Create schema for explainer input"""

    pred = explainer.func(explainer_schema_example)
    baseline, explanation = explainer.explain(explainer_schema_example)

    example = {
        "inputs": explain_input_example,
        "explanations": df_to_dict(explanation),
        "prediction": list(pred),
        "baseline": list(baseline),
    }
    # build schema
    schema = {"input_descriptions": input_descriptions, "example": example}
    return schema


def create_accuracy(
    func: Callable,
    x: pandas.DataFrame,
    y: pandas.Series,
    endpoint_name: str,
    profile_columns: List[str],
    kind: str,
) -> None:
    """Create accuracy profile for endpoint"""

    folder = mkdir(endpoint_name=endpoint_name, spec_path="accuracy")

    logging.info("Accuracy - Creating calibration plot")
    fname = "calibration.json"
    fpath = os.path.join(folder, fname)
    chart = calibration(func, x, y)
    chart.save(fpath, format="json")

    logging.info("Accuracy - Creating metrics table")
    fname = "metrics.json"
    fpath = os.path.join(folder, fname)
    metrics_table = metrics(func, x, y, kind)
    with open(fpath, "w") as f:
        f.write(metrics_table)

    logging.info("Accuracy - Finding largest errors")
    fname = "errors.json"
    fpath = os.path.join(folder, fname)
    errors_table = largest_errors(func, x, y, profile_columns)
    with open(fpath, "w") as f:
        f.write(errors_table)


def create_dependence(
    func: Callable, x: pandas.DataFrame, endpoint_name: str, profile_columns: List[str],
) -> None:
    """Create partial dependence graphs for all variables"""

    x = x.reset_index(drop=True)
    folder = mkdir(endpoint_name=endpoint_name, spec_path="anatomy/partialdep")

    for var in profile_columns:
        logging.info(f"Explanations - Creating partial dependence for {var}")
        fname = var + ".json"
        fpath = os.path.join(folder, fname)
        try:
            chart = partialdep(func=func, x=x, var=var)
            chart.save(fpath, format="json")
        except AttributeError:
            logging.warning(f"Could not generate valid chart for {var}")


def create_expectations(
    func: Callable,
    x: pandas.DataFrame,
    y: pandas.Series,
    endpoint_name: str,
    profile_columns: List[str],
) -> None:
    """Create conditional expectations graphs for all variables"""

    x, y = x.reset_index(drop=True), y.reset_index(drop=True)
    folder = mkdir(endpoint_name=endpoint_name, spec_path="anatomy/condexp")

    for var in profile_columns:
        logging.info(f"Explanations - Creating conditional expectations for {var}")
        fname = var + ".json"
        fpath = os.path.join(folder, fname)
        try:
            chart = condexp(func, x, y, var)
            chart.save(fpath, format="json")
        except AttributeError as e:
            logging.warning(f"Could not generate valid chart for {var}: {repr(e)}")
        except TypeError as e:
            # happens when object columns cannot be serialized to JSON
            # https://github.com/altair-viz/altair/issues/1355
            logging.warning(f"Could not generate valid chart for {var}: {repr(e)}")


def create_importance(
    func: Callable,
    x: pandas.DataFrame,
    endpoint_name: str,
    profile_columns: List[str],
    kind: str,
) -> None:

    logging.info("Explanations - Calculating variable importance")
    if kind in ["regression", "binary"]:
        chart, varlist = varimp(func, x, profile_columns=profile_columns)
    else:
        raise NotImplementedError("Unknown endpoint kind:" + kind)

    # Save to disk
    folder = mkdir(endpoint_name=endpoint_name, spec_path="anatomy")

    fname = "varimp.json"
    fpath = os.path.join(folder, fname)
    chart.save(fpath, format="json")

    fname = "varlist.json"
    fpath = os.path.join(folder, fname)
    with open(fpath, "w") as f:
        json.dump(varlist, f)


def create_summary(
    endpoint_name: str, input_names: List[str], output_names: str, kind: str
) -> None:

    logging.info(f"Summary - creating endpoint summary for endpoint: {endpoint_name}")
    as_json = {
        "name": endpoint_name,
        "kind": kind,
        "inputs": input_names,
        "output": output_names,
    }
    # Save to disk
    folder = mkdir(endpoint_name=endpoint_name)
    with open(os.path.join(folder, "summary.json"), "w") as summary:
        json.dump(as_json, summary)
