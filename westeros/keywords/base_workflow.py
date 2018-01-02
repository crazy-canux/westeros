import os
import tempfile

from robot.api import logger
from super_devops.yaml.yaml_wrapper import BaseYaml


class BaseWorkflow(object):

    """Basic keywords every workflow shoud be used.

    If this keyword just for specify workflow, put it in workflows keywords.
    """

    def __init__(self, generic_conf_file=None, *specific_conf_files):
        self.ctx = self.load_configurations(
            generic_conf_file, *specific_conf_files
        )
        self.ctx_tmp_folder = os.path.join(
            tempfile.gettempdir(), 'ctx4westeros'
        )
        if not os.path.exists(self.ctx_tmp_folder):
            os.mkdir(self.ctx_tmp_folder)

        logger.debug("Init BaseWorkflow")

    def load_configurations(
            self,
            global_conf_file,
            *workflow_conf_file,
            **kwargs
    ):
        """Load confirurations in yaml file.

        Run this keyword before every workflow start.
        Every workflow can have different configuration files.
        """
        self.ctx = BaseYaml(global_conf_file, *workflow_conf_file)
        self.ctx[self.ctx.local_tag] += kwargs
        return self.ctx
