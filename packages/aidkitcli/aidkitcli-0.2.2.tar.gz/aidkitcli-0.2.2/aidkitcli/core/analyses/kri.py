"""Create a RequestModel for a Key Robustness Indicator analysis."""
from typing import List, Union
from dataclasses import dataclass, asdict

from aidkitcli.core.utils import create_toml
from aidkitcli.core.request_model import RequestModel
from aidkitcli.data_access.stored_model_access import load_stored_model


@dataclass
class Distribution:
    start_index: int
    perturbation_length: int
    saver: int


@dataclass
class ConstantDistribution(Distribution):
    variable_name: str
    constant: Union[float, str]
    name: str = "constant"


@dataclass
class RelativeConstantDistribution(Distribution):
    variable_name: str
    relative_constant: float
    name: str = "relative_constant"


@dataclass
class IncDecDistribution(Distribution):
    variable_name: str
    factor: float
    start_constant: float
    end_constant: float
    step_length: int
    name: str = "inc_dec"


@dataclass
class RandomDistribution(Distribution):
    variable_name: str
    lower_bound: float
    upper_bound: float
    step_length: int
    name: str = "random"


@dataclass
class FGSMDistribution(Distribution):
    epsilon: List[float]
    iteration_step: int
    ascend: bool
    mask: List[int]
    step_length: List[int]
    name: str = "fgsm"


@dataclass
class CorrelationDistribution(Distribution):
    epsilon: List[float]
    iteration_step: int
    mask: List[int]
    step_length: List[int]
    name: str = "correlation"


@dataclass
class PeakDistribution(Distribution):
    epsilon: List[float]
    iteration_step: int
    mask: List[int]
    step_length: List[int]
    name: str = "peak"


@dataclass
class BlackboxDistribution(Distribution):
    epsilon: List[float]
    population_nr: int
    selection_nr: int
    evolutionary_step: int
    ascend: bool
    mask: List[int]
    step_length: List[int]
    name: str = "blackbox"


def constant_distribution_factory(variable_name: str,
                                  constant: Union[float, str],
                                  start_index: int = 0,
                                  perturbation_length: int = 100000
                                  ) -> ConstantDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Constant Corruption. This object can then be fed to the KRI
    function to determine a robustness risk score.

    When a Constant Corruption is executed, the values of the selected variable
    are replaced with a constant value given by the constant parameter.

    This corruption can be applied to both quantitative and categorical input
    variables. The supported ML models are:
        - Keras regression recurrent models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models

    :param variable_name: name of the variable to corrupt
    :param constant: constant value of the perturbation
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    """
    distribution = ConstantDistribution(
        variable_name=variable_name,
        constant=constant,
        start_index=start_index,
        perturbation_length=perturbation_length,
        saver=1
    )
    return distribution


def relative_constant_distribution_factory(variable_name: str,
                                           relative_constant: float,
                                           start_index: int = 0,
                                           perturbation_length: int = 100000
                                           ) -> RelativeConstantDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Relative Constant Corruption. This object can then be fed to the
    KRI function to determine a robustness risk score.

    When a Relative Constant Corruption is executed, the values of the selected
    variable are increased or decreased by a constant value relative_constant.

    This corruption can only be applied to quantitative input variables. The
    supported ML models are:
        - Keras regression recurrent models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models

    :param variable_name: name of the variable to corrupt
    :param relative_constant: constant value added to the original data
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    """
    distribution = RelativeConstantDistribution(
        variable_name=variable_name,
        relative_constant=relative_constant,
        start_index=start_index,
        perturbation_length=perturbation_length,
        saver=1
    )
    return distribution


def inc_dec_distribution_factory(variable_name: str,
                                 step_length: int,
                                 start_constant: float,
                                 end_constant: float,
                                 start_index: int = 0,
                                 perturbation_length: int = 100000
                                 ) -> IncDecDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Increasing - Decreasing Corruption. This object can then be fed
    to the KRI function to determine a robustness risk score.

    When an Increasing - Decreasing Corruption is executed, the values of the
    selected variable are first set to the start_constant value and then
    changed every step_length data points in the file. Depending on whether
    end_constant is bigger or smaller than start_constant, the values are
    increased or decreased after step_length data points.

    This corruption can only be applied to quantitative input variables. The
    supported ML models are:
        - Keras regression recurrent models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models

    :param variable_name: name of the variable to corrupt
    :param step_length: number of data points with a constant value before
    the next increase/decrease
    :param start_constant: starting value of the perturbation
    :param end_constant: maximal corruption value that should not be surpassed
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    """
    if start_constant < end_constant:
        factor = 1.0
    else:
        factor = -1.0

    distribution = IncDecDistribution(
        variable_name=variable_name,
        step_length=step_length,
        start_constant=start_constant,
        end_constant=end_constant,
        factor=factor,
        start_index=start_index,
        perturbation_length=perturbation_length,
        saver=1
    )
    return distribution


def random_distribution_factory(variable_name: str,
                                step_length: int,
                                lower_bound: float,
                                upper_bound: float,
                                start_index: int = 0,
                                perturbation_length: int = 100000
                                ) -> RandomDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Random Corruption. This object can then be fed to the KRI
    function to determine a robustness risk score.

    When a Random Corruption is executed, the values of the selected variable
    are set to random values sampled from a uniform distribution within the
    fixed range [lower_bound, upper_bound].

    This corruption can only be applied to quantitative input variables. The
    supported ML models are:
        - Keras regression recurrent models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models

    :param variable_name: name of the variable to corrupt
    :param step_length: number of data points with a constant value before
    the next increase/decrease
    :param lower_bound: minimal corruption value which should not be surpassed
    :param upper_bound: maximal corruption value which should not be surpassed
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    """
    distribution = RandomDistribution(
        variable_name=variable_name,
        step_length=step_length,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        start_index=start_index,
        perturbation_length=perturbation_length,
        saver=1
    )
    return distribution


def fgsm_distribution_factory(epsilon: List[float],
                              start_index: int = 0,
                              perturbation_length: int = 100000,
                              iteration_step: int = 10,
                              ascend: bool = True,
                              mask: List[int] = [],
                              step_length: List[int] = []
                              ) -> FGSMDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute an FGSM Attack. This object can then be fed to the KRI function to
    determine a robustness risk score.

    An FGSM Attack creates a perturbation per eligible data point in each file
    of the data set. The execution of this request returns a plot showing the
    performance of the model on the clean and the perturbed data.

    By default, all the data points are eligible to be perturbed. This changes
    if step_length determines that a certain number of consecutive perturbations
    should be the same or if start_index/perturbation_length limits the number
    of data points that can be perturbed in a data file.

    The perturbations are generated using the gradient of the neural network
    following this formula:
        x_perturbed = x + epsilon * sign[grad_x(loss(x, y, params))]

    The idea is to add a perturbation - scaled by epsilon - whose direction is
    the same as the gradient of the loss function w.r.t. the data.

    If the task of the attacked model is regression, the perturbation tries to
    increase or decrease - depending on the value of ascend - the value of the
    output node (the loss). If the task is classification the perturbation
    tries to decrease the probability value of the original prediction.

    Currently, this attack strategy can be applied to:
        - Keras regression recurrent models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models
    The data set must consist only of quantitative variables.

    :param epsilon: array of maximal L^inf perturbations for every variable
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param iteration_step: number of iterations in the attack
    :param ascend: whether the output value should increase (True) or decrease
    (False). Only needed if the attack is applied to a regression model
    :param mask: list of binary values that decide whether a variable can be
    perturbed by the attack, the list length must be the number of variables
    :param step_length: number of time steps with constant value before next
    increase or decrease
    """
    distribution = FGSMDistribution(
        epsilon=epsilon,
        start_index=start_index,
        perturbation_length=perturbation_length,
        iteration_step=iteration_step,
        ascend=ascend,
        mask=mask,
        step_length=step_length,
        saver=1
    )
    return distribution


def correlation_distribution_factory(epsilon: List[float],
                                     start_index: int = 0,
                                     perturbation_length: int = 100000,
                                     iteration_step: int = 10,
                                     mask: List[int] = [],
                                     step_length: List[int] = []
                                     ) -> CorrelationDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Correlation Attack. This object can then be fed to the KRI
    function to determine a robustness risk score.

    A Correlation Attack creates a perturbation per eligible data point in each
    file of the data set. The execution of this request returns a plot showing
    the performance of the model on the clean and the perturbed data.

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

    :param epsilon: array of maximal L^inf perturbations for every variable
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param iteration_step: number of iterations in the attack
    :param mask: list of binary values that decide whether a variable can be
    perturbed by the attack, the list length must be the number of variables
    :param step_length: number of time steps with constant value before next
    increase or decrease
    """
    distribution = CorrelationDistribution(
        epsilon=epsilon,
        start_index=start_index,
        perturbation_length=perturbation_length,
        iteration_step=iteration_step,
        mask=mask,
        step_length=step_length,
        saver=1
    )
    return distribution


def peak_distribution_factory(epsilon: List[float],
                              start_index: int = 0,
                              perturbation_length: int = 100000,
                              iteration_step: int = 10,
                              mask: List[int] = [],
                              step_length: List[int] = []
                              ) -> PeakDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Peak Attack. This object can then be fed to the KRI function to
    determine a robustness risk score.

    A Peak Attack creates a perturbation per eligible data point in each file
    of the data set. The execution of this request returns a plot showing the
    performance of the model on the clean and the perturbed data.

    The perturbations affect perturbation_length values starting at some point
    after start_index. The attack compares the MSE values of the different
    perturbations and using gradient information it optimizes the deviation of
    the predictions from the labels to find the consecutive data points in the
    data set where the highest possible "peak" error is achieved.

    The idea is to find the area in the file after start_index where the
    perturbation of perturbation_length values has the biggest impact.

    Currently, this attack strategy can be applied to Keras regression
    recurrent ML models and the data set must consist only of quantitative
    variables.

    :param epsilon: array of maximal L^inf perturbations for every variable
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param iteration_step: number of iterations in the attack
    :param mask: list of binary values that decide whether a variable can be
    perturbed by the attack, the list length must be the number of variables
    :param step_length: number of time steps with constant value before next
    increase or decrease
    """
    distribution = PeakDistribution(
        epsilon=epsilon,
        start_index=start_index,
        perturbation_length=perturbation_length,
        iteration_step=iteration_step,
        mask=mask,
        step_length=step_length,
        saver=1
    )
    return distribution


def blackbox_distribution_factory(epsilon: List[float],
                                  start_index: int = 0,
                                  perturbation_length: int = 100000,
                                  population_nr: int = 100,
                                  selection_nr: int = 10,
                                  evolutionary_step: int = 5,
                                  ascend: bool = True,
                                  mask: List[int] = [],
                                  step_length: List[int] = []
                                  ) -> BlackboxDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Black-Box Attack. This object can then be fed to the KRI function
    to determine a robustness risk score.

    A Black-Box Attack creates one perturbation per file in the data set. The
    perturbation is then added to every eligible data point in the corresponding
    data file. Finally, the performance of the model on the clean and the
    perturbed data is displayed on a plot.

    By default, all the data points are eligible to be perturbed. This changes
    if step_length determines that a certain number of consecutive perturbations
    should be the same or if start_index/perturbation_length limits the number
    of data points that can be perturbed in a data file.

    The perturbations are generated via an evolutionary algorithm, where
    the fitness function is determined by the output neuron of the given
    regression model. Population candidates are generated via a uniform
    distribution, and the crossover is given by an addition and clipping
    operation.

    Currently, this attack strategy can be applied to Keras regression
    recurrent ML models and the data set must consist only of quantitative
    variables.

    :param epsilon: array of maximal L^inf perturbations for every variable
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param population_nr: number of potential perturbations (candidates) in
    one population
    :param selection_nr: number of perturbations selected from population
    :param evolutionary_step: number of evolutions (crossover/mutations)
    :param ascend: whether the output value should increase (True) or decrease
    (False)
    :param mask: list of binary values that decide whether a variable can be
    perturbed by the attack, the list length must be the number of variables
    :param step_length: number of time steps with constant value before next
    increase or decrease
    """
    distribution = BlackboxDistribution(
        epsilon=epsilon,
        start_index=start_index,
        perturbation_length=perturbation_length,
        population_nr=population_nr,
        selection_nr=selection_nr,
        evolutionary_step=evolutionary_step,
        ascend=ascend,
        mask=mask,
        step_length=step_length,
        saver=1
    )
    return distribution


def kri(data: str, model: str,
        p_x: List[float], p_cond: List[float],
        distributions: List[Distribution],
        title="Config KRI Analysis"
        ) -> RequestModel:
    """
    Create a RequestModel to calculate the key robustness indicators (KRI) of
    the model on the basis of a given data set and realistic distributions
    for the deployment context. The relevance (probability of occurrence) of
    the data files and the distributions is given by the probability vectors
    p_x and p_cond. The method returns three different risk scores, based on
    different severity estimation metrics (error metrics):
        - Average Absolute Error of the predictions w.r.t. the labels (useful
        for regression)
        - Maximal Error of the predictions w.r.t. the labels (useful for
        regression)
        - Percentage of Errors / Accuracy (useful for classification)

    A more detailed explanation of this analysis can be found in the following
    paper: https://arxiv.org/abs/2011.04328

    The analysis can be executed using different corruption distributions
    and adversarial attacks:
        - "constant" - Constant Corruption
        - "relative_constant" - Relative Constant Corruption
        - "inc_dec" - Increase/Decrease Corruption
        - "random" - Random Corruption
        - "fgsm" - Fast Gradient Sign Method Attack
        - "correlation" - Correlation Attack
        - "peak" - Peak Attack
        - "blackbox" - Black-Box Attack
    Each distribution has its own parameters. Check the documentation of each
    factory method (<distribution_name>_distribution_factory) for a more
    detailed explanation of the different corruptions and attacks and their
    parameters.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param p_x: list of the probabilities of occurrence of a data file in the
    deployment context, the length of the list must be equal to the number of
    data files in the provided data set and the probabilities must sum up to 1
    :param p_cond: list of the probabilities of each distribution (corruption/
    attack) given a data set, the length of the list must be equal to the
    number of distributions and the probabilities must sum up to 1
    :param distributions: list of the distributions (corruptions/attacks) for
    the KRI analysis, each distribution is created by its corresponding
    factory method <distribution_name>_distribution_factory
    :param title: title of the configuration (default: "Config KRI Analysis")
    :return: a RequestModel instance containing all the information needed to
    execute a Key Robustness Indicator analysis
    """
    stored_model = load_stored_model(path=model)

    distributions_asdict = []
    for dist in distributions:
        name = dist.name
        params = asdict(dist)
        distributions_asdict.append({name: params})

    toml_dict = create_toml(
        title=title,
        data=data,
        stored_model=stored_model,
        key_robustness_indicator={
            "p_x": p_x,
            "p_cond": p_cond,
            "distributions": distributions_asdict
        }
    )
    return RequestModel(toml_dict)
