from dataclasses import asdict
from typing import List, Union, Mapping

from aidkitcli.core.stored_model import StoredModel, InputFeatures
from aidkitcli.data_access.stored_model_access import create_stored_model, save_stored_model


def create_toml(title: str, data: str, stored_model: StoredModel, **kwargs) -> dict:
    """
    Create a dictionary with the structure of the config TOML files and
    the information needed to run an analysis.

    :param title: title of the configuration
    :param data: name of the dataset
    :param stored_model: StoredModel dataclass with the model information
    :param kwargs: additional keyword arguments related to the analyses
    :return: dictionary containing the information needed to run an analysis
    """
    toml_dict = dict()
    toml_dict["title"] = title
    toml_dict["data"] = list(data.split())
    toml_dict["model"] = asdict(stored_model)
    toml_dict["analyses"] = {**kwargs}
    return toml_dict


def store_model(checkpoints: List[str],
                type: List[str],
                task: List[str],
                framework: List[str],
                output_columns: List[str],
                output_type: str,
                output_processing: str,
                max_output: float,
                min_output: float,
                output_categories: List[Union[str, float]],
                prediction_window: int,
                start_eval: int,
                columns: Mapping[str, InputFeatures],
                path: str):
    """
    Create a StoredModel instance and store it as a TOML file at a
    specified location.

    :param checkpoints: list of checkpoints
    :param type: feedforward or recurrent
    :param task: classification or regression
    :param framework: keras or scikit
    :param output_columns: name of the output columns containing the
        label information (e.g: MAX, LABEL)
    :param output_type: quantitative or categorical
    :param output_processing: name of the function to be used for
        output processing (e.g: min_max)
    :param max_output: maximum value of the output
    :param min_output: minimum value of the output
    :param output_categories: list of output categories
    :param prediction_window: number of predictions to be aggregated by mean calculation
    :param start_eval: index of first data point to be used for evaluations
    :param columns: dictionary where each key is the name of a column and
        each value is an InputFeatures dataclass:
        max_input: maximum input value of the column
        min_input: minimum input value of the column
    :param path: path where the TOML file is saved
    """
    stored_model = create_stored_model(
        checkpoints=checkpoints,
        type=type,
        task=task,
        framework=framework,
        output_columns=output_columns,
        output_type=output_type,
        output_processing=output_processing,
        max_output=max_output,
        min_output=min_output,
        output_categories=output_categories,
        prediction_window=prediction_window,
        start_eval=start_eval,
        columns=columns
    )

    save_stored_model(stored_model=stored_model, path=path)