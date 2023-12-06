from faker import Faker
import random
from functools import lru_cache
import json

@lru_cache(maxsize=None)
def generate_random_data(num_records):
    fake = Faker()

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

        yield json.dumps(record).encode('utf-8')


    # # Generate 5 random records
    # random_records = generate_random_data(100)
    #
    # # Print the generated data
    # for record in random_records:
    #     print(record)
    #     # for key, value in record.items():
    #     #     print(f"{key}: {value}")
    #     print("\n")