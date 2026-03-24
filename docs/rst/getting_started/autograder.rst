.. _autograder:

##########
Autograder
##########

This project includes a grading API and a runnable application prepared to evaluate notebook submissions against a YAML grader configuration.

The application lives in ``apps/autograder`` and accepts either:

- one notebook file ``.ipynb``
- one zip archive ``.zip`` containing several notebook files

In both cases, the application extracts the function ``path_finding`` from each notebook, runs the configured terrain battery, and writes the results to a CSV file.


===========
Local usage
===========

Run from the repository root:

.. code-block:: bash

    python apps/autograder/autograder.py \
      --input submissions.zip \
      --config resources/graders/IA_practica_0.yaml \
      --output results.csv

To grade a single notebook:

.. code-block:: bash

    python apps/autograder/autograder.py \
      --input resources/exercises/IA_practica_0.ipynb \
      --config resources/graders/IA_practica_0.yaml \
      --output results.csv

The script also accepts:

- ``--iterations`` number of executions per terrain
- ``--debug`` to show debug information while running the tests
- ``--author-pattern`` regular expression used to derive the author from the notebook file name

By default, the application uses the text before the first underscore of the notebook file stem as the author name.
For example, ``alice_submission_1.ipynb`` is reported as author ``alice``.


=============
Docker usage
=============

The autograder application can also run inside a Docker container.

Build the image from the repository root:

.. code-block:: bash

    docker build -f apps/autograder/Dockerfile -t siarena-autograder .

The Docker image installs ``sIArena`` from GitHub.
By default it uses branch ``main``, but another branch, tag or commit can be selected with ``SIARENA_REF``:

.. code-block:: bash

    docker build \
      -f apps/autograder/Dockerfile \
      --build-arg SIARENA_REF=my-branch \
      -t siarena-autograder .

To run the grader, mount the host directory that contains the notebooks and grader YAML file into the container:

.. code-block:: bash

    docker run --rm \
      -v "$PWD:/work" \
      siarena-autograder \
      --input /work/submissions.zip \
      --config /work/resources/graders/IA_practica_0.yaml \
      --output /work/results.csv

The image contains the application code.
The notebooks, zip archives, YAML files, and generated CSV files are provided at runtime through the mounted directory.


==========
CSV output
==========

The generated CSV contains:

- ``file_name``
- ``author``
- one ``<test_id>_time`` column per configured test
- one ``<test_id>_optimality`` column per configured test
- ``optimality_percentage``
- ``comments``

Repeated exceptions are compressed in the ``comments`` column.
For example:

.. code-block:: text

    20x Function path_finding returned an invalid path: Empty path


================
Related material
================

For the Python API and the structure of the grading configuration, see :ref:`grading`.
