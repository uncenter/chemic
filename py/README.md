# Chemic

Chemic is a Python library for chemistry. It is designed to be easy to use and to provide a simple interface to search for information and to perform calculations.

The core of Chemic can be found in `main.py` and `utils.py`. The `main.py` file contains the main functions for searching and calculating. The `utils.py` file contains the functions for parsing the data files and for performing calculations.

## Installation

Chemic is available on PyPI. To install, run the following command:

```sh
pip install chemic
```

## Usage

### Importing Chemic

To use Chemic, import it into your Python script:

```python
import chemic
```

### Run the CLI

To start the CLI, add/adjust the following to your Python script:

```python
from chemic import run

run.cli()
```

### Start the GUI

To start the GUI, add/adjust the following to your Python script:

```python
from chemic import run

run.gui()
```

This will start a local server and open a web browser to the GUI.

## Development

You can run Chemic without installing by grabbing the `build/main.py` file on GitHub. Also in the `build` folder is the `chemic` installable. Run it and ignore any errors in the console.
