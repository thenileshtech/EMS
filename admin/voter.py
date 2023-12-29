import ems
import random
from datetime import date
import config.design_config as design
import config.error_config as err
import common.data_saver as db, common.dashboard as dash

def add_voter(user_type) -> None:
    try:
        dash.start_screen().print_header(user_type)
        print(f"Voter Registration".center(design.size))
        print('\n')
        name  = input("Enter voter name : ").strip().upper()
        day   = int(input("Day (DD)         : ").strip())
        month = int(input("Month (MM)       : ").strip())
        year  = int(input("Year (YYYY)      : ").strip())

        # concatinate date in (yyy-mm-dd)
        dob = date(year,month,day)
        # Calculating age
        age = ems.calculateAge(dob)

    except ValueError:
        ems.logger.error(err.e104)
        print(f"\n{err.e104}")
        input()
    else:
        city = input("Enter city       : ").strip().upper()
        # Checking age
        if age >= 18:
            # Generating Password
            password = ''.join(random.choice('0123456789ABCDEF') for i in range(4))
            # Saving the data to database
            conn = db.voter_info()
            conn.add_info(name,dob,age,city,password)
            print(f"\tYour Password Is: {password}")
            input()
        else:
            ems.logger.info(err.i105)
            print(err.i105)
            input()

def update_voter():
    pass
def delete_voter():
    pass