import config.error_config as err
import sqlite3
import ems
import common.dashboard as dash
import config.design_config as design

@staticmethod
def validate_user(func):
    def authenticate(*args):
        choice = 1
        while(choice <= 3):
            ems.clear_screen()
            dash.start_screen().print_header("Authentication")
            print(f"Login\n".center(design.size))
            u = input(f"User Id  : ").upper()
            p = input(f"Password : ")
            flag = data_reader(u,p)
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
    conn = sqlite3.connect(f'{str(ems.path) + '/ems.db'}')
    my_cursor = conn.cursor()
    my_cursor_2 = conn.cursor()

    query = f'''Select user_id, password from tabAdmin
            Where user_id = "{user_id}" and password = "{password}";
            '''
    data_checker = f'select * from tabAdmin LIMIT 5'
    
    my_cursor.execute(query)
    my_cursor_2.execute(data_checker)

    result = my_cursor.fetchone()
    result_1 = my_cursor_2.fetchall()

    conn.close()

    if result == None:
        if len(result_1) == 0:
            print("\nPlease contact support !")
            input()
            return 500
        return False
    else:
        return True