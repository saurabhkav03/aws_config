
import json
import boto3

def lambda_handler(event, context):

    compliance_status = "COMPLIANT"

#boto3.client('ec2'): Creates a client object for interacting with EC2 (Elastic Compute Cloud) service.
#boto3.client('config'): Creates a client object for interacting with AWS Config service.
    ec2_client = boto3.client('ec2')
    config_client = boto3.client('config')

#This line uses the json.loads() function to parse the JSON data stored in the invokingEvent field of the event parameter.
#It converts the JSON string into a Python dictionary and stores it in the variable config.
    config = json.loads(event['invokingEvent'])
    config_item = config["configurationItem"]
    instance_id = config_item["configuration"]["instanceId"]

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html
#This part calls the describe_instances method of the EC2 client (ec2_client). It retrieves information about EC2 instances based on the provided parameters. In this case, it specifies the InstanceIds parameter with a list containing a single instance ID (instance_id), indicating that information about a specific instance is requested.
    instance = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]

#Checks if detailed monitoring (CloudWatch monitoring) is enabled for the EC2 instance.
#If monitoring state is not "enabled", it marks the instance as "NON_COMPLIANT".
    if not instance['Monitoring']['State'] == 'enabled':
        compliance_status = "NON_COMPLIANT"


#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_evaluations.html

#Constructs an evaluation object containing information about compliance status, resource type, resource ID, annotation, and ordering timestamp.
#This object will be used to report the compliance status to AWS Config.
    evaluation = {
        'ComplianceResourceType': 'AWS::EC2::Instance',
        'ComplianceResourceId': instance_id,
        'ComplianceType': compliance_status,
        'Annotation': 'Detailed monitoring is not enabled',
        'OrderingTimestamp': config['notificationCreationTime']
    }

#Uses the put_evaluations method of the AWS Config client to report the evaluation results.
#It passes the evaluation object and the resultToken from the event parameter.
    response = config_client.put_evaluations(
        Evaluations=[evaluation],
        ResultToken=event['resultToken']
    )

    return response