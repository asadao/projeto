#!/bin/bash

# Look for all EC2 instances and add the IDs to an array
echo "Checking for EC2 instances."
INSTANCES=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].{ID:InstanceId}' --output text)

# Cycle through each instance in the array
for instance_id in ${INSTANCES}; do
  echo
  
  echo "- Querying instance-id: ${instance_id} for tag contents..."
  ENVIRONMENT=$(aws ec2 describe-tags --filters "Name=resource-id,Values=${instance_id}" 'Name=key,Values=Ambiente' --query 'Tags[].{Value:Value}' --output text)
  echo "  Application tag contents found: '${ENVIRONMENT}'"

  echo "  Locating volumes attached to ${instance_id}"
  VOLUMES=$(aws ec2 describe-volumes --filters "Name=attachment.instance-id,Values=${instance_id}" --query 'Volumes[*].Attachments[*].{volume_id:VolumeId}' --output text)


  for volume_id in ${VOLUMES}; do
    echo "  - Volume found.  Adding tag data to volume-id: ${volume_id}"
    aws ec2 create-tags --resources ${volume_id} --tags Key=Ambiente,Value="${ENVIRONMENT}"


# Mostra os valores a serem aplicados mais nao aplica, pra aplicar tem que remover o ultimo "echo"
#  for volume_id in ${VOLUMES}; do
#    echo "  - Volume found.  Adding tag data to volume-id: ${volume_id}"
#    echo      aws ec2 create-tags --resources ${volume_id} --tags Key=Aplicacao,Value="${APPLICATION}"
  done
done

