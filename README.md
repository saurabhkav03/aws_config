# AWS Config

We'll use AWS Config to detect compliant and non-compliant EC2 instances for the following rule:
- A compliant EC2 instance has monitoring enabled.
- A non-compliant EC2 instance does not have monitoring enabled.

## Step 1: Set Up AWS Config

1. Log in to your AWS Management Console.
2. Navigate to the AWS Config service.
3. Click on "Get started" if you're using AWS Config for the first time.
4. Configure the delivery channel settings, which include specifying an Amazon S3 bucket where AWS Config will store configuration history.
5. Choose the resource types you want AWS Config to monitor. In this case, select "Amazon EC2 Instances."

## Step 2: Create a Custom Config Rule

1. Navigate to the AWS Config console.
2. In the left navigation pane, click on "Rules."
3. Click on the "Add rule" button.
4. Choose "Create a custom rule."
5. Give your rule a name and description (e.g., "Monitoring for EC2 Instances").
6. For "Scope of changes," choose "Resources."
7. Define the rule trigger. You can use AWS Lambda as the trigger source. If you haven't already created a Lambda function for this rule, create one that checks whether monitoring is enabled for an EC2 instance. The Lambda function will return whether the resource is compliant or not based on the monitoring status.

## Step 3: Define the Custom Rule in AWS Config

1. Choose your Lambda function from the dropdown list as the evaluator for the rule.
2. Specify the trigger type (e.g., "Configuration changes").
3. Save the rule.

## Step 4: Monitor and Alert

- AWS Config will now continuously evaluate your EC2 instances against the rule you've created.
- If any EC2 instance is found without monitoring enabled, the custom rule's Lambda function will mark it as non-compliant.

**Note:** Below are the permissions that you need to grant to the role that executes the Lambda function used in the project.

[Permissions Required](https://github.com/iam-veeramalla/aws-devops-zero-to-hero/assets/43399466/99e08bdb-17aa-4962-a96a-3cecdb99ee8d)

**Reference Documents:**
- To describe instances: [Boto3 EC2 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)
- For evaluation: [Boto3 Config Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config/client/put_evaluations.html)
