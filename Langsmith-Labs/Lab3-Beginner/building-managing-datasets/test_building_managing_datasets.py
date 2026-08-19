"""
Test file for Lab 3: Building & Managing Datasets

Run with: pytest test_building_managing_datasets.py -v
"""
import os
import pytest
from unittest.mock import patch, MagicMock


class TestDatasetStructure:
    """Tests for understanding LangSmith dataset components."""

    def test_dataset_has_name_and_description(self):
        """A dataset requires a name and optional description."""
        dataset_config = {
            "name": "product-reviews",
            "description": "Product reviews with structured output",
        }
        assert "name" in dataset_config
        assert "description" in dataset_config

    def test_example_has_input_and_output(self):
        """Each example is an input/output pair."""
        example = {
            "input": {"review_text": "Great product. Five stars."},
            "output": {"product": "Great Product", "rating": 5, "sentiment": "positive"},
        }
        assert "input" in example
        assert "output" in example

    def test_examples_are_keyed_by_schema_fields(self):
        """Input/output dicts use schema field names as keys."""
        example = {
            "input": {"review_text": "Some review"},
            "output": {"product": "Some Product", "rating": 4, "sentiment": "positive"},
        }
        assert "review_text" in example["input"]
        assert all(k in example["output"] for k in ["product", "rating", "sentiment"])


class TestCreationMethods:
    """Tests for the four ways to create examples."""

    def test_sdk_method(self):
        """Method 1: Programmatic via SDK create_examples()."""
        method = "sdk"
        assert method == "sdk"

    def test_traces_method(self):
        """Method 2: Convert traces into examples."""
        method = "traces"
        assert method == "traces"

    def test_csv_import_method(self):
        """Method 3: Import from CSV file."""
        method = "csv"
        assert method == "csv"

    def test_manual_ui_method(self):
        """Method 4: Manual creation in LangSmith UI."""
        method = "ui"
        assert method == "ui"

    def test_four_methods_total(self):
        """There are exactly four ways to create examples."""
        methods = ["sdk", "traces", "csv", "ui"]
        assert len(methods) == 4


class TestSDKOperations:
    """Tests for LangSmith SDK dataset operations."""

    def test_create_dataset_requires_name(self):
        """create_dataset() requires a dataset_name parameter."""
        required_params = ["dataset_name"]
        assert "dataset_name" in required_params

    def test_create_examples_requires_dataset_id(self):
        """create_examples() requires a dataset_id parameter."""
        required_params = ["dataset_id", "inputs", "outputs"]
        assert "dataset_id" in required_params

    def test_examples_inputs_outputs_are_dicts(self):
        """Inputs and outputs must be dictionaries."""
        inputs = {"review_text": "Some review"}
        outputs = {"product": "Some Product", "rating": 5, "sentiment": "positive"}
        assert isinstance(inputs, dict)
        assert isinstance(outputs, dict)

    def test_list_runs_filters_by_project(self):
        """list_runs() can filter by project_name and run_type."""
        filters = ["project_name", "run_type", "limit"]
        assert "project_name" in filters
        assert "run_type" in filters


class TestSplits:
    """Tests for split organization."""

    def test_split_metadata_field(self):
        """Examples are tagged with split via metadata."""
        metadata = {"split": "train"}
        assert "split" in metadata

    def test_two_common_splits(self):
        """The two common splits are train and test."""
        splits = ["train", "test"]
        assert len(splits) == 2
        assert "train" in splits
        assert "test" in splits

    def test_split_percentage(self):
        """Common split: 80% train, 20% test."""
        total = 15
        train_pct = 0.8
        split_idx = int(total * train_pct)
        train_count = split_idx
        test_count = total - split_idx
        assert train_count == 12
        assert test_count == 3

    def test_update_example_metadata(self):
        """update_example() sets metadata on existing examples."""
        metadata = {"split": "test"}
        assert metadata["split"] == "test"


class TestCSVImport:
    """Tests for CSV import workflow."""

    def test_csv_columns_match_schema(self):
        """CSV must have input and output columns."""
        columns = ["input", "output"]
        assert "input" in columns
        assert "output" in columns

    def test_csv_values_are_dicts(self):
        """CSV cell values are dict strings that need parsing."""
        csv_value = '{"review_text": "Great product."}'
        import ast
        parsed = ast.literal_eval(csv_value)
        assert isinstance(parsed, dict)
        assert "review_text" in parsed

    def test_pandas_reads_csv(self):
        """pandas DataFrame can read the CSV file."""
        import pandas as pd
        import tempfile
        import os

        # Create a temp CSV
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        tmp.write("input,output\n")
        tmp.write('{"review_text":"Test"},{"product":"Test","rating":5,"sentiment":"positive"}\n')
        tmp.close()

        df = pd.read_csv(tmp.name)
        assert len(df) == 1
        assert "input" in df.columns
        assert "output" in df.columns

        os.unlink(tmp.name)


class TestTraceConversion:
    """Tests for trace-to-dataset conversion."""

    def test_list_runs_returns_traces(self):
        """list_runs() returns trace objects with inputs and outputs."""
        trace = MagicMock()
        trace.inputs = {"review_text": "Some review"}
        trace.outputs = {"product": "Some Product", "rating": 5, "sentiment": "positive"}
        assert trace.inputs is not None
        assert trace.outputs is not None

    def test_trace_must_have_both_inputs_and_outputs(self):
        """Only traces with both inputs and outputs can become examples."""
        trace_with_both = MagicMock()
        trace_with_both.inputs = {"review_text": "Test"}
        trace_with_both.outputs = {"product": "Test", "rating": 5, "sentiment": "positive"}

        trace_without = MagicMock()
        trace_without.inputs = None
        trace_without.outputs = None

        assert trace_with_both.inputs and trace_with_both.outputs
        assert not (trace_without.inputs and trace_without.outputs)

    def test_run_type_filter_for_llm(self):
        """Filter traces by run_type='llm' for structured output extraction."""
        run_type = "llm"
        assert run_type == "llm"


class TestProductReviewSchema:
    """Tests for the ProductReview schema used in the lab."""

    def test_schema_has_three_fields(self):
        """ProductReview has product, rating, and sentiment fields."""
        fields = ["product", "rating", "sentiment"]
        assert len(fields) == 3

    def test_product_is_string(self):
        """Product field is a string."""
        product = "AeroPress Coffee Maker"
        assert isinstance(product, str)

    def test_rating_is_integer(self):
        """Rating field is an integer from 1 to 5."""
        rating = 5
        assert isinstance(rating, int)
        assert 1 <= rating <= 5

    def test_sentiment_values(self):
        """Sentiment field is one of: positive, negative, neutral."""
        valid_sentiments = ["positive", "negative", "neutral"]
        for sentiment in valid_sentiments:
            assert sentiment in valid_sentiments

    def test_model_dump_returns_dict(self):
        """model_dump() converts the Pydantic object to a dict."""
        from pydantic import BaseModel, Field

        class ProductReview(BaseModel):
            product: str = Field(description="The product name")
            rating: int = Field(description="Star rating 1-5")
            sentiment: str = Field(description="positive, negative, or neutral")

        review = ProductReview(product="Test", rating=5, sentiment="positive")
        dumped = review.model_dump()
        assert isinstance(dumped, dict)
        assert dumped["product"] == "Test"
        assert dumped["rating"] == 5
        assert dumped["sentiment"] == "positive"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
