Working with the ``pandas.DataFrame`` objects directly
======================================================

.. warning::
    The package authors are seriously considering re-naming several of the
    classes and DataFrames. The methodology presented below will be the same
    in spirit, but the actual names will change. Soon. Very soon.


The ``CellpyData`` object stores the data in several ``pandas.DataFrame`` objects.
The easies way to get to the DataFrames is by the following procedure:

.. code-block:: python

    # Assumed name of the CellpyData object: cellpy_data

    # get the 'test':
    c = cell_data.cell
    # cellpy_test is now a cellpy Cell object (cellpy.readers.cellreader.Cell)

    # pandas.DataFrame with data vs cycle number (e.g. coulombic efficiency):
    summary_data = c.summary

    # pandas.DataFrame with the raw data:
    raw_data = c.raw

    # pandas.DataFrame with statistics on each step and info about step type:
    step_info = c.steps


You can then manipulate your data with the standard ``pandas.DataFrame`` methods
(and ``pandas`` methods in general).

.. note::
    At the moment, ``CellpyData`` objects can store several sets of test-data
    (several 'tests'). They are stored
    in a list. It is not recommended to utilise this
    *'possible to store multiple tests'* feature as it might be
    removed very soon (have not decided upon that yet).

Happy pandas-ing!
