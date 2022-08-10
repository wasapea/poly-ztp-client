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

Place this key in a file called `apikey` in this folder.

## Polycom MAC addresses
These can be imported from a CSV file or entered manually. The CSV file should have no headers and list one MAC per line. Manual entry still allows for more than one MAC to be input.

Place the CSV in the csvs folder in the parent directory.

## Provisioning profile
Each Metaswitch we own has its own provisioning profile. The program will ask which profile you would like to use. The options are
* HPBX-1 - This points to the Minnesota Metaswitch
* Indy-Meta - This points to the Indy Metaswitch
* CTS-Meta - This points to the Michigan Metaswitch
* jaguar - This should not be used

# Usage
Run `main.py`. Several questions will be asked in the CLI window you ran the script from.

* Startup
    * The script contacts Poly ZTP to download profile names and IDs
* User questions
    * Do you want to import a CSV file?
        * Accepts Y, y, Yes, yes, N, n, No, no
        * If you choose not to import a CSV you can still enter multiple MACs via the CLI
    * What would you like to do?
        * Check if a device exists in ZTP
            * Make a GET request to the Poly ZTP devices endpoint
            * Determine if the device exists by checking status code and return message 
            * List what profile it's tied to (if any)
        * Register a device in ZTP
            * Print the available profiles and ask user to make a choice
            * Make a POST request to the Poly ZTP registration endpoint
        * Remove an existing device from ZTP
            * Make a DELETE request to the Poly ZTP device endpoint
    * Would you like to make another choice with the same MACs?
        * Repeat the above