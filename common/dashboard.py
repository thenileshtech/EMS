try:
    import admin.voter as voter
    import voter.menu_page as voter_menu
    import config.design_config as design # User Interface config module
    import datetime,ems,admin.menu_page,config.error_config as err
except ModuleNotFoundError:
    print(err.e101)
    raise

class start_screen:
    def __init__(self) -> None:
        self.style = design.style_1
        self.size = design.size
        self.border = design.style_1 * design.size

    def print_header(self,user_type='--') -> None:
        print(f'\n{self.border}')
        print(f'{design.heading} {datetime.datetime.now().year}'.center(self.size))
        print(f'{self.border}')
        print(f'Welcome to {user_type.upper()} portal'.center(self.size),'\n')

    def main_menu(self) -> None:
        while True:
            ems.clear_screen()
            self.print_header('EMS')
            ems.logger.info('Visited : Main Menu')
            print(f'1. Admin Login'.center(self.size))
            print(f'2. Voter Login'.center(self.size))
            print(f'3. New Registration\n'.center(self.size+5))
            print(f'0. Exit'.center(self.size-7))
            print(f'{self.border}')
            option = input("Enter option: -").strip()
            match option:
                case '1':
                    main_menu_session =  admin.menu_page.admin_class()
                    main_menu_session.admin_menu(self.print_header)
                    continue
                case '2':
                    ems.clear_screen()
                    # self.print_header('Voter')
                    voter_menu.voter_menu()
                    continue
                case '3':
                    ems.clear_screen()
                    voter.add_voter('EMS')
                    continue
                case '0':
                    return False
                case _:
                    print(err.w102)
                    input()
        