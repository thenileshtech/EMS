try:
    import ems,admin.candidate as candidate
    import admin.voter as voter
    import admin.party as party
    import admin.admin as admin
    import config.design_config as design # User Interface config module
    import config.error_config as err
    import common.authentication as auth
    import admin.election as election
except ModuleNotFoundError:
    print(err.e101)
    raise

class admin_class:
    def __init__(self) -> None:
        self.size = design.size
        self.style = design.style_1
        self.border = design.style_1 * design.size

    @auth.validate_user # Decoretor for authentication
    def admin_menu(self,print_header):
        while True:
            ems.clear_screen()
            print_header('Admin')
            ems.logger.info(f"Visited : Admin Menu")
            print(f'1. Conduct Election'.center(self.size))
            print(f'2. Add Political Party'.center(self.size+2))
            print(f'3. Add User\n'.center(self.size-8))
            print(f'0. Logout'.center(self.size-10))
            print(f'{self.border}')
            option = input("Enter option: -").strip()
            match option:
                case '1':
                    ems.clear_screen()
                    election.cunduct_election()
                    continue
                case '2':
                    ems.clear_screen()
                    party.add_party()
                    continue
                case '3':
                    ems.clear_screen()
                    self.admin_sub_menu(print_header)
                    continue
                case '0':
                    return False
                case _:
                    print(err.w102)
                    ems.logger.warning(err.w102)
                    input()

    def admin_sub_menu(self,print_header):
        while True:
            ems.clear_screen()
            print_header('Admin')
            ems.logger.info(f"Visited : Admin Sub Menu")
            print(f'1. Add Candidate'.center(self.size))
            print(f'2. Add Voter'.center(self.size-4))
            print(f'3. Add Admin\n'.center(self.size-3))
            print(f'0. Go back'.center(self.size-7))
            print(f'{self.border}')
            option = input("Enter option: -").strip()
            match option:
                case '1':
                    ems.clear_screen()
                    candidate.add_candidate()
                    continue
                case '2':
                    ems.clear_screen()
                    voter.add_voter('Admin')
                    continue
                case '3':
                    ems.clear_screen()
                    admin.add_admin()
                    continue
                case '0':
                    return False
                case _:
                    print(err.w102)
                    ems.logger.warning(err.w102)
                    input()