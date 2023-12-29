import ems,sqlite3
from datetime import date
import config.design_config as design
import config.error_config as err
import common.data_saver as db, common.dashboard as dash

def cunduct_election():
    i = 0
    while i < 3:
        try:
            flag = db.party_info().get_city()
            if flag:
                city = input(f"\nPlease enter City from above list for which Elections to be conduct : ").strip().upper()
                print(f"\n---Please Enter Election Date---\n")
                day   = int(input("Day (DD)             : ").strip())
                month = int(input("Month (MM)           : ").strip())
                year  = int(input("Year (YYYY)          : ").strip())
                # Concatinatin date
                election_date = date(year,month,day)
                if election_date <= date.today():
                    i+=1
                    ems.logger.error(err.e106)
                    print(f"\n{err.e106}")
                    input()
                    continue
                else:
                    conn = db.election_info()
                    conn.add_info(city,election_date)
                    i = 3
            else:
                return False
        except sqlite3.IntegrityError:
            ems.logger.error(err.e107)
            print(f"\n{err.e107}")
            input()
            return False
        except ValueError:
            ems.logger.error(err.e104)
            print(f"\n{err.e104}")
            input()
            continue
    if i == 3:
        print(err.e103)

def update_election():
    pass

def delete_election():
    pass