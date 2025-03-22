import random
import string

def generate_booking_reference():
    # generate a unique booking reference from a pool of existing ones
    try:
        with open('booking3.txt', 'r') as file:
            existing_refs = {line.split(',')[0] for line in file.readlines()}
    except FileNotFoundError:
        existing_refs = set()
    while True:
        reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if reference not in existing_refs:
            return reference

def load_seating():
    # load seating data from the file
    flights = {}
    with open('seating3.txt', 'r') as file:
        data = file.read().splitlines()
        for line in data:
            flight_data = line.split(':')
            flight_number, seat_data = flight_data[0], flight_data[1]
            seats = {}
            for seat in seat_data.split(','):
                parts = seat.strip().split()
                if len(parts) > 1:
                    seat_id = parts[0]
                    status = ' '.join(parts[1:])
                    seats[seat_id] = status
            flights[flight_number] = seats
    return flights

def save_seating(flights):
    # save the updated seating data to the file
    output = []
    for flight_number, seats in flights.items():
        seat_str = ','.join([seat_id + " " + status for seat_id, status in seats.items()])
        output.append(flight_number + ":" + seat_str)
    with open('seating3.txt', 'w') as file:
        file.write('\n'.join(output))

def update_booking_database(action, reference, passport_number='', first_name='', last_name='', flight_number='', seat_number=''):
    # update booking details in the database
    if action == 'add':
        with open('booking3.txt', 'a') as file:
            file.write(reference + "," + passport_number + "," + first_name + "," + last_name + "," + flight_number + "," + seat_number + "\n")
    elif action == 'remove':
        with open('booking3.txt', 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if not line.startswith(reference):
                    file.write(line)
            file.truncate()

def check_availability(flights):
    # check and display seat availability for a specified flight
    flight_number = input("Enter flight number (e.g., Flight1): ")
    if flight_number in flights:
        print("Current Seating Arrangement for " + flight_number + ":")
        for seat_id, status in flights[flight_number].items():
            print(seat_id + ": " + status)
    else:
        print("Flight number not found.")

def book_seat(flights):
    # book a seat and store the booking details
    flight_number = input("Enter flight number (e.g., Flight1): ")
    if flight_number in flights:
        seat_number = input("Enter seat number to book (e.g., 1A): ").upper()
        if flights[flight_number].get(seat_number, '') == 'F':
            reference = generate_booking_reference()
            passport_number = input("Enter passport number: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            flights[flight_number][seat_number] = reference + " " + passport_number + " " + first_name + " " + last_name
            save_seating(flights)
            update_booking_database('add', reference, passport_number, first_name, last_name, flight_number, seat_number)
            print("Seat booked successfully with reference " + reference + ".")
        else:
            print("Seat not available or invalid seat number.")
    else:
        print("Flight number not found.")

def free_seat(flights):
    # free a reserved seat
    flight_number = input("Enter flight number (e.g., Flight1): ")
    if flight_number in flights:
        seat_number = input("Enter seat number to free (e.g., 1A): ").upper()
        current_status = flights[flight_number].get(seat_number, '')
        if 'F' not in current_status:
            update_booking_database('remove', current_status.split(' ')[0])
            flights[flight_number][seat_number] = 'F'
            save_seating(flights)
            print("Seat freed successfully.")
        else:
            print("Seat not currently reserved or does not exist.")
    else:
        print("Flight number not found.")

def show_booking_status(flights):
    # display the booking status for all flights
    for flight_number, seats in flights.items():
        print("Booking Status for " + flight_number + ":")
        for seat_id, status in seats.items():
            if 'F' not in status:
                print(seat_id + ": Booked")
            else:
                print(seat_id + ": Free")

def main_menu():
    # display the main menu and handle user input
    flights = load_seating()
    while True:
        print("\nMenu:")
        print("1. Check seat availability")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            check_availability(flights)
        elif choice == '2':
            book_seat(flights)
        elif choice == '3':
            free_seat(flights)
        elif choice == '4':
            show_booking_status(flights)
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
