# MerakiMXVlansSubnetsCSV

This script creates a CSV of every network that has an MX in it with the subnets and vlans configured for the MX

Prerequisites: Python version 3 3 python modules are needed for this script. To download or update the modules run: pip3 install asyncio pip3 install meraki.aio pip3 install csv You will need your Meraki API key with org wide read or read&write access You will need the organization number you wish to run the script against. You can get this on dashboard at the very bottom of the page "Data for Example Company (organization ID: 123456787) is hosted in United States". Or you can get the org ID through API call getOrganizations

Before you execute the script: Edit line 5 and enter your API key Edit line 6 and enter the org ID

After you execute the script it will save a CSV file to the directory in which the script is executed from.
