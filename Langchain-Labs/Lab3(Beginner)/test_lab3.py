"""Pytest tests for Lab 3: Structured Output.

Follows the TEST.md framework (core logic, output structure, docs-vs-behavior).
The schema classes are exec'd from the notebook's own cells, so these tests
exercise the actual lab code — not a copy. No API calls are made.

Run: python3 -m pytest test_lab3.py -v
"""

import ast
import json
from pathlib import Path

import pytest
from pydantic import BaseModel, Field, ValidationError

NB_PATH = Path(__file__).with_name("lab-structured-output.ipynb")


def code_cells():
    with open(NB_PATH) as f:
        notebook = json.load(f)
    return ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


def run_class_definitions(class_names, namespace=None):
    """Exec just the class definitions (not whole cells) for the given names."""
    namespace = namespace or {}
    for source in code_cells():
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue  # e.g. the !pip install shell-magic cell is not valid Python
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name in class_names:
                exec(compile(ast.Module(body=[node], type_ignores=[]), "<cell>", "exec"), namespace)
    missing = set(class_names) - set(namespace)
    if missing:
        raise AssertionError(f"Class definitions not found: {missing}")
    return namespace


@pytest.fixture(scope="module")
def schemas():
    """Import the pydantic classes from the notebook's class definitions."""
    namespace = {"BaseModel": BaseModel, "Field": Field}
    run_class_definitions({"Movie", "ProductReview"}, namespace)
    return namespace


class TestMovieSchema:
    """Docs-vs-behavior: the Movie schema matches what the lab teaches."""

    def test_movie_is_base_model(self, schemas):
        assert issubclass(schemas["Movie"], schemas["BaseModel"])

    def test_movie_field_types(self, schemas):
        movie = schemas["Movie"]
        assert movie.model_fields["title"].annotation is str
        assert movie.model_fields["director"].annotation is str
        assert movie.model_fields["year"].annotation is int

    def test_movie_descriptions_present(self, schemas):
        movie = schemas["Movie"]
        assert movie.model_fields["title"].description == "The movie's title"
        assert movie.model_fields["year"].description == "The movie's release year"

    def test_movie_validates_good_data(self, schemas):
        movie = schemas["Movie"](
            title="Inception",
            director="Christopher Nolan",
            year=2010,
        )
        assert movie.year == 2010
        assert isinstance(movie.year, int)

    def test_movie_rejects_bad_year(self, schemas):
        with pytest.raises(ValidationError):
            schemas["Movie"](
                title="Inception",
                director="Christopher Nolan",
                year="two thousand and ten",
            )


class TestProductReviewSchema:
    """The extraction schema used in Steps 8 and 9."""

    def test_review_is_base_model(self, schemas):
        assert issubclass(schemas["ProductReview"], schemas["BaseModel"])

    def test_review_field_types(self, schemas):
        review = schemas["ProductReview"]
        assert review.model_fields["product"].annotation is str
        assert review.model_fields["rating"].annotation is int
        assert review.model_fields["sentiment"].annotation is str

    def test_review_validates(self, schemas):
        review = schemas["ProductReview"](
            product="AeroPress Coffee Maker", rating=5, sentiment="positive"
        )
        assert review.model_dump() == {
            "product": "AeroPress Coffee Maker",
            "rating": 5,
            "sentiment": "positive",
        }


class TestNotebookArtifact:
    """CQ-10: the first code cell is a single pinned `!pip install` line."""

    def test_first_code_cell_is_single_pinned_pip_install(self):
        lines = code_cells()[0].splitlines()
        pip_lines = [ln for ln in lines if ln.startswith("!pip install")]
        assert len(pip_lines) == 1
        for line in lines:
            if line.startswith("!pip install"):
                break
            assert line.strip() == "" or line.startswith("#")
        packages = [tok.strip('"') for tok in pip_lines[0].split()[2:] if not tok.startswith("-")]
        assert packages, "install line lists at least one module"
        assert all("==" in pkg for pkg in packages), "every module must be pinned"
