from google.cloud import compute_v1

def create_instance(project_id, zone, instance_name):
    instance_client = compute_v1.InstancesClient()

    # Define the instance configuration
    instance = compute_v1.Instance()
    instance.name = instance_name
    instance.zone = zone
    instance.machine_type = f"zones/{zone}/machineTypes/n1-standard-1"

    # Define the boot disk
    disk = compute_v1.AttachedDisk()
    disk.boot = True
    disk.auto_delete = True
    disk.type_ = "PERSISTENT"
    disk.initialize_params = compute_v1.AttachedDiskInitializeParams()
    disk.initialize_params.source_image = "projects/debian-cloud/global/images/family/debian-10"

    instance.disks = [disk]

    # Define the network interface
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "global/networks/default"
    instance.network_interfaces = [network_interface]

    # Create the instance
    operation = instance_client.insert(project=project_id, zone=zone, instance_resource=instance)

    print(f"Creating instance '{instance_name}'...")

    # Wait for the operation to complete
    operation_client = compute_v1.GlobalOperationsClient()
    while True:
        result = operation_client.get(project=project_id, operation=operation.name)
        if result.status == 'DONE':
            print("Instance created.")
            break

# Replace these variables with your values
project_id = 'YOUR_PROJECT_ID'
zone = 'us-central1-a'  # Specify your desired zone
instance_name = 'my-instance'

create_instance(project_id, zone, instance_name)
