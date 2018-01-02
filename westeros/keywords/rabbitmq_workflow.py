from westeros.auc.infrastructure.manager import InfraManager
from .base_workflow import BaseWorkflow


class RabbitWorkflow(BaseWorkflow):

    def restart_rabbitmq_process(
            self, host=None, username=None, password=None,
            sudo_pw=None, process=None
    ):
        try:
            if not host:
                host = self.ctx.Rabbitmq['host']
                username = self.ctx.Rabbitmq['username']
                password = self.ctx.Rabbitmq['password']
                sudo_pw = self.ctx.Rabbitmq['sudo_pw']

            if not process:
                process = self.ctx.Rabbitmq['process']

            InfraManager(
                self.restart_rabbitmq_process.__name__,
                host, username, password, sudo_pw
            ).restart_process(process)
        except Exception:
            raise
