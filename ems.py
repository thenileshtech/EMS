try:
    import os,logging,platform,sys
    from datetime import date
    from pathlib import Path
    path = Path(__file__).parent
    sys.path.append(path)
    # sys.path.append(r"C:\Users\nilesh\Documents\EMS")
    # sys.path.append(r"C:\EMS")
    import config.error_config as err
    import common.dashboard as dashboard
    import common.data_saver as db
    logger = logging.getLogger('EMS') # Creating logger to track activities
    logging.basicConfig(filename=f'{str(path) + '/logs.log'}',filemode='a',encoding='utf-8', level=logging.DEBUG)
except ModuleNotFoundError:
    print(err.e101)
    raise
except AttributeError:
    logger.error(err.e102)
    raise AttributeError(f"-----------{err.e102}---------------")

class compatibility_check:
    def __init__(self) -> None:
        operating_system = platform.system().upper()
        if operating_system in ['WINDOWS','LINUX','DARWIN']:
            logger.info(f"{err.i101} {operating_system}")
        else:
            logger.warning(f"{operating_system}; {err.w101}")

class clear_screen:
    def __init__(self) -> None:
        operating_system = platform.system().upper()
        if operating_system == "WINDOWS":
            os.system('cls')
        elif operating_system in ['LINUX','DARWIN']:
            os.system('clear')
            
def calculateAge(birthDate) -> int:
                today = date.today()
                age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                return int(age)

def main():
    compatibility_check()
    session = dashboard.start_screen()
    db.create_tables() # Tables creation if tables are not exists
    session.main_menu()
    db.conn.close()

if __name__ == '__main__':
    main()