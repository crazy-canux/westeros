from robot.api import logger

class Listener(object):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        pass

    def start_suite(self, name, attributes):
        logger.info("Start suite.", also_console=True)

    def end_suite(self, name, attributes):
        logger.info("End suite.", also_console=True)

    def start_test(self, name, attributes):
        logger.info("Start test.", also_console=True)

    def end_test(self, name, attributes):
        logger.info("End test.", also_console=True)

    def start_keyword(self, name, attributes):
        logger.info("Start keyword.", also_console=True)

    def end_keyword(self, name, attributes):
        logger.info("End keyword.", also_console=True)

    def log_message(self, message):
        pass

    def message(self, message):
        pass

    def library_import(self, name, attributes):
        pass

    def resource_import(self, name, attributes):
        pass

    def variables_import(self, name, attributes):
        pass

    def output_file(self, path):
        pass

    def log_file(self, path):
        pass

    def report_file(self, path):
        pass

    def xunit_file(self, path):
        pass

    def debug_file(self, path):
        pass

    def close(self):
        logger.info("Exit robot and clean environment.", also_console=True)
