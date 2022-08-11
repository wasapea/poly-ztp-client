#!/usr/bin/env python
"""A cli client for interacting with the Poly ZTP system
Poly ZTP allows us to set a provisioning URL for phones that cannot receive it via DHCP option 66 and do not have it hardcoded
"""
import os, sys
import json, csv, re
import requests
from pprint import pprint
import argparse

__author__ = "Skylar Baker"
__version__ = ".1"
__status__ = "Development"
__maintainer__ = "Skylar Baker"
__email__ = "skylar.baker@metronet.com"

def parse_args():
    parser=argparse.ArgumentParser(description="CLI client for Poly ZTP")
    parser.add_argument("-m", "--mac", nargs='+', help="MACs to query separated by spaces. If none are specified the user will be prompted to enter them via the CLI or upload a csv")
    parser.add_argument("-k", "--key", help="API key to use, if none is supplied it will load from the apikey file")
    args = parser.parse_args()
    return args

def get_yes_no(question, default=False):
    """Get a yes or no answer from the user

    Args:
        question (string): Question for the user

    Returns:
        bool: User's answer of yes/no converted to True/False
    """
    regex_yes = re.compile("^yes|Yes|Y|y$")
    regex_no = re.compile("^no|No|N|n$")
    answer = input(f"{question}\n")
    if answer == '':
        return default
    elif re.match(regex_yes, answer):
        return True
    elif re.match(regex_no, answer):
        return False
    else:
        print("Please input yes or no")
        return get_yes_no(question)
        
def get_mac(question, mac='', line=''):
    """Get input from the user and make sure it's a mac address
    If a mac and line number are specified, instead verify the mac is legitimate

    Args:
        question (string): Question to ask the user

    Returns:
        string: User's answer
    """
    if not mac:
        answer = input(f"{question}\n")
    else:
        answer = mac
    regex = re.compile('^\S{2}[\s:\.-]?\S{2}[\s:\.-]?\S{2}[\s:\.-]?\S{2}[\s:\.-]?\S{2}[\s:\.-]?\S{2}[\s:\.-]?$')
    if re.match(regex, answer):
        return answer.replace(":", "").replace("-", "").replace(" ", "")
    else:
        if mac and line:
            print(f"{mac} on line {line} is not a valid mac address")
            sys.exit(1)
        elif mac:
            print(f"{mac} is not a valid mac address")
            sys.exit(1)
        else:
            return get_mac(question)

def import_macs():
    """Import a csv of mac addresses

    Returns:
        list: List of mac addresses
    """
    csvs_exist = os.path.exists('../csvs')
    if not csvs_exist:
        print("Please create a folder named 'csvs' in the same directory as this file")
        sys.exit(1)
    files = os.listdir('csvs')
    csvs = []
    count = 1
    for f in files:
        if ".csv" in f:
            print(f"{count}: {f}")
            csvs.append(f)
            count += 1
    if count == 1:
        print("Please add a .csv file to the csvs folder. The CSV should have no header and have one mac per line")
        sys.exit(1)
    while True:
        answer = input("Which file would you like to scan?\nPlease enter the number\n")
        try:
            answer = int(answer)
            if 1 <= answer < count:
                answer = csvs[answer-1]
                break
            else:
                print(f"Please input a number between 1 and {count-1}")
        except:
            print("Please input a number")

    macs = []
    with open(f"csvs/{answer}") as f:
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if "MAC" in row:
                line_count += 1
                pass
            else:
                line_count += 1
                verified_mac = get_mac("", mac=row[0], line=line_count)
                macs.append(verified_mac)

    return macs

def get_choice(question, choices):
    """Asks a user a multiple choice question and returns the index of their choice in the list

    Args:
        question (string): Question to ask the user
        choices (list): List of questions for the user

    Returns:
        int: Index in the list of the selected choice
    """
    count = 1
    print(f"{question}")
    for c in choices:
        print(f"{count}: {c}")
        count += 1
    while True:
        answer = input()
        try:
            answer = int(answer)
            if 0 < answer < count:
                return answer-1
            else:
                print(f"Please enter a number between 1 and {count-1}")
        except:
            print(f"Please enter a number between 1 and {count-1}")

def load_profiles(url, headers):
    """Query API for profiles and return a list of them

    Args:
        url (string): URL of the API
        headers (dict): Headers for the request

    Returns:
        list: List of profiles attached to our account
    """
    profile_response = requests.get(f"{url}/profiles", headers=headers)
    if not profile_response.status_code == 200:
        print("Unable to load profiles from Poly ZTP. Is your api key correct?")
        sys.exit(1)
    profiles = []
    profile_data = json.loads(profile_response.content)["results"]
    for p in profile_data:
        profiles.append({"name": p["name"], "id": p["id"]})
    return profiles

def check_devices(url, headers, macs, profiles):
    """Get information on wanted devices

    Args:
        url (string): URL of the API
        headers (dict): Headers for the request
        macs (list): List of mac addresses
        profiles (list): List of ZTP profiles
    """
    for m in macs:
        device = {"mac":m, "profile name":"Not found", "profile id":"Not found"}
        try:
            device_response = requests.get(f"{url}/devices/{m}", headers=headers)
        except:
            print(f"I couldn't query for {m}, is Poly ZTP down?")
        else:
            device_data = json.loads(device_response.content)
            if "message" in device_data.keys() or device_response.status_code == 404:
                if device_data["message"] == "Unauthorized":
                    print(f"I couldn't query for {m}, is the API key correct?")
                    sys.exit(1)
                elif device_data["message"] == "Not Found":
                    print(f"Device with MAC {m} does not exist within our Poly ZTP")
            else:
                device["mac"] = m
                device["profile id"] = device_data["profileid"]
                for p in profiles:
                    if device["profile id"] == p["id"]:
                        device["profile name"] = p["name"]
                pprint(device)

def register_devices(url, headers, macs, profiles):
    """Register devices with Poly ZTP

    Args:
        url (string): URL of the API
        headers (dict): Headers for the request
        macs (list): List of mac addresses
        profiles (list): List of ZTP profiles
    """
    these_headers = headers.copy()
    these_headers["Content-Type"] = "application/json"
    choices = []
    for p in profiles:
        choices.append(p["name"])
    choice = get_choice("What profile would you like to assign them to?", choices) 
    profile_id = profiles[choice]["id"]
    for m in macs:
        body = json.dumps({"id": m, "profile": profile_id})
        register_response = requests.post(f"{url}/devices", headers=these_headers, data=body)
        if not register_response.status_code == 200:
            print(f"Something went wrong when registering {m}, please verify the mac address try again")
        else:
            register_data = json.loads(register_response.content)
            check_devices(url, headers, [m], profiles)

def delete_device(url, headers, macs, profiles):
    """Deregister devices from Poly ZTP

    Args:
        url (string): URL of the API
        headers (dict): Headers for the request
        macs (list): List of mac addresses
        profiles (list): List of ZTP profiles
    """
    for m in macs:
        delete_request = requests.delete(f"{url}/devices/{m}", headers=headers)
        if delete_request.status_code == 400:
            print(f"Could not delete mac {m}. Is the mac address valid?")
        elif delete_request.status_code == 409:
            print(f"{m} is registered with a different account")
        elif delete_request.status_code == 200:
            check_devices(url, headers, [m], profiles)

def main ():
    """The main function
    Gathers input from the user and calls appropriate functions
    """
    args = parse_args()
    # Get the api key and set up variables to use later
    if not args.key:
        try:
            with open("apikey", 'r') as f:
                apikey = f.read()
            apikey = apikey.strip()
            print("Loaded apikey file")
        except:
            print("Please create a file named 'apikey' that only contains the Poly ZTP API key")
            sys.exit(1)
    else:
        apikey = args.key.strip()
    url = "https://api.ztp.poly.com/preview"
    headers = {"API-KEY": apikey}
    profiles = load_profiles(url, headers)

    # First get the macs
    if not args.mac:
        will_upload = get_yes_no("Would you like to upload a csv?\nIf you answer no you can still enter multiple macs")
        if will_upload:
            macs = import_macs()
        else:
            macs = []
            while True:
                macs.append(get_mac("What is the mac?"))
                more_macs = get_yes_no("Would you like to upload another mac address?")
                if not more_macs:
                    break
    else:
        macs = []
        for m in args.mac:
            verified_mac = get_mac("", mac=m)
            macs.append(verified_mac)

    # Then see what they want to do
    while True:
        choices = ["Check if device(s) exists", "Register new device(s)", "Remove existing device(s)"]
        answer = get_choice("What would you like to do?", choices)
        if answer == 0:
            # Check if device(s) exists
            check_devices(url, headers, macs, profiles)
        elif answer == 1:
            # Register new device(s)
            register_devices(url, headers, macs, profiles)
        elif answer == 2:
            # Remove device(s)
            delete_device(url, headers, macs, profiles)
        answer = get_yes_no("Would you like to make another selection with the same MAC addresses?")
        if answer:
            pass
        else:
            break

if __name__ == '__main__':
    main()