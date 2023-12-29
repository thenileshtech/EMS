try:
    # import logging,sys
    # sys.path.append(r"C:\Users\nilesh\Documents\EMS")
    import sqlite3
    import config.design_config as design # User Interface config module
    import config.error_config as err,ems
    from datetime import datetime,date
except ModuleNotFoundError:
    print(err.e101)
    raise
except AttributeError:
    ems.logger.error(err.e102)
    raise AttributeError(f"-----------{err.e102}---------------")

# Create a connection to the database
conn = sqlite3.connect(r"DB/ems.db")
# print("Connection Successful !!")

# Create a cursor
my_cursor = conn.cursor()

# Enabling Foreign key constraint (In SQLite 4.x, FK constraints will be enabled by default.)
my_cursor.execute('PRAGMA foreign_keys = ON;')

def get_id(query):
    # Executing Query
    my_cursor.execute(query)
    # Lambda Function
    next_id = lambda prefix, id : prefix + '-' + str(int(id) + 1)

    # Fetching data
    result = my_cursor.fetchone()

    if result == None:
        return None
    else:
        result = result[0].split('-')
        result = next_id(result[0],result[1])
        # Retruning the result
        return str(result)

class create_tables:
    def __init__(self) -> None:
        self.party_table()
        self.candidate_table()
        self.voter_table()
        self.admin_table()
        self.voting_table()
        self.election_table()
        ems.logger.info("Checking Tables")

    def candidate_table(self):
        query = '''
        create table IF NOT EXISTS tabCandidate(
            candidate varchar(25) primary key,
            name varchar(25) not null,
            dob date not null,
            age int check(age >= 18),
            party varchar(25),
            created_at date DEFAULT (datetime('now','localtime')),
            FOREIGN KEY(party) REFERENCES tabParty(party),
            UNIQUE(name,dob,party)
        )'''
        my_cursor.execute(query)
        return

    def party_table(self):
        query = '''
        create table IF NOT EXISTS tabParty(
            party varchar(25) primary key,
            name varchar(25) not null,
            city varchar(25) not null,
            created_at date DEFAULT (datetime('now','localtime')),
            UNIQUE(name,city)
        )'''
        my_cursor.execute(query)
        return

    def voter_table(self):
        query = '''
        create table IF NOT EXISTS tabVoter(
            voter varchar(25) primary key,
            name varchar(25) not null,
            dob date not null,
            age int check(age >= 18),
            city varchar(25) not null,
            password varchar(25) not null,
            created_at date DEFAULT (datetime('now','localtime')),
            UNIQUE(name,dob,city)
        )'''
        my_cursor.execute(query)
        return

    def voting_table(self):
        query = '''
        create table IF NOT EXISTS tabVoting(
            sr_no INTEGER PRIMARY KEY AUTOINCREMENT,
            voter varchar(25) NOT NULL UNIQUE,
            party varchar(25) NOT NULL,
            candidate varchar(25) NOT NULL,
            city varchar(25) NOT NULL,
            voting_date date,
            created_at date default (datetime('now','localtime')),
            -- UNIQUE(voter,party,candidate,city,voting_date),
            FOREIGN KEY(party) REFERENCES tabParty(party),
            FOREIGN KEY(candidate) REFERENCES tabCandidate(candidate)
        )'''
        my_cursor.execute(query)
        return

    def admin_table(self):
        query = '''
        create table IF NOT EXISTS tabAdmin(
            user_id varchar(25) PRIMARY KEY,
            name varchar(25) not null,
            password varchar(25) not null,
            created_at date DEFAULT (datetime('now','localtime'))
        )'''
        my_cursor.execute(query)
        return
    
    def election_table(self):
        query = f'''
        create table IF NOT EXISTS tabElection(
            election_id varchar(25) PRIMARY KEY,
            city varchar(25) NOT NULL,
            election_date date NOT NULL,
            election_start_time date,
            election_end_time date,
            status varchar(25) DEFAULT 'NOT STARTED',
            created_at date DEFAULT (datetime('now','localtime')),
            UNIQUE(city,status)
        )
            '''
        my_cursor.execute(query)
        return

# save, update, delete candidate info
class candidate_info:
    def __init__(self) -> None:
        query = f'''
            SELECT candidate FROM tabCandidate
            ORDER BY candidate DESC LIMIT 1;
        '''
        # Get next id
        self.next_id = get_id(query)

        # If it is a first record
        if self.next_id == None:
            self.next_id = design.candidate_start_from

    def add_info(self,name,dob,age,party) -> str:
        query = f'''
            INSERT INTO tabCandidate (candidate,name,dob,age,party)
            VALUES ('{self.next_id}','{name}','{dob}','{age}','{party}')
        '''
        my_cursor.execute(query)
        conn.commit()
        print(f"\nNew record added - {self.next_id}")
        input()

# save, update, delete voter info
class voter_info:
    def __init__(self) -> None:
        query = f'''
            SELECT voter FROM tabVoter
            ORDER BY voter DESC LIMIT 1;
        '''
        # Get next id
        self.next_id = get_id(query)

        # If it is a first record
        if self.next_id == None:
            self.next_id = design.voter_start_from

    def add_info(self,name,dob,age,city,password) -> str:
        query = f'''
            INSERT INTO tabVoter (voter,name,dob,age,city,password)
            VALUES ('{self.next_id}','{name}','{dob}','{age}','{city}','{password}')
        '''
        my_cursor.execute(query)
        conn.commit()
        print(f"\n\tYour User Id Is : {self.next_id}")
        input()

# save, update, delete party info
class party_info:
    def __init__(self) -> None:
        query = f'''
            SELECT party FROM tabParty
            ORDER BY party DESC LIMIT 1;
        '''
        # Get next id
        self.next_id = get_id(query)

        # If it is a first record
        if self.next_id == None:
            self.next_id = design.party_start_from

    def add_info(self,name,city) -> str:
        query = f'''
            INSERT INTO tabParty (party,name,city)
            VALUES ('{self.next_id}','{name}','{city}')
        '''
        my_cursor.execute(query)
        conn.commit()
        print(f"\nNew record added - {self.next_id}")
        input()

    def get_party(self) -> bool:
        query = '''
            Select party,name from tabParty;
        '''
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        if len(result) == 0:
            ems.logger.info(err.i106)
            print(err.i106.center(design.size))
            input()
            return False
        else:
            print(f"\nParty Id",f"Party Name\n".center(design.size))
            for key,val in dict(result).items():
                print(f"{key}\t",f"{val}".center(design.size))
            return True
    
    def get_city(self) -> bool:
        query = '''Select city, count(city) as 'Total Parties' from tabParty GROUP BY city'''
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        if len(result) == 0:
            ems.logger.info(err.i106)
            print(err.i106.center(design.size))
            input()
            return False
        else:
            print(f"\nCity",f"Total Parties\n".center(design.size))
            for key, val in dict(result).items():
                print(f"{key}\t",f"{val}".center(design.size))
            return True

# save, update, delete admin info
class admin_info:
    def __init__(self) -> None:
        query = f'''
            SELECT user_id FROM tabAdmin
            ORDER BY user_id DESC LIMIT 1;
        '''
        # Get next id
        self.next_id = get_id(query)

        # If it is a first record
        if self.next_id == None:
            self.next_id = design.admin_start_from

    def add_info(self,user,passwd):
        query = f'''
            INSERT INTO tabAdmin (user_id,name,password)
            VALUES ('{self.next_id}','{user}','{passwd}')
        '''
        my_cursor.execute(query)
        conn.commit()
        print(f"\nNew record added - {self.next_id}")
        input()

# save, update, delete election info
class election_info:
    def __init__(self) -> None:
        query = f'''
            SELECT election_id FROM tabElection
            ORDER BY city DESC LIMIT 1;
        '''
        # Get next id 
        self.next_id = get_id(query)

        # If it is a first record
        if self.next_id == None:
            self.next_id = design.election_start_from

    def add_info(self,city,election_date):
        election_start_time = datetime(election_date.year,election_date.month,election_date.day,8)
        election_end_time = datetime(election_date.year,election_date.month,election_date.day,17)
        query = f'''
            INSERT INTO tabElection (election_id,city,election_date,election_start_time,election_end_time)
            VALUES (
            '{self.next_id}',
            '{city}',
            '{election_date}',
            '{election_start_time}',
            '{election_end_time}'
            )
        '''
        my_cursor.execute(query)
        conn.commit()
        print(f"\nNew record added - {self.next_id}")
        input()

class voting_info:
    def __init__(self) -> None:
        pass

    def add_info(self,current_voter,selected_party,selected_candidate,voter_city):
        query = f'''
            INSERT INTO
        tabVoting
            (voter,party,candidate,city,voting_date)
        VALUES
            ('{current_voter}','{selected_party}','{selected_candidate}','{voter_city}','{date.today()}')
'''
        try:
            my_cursor.execute(query)
            conn.commit()
            print(f"\nVote Captured Successfully !")
            input()
        except sqlite3.IntegrityError:
            ems.logger.error(err.e108)
            print(err.e108)
            input()
