# python-entangld

This is a python port of the node.js library `entangld`, which you can checkout
[here](https://github.com/DaxBot/entangld)

## Basic Usage
// TODO

Be sure to checkout the full api [here](API.md)

# TODO
 - GIVE `entangld.Entangld` A `__repr__` for goodness sake!
 - Add more some examples to the readme
 - Add more documentation
 - Add more tests
 - Add limit to set/push request for recursion depth
 - Standardize how methods are treated as sync or async

# Development
Setup the a virtual environment
```bash
 $ python3 -m venv venv
 $ source venv/bin/activate
 (venv) $ pip install -r requirements.txt  # install dependencies
 (venv) $ python setup.py install          # build an installation
```

Run tests like:
```bash
 $ ./scripts/run_tests.sh
```

Build documentation like:
```bash
 $ ./scripts/gen_docs.sh
```

# Pip stuff
To upload to pip, first remove old source packages and build new ones:
```bash
 (venv) $ rm -r build dist entangld.egg-info
 (venv) $ python setup.py sdist
```

Then push it to pip with (with appropriate `~/.pypirc` file):
```bash
 $ ./venv/bin/twine upload dist/*
```
