import boto3
import json
import re

# Descricao
# Esse script pega todos os detalhes de todas as instancias em busca de algumas
# tags e se a intancia possui essas tags ele aplica nos EBS relacionados a instancia

def defineEbsTags():
    # Create the SSM Client
    region_target = 'us-east-1'

    ec2 = boto3.client('ec2',
        region_name=region_target
    )
    ec2Resource = boto3.resource('ec2',
        region_name=region_target
    )

    # Get the requested parameter
    listInstances = ec2.describe_instances()

    countInstances = 0
    countEbs = 0

    for instance in listInstances['Reservations']:
        countInstances +=1
        tags = True
        tag=[]
        try:
            for tags in instance['Instances'][0]['Tags']:
                if tags['Key'] == 'Aplicacao':
                    tag.append({'Key': 'Aplicacao', 'Value': tags['Value']})
                if tags['Key'] == 'Name':
                    tag.append({'Key': 'Name', 'Value': tags['Value']})
                if tags['Key'] == 'Ambiente':
                    tag.append({'Key': 'Ambiente', 'Value': tags['Value']})
        except KeyError:
            tags = False
        if (tags == False):
            print "Instances no tagged: ", instance['Instances'][0]['InstanceId']
            continue
        for ebs in instance['Instances'][0]['BlockDeviceMappings']:
            countEbs += 1
            volume = ec2Resource.Volume(ebs['Ebs']['VolumeId'])
            volume.create_tags(
                DryRun=False,
                Tags= tag
            )
    print "Qtd intances avaliadas: ", countInstances
    print "Qtd volumes avaliados: ", countEbs
    return

defineEbsTags()