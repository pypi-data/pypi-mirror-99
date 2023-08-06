# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The notebook magic extension module."""
import IPython
from IPython.core.magic import (Magics, magics_class, line_magic)


@magics_class
class Extension(Magics):
    """
    Defines the IPython magic extension for Azure Machine Learning.

    This class identifies the current notebook as the run creation context for any submit run.
    """

    @line_magic
    def CaptureNotebook(self, line):
        """Identify the current notebook as the notebook to be captured upon submitting runs.

        :param line: The magic line.
        :type line: str
        """
        return IPython.display.Javascript(
            "IPython.notebook.kernel.execute(`import os;os.environ['AZUREML_NB_PATH'] =" +
            " '${IPython.notebook.notebook_path}'; import azureml._jupyter_common;`);")


def load_ipython_extension(ipython):
    """Load the extension in the module."""
    ipython.register_magics(Extension)
