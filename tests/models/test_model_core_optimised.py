# © 2024 Seb Garrioch. All rights reserved.
# Published under the MIT License.
import cupy as cp
import pandas as pd
import pytest

from src.models import ModelCoreOptimised

@pytest.fixture
def sample_data():
    """Returns a sample dataset for testing."""
    data = {
        "TV": [1, 2, 3],
        "Sales": [1, 2, 3]
    }
    df = pd.DataFrame(data)
    feature_names = ["TV"]
    label_name = "Sales"
    return df, feature_names, label_name

def test_initialisation():
    """Tests the initialisation of the ModelCoreOptimised class."""
    model_core = ModelCoreOptimised()
    assert not model_core.get_training_setup_completed()

def test_get_parameters_returns_keyed_data(sample_data: tuple[pd.DataFrame, list[str], str]):
    """Tests that the get_parameters method returns keyed data.
    :param sample_data: The sample data for testing.
    """
    df, feature_names, label_name = sample_data
    model_core = ModelCoreOptimised()
    model_core.setup_linear_regression_training(
        feature_names
        , label_name
        , 1e-8
        , "devzohaib/tvmarketingcsv"
        , "tvmarketing.csv"
        , False
        , df)
    actual = model_core.get_parameters()
    assert len(actual) == 2
    assert actual["W_0"] is not None
    assert actual["b"] is not None

def test_back_propagation(sample_data: tuple[pd.DataFrame, list[str], str]):
    """Tests the back_propagation method.
    :param sample_data: The sample data for testing.
    """
    df, feature_names, label_name = sample_data
    model_core = ModelCoreOptimised()
    model_core.setup_linear_regression_training(
        feature_names
        , label_name
        , 1e-8
        , "devzohaib/tvmarketingcsv"
        , "tvmarketing.csv"
        , False
        , df)
    y_hat = model_core.predict(pd.DataFrame({"TV": [4, 5, 6]}))
    actual = model_core.back_propagation(y_hat)

    # No training has been performed, so the gradients are -1.0 and 2.0 respectively.
    assert cp.isclose(actual[0, 0], -1, rtol=1e-3)
    assert cp.isclose(actual[0, 1], 2.0, rtol=1e-3)

def test_forward_propagation(sample_data: tuple[pd.DataFrame, list[str], str]):
    """Tests the forward_propagation method.
    :param sample_data: The sample data for testing.
    """
    df, feature_names, label_name = sample_data
    model_core = ModelCoreOptimised()
    model_core.setup_linear_regression_training(
        feature_names
        , label_name
        , 1e-8
        , "devzohaib/tvmarketingcsv"
        , "tvmarketing.csv"
        , False
        , df)
    actual = model_core.forward_propagation()

    # No training has been performed, so the forward propagation will yield values based on the initial weights.
    assert len(actual[0]) == 3

def test_flush_training_setup(sample_data: tuple[pd.DataFrame, list[str], str]):
    """Tests the flush_training_setup method."""
    df, feature_names, label_name = sample_data
    model_core = ModelCoreOptimised()
    model_core.setup_linear_regression_training(
        feature_names
        , label_name
        , 1e-8
        , "devzohaib/tvmarketingcsv"
        , "tvmarketing.csv"
        , False
        , df)
    assert model_core.get_training_setup_completed()
    model_core.flush_training_setup()
    assert not model_core.get_training_setup_completed()

def test_predict(sample_data: tuple[pd.DataFrame, list[str], str]):
    """Tests the predict method.
    :param sample_data: The sample data for testing.
    """
    df, feature_names, label_name = sample_data
    model_core = ModelCoreOptimised()
    model_core.setup_linear_regression_training(
        feature_names
        , label_name
        , 1e-8
        , "devzohaib/tvmarketingcsv"
        , "tvmarketing.csv"
        , False
        , df)
    y_hat = model_core.predict(pd.DataFrame({ "TV": [4, 5, 6] }))

    actual1 = y_hat[0][0]
    actual2 = y_hat[0][1]
    actual3 = y_hat[0][2]

    # No training has been performed, so the prediction yields approximately 2.0 for all cases.
    assert cp.isclose(actual1, 2.0, rtol=1e-3)
    assert cp.isclose(actual2, 2.0, rtol=1e-3)
    assert cp.isclose(actual3, 2.0, rtol=1e-3)

def test_setup_linear_regression_training(sample_data: tuple[pd.DataFrame, list[str], str]):
    """Tests the setup_linear_regression_training method.
    :param sample_data: The sample data for testing.
    """
    df, feature_names, label_name = sample_data
    model_core = ModelCoreOptimised()
    model_core.setup_linear_regression_training(
        feature_names
        , label_name
        , 1e-8
        , "devzohaib/tvmarketingcsv"
        , "tvmarketing.csv"
        , False
        , df)

    assert model_core.get_dataset() is not None
    assert model_core.get_input_size() == len(feature_names)
    assert model_core.get_output_size() == 1
    assert model_core.get_training_setup_completed()

def test_update_parameters(sample_data: tuple[pd.DataFrame, list[str], str]):
    """Tests the update_parameters method.
    :param sample_data: The sample data for testing.
    """
    df, feature_names, label_name = sample_data
    model_core = ModelCoreOptimised()
    learning_rate = 1e-8
    model_core.setup_linear_regression_training(
        feature_names
        , label_name
        , learning_rate
        , "devzohaib/tvmarketingcsv"
        , "tvmarketing.csv"
        , False
        , df)
    gradients = cp.array([[1], [2]])
    parameters_raw = cp.ndarray((2, 0))
    parameters_raw[0] = model_core.get_parameters()["W_0"]
    parameters_raw[1] = model_core.get_parameters()["b"]

    model_core.update_parameters(gradients)
    actual = model_core.get_parameters()
    expected = parameters_raw - learning_rate * gradients

    assert cp.allclose(actual["W_0"], expected[0])
    assert cp.allclose(actual["b"], expected[1])