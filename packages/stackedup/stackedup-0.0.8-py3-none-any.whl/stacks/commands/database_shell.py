import logging
from os import path

from stacks.config import (
    config_get_stack_config,
    config_get_stack_region,
    config_get_role,
)

from stacks.stack import Stack

from stacks.command import (
    InstanceCommand,
)

from stacks.cluster import cluster_instance_ip

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format="%(levelname)s - %(message)s")


class DatabaseShellCommand(InstanceCommand):
    def __init__(self):
        super().__init__()
        stack_type = "application"
        stack_config_instance = config_get_stack_config(
            self.config, stack_type, self.args.name
        )
        self.stack = Stack(
            project_name=self.project_name,
            stack_type=stack_type,
            name=self.args.name,
            stack_config=stack_config_instance,
            region=config_get_stack_region(self.config, stack_type, self.args.name),
        )

        cluster_name = stack_config_instance["cluster"]
        stack_config_cluster = config_get_stack_config(
            self.config, "cluster", cluster_name
        )
        self.cluster_stack = Stack(
            project_name=self.project_name,
            stack_type="cluster",
            name=cluster_name,
            stack_config=stack_config_cluster,
            region=config_get_stack_region(self.config, stack_type, self.args.name),
        )

    def add_arguments(self):
        super().add_arguments()
        self.argparser.add_argument("service", type=str)
        self.argparser.add_argument("ecsservice", type=str)
        self.argparser.add_argument("container_name", type=str)

    def run(self):

        key_name = self.cluster_stack.get_parameters()["KeyName"]
        ssh_key = path.join(path.expanduser("~"), ".ssh", key_name)
        if not path.exists(ssh_key):
            logger.error(f"Could not find the required SSH key {ssh_key}")
            exit(1)

        public_dns_name, container_id = cluster_instance_ip(self.stack, foo)

        ssh_command = (
            f"ssh -t -i ~/.ssh/{key_name} ec2-user@{public_dns_name} "
            f"docker exec -it {container_id} sh"
        )
        print(ssh_command)


def run():
    cmd = ContainerShellCommand()
    cmd.run()
