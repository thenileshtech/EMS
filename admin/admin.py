import config.design_config as design
import common.data_saver as db, common.dashboard as dash

def add_admin() -> None:
    while(True):
        dash.start_screen().print_header('Admin')
        print(f"Add Admin".center(design.size))
        print('\n')
        user      = input("User Name          : ").strip().upper()
        new_pass  = input("New Password       : ").strip()
        conf_pass = input("Confirm Password   : ").strip()

        if user.isalpha() and new_pass == conf_pass:
            # Saving the data to database
            conn = db.admin_info()
            conn.add_info(user,new_pass)
            return False
        elif new_pass != conf_pass:
            print(f"Password Mistmatch ! Try again")
            input()
        else:
            print(f"User name should in alphabates [a-Z] or numbers [0-9] \n Try again !!")
            input()

def update_candidate():
    pass
def delete_candidate():
    pass