import requests
import pytest

from pinecone_datasets.catalog import Catalog
from pinecone_datasets.catalog import DatasetMetadata, DenseModelMetadata

from pydantic import ValidationError


def download_json_from_https(url):
    return requests.get(url).json()


def test_catalog():
    catalog = Catalog.load()

    catalog_as_dict = download_json_from_https(
        "https://storage.googleapis.com/pinecone-datasets-dev/quora_all-MiniLM-L6-bm25/metadata.json"
    )

    found = any(
        catalog_as_dict["name"] == dataset
        for dataset in catalog.list_datasets(as_df=False)
    )
    assert found


def test_metadta_fields_minimal():
    try:
        meta = DatasetMetadata(
            name="test",
            documents=1,
            created_at="2021-01-01 00:00:00.000000",
            queries=1,
            dense_model=DenseModelMetadata(
                name="ada2",
                dimension=2,
            ),
        )
    except NameError:
        pytest.fail("Validation error")


def test_validation_error_mandatory_field():
    with pytest.raises(ValidationError):
        meta = DatasetMetadata(
            documents=1,
            queries=1,
            dense_model=DenseModelMetadata(
                name="ada2",
                dimensions=2,
            ),
        )


def test_validation_error_optional_field():
    with pytest.raises(ValidationError):
        meta = DatasetMetadata(
            name="test",
            documents=1,
            queries=1,
            dense_model=DenseModelMetadata(name="ada2", dimension=2),
            tags="test",
        )
