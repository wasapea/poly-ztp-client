# Poly ZTP command line client
This repo houses scripts used to easily interface with the Poly Zero Touch Provisioning system.

When an HPBX phone is plugged in it needs to contact a provisioning server to download its configs. This url can be statically set in the phone, delivered by DHCP option 43, or by reaching out to the manufactorer (Poly) and checking their ZTP database. If a customer brings a phone home that does not have a statically set provisioning server url then it has to be set up in Poly ZTP as it wont receive that url over DHCP options from the customer's home router.

This client was written in several different languages to practice making requests in those languages. There is a README within each language's folder with instructions specific to that implimentation.

# Required information
## API key
This is acquired from the Poly ZTP website. You must have a Poly account tied to our organization to retrieve it.

To retrieve the key, follow the below steps

1. Navigate to ztpconsole.poly.com
2. Enter your email to receive a one time code
3. Enter the code you received
4. Click on Integrations
5. Click Manage to the right of Zero Touch Partner API
6. Click the copy button to copy the key

## Polycom MAC addresses
These can be imported from a CSV file or entered manually. The CSV file should have no headers and list one MAC per line. Manual entry still allows for more than one MAC to be input.

## Provisioning profile
Each Metaswitch we own has its own provisioning profile. The program will ask which profile you would like to use. The options are
* HPBX-1 - This points to the Minnesota Metaswitch
* Indy-Meta - This points to the Indy Metaswitch
* CTS-Meta - This points to the Michigan Metaswitch
* jaguar - This should not be used

# Usage
Please consult the README inside each language's folder for instructions.