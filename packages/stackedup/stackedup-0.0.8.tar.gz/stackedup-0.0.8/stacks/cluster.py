import logging

logger = logging.getLogger(__name__)


def get_ec2_instances(stack, boto_session, ecs_service="", container_name=""):  #

    cf_client = boto_session.client("cloudformation")
    stack_details = stack.get_details(cf_client)
    cluster_name = stack.get_parameters()["ClusterStack"]

    service_name = None
    try:
        service_name = [
            d["OutputValue"]
            for d in stack_details["Outputs"]
            if d["OutputKey"] == f"ServiceName{ecs_service}"
        ][0]
    except IndexError:
        logger.error(
            f"Unable to find output ServiceName{ecs_service} " f"in {cluster_name}"
        )
        exit(1)

    # Get the task id from list_tasks
    ecs_client = boto_session.client("ecs")
    response = ecs_client.list_tasks(
        cluster=cluster_name,
        serviceName=service_name,
    )
    task_id = response["taskArns"][0]

    # Get the container instance ARN and the container id from ecs describe_tasks
    response = ecs_client.describe_tasks(cluster=cluster_name, tasks=(task_id,))
    container_instance_id = response["tasks"][0]["containerInstanceArn"]
    container_id = None
    try:
        container_id = [
            d["runtimeId"]
            for d in response["tasks"][0]["containers"]
            if d["name"] == container_name
        ][0]
        logger.info(
            f"Found an instance {container_instance_id} running the container "
            f"{container_id}"
        )
    except KeyError:
        logger.error(f"Unable to find a container id for the task {task_id}")
        exit(1)

    # Get the instance public IP from ec2 describe-instances
    response = ecs_client.describe_container_instances(
        cluster=cluster_name, containerInstances=(container_instance_id,)
    )
    instance_id = response["containerInstances"][0]["ec2InstanceId"]

    ec2_client = boto_session.client("ec2")
    response = ec2_client.describe_instances(InstanceIds=(instance_id,))
    public_dns_name = response["Reservations"][0]["Instances"][0]["PublicIpAddress"]
    return public_dns_name, container_id
