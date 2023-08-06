:notoc:

=========
Notebooks
=========

Coiled supports running hosted, sharable notebooks on https://cloud.coiled.io through
the :func:`coiled.create_notebook` interface. This enables you to run Jupyter sessions
on the cloud with no local setup.

.. note::

    Coiled notebooks are currently experimental with new features under active development

When creating a Coiled notebook, you can specify:

- Software to install for use in your Jupyter session
- Any hardware resources to specify (e.g. amount of RAM, number of CPUs)
- Local files to upload for use in the notebook (e.g. a local ``.ipynb`` notebook file)
- Description of the notebook which will be rendered on https://cloud.coiled.io

For example, below is a snippet which creates a "xgboost-demo" Coiled notebook:

.. code-block:: python

    import coiled

    coiled.create_notebook(
        name="xgboost-demo",
        conda={"channels": ["conda-forge"], "dependencies": ["xgboost", "dask"]},
        cpu=2,
        memory="8 GiB",
        files=["analysis.ipynb"],
        description="Analyzes dataset with XGBoost",
    )

.. note::

    Currently any directory structure for uploaded ``files`` will be removed and files
    will be placed in the working directory of the Jupyter session.
    For example, ``/path/to/notebook.ipynb`` will appear as ``notebook.ipynb`` in the
    Jupyter session.

After you've created a notebook, you can run the notebook by navigating to the "Notebooks"
tab on the left sidebar of https://cloud.coiled.io. There you'll find entries for notebooks
you've created (see the screenshot below for an example), each of which has a button
to launch a new Jupyter session for the corresponding notebook.

.. note::

    By default, any Coiled notebooks you create are publicly accessible to other
    Coiled users to promote sharing and collaborating. Private notebooks will be
    added in the future.

.. figure:: images/notebooks.png


Using a custom image
--------------------

By default, the command :func:`coiled.create_notebook` will use the Docker image 
``coiled/notebook:latest`` to create your notebook, this image contains all the 
necessary dependencies and configuration for you to get started using notebooks.

If you want to use a custom image when creating a notebook, you will need to do
some changes on how you create the notebook. 

* Make sure that you have ``jupyterlab`` installed
* Add a custom command to start the notebook

For example, you could create your notebook following this snippet:

.. code-block:: python

    import coiled

    coiled.create_notebook(
        name="my-custom-notebook",
        container="<your custom image>",
        conda=["jupyterlab", "ipywidgets"],
        command=("jupyter", "lab", "--allow-root", "--ip=0.0.0.0", "--no-browser"),
    )

Remember that you can still upload your files using the ``files`` keyword, alternatively
you can copy those files into your custom image and they will be accessible when you start
a notebook.

.. warning::

    Even though you can access your files from your image, you will need to do some admin 
    work if you want to save your work, since notebooks might be shutdown after some
    inactivity, making your changes unrecoverable.