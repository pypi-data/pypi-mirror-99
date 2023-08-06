
# Table of Contents

1.  [CSV Reconcile](#orga5c90a9)
    1.  [Quick start](#org1b422ae)
    2.  [Poetry](#org8b4627b)
    3.  [Description](#org86e08ad)
    4.  [Usage](#org55ecd97)
    5.  [Common configuration](#orge7e9f64)
    6.  [Scoring plugins](#org93437fb)
        1.  [Implementing](#org02825f9)
        2.  [Installing](#orgf9bbffa)
        3.  [Using](#orgce3ac9e)
    7.  [Future enhancements](#orga668c9a)


<a id="orga5c90a9"></a>

# CSV Reconcile

A [reconciliation service](https://github.com/reconciliation-api/specs) for [OpenRefine](https://openrefine.org/) based on a CSV file similar to [reconcile-csv](http://okfnlabs.org/reconcile-csv/).  This one is written in Python and has some more configurability.


<a id="org1b422ae"></a>

## Quick start

-   Clone this repository
-   Run the service
    
        $ python -m venv venv                                             # create virtualenv
        $ venv/bin/pip install dist/csv_reconcile-0.1.0-py3-none-any.whl  # install package
        $ source venv/bin/activate                                        # activate virtual environment
        (venv) $ csv-reconcile --init-db sample/reps.tsv item itemLabel   # start the service
        (venv) $ deactivate                                               # remove virtual environment

The service is run at <http://127.0.0.1:5000/reconcile>.  You can point at a different host:port by
adding [SERVER\_NAME](https://flask.palletsprojects.com/en/0.12.x/config/) to the sample.cfg.  Since this is running from a virtualenv, you can simply
delete the whole lot to clean up.

If you have a C compiler installed you may prefer to install the sdist
`dist/csv-reconcile-0.1.0.tar.gz` which will build a [Cython](https://cython.readthedocs.io/en/latest/) version of the computationally
intensive fuzzy match routine for speed.


<a id="org8b4627b"></a>

## Poetry

This is packaged with [poetry](https://python-poetry.org/docs/), so you can use those commands if you have it installed.

    $ poetry install
    $ poetry run csv-reconcile --init-db sample/reps.tsv item itemLabel


<a id="org86e08ad"></a>

## Description

This reconciliation service uses [Dice coefficient scoring](https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient) to reconcile values against a given column
in a [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) file.  The CSV file must contain a column containing distinct values to reconcile to.
We'll call this the *id column*.  We'll call the column being reconciled against the *name column*.

For performance reasons, the *name column* is preprocessed to normalized values which are stored in
an [sqlite](https://www.sqlite.org/index.html) database.  This database must be initialized at least once by passing the `--init-db` on
the command line.  Once initialized this option can be removed from subsequent runs.

Note that the service supplies all its data with a dummy *type* so there is no reason to reconcile
against any particular *type*.

In addition to reconciling against the *name column*, the service also functions as a [data extension
service](https://reconciliation-api.github.io/specs/latest/#data-extension-service), which offers any of the other columns of the CSV file.

Note that Dice coefficient scoring is agnostic to word ordering.


<a id="org55ecd97"></a>

## Usage

Basic usage requires passing the name of the CSV file, the *id column* and the *name column*.

    $ poetry run csv-reconcile --help
    Usage: csv-reconcile [OPTIONS] CSVFILE IDCOL NAMECOL
    
    Options:
      --config TEXT  config file
      --scorer TEXT  scoring plugin to use
      --init-db      initialize the db
      --help         Show this message and exit.
    $

In addition to the `--init-db` switch mentioned above you may use the `--config` option to point to
a configuration file.  The file is a [Flask configuration](https://flask.palletsprojects.com/en/1.1.x/config/) and hence is Python code though most
configuration is simply setting variables to constant values.


<a id="orge7e9f64"></a>

## Common configuration

-   `SERVER_NAME`  - The host and port the service is bound to.
    e.g. `SERVER_NAME=localhost:5555`.  ( Default localhost:5000 )
-   `CSVKWARGS`  - Arguments to pass to [csv.reader](https://docs.python.org/3/library/csv.html).
    e.g. `CSVKWARGS={'delimiter': ',',  quotechar='"'}` for comma delimited files using `"` as quote character.
-   `CSVECODING` - Encoding of the CSV file.
    e.g. `CSVECODING='utf-8-sig'` is the encoding used for data downloaded from [GNIS](https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data).
-   `SCOREOPTIONS`  - Options passed to scoring plugin during normalization.
    e.g. `SCOREOPTIONS={'stopwords':['lake','reservoir']}`
-   `LIMIT`      - The maximum number of reonciliation candidates returned per entry.  ( Default 10 )
    e.g. `LIMIT=10`
-   `THRESHOLD`  - The minimum score for returned reconciliation candidates.  ( Default 30.0 )
    e.g. `THRESHOLD=80.5`
-   `DATABASE`   - The name of the generated sqlite database containing pre-processed values.  (Default `csvreconcile.db`)
    e.g. `DATABASE='lakes.db'`  You may want to change the name of the database if you regularly switch between databases being used.
-   `MANIFEST`   - Overrides for the service manifest.
    e.g. `MANIFEST={"name": "My service"}` sets the name of the service to "My service".

This last is most interesting.  If your data is coming from [Wikidata](https://www.wikidata.org) and your *id column*
contains [Q values](https://www.wikidata.org/wiki/Help:Items), then a manifest like the following will allow your links to be clickable inside OpenRefine.

    MANIFEST = {
      "identifierSpace": "http://www.wikidata.org/entity/",
      "schemaSpace": "http://www.wikidata.org/prop/direct/",
      "view": {"url":"https://www.wikidata.org/wiki/{{id}}"},
      "name": "My reconciliation service"
    }

If your CSV is made up of data taken from another [reconciliation service](https://reconciliation-api.github.io/testbench/), you may similiarly copy
parts of their manifest to make use of their features, such as the [preview service](https://reconciliation-api.github.io/specs/latest/#preview-service).  See the
reconciliation spec for details.


<a id="org93437fb"></a>

## Scoring plugins

As mentioned above the default scoring method is to use [Dice coefficient scoring](https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient), but this method
can be overridden by implementing a `cvs_reconcile.scorers` plugin.


<a id="org02825f9"></a>

### Implementing

A plugin module may override any of the methods in the `csv_reconcile.scorers` module by simply
implementing a method of the same name with the decorator `@cvs_reconcile.scorer.register`.

See `csv_reconcile_dice` for how Dice coefficient scoring is implemented.

The basic hooks are as follows:

-   `normalizedWord(word, **scoreOptions)` preprocesses values to be reconciled to produce a
    tuple used in fuzzy match scoring.  Note that this preprocessing happens for both the value to
    be reconciled and to all the values in the csv column to be reconciled against.  The value of
    `SCOREOPTIONS` in the configuration will be passed in to allow configuration of this
    preprocessing.  This hook is required.
-   `getNormalizedFields()` returns a tuple of names for the columns produced by `normalizeWord()`.
    The length of the return value from both functions must match.  This hook is required.
-   `processScoreOptions(options)` is passed the value of `SCOREOPTIONS` to allow it to be adjusted
    prior to being used.  This can be used for adding defaults and/or validating the configuration.
    This hook is optional
-   `scoreMatch(left, right)` gets passed two tuples as returned by `normalizedWord()`.  The `left`
    value is the value being reconciled and the `right` value is the value being reconciled
    against.  This hook is required.
-   `valid(normalizedFields)` is passed the normalized tuple prior to being scored to make sure
    it's appropriate for the calculation.  This hook is optional.


<a id="orgf9bbffa"></a>

### Installing

Hooks are automatically discovered as long as they provide a `csv_reconcile.scorers` [setuptools
entry point](https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html).  Poetry supplies a [plugins](https://python-poetry.org/docs/pyproject/#plugins) configuration which wraps the setuptools funtionality.

The default Dice coefficent scoring is supplied via the following snippet from `pyproject.toml`
file.

    [tool.poetry.plugins."csv_reconcile.scorers"]
    "dice" = "csv_reconcile_dice"

Here `dice` becomes the name of the scoring option and `csv_reconcile_dice` is the package
implementing the plugin.


<a id="orgce3ac9e"></a>

### Using

If there is only one scoring plugin available, that plugin is used.  If there are more than one
available, you will be prompted to pass the `--scorer` option to select among the scoring options.


<a id="orga668c9a"></a>

## Future enhancements

It would be nice to add support for using [properties](https://reconciliation-api.github.io/specs/latest/#structure-of-a-reconciliation-query) as part of the scoring, so that more than
one column of the csv could be taken into consideration.

