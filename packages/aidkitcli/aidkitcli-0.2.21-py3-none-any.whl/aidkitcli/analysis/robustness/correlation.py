"""Create a RequestModel to execute a Correlation attack."""
from typing import Dict, List

from aidkitcli.core.analyses.correlation import correlation as request_factory
from aidkitcli.data_access.analysis import post_analysis


def correlation(data: str,
                model: str,
                epsilon: List[float],
                start_index: int = 0,
                perturbation_length: int = 100000,
                iteration_step: int = 10,
                mask: List[int] = [],
                step_length: List[int] = [],
                title: str = "Config Correlation Attack"
                ) -> Dict[str, int]:
    """
    Execute a Correlation Attack that creates a perturbation per eligible data
    point in each file of the data set and return a plot showing the performance
    of the model on the clean and the perturbed data.

    By default, all the data points are eligible to be perturbed. This changes
    if step_length determines that a certain number of consecutive perturbations
    should be the same or if start_index/perturbation_length limits the number
    of data points that can be perturbed in a data file.

    The perturbations are generated via a gradient-based optimization algorithm
    whose objective function penalizes the correlation between the predicted
    values and the true labels.

    Currently, this attack strategy can be applied to Keras regression
    recurrent ML models and the data set must consist only of quantitative
    variables.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param epsilon: array of maximal L^inf perturbations for every variable
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param iteration_step: number of iterations in the attack
    :param mask: list of binary values that decide whether a variable can be
    perturbed by the attack, the list length must be the number of variables
    :param step_length: number of time steps with constant value before next
    increase or decrease
    :param title: title of the configuration (default: "Config Correlation
    Attack")
    :return: a RequestModel instance containing all the information needed to
    execute a Correlation Attack
    """
    request_model = request_factory(
        title=title,
        data=data,
        model=model,
        epsilon=epsilon,
        start_index=start_index,
        perturbation_length=perturbation_length,
        iteration_step=iteration_step,
        mask=mask,
        step_length=step_length,
    )
    return post_analysis(request_model=request_model)
