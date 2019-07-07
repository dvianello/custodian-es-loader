import sys

def resource_id(resource_type, resource_obj):

    if resource_type == "ec2":
        return resource_obj['InstanceId']

    elif resource_type == "security-group":
        return resource_obj['GroupId']

    elif resource_type == "ebs":
        return resource_obj['VolumeId']

    elif resource_type == "iam-user":
        return resource_obj['UserId']

    elif resource_type == "asg":
        return resource_obj['AutoScalingGroupARN']

    elif resource_type == "launch-config":
        return resource_obj['LaunchConfigurationARN']

    elif resource_type == "lambda":
        return resource_obj['FunctionArn']

    else:
        print("Unknown resource type {}. Aborting".format(resource_type))
        sys.exit()
