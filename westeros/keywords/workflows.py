from robot.api import logger
from super_devops.robotframework.listener import Listener

from westeros import __version__
from .database_workflow import DatabaseWorkflow
from .rabbitmq_workflow import RabbitWorkflow
from .browser_workflow import BrowserWorkflow
from .rest_workflow import RestWorkflow


class Workflows(DatabaseWorkflow,
                RabbitWorkflow,
                BrowserWorkflow,
                RestWorkflow):

    ROBOT_LIBRARY_SCOPY = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LIBRARY_DOC_FORMAT = 'ROBOT'

    def __init__(self, generic_conf_file=None, *specific_conf_files):
        super(Workflows, self).__init__(
            generic_conf_file, *specific_conf_files
        )

        self.ROBOT_LIBRARY_LISTENER = Listener()

        logger.debug("Init Worflows.")

    def clean_environment(self):
        """Clean the environment.

        Run this keyword before every workflow started.
        Clean everything created in last workflow.
        """
        self.restart_rabbitmq_process()

    def backup_environment(self):
        """Backup the environment.

        Run this keyword after every workflow finished.
        Backup logs, storages and content inside this workflow.
        """
        # TODO: backup logs, metrics, tempfiles.
        pass

    def setup_environment(self):
        """Setup major.minor on cluster."""
        pass

    def update_environment(self):
        """Update patch on cluster."""
        pass

    def destroy_environment(self):
        """Uninstall the whole cluster."""
        pass
