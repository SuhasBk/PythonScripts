#!/usr/local/bin/python3
import requests, os
from pyfiglet import figlet_format
from datetime import datetime, timedelta

def get_next_delta(dt, delta_type, delta_value):
    if delta_type == 'days':
        date = datetime.strptime(dt, "%Y-%m-%d")
        next_day = date + timedelta(days=delta_value)
        next_day_string = next_day.strftime("%Y-%m-%d")
        return next_day_string
    elif delta_type == 'minutes':
        time_obj = datetime.strptime(dt, "%H:%M")
        new_time = time_obj + timedelta(minutes=delta_value)
        end_time_string = new_time.strftime("%H:%M")
        return end_time_string

def choose_a_room():
    print('Enter the room you want in 5th floor:')
    for index, room in enumerate(room_mappings.keys()):
        print(index + 1, '--->', room)
    ch = int(input("\nEnter your choice:\n> ")) - 1
    return room_mappings[list(room_mappings.keys())[ch]]

def search():
    data = {
        'lid': metaData['lid'],
        'gid': metaData['gid'],
        'eid': metaData['itemId'],
        'seat': '0',
        'seatId': '0',
        'zone': metaData['zone'],
        'start': metaData['startDate'],
        'end': metaData['endDate'],
        'pageIndex': '0',
        'pageSize': '18'
    }

    url = 'https://uta.libcal.com/spaces/availability/grid'

    response = requests.post(url, headers=headers, data=data)
    seats = list(filter(lambda seat: 'className' not in seat and seat['itemId'] == metaData['itemId'], response.json()['slots']))
    
    for seat in seats:
        seat_time = seat['start'].split(' ')[1][:-3]
        if seat['itemId'] == metaData['itemId'] and seat_time == metaData['time']:
            return seats, seat['checksum']
    
    return seats, ''


def add(seat_checksum):
    data = {
        'add[eid]': metaData['itemId'],
        'add[gid]': metaData['gid'],
        'add[lid]': metaData['lid'],
        'add[start]': metaData['startDate'] + ' ' + metaData['time'],
        'add[checksum]': seat_checksum,
        'lid': metaData['lid'],
        'gid': metaData['gid'],
        'start': metaData['startDate'],
        'end': metaData['endDate']
    }

    url = 'https://uta.libcal.com/spaces/availability/booking/add'

    response = requests.post(url, headers=headers, data=data)
    return response.json()['bookings'][0]['checksum'] if response.ok else ''


def book(checksum):
    end_time_string = get_next_delta(metaData['time'], 'minutes', 30)
    url = 'https://uta.libcal.com/ajax/space/book'
    headers['content-type'] = 'multipart/form-data; boundary=----WebKitFormBoundaryhdaUJdAeBSWES7e8'

    # <DO NOT TOUCH THIS FORMATTING OR INDENTATION
    data = f'''------WebKitFormBoundaryhdaUJdAeBSWES7e8
Content-Disposition: form-data; name="session"

42106807
------WebKitFormBoundaryhdaUJdAeBSWES7e8
Content-Disposition: form-data; name="fname"

{metaData['fname']}
------WebKitFormBoundaryhdaUJdAeBSWES7e8
Content-Disposition: form-data; name="lname"

{metaData['lname']}
------WebKitFormBoundaryhdaUJdAeBSWES7e8
Content-Disposition: form-data; name="email"

{metaData['email']}
------WebKitFormBoundaryhdaUJdAeBSWES7e8
Content-Disposition: form-data; name="bookings"

[{{"id":1,"eid":{metaData['itemId']},"seat_id":0,"gid":{metaData['gid']},"lid":{metaData['lid']},"start":"{metaData['startDate']} {metaData['time']}","end":"{metaData['startDate']} {end_time_string}","checksum":"{checksum}"}}]
------WebKitFormBoundaryhdaUJdAeBSWES7e8
Content-Disposition: form-data; name="returnUrl"

/space/111716
------WebKitFormBoundaryhdaUJdAeBSWES7e8
Content-Disposition: form-data; name="pickupHolds"


------WebKitFormBoundaryhdaUJdAeBSWES7e8
Content-Disposition: form-data; name="method"

12
------WebKitFormBoundaryhdaUJdAeBSWES7e8--'''
    # DO NOT TOUCH THIS FORMATTING OR INDENTATION>

    response = requests.post(url, headers=headers, data=data)
    response.ok and print('Seat booked successfully!')
    not response.ok and print('Failed to book your seat! Check payload.')

if __name__ == '__main__':
    print(figlet_format('UTA LIBRARY'))
    # common header for all requests
    headers = {
        'authority': 'uta.libcal.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://uta.libcal.com',
        'referer': 'https://uta.libcal.com/space/111716',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-requested-with': 'XMLHttpRequest',
    }

    # hard-coded 5th floor room mappings
    room_mappings = {
        '519 (Capacity 5)': 111713,
        '520A (Capacity 6)': 111714,
        '520B (Capacity 3)': 111716,
        '520C (Capacity 2)': 130324
    }

    # data structure to store all possible details
    metaData = {
        # fixed for Central Library 5th floor rooms:
        'lid': 10450,
        'zone': 5909,
        'gid': 29456,
        
        # get room, student and booking details:
        'itemId': int(os.getenv('roomno') or choose_a_room()),
        'fname': os.getenv('fname') or input('Enter your first name:\n> '),
        'lname': os.getenv('lname') or input('Enter your last name:\n> '),
        'email': os.getenv('mavemail') or input("Enter your MAV email ID only:\n> "),
        'startDate': input("Enter the date (YYYY-MM-DD) on which you want to book seats:\n> "), #'2023-12-20'
        'time': input("Enter the time (HH:mm) slot at which you want to book seats:\n> "), #'11:30'
    }

    # weird request parameter to pass endDate while searching
    metaData['endDate'] = get_next_delta(metaData['startDate'], 'days', 1)

    # try to search for given seat
    available_seats, seat_checksum = search()

    # adjust time if slot not found
    if not seat_checksum:
        if not available_seats:
            exit('No seats! Try again!')

        print('Seat not available at that slot! Pick one from available ones below:\n')
        
        for index, seat in enumerate(available_seats):
            print(index + 1, ' ---> ' 'From: ', seat['start'], ' to ', seat['end'], '\n')
        
        ch = int(input("\nEnter your choice:\n> ")) - 1
        seat_checksum = available_seats[ch]['checksum']
        # update new room and new time
        metaData['itemId'] = available_seats[ch]['itemId']
        metaData['time'] = available_seats[ch]['start'].split(' ')[1][:-3]

    # reserve and book it!
    new_checksum = add(seat_checksum)
    book(new_checksum)