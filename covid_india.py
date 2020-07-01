#!/usr/bin/python3
import requests
from threading import Thread

def fetch():
    global data1, data2
    api1 = requests.get("https://api.covid19india.org/v2/state_district_wise.json")
    api2 = requests.get("https://api.covid19india.org/v3/data.json")

    data1 = api1.json()
    data2 = api2.json()

def print_paramters(data,type):
    if type=='district':
        active = data['active']
        confirmed = data['confirmed']
        recovered = data['recovered']
        deceased = data['deceased']

        print(f"\nACTIVE cases : {active}\nCONFIRMED cases : {confirmed}\nRECOVERED cases : {recovered}\nDECEASED cases : {deceased}\n")
    else:
        confirmed = data['confirmed']
        deceased = data['deceased']
        recovered = data['recovered']
        tested = data['tested']

        print(f"\nCONFIRMED cases : {confirmed}\nRECOVERED cases : {recovered}\nDECEASED cases : {deceased}\nTESTED : {tested}\n")

if __name__ == '__main__':
    # GET data from API:
    data1 = None
    data2 = None
    t = Thread(target=fetch)
    t.start()

    # Get input from user:
    state = input("Enter the state name\n> ").lower()
    district = input("Enter the district name\n> ").lower()
    if t.is_alive():
        t.join()

    # Filter state data:
    states = [data1.index(x) for x in data1 if state in x['state'].lower()]
    
    for st in states:
        state_code = data1[st]['statecode']
        print(f"\n*** STATE NAME : {data1[st]['state']} ***")
        state_data = data2[state_code]['total']
        
        print_paramters(state_data,'state')

        districts_data = data1[st]['districtData']
        districts = [districts_data.index(x) for x in districts_data if district in x['district'].lower()]

        for dist in districts:
            district_data = districts_data[dist]
            print(f"\n{districts.index(dist)+1}) DISTRICT NAME: {district_data['district']}")
            print_paramters(district_data,'district')
