import config.design_config as design
import common.data_saver as db, common.dashboard as dash

def add_party():
    dash.start_screen().print_header('Admin')
    print(f"Add Political Party".center(design.size))
    print('\n')
    name  = input("Enter party name : ").strip().upper()
    city = input("Enter city       : ").strip().upper()

    # Saving the data to database
    conn = db.party_info()
    conn.add_info(name,city)
    
def update_party():
    pass
def delete_party():
    pass