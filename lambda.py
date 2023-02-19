import boto3

def lambda_handler(event, context):

    #-------------------- Debug ---------------------------
    #print( 'Hello  {}'.format(event))
    #print( 'User Name- {}'.format(event['detail']['userIdentity']['principalId']))
    #print( 'Instance ID- {}'.format(event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']))
    
    # Variables
    instanceId = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
    userNameSTring = event['detail']['userIdentity']['principalId'] 
    
    if ":" in userNameSTring:
        userName  = userNameSTring.split(":")[1]
    else:
        userName  = event['detail']['userIdentity']['userName']  
        
    
    print( 'Instance Id - ' , instanceId)
    print( 'User Name - ' , userName)
    
    
    tagKey = 'owner'
    tagValue = userName
    
    if userName != 'AutoScaling': # to ignore the tagging if instance is scaled by auto scaling group so we can use the custom value of owner as key
        # EC2 tagging
        client = boto3.client('ec2')
        response = client.create_tags(
            Resources=[
                instanceId
            ],
            Tags=[
                {
                    'Key': tagKey,
                    'Value': tagValue
                },
            ]
        )
    
        print(response)
    else:
        print("increased using" , userName)