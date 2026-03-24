# Autograder app

This app evaluates one notebook submission (`.ipynb`) or a zip archive of notebooks (`.zip`) against one grader YAML file and writes the results to a CSV file.

## Local usage

Run from the repository root:

```bash
python apps/autograder/autograder.py \
  --input resources/exercises/IA_practica_0.ipynb \
  --config resources/graders/IA_practica_0.yaml \
  --output results.csv
```

For a zip archive:

```bash
python apps/autograder/autograder.py \
  --input submissions.zip \
  --config resources/graders/IA_practica_0.yaml \
  --output results.csv
```

Optional flags:

- `--iterations 3`
- `--debug`
- `--author-pattern '^(?P<author>[^_]+)'`

By default, the author name is extracted from the notebook file stem using the text before the first underscore.

## Build the Docker image

The Docker image installs `sIArena` from GitHub. It does not rely on copying the local library source into the image.

This matters because Docker cannot access files above the build context. If you build with `apps/autograder` as the build context, paths such as `../../src` are not available inside `COPY`. Installing from GitHub avoids that limitation.

Build from the repository root:

```bash
docker build -f apps/autograder/Dockerfile -t siarena-autograder .
```

Use a different branch, tag, or commit with `SIARENA_REF`:

```bash
docker build \
  -f apps/autograder/Dockerfile \
  --build-arg SIARENA_REF=my-branch \
  --no-cache \
  -t siarena-autograder \
  .
```

If you do not pass `SIARENA_REF`, the image uses `main`.

## Run with Docker

Mount your working directory into `/work`:

```bash
docker run --rm \
  -v "$PWD:/work" \
  siarena-autograder \
  --input /work/submissions.zip \
  --config /work/resources/graders/IA_practica_0.yaml \
  --output /work/results.csv
```

For a single notebook:

```bash
docker run --rm \
  -v "$PWD:/work" \
  siarena-autograder \
  --input /work/resources/exercises/IA_practica_0.ipynb \
  --config /work/resources/graders/IA_practica_0.yaml \
  --output /work/results.csv
```

## Output

The generated CSV contains:

- `file_name`
- `author`
- one `<test_id>_time` column per YAML test
- one `<test_id>_optimality` column per YAML test
- `optimality_percentage`
- `comments`

Repeated exceptions are compressed in `comments`, for example:

```text
20x Function path_finding returned an invalid path: Empty path
```
