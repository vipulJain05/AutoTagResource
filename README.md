
# # Automatically tag new AWS resources based on identity or role
### Problem:
EC2 instance and Volume to be tagged with the identity of the provisioner upon resource creation. (For example- Tag-name: **_Owner_** Tag-Value: **_Vipul_**)

### Solution:

To Solve the problem, we have to use the following services:

- **_AWS Cloud Trail_**: AWS CloudTrail is an AWS service that helps you enable operational and risk auditing, governance, and compliance of your AWS account. Actions taken by a user, role, or AWS service are recorded as events in CloudTrail.
- **_AWS Lambda_**: AWS _Lambda_ is a serverless compute service for running code without having to provision or manage servers.
- **_Cloudwatch_**: Amazon CloudWatch collects and visualizes real-time logs, metrics, and event data in automated dashboards to streamline your infrastructure and application maintenance.
- **_IAM ROLE_**: An IAM role is an IAM identity that you can create in your account that has specific permissions.

### Steps to tag AWS resources automatically
-  **AWS Cloudtrail's trail**.
    - [CloudTrail trail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-trails) help to detect and respond to AWS resource creation API events like _RunInstance_ event after launching EC2 instance. If you do not already have a trail, follow the steps in [Creating a Trail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-a-trail-using-the-console-first-time.html) in the AWS CloudTrail User Guide.

- **IAM ROLE**:

    - Create an IAM ROLE which will be used by AWS LAMBDA to automatically attach tags to the service.
    - Create a policy and attach the following JSON file to provide the required permissions to AWS LAMBDA. Make sure to replace `240906956586` with your AWS accountID
    
> {
	"Version": "2012-10-17",
	"Statement": [
    	{
        	"Sid": "VisualEditor0",
        	"Effect": "Allow",
        	"Action": "cloudwatch:PutMetricData",
        	"Resource": "*"
    	},
    	{
        	"Sid": "VisualEditor1",
        	"Effect": "Allow",
        	"Action": [
            	"ec2:CreateTags",
            	"logs:GetLogEvents",
            	"logs:PutLogEvents"
        	],
        	"Resource": [
            	"arn:aws:logs:*:240906956586:log-group:*:log-stream:*",
            	"arn:aws:ec2:*:240906956586:instance/*"
        	]
    	},
    	{
        	"Sid": "VisualEditor2",
        	"Effect": "Allow",
        	"Action": [
            	"logs:CreateLogStream",
            	"logs:DescribeLogGroups",
            	"logs:DescribeLogStreams",
            	"logs:CreateLogGroup"
        	],
        	"Resource": "arn:aws:logs:*:240906956586:log-group:*"
    	}
	]
}


- **AWS LAMBDA**: Lambda is responsible to tag AWS resource automatically.

    - Create a Lambda function with _python 3.9_ runtime and attach the IAM ROLE we created earlier.
    - upload the lambda.py file or paste the file under the **function code** section of the lambda function.
- **Cloudwatch**:

    - Create a rule in CloudWatch Events to trigger on the Amazon EC2  **RunInstances**  API action. For information, see  [Creating a CloudWatch Events Rule That Triggers on an AWS API Call Using AWS CloudTrail](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/Create-CloudWatch-Events-CloudTrail-Rule.html)  in the Amazon CloudWatch Events User Guide. Use the following settings for the rule:

   	 -   For  **Event source**, choose  **Event Pattern**.
   	 -   For  **Service Name**, choose EC2.
   	 -   For  **Event Type**, choose  **AWS API Call via CloudTrail**.
   	 -   Choose  **Specific operation(s)**, and then enter  **RunInstances**.
   	 -   For  **Targets**, choose the Lambda function.


- After all setup, create an EC2 instance from the AWS console or using CLI and after creating the instance, select the instance, and under the tags section, the required tag is automatically added to the instance like **owner: vipul**.

By using the same way we can add tags to any service AWS based on identity or role. We just need to add the specific operation in the cloudwatch event rule (or create new rules for services other than EC2) and change the lambda.py code to add the tag for that service.

**NOTE** If we want to attach the tags to those instances which are created by the AWS Autoscaling group (ASG), there are 2 ways to achieve this

- Add the tags at the time of the creation of AWS ASG so that those tags can automatically be attached with the instance at run time.
- Update the tags of ASG after the creation with the help of the above steps, in this case, all the auto-scaled instances with be tagged with the name of the role/user who created the ASG, the operation name/Event Name for ASG is **CreateAutoScalingGroup**.



