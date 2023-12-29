import sqlite3
import ems
import config.error_config as err
import config.design_config as design
import common.dashboard as dash
import common.data_saver as db

# global current_voter
# global voter_city

@staticmethod
def validate_user(func):
    def authenticate(*args):
        choice = 1
        while(choice <= 3):
            ems.clear_screen()
            dash.start_screen().print_header("Authentication")
            print(f"Login\n".center(design.size))
            user_id = input(f"User Id  : ").upper()
            password = input(f"Password : ")
            flag = data_reader(user_id,password)
            if flag == True:
                print("Login Successfully".center(design.size))
                input()
                func(*args)
                return
            elif flag == 500:
                choice = 4
            else:
                print(f'{err.w103}\n')
                choice+=1
        print(err.e103)
        input()
    return authenticate

def data_reader(user_id,password) -> bool:
    global current_voter
    global voter_city

    conn = sqlite3.connect(r"DB/ems.db")
    my_cursor = conn.cursor()
    my_cursor_2 = conn.cursor()

    query = f'''Select voter, city from tabVoter
            Where voter = "{user_id}" and password = "{password}";
            '''
    data_checker = f'select * from tabVoter LIMIT 5'
    
    my_cursor.execute(query)
    my_cursor_2.execute(data_checker)

    result = my_cursor.fetchone()
    result_1 = my_cursor_2.fetchall()

    conn.close()

    if result == None:
        if len(result_1) == 0:
            print("\nNo voter found !")
            input()
            return 500
        return False
    else:
        current_voter = result[0]
        voter_city = result[1]
        return True

def get_details() -> bool:
    query = f'''
        SELECT 
            voting_date
        FROM 
            tabVoting
        WHERE
            voter = '{current_voter}'
    '''
    db.my_cursor.execute(query)
    result = db.my_cursor.fetchone()

    if result == None:
        return False
    else:
        print(f"Your vote is already captured on {list(result)}".center(design.size))
        input()
        return True

@validate_user
def voter_menu():
    ems.clear_screen()
    dash.start_screen().print_header('Voter')

    # Process will terminate here if voter is already available in Voting table
    if get_details():
        return
    
    ems.logger.info(f"Visited : Voter Menu")
    query = f'''
        SELECT 
            tabParty.party,
            tabParty.name
            -- tabParty.city
        FROM
            tabParty, tabVoter, tabElection, tabCandidate
        WHERE
            tabParty.city = '{voter_city}' and 
            tabParty.city = tabElection.city and 
            tabElection.status = 'STARTED' and
            -- tabParty.city = tabCandidate.city and 
            tabElection.election_start_time <= datetime('now','localtime') and 
            tabElection.election_end_time >= datetime('now','localtime')
    '''
    result = db.my_cursor.execute(query).fetchall()
    
    # Exit the fuction if there is no data found
    if len(result) <= 0:
        print(f"Voting window is not yet started at {voter_city} location !!".center(design.size))
        input()
        return

    i = 0
    # Printing Available parties for current City
    while i < 3:
        print(f"\nParty Id",f"Name\n".center(design.size))
        for key, val in dict(result).items():
            print(f"{key}\t",f"{val}".center(design.size))
        
        party = input("Select Party Id From Above List : ").strip().upper()

        flag = db.my_cursor.execute(f"SELECT * FROM tabParty WHERE party = '{party}';").fetchone()

        if flag == None:
            ems.logger.error(err.e105)
            print(f"\n{err.e105} Try Again !!!")
            input()
            i += 1
            continue
        else:
            break
    if i == 3:
        ems.logger.error(err.e103)
        print(f"\n{err.e103} Please Log-in Again !!")
        input()
        return
    
    query = f'''
        SELECT
            tabCandidate.candidate,
            tabCandidate.name
        FROM
            tabCandidate, tabParty
        WHERE
            tabParty.party = '{party}' and
            tabCandidate.party = '{party}'
            -- tabCandidate.city = '{voter_city}'
    '''

    result = db.my_cursor.execute(query).fetchall()
    i = 0
    # Printing Available candidates for selected Party in current city
    while i < 3:
        print(f"\nCandidate Id",f"Name\n".center(design.size))
        for key, val in dict(result).items():
            print(f"{key}\t",f"{val}".center(design.size))
        
        selected_candidate = input("Select Candidate From Above List : ").strip().upper()

        flag = db.my_cursor.execute(f"SELECT candidate FROM tabCandidate WHERE candidate = '{selected_candidate}';").fetchone()

        if flag == None:
            ems.logger.error(err.e109)
            print(f"\n{err.e109} Try Again !!!")
            input()
            i += 1
            continue
        else:
            break
    if i == 3:
        ems.logger.error(err.e103)
        print(f"\n{err.e103} Please Log-in Again !!")
        input()
        return
    
    db.voting_info().add_info(current_voter,party,selected_candidate,voter_city)