import ems,sqlite3
import config.design_config as design
import config.error_config as err
import common.data_saver as db, common.dashboard as dash

from datetime import date

def add_candidate() -> None:
    try:
        dash.start_screen().print_header('Admin')
        print(f"Add Candidate".center(design.size))
        print('\n')
        name  = input("Enter candidate name : ").strip().upper()
        day   = int(input("Day (DD)             : ").strip())
        month = int(input("Month (MM)           : ").strip())
        year  = int(input("Year (YYYY)          : ").strip())
        # concatinate date in (yyyy-mm-dd)
        dob = date(year,month,day)
        # Calculating age
        age = ems.calculateAge(dob)

    except ValueError:
        ems.logger.error(err.e104)
        print(f"\n{err.e104}")
        input()
    else:
        #Checking age
        if age >= 18:
            while(True):
                try:
                    # Display available parties
                    flag = db.party_info().get_party()
                    if flag:
                        party = input(f"\nPlease enter party id from above list  : ").strip().upper()
                        # Saving the data to database
                        conn = db.candidate_info()
                        conn.add_info(name,dob,age,party)
                        return False
                    else:
                        return False
                except sqlite3.IntegrityError:
                    ems.logger.error(err.e105)
                    print(f"\n{err.e105}")
                    input()
                    continue
        else:
            ems.logger.info(err.i105)
            print(err.i105)
            input()

def update_candidate():
    pass
def delete_candidate():
    pass