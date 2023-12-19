from faker import Faker
import random
from functools import lru_cache
import json


def generate_random_data(num_records):
    fake = Faker()
    a = []
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        salary = random.randint(30000, 100000)  # Adjust salary range as needed
        email = fake.email()
        gender = random.choice(['Male', 'Female'])
        ip_address = fake.ipv4()
        address = fake.address()
        phone = fake.phone_number()

        record = {
            'First Name': first_name,
            'Last Name': last_name,
            'Salary': salary,
            'Currency': '$',
            'Email': email,
            'Gender': gender,
            'IP Address': ip_address,
            'Address': address,
            'Phone Number': phone
        }

        a.append(record)
    return a

def v3_generate_random_data():
    fake = Faker()
    a = []
    for _ in range(10000):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        gender = random.choice(['Male', 'Female'])
        salary = random.randint(10000, 999999)  # Adjust salary range as needed


        record = {
            'First Name': first_name,
            'Last Name': last_name,
            'Email': email,
            'Gender': gender,
            'Salary': salary
        }

        a.append(record)
    return a

    # # Generate 5 random records
    # random_records = generate_random_data(100)
    #
    # # Print the generated data
    # for record in random_records:
    #     print(record)
    #     # for key, value in record.items():
    #     #     print(f"{key}: {value}")
    #     print("\n")
