.. _grading:

############
Grading API
############

.. contents::
    :local:
    :backlinks: none
    :depth: 2

The grading module provides a reusable API to:

- load a grader configuration from YAML
- generate all configured terrains once and reuse them across many notebook evaluations
- extract ``path_finding`` from notebook submissions
- evaluate one notebook or a zip archive of notebooks
- export the results to CSV


====================
Grader configuration
====================

The grading configuration is a YAML file.
It contains assignment metadata, defaults, and a list of tests.

Example:

.. code-block:: yaml

    version: 1

    assignment:
      id: IA_practica_0
      notebook_function: path_finding
      author_from: file_stem
      author_pattern: null

    defaults:
      oracle: dijkstra
      terrain_type: Terrain
      time_limits:
        max_seconds: 60.0

    tests:
      - id: trivial
        generator: FocusedGenerator
        seeds: [43, 44, 45]
        parameters:
          n: 5
          m: 5
          min_height: 0
          max_height: 0
          min_step: 10
          abruptness: 0.7
          origin: [0, 0]
          destination: [4, 4]

Each test defines:

- ``id`` stable name for the CSV columns
- ``generator`` one of the available terrain generators
- ``seeds`` list of seeds to generate several terrains for the same parameter set
- ``terrain_type`` terrain class to instantiate
- ``parameters`` arguments passed to the generator
- ``oracle`` reference algorithm used to check optimality
- ``time_limits`` timeout configuration

Supported generators:

- ``FocusedGenerator``
- ``PerlinGenerator``
- ``MazeGenerator``

Supported terrain types:

- ``Terrain``
- ``MultipleDestinationTerrain``
- ``SequentialDestinationTerrain``
- ``NoPathTerrain``

Supported named cost functions:

- ``default_cost_function``


==========================
Loading and reusing a suite
==========================

The class ``GraderTestSuite`` stores the parsed configuration, prepared terrain cases, and cached oracle results.
This is the recommended entry point when the same YAML file will be used to evaluate many notebooks.

.. code-block:: python

    from sIArena.grading import GraderTestSuite

    suite = GraderTestSuite.from_yaml("resources/graders/IA_practica_0.yaml")

    # Reuse the same suite for several evaluations
    result_a = suite.evaluate_notebook("alice_submission.ipynb")
    result_b = suite.evaluate_notebook("bob_submission.ipynb")


==================
Notebook execution
==================

Notebook evaluation works in two steps:

1. Read the notebook and find the single code cell that defines ``path_finding``.
2. Execute that cell, retrieve the function, and run it against every terrain of the suite.

The notebook loader is provided by ``NotebookFunctionLoader`` and is used internally by ``GraderTestSuite``.

.. code-block:: python

    from sIArena.grading import GraderTestSuite

    suite = GraderTestSuite.from_yaml("resources/graders/IA_practica_0.yaml")
    notebook_result = suite.evaluate_notebook("alice_submission.ipynb")

    print(notebook_result.submission.author)
    print(notebook_result.comments)


===================
Batch zip grading
===================

The batch grader accepts a zip archive, evaluates every notebook inside it, and can write the final CSV file.

.. code-block:: python

    from sIArena.grading import grade_input_to_csv

    grade_input_to_csv(
        "submissions.zip",
        "resources/graders/IA_practica_0.yaml",
        "results.csv",
    )

For explicit zip grading, ``ZipNotebookGrader`` is also available:

.. code-block:: python

    from sIArena.grading import ZipNotebookGrader

    grader = ZipNotebookGrader.from_yaml("resources/graders/IA_practica_0.yaml")
    batch_result = grader.grade_archive_to_csv("submissions.zip", "results.csv")


================
Result objects
================

The grading module exposes structured result objects:

- ``TerrainEvaluationResult``: one terrain run for one seed
- ``TestEvaluationResult``: aggregated result for one YAML test
- ``FunctionEvaluationResult``: all terrain and test results for one function
- ``NotebookEvaluationResult``: one evaluated notebook submission
- ``SubmissionGrade``: one CSV row worth of grading data
- ``BatchEvaluationResult``: whole archive result

The ``comments`` field is prepared for reporting and CSV export.
When several runs fail with the same error, repeated messages are compressed using counters.

Example:

.. code-block:: text

    20x Function path_finding returned an invalid path: Empty path


=================
CSV report format
=================

The generated CSV contains:

- ``file_name``
- ``author``
- one ``<test_id>_time`` column per configured test
- one ``<test_id>_optimality`` column per configured test
- ``optimality_percentage``
- ``comments``

The ``author`` value comes from the notebook file name.
The default application rule is the text before the first underscore, although the Python API can override it with another regular expression.
