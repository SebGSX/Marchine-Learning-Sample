# © 2024 Seb Garrioch. All rights reserved.
# Published under the MIT License.
import pandas as pd
import pytest

from src.data import DataSetManager

@pytest.fixture
def manager() -> DataSetManager:
    """Fixture to create a DataSetManager instance.
    :returns: A DataSetManager instance.
    """
    return DataSetManager()

@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Returns a sample dataset for testing."""
    data = {
        "Newspaper": [69.2, 45.1, 69.3],
        "Sales": [22.1, 10.4, 9.3]
    }
    return pd.DataFrame(data)

def test_add_dataset(manager: DataSetManager, sample_data: pd.DataFrame):
    """Test adding a dataset.
    :param manager: The DataSetManager instance.
    :param sample_data: The sample data for testing.
    """
    manager.add_dataset(sample_data)
    assert manager.get_dataset(0)["Newspaper"].tolist() == [69.2, 45.1, 69.3]
    assert manager.get_dataset(0)["Sales"].tolist() == [22.1, 10.4, 9.3]

def test_get_datasets(manager: DataSetManager, sample_data: pd.DataFrame):
    """Test retrieving all datasets.
    :param manager: The DataSetManager instance.
    :param sample_data: The sample data for testing.
    """
    manager.add_dataset(sample_data)
    manager.add_dataset(sample_data)
    assert manager.get_datasets() == [sample_data, sample_data]

def test_get_dataset(manager: DataSetManager, sample_data: pd.DataFrame):
    """Test retrieving a specific dataset by index.
    :param manager: The DataSetManager instance.
    :param sample_data: The sample data for testing.
    """
    manager.add_dataset(sample_data)
    assert manager.get_dataset(0)["Newspaper"].tolist() == [69.2, 45.1, 69.3]
    assert manager.get_dataset(0)["Sales"].tolist() == [22.1, 10.4, 9.3]

def test_get_dataset_count(manager: DataSetManager, sample_data: pd.DataFrame):
    """Test counting the number of datasets.
    :param manager: The DataSetManager instance.
    :param sample_data: The sample data for testing.
    """
    manager.add_dataset(sample_data)
    manager.add_dataset(sample_data)
    assert manager.get_dataset_count() == 2

def test_remove_dataset(manager: DataSetManager, sample_data: pd.DataFrame):
    """Test removing a dataset by index.
    :param manager: The DataSetManager instance.
    :param sample_data: The sample data for testing.
    """
    manager.add_dataset(sample_data)
    manager.add_dataset(sample_data)
    manager.remove_dataset(0)
    assert manager.get_datasets() == [sample_data]

def test_clear_datasets(manager: DataSetManager, sample_data: pd.DataFrame):
    """Test clearing all datasets.
    :param manager: The DataSetManager instance.
    :param sample_data: The sample data for testing.
    """
    manager.add_dataset(sample_data)
    manager.add_dataset(sample_data)
    manager.clear_datasets()
    assert manager.get_datasets() == []
