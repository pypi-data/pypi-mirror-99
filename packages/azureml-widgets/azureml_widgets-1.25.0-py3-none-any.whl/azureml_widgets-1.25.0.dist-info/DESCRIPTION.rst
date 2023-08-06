Project description
==========================================
.. _`AzureML Widgets` : https://docs.microsoft.com/en-us/python/api/azureml-widgets/?view=azure-ml-py

`AzureML Widgets`_ are fully supported, with interactivity, async auto-updates, and non-blocking cell execution. These widgets will be a way to monitor jobs as they run, monitor logs, and stream useful charts.

Within a Jupyter notebook, widgets should be used to display the main highlights of the current run, for more run information the user will switch to the full Run Details page. 

Setup
==========================================

.. _instructions : https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-environment#local

Follow these instructions_ to install the Azure ML SDK on your local machine, create an Azure ML workspace, and set up your notebook environment, which is required for the next step.

Once you have set up your environment, install the Azure ML Widget SDK::

    pip install azureml-widgets


azureml-widget supported runs
==========================================
The following types of runs are supported:

.. _StepRun : https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.steprun?view=azure-ml-py
.. _HyperDriveRun : https://docs.microsoft.com/en-us/python/api/azureml-train-core/azureml.train.hyperdrive.hyperdriverun?view=azure-ml-py>
.. _AutoMLRun : https://docs.microsoft.com/en-us/python/api/azureml-train-automl-client/azureml.train.automl.run.automlrun?view=azure-ml-py
.. _PipelineRun : https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.run.pipelinerun?view=azure-ml-py
.. _ReinforcementLearningRun : https://docs.microsoft.com/en-us/python/api/azureml-contrib-reinforcementlearning/azureml.contrib.train.rl.reinforcementlearningrun?view=azure-ml-py

* StepRun_ : Shows run properties, output logs, metrics.

* HyperDriveRun_ : Shows parent run properties, logs, child runs, primary metric chart, and parallel coordinate chart of hyperparameters.

* AutoMLRun_ : Shows child runs and primary metric chart with option to select individual metrics.

* PipelineRun_ : Shows running and non-running nodes of a pipeline along with graphical representation of nodes and edges.

* ReinforcementLearningRun_ : Shows status of runs in real time. Azure Machine Learning Reinforcement Learning is currently a preview feature. For more information, see Reinforcement learning with Azure Marchine Learning.

Resources
==========================================
.. _`Monitor and view ML run logs and metrics` : https://docs.microsoft.com/en-us/azure/machine-learning/how-to-monitor-view-training-logs
.. _`AzureML Widgets SDK Docs` : https://docs.microsoft.com/en-us/python/api/azureml-widgets/?view=azure-ml-py

`Monitor and view ML run logs and metrics`_

`AzureML Widgets SDK Docs`_ 




