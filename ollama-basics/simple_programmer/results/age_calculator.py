import datetime
import sys

day = int(sys.argv[1])
month = int(sys.argv[2])
year = int(sys.argv[3])

birth_date = datetime.datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y")
today = datetime.datetime.today()

base_age = today.year - birth_date.year
if (today.month, today.day) < (birth_date.month, birth_date.day):
    base_age -= 1

print(base_age)
