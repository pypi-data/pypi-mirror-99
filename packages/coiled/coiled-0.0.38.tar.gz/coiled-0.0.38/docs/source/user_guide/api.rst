=============
API Reference
=============

.. panels::
   :body: text-center

    :opticon:`file-code,size=24`

    .. link-button:: python-api
        :type: ref
        :text: Python API Reference
        :classes: btn-outline-primary btn-block stretched-link

    ---

    :opticon:`terminal,size=24`

    .. link-button:: command-line-api
        :type: ref
        :text: Command Line API Reference
        :classes: btn-outline-primary btn-block stretched-link


.. _python-api:

Python API Reference
====================

.. currentmodule:: coiled

.. autosummary::
    coiled.create_software_environment
    coiled.create_cluster_configuration
    coiled.create_notebook
    coiled.create_job_configuration
    coiled.list_software_environments
    coiled.list_cluster_configurations
    coiled.list_clusters
    coiled.list_job_configurations
    coiled.list_core_usage
    coiled.list_local_versions
    coiled.delete_software_environment
    coiled.delete_cluster_configuration
    coiled.delete_cluster
    coiled.delete_cluster_configuration
    coiled.Cluster
    coiled.cluster_cost_estimate
    coiled.install
    coiled.start_job
    coiled.stop_job
    coiled.list_jobs
    coiled.info

Software Environments
---------------------
.. autofunction:: coiled.create_software_environment
.. autofunction:: coiled.list_software_environments
.. autofunction:: coiled.delete_software_environment
.. autofunction:: coiled.install
.. autofunction:: coiled.inspect


Cluster Configurations
----------------------
.. autofunction:: coiled.create_cluster_configuration
.. autofunction:: coiled.list_cluster_configurations
.. autofunction:: coiled.delete_cluster_configuration


Clusters
--------
.. autoclass:: coiled.Cluster
    :members:
    :undoc-members:

.. autofunction:: coiled.list_clusters
.. autofunction:: coiled.delete_cluster
.. autofunction:: coiled.cluster_cost_estimate
.. autofunction:: coiled.list_core_usage


Notebooks
---------
.. autofunction:: coiled.create_notebook


Jobs
----
.. autofunction:: coiled.create_job_configuration
.. autofunction:: coiled.delete_job_configuration
.. autofunction:: coiled.list_job_configurations
.. autofunction:: coiled.start_job
.. autofunction:: coiled.stop_job
.. autofunction:: coiled.list_jobs


Information
-----------
.. autofunction:: coiled.list_local_versions
.. autofunction:: coiled.info


.. _command-line-api:

Command Line API Reference
==========================

.. click:: coiled.cli.login:login
   :prog: coiled login
   :show-nested:

.. _coiled-install-api:

.. click:: coiled.cli.install:install
   :prog: coiled install
   :show-nested:

.. click:: coiled.cli.env:create
   :prog: coiled env create
   :show-nested:

.. click:: coiled.cli.env:delete
   :prog: coiled env delete
   :show-nested:

.. click:: coiled.cli.env:list
   :prog: coiled env list
   :show-nested:

.. click:: coiled.cli.env:inspect
   :prog: coiled env inspect
   :show-nested:

.. click:: coiled.cli.kubernetes:create_kubeconfig
   :prog: coiled create-kubeconfig
   :show-nested:
