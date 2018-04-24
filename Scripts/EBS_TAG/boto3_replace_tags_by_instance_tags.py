import boto3
import json
import re

def defineNewParameters():
    # Create the SSM Client
    ec2 = boto3.client('ec2',
        region_name='sa-east-1'
    )
    ec2Resource = boto3.resource('ec2',
        region_name='sa-east-1'
    )

    # Get the requested parameter
    listInstances = ec2.describe_instances()

    for instance in listInstances['Reservations']:
        tag=[]
        print "INSTANCES---------------------------------"
        print instance['Instances'][0]['InstanceId']
        print "TAGS---------------------------------"
        try:
            print instance['Instances'][0]['Tags']
            for tags in instance['Instances'][0]['Tags']:
                if tags['Key'] == 'Aplicacao':
                    print 'Aplicacao: ', tags['Value']
                    tag.append({'Key': 'Aplicacao', 'Value': tags['Value']})
                if tags['Key'] == 'Name':
                    print 'Name: ', tags['Value']
                    tag.append({'Key': 'Name', 'Value': tags['Value']})
                if tags['Key'] == 'Ambiente':
                    print 'Ambiente: ', tags['Value']
                    tag.append({'Key': 'Ambiente', 'Value': tags['Value']})
        except KeyError:
            print "NO TAGS ---------------------------------------------------------"
        print "EBS---------------------------------"
        for ebs in instance['Instances'][0]['BlockDeviceMappings']:
            print ebs['Ebs']['VolumeId']
            volume = ec2Resource.Volume(ebs['Ebs']['VolumeId'])
            print volume
            print tag
            volume.create_tags(
                DryRun=False,
                Tags= tag
            )

    return
    #contador
    num = 0

    #o prefixo que sera adicionado na nova variavel
    prefix = 'secParam-'

    for i in listParameters['Parameters']:
        #nao executa novamente as variaveis ja migradas
        if i['Name'].find(prefix) >= 0:
            continue
        #contador para controlar a quantidade de variaveis migradas
        num=num+1
        print num
        #nome da variavel que sera migrada
        print "Parameters:", i['Name']
        #para cada parametro busca os detalhes que traz os valores
        detailParameter = ssm.get_parameters(
            Names=[
                i['Name'],
            ],
            WithDecryption=True
        )
        #como nem todos os parameters stores tem descricao precisou fazer esse
        #tratamento
        description = ''
        try:
            description = i['Description']
        except KeyError:
            description = ''
        continue

        #os valores das atuais variaveis tem export no inicio e essa parte remove esse prefixo
        strReplacedExport = re.sub(r'export', '', detailParameter['Parameters'][0]['Value'])
        strReplacedExportOneLine = re.sub(r'(?:\n|\r\n?)', '', strReplacedExport)

        #o limite na AWS eh de 4096 caracteres esse tratamento pula as variaveis com mais de 4096 caracteres
        if len(strReplacedExportOneLine) > 4096:
            print "Possui mais do que 4096 caracteres e sera ignorado -> " , i['Name']
            continue

        newName = prefix + i['Name']

        #cria o novo parametro
        putParameter = ssm.put_parameter(
            Name=newName,
            Description=description,
            Value=strReplacedExportOneLine,
            Type='SecureString',
            Overwrite=True
        )
        break
defineNewParameters()
