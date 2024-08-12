import asyncio
import meraki.aio
import csv

API_KEY = ''
ORG_ID = ''  # Replace with your actual organization ID

def print_colored(message, color):
    colors = {
        'green': '\033[92m',  # Green text
        'red': '\033[91m',    # Red text
        'purple': '\033[95m', # Purple text
    }
    reset_code = '\033[0m'  # Reset to default text color
    print(f"{colors.get(color, '')}{message}{reset_code}")

async def main():
    async with meraki.aio.AsyncDashboardAPI(api_key=API_KEY,output_log=False) as dashboard:
        try:
            # Get the organization's networks
            networkresponse = await dashboard.organizations.getOrganizationNetworks(ORG_ID)

            # Prepare CSV file
            with open(f'networks_subnets_OrgID_{ORG_ID}.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Network Name', 'Network ID', 'VLAN Number', 'Subnet Name', 'Subnet'])

                for network in networkresponse:
                    network_id = network['id']
                    network_name = network['name']
                    product_types = network.get('productTypes', [])

                    # Check if the network has a security appliance
                    if 'appliance' in product_types:
                        try:
                            # Get the subnets for each network
                            subnets = await dashboard.appliance.getNetworkApplianceVlans(network_id)

                            first_subnet = True
                            for subnet in subnets:
                                vlan_number = subnet['id']
                                subnet_name = subnet['name']
                                subnet_cidr = subnet['subnet']
                                
                                if first_subnet:
                                    writer.writerow([network_name, network_id, vlan_number, subnet_name, subnet_cidr])
                                    first_subnet = False
                                else:
                                    writer.writerow(['', '', vlan_number, subnet_name, subnet_cidr])

                        except meraki.aio.AsyncAPIError as e:
                             print_colored(f"API Error for network {network_name} ({network_id}): {e}", 'red')

        except meraki.aio.AsyncAPIError as e:
            print_colored(f"API Error: {e}", 'red')

if __name__ == '__main__':
    asyncio.run(main())
