(Get-EC2Instance).Instances | ` # Get EC2 instances and pass to pipeline
ForEach-Object -Process {
    # Get the name tag of the current instance ID; Amazon.EC2.Model.Tag is in the Instances object
    $instanceName = $_.Tags | Where-Object -Property Key -EQ "Name" | Select-Object -ExpandProperty Value
    $_.BlockDeviceMappings | ` # Pass all the current block device objects down the pipeline
    ForEach-Object -Process {
        $volumeid = $_.ebs.volumeid # Retrieve current volume id for this BDM in the current instance
        # Get the current volume's Name tag
        $volumeNameTag = Get-EC2Tag -Filter @(@{ name = 'tag:Name'; values = "*" }; @{ name = "resource-type"; values = "volume" }; @{ name = "resource-id"; values = $volumeid }) | Select-Object -ExpandProperty Value
        
        if (-not $volumeNameTag) # Replace the tag in the volume if it is blank
        {
            New-EC2Tag -Resources $volumeid -Tags @{ Key = "Name"; Value = $instanceName } # Add volume name tag that matches InstanceID
        }
    }
}