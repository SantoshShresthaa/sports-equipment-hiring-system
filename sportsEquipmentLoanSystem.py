# =============================================================================
# Sports Equipment Loan System
# Group: XX
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# FILE PATH CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
USERS_FILE = "files/users.txt"
EQUIPMENT_LIST_FILE = "files/equipment_lists.txt"

# ─────────────────────────────────────────────────────────────────────────────
# system color code
# ───
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


import json


class User:
    def __init__(self, user_id, username, role) -> None:
        self.user_id =  user_id
        self.username = username
        self.role = role

    def getUsername(self):
        return self.username

    def getUserRole(self):
        return self.role

class Coordinator(User):
    def load_user_menu (self):
        while True:
            print("\n" + "═" * 50)
            print("   COORDINATOR MENU")
            print("═" * 50)
            print("  [1] Add New Equipment")
            print("  [2] Edit Equipment")
            print("  [3] Remove Equipment")
            print("  [4] View All Equipment")
            print("  [5] View All Loan Records")
            print("  [6] View Loan History by Student")
            print("  [0] Logout")
            print("═" * 50)

            choice = input("  Enter choice: ").strip()
            if   choice == "1": self.addEquipment()
            elif choice == "2": self.editEquipment()
            # elif choice == "3": self.remove_equipment()
            # elif choice == "4": view_all_equipment()
            # elif choice == "5": self.view_all_loans()
            # elif choice == "6": self.view_loans_by_student()
            # elif choice == "0":
            #     print("\n  Logging out...")
            #     break
            else:
                print(f"\n {RED} [!] Invalid choice. Please try again. {RESET}")

    def addEquipment (self):
        print("\n  ── Add New Equipment ──")

        try:
            equipment_id = input("  Enter Equipment ID (e.g. EQ010): ").strip().upper()
            name = input("  Enter Equipment Name : ").strip()
            category = input ("  Enter Equipment Category (e.g. Ball/Bat): ").strip()
            sport_type = input ("  Enter Sport Type (e.g. Football): ").strip()
            quantity = input ("  Enter available quantity: ").strip()

            
            if not equipment_id or not name or not category or not sport_type or not quantity:
                print(f"\n {RED} [!] All the fields are required. Please reenter the fields. {RESET}")
                return
            
            if not quantity.isdigit():
                print(f"\n {RED} [!] Quantity must be positive number. {RESET}")
                return

            
            equipment_lists = getEquipmentLists()

            #check whether the id exists or not
            for equipment in equipment_lists:
                if(equipment['eq_id'] == equipment_id):
                    print(f"\n {RED} [!] Equipment ID {equipment_id} already exists. {RESET}")
                    return
            
            req_equipment_list = {
                    "eq_id" : equipment_id,
                    "name" : name, 
                    "category" : category, 
                    "type" : sport_type, 
                    "Quantity" : quantity
                     }
            
            equipment_lists.append(req_equipment_list)

            with open(EQUIPMENT_LIST_FILE, 'w') as list:
                json.dump(equipment_lists, list, indent=4)
            
            print(f"\n {GREEN} \n  [✓] Equipment '{name}' added successfully. {RESET}")


        except IOError as e:
            print(f"\n {RED} [!] File error: {e} {RESET}")


    def editEquipment (self):
        print("\n ---- Edit Equipment ---- ")

        equipment_id = input("Enter the equipment id: ").strip().upper()

        get_all_equipments = getEquipmentLists()
        found = False
        # print(get_all_equipments)

        for equipment in  get_all_equipments:
            if equipment['eq_id'] == equipment_id:
                found = True
                print(f"\n Current details: Equipment ID : {equipment['eq_id']} | Equipment Name: {equipment['name']} | Equipment Category:{equipment['category']} | Equipment Quantity: {equipment['Quantity']}")
                new_name     = input("  New Name     (Enter to keep): ").strip()
                new_category = input("  New Category (Enter to keep): ").strip()
                new_sport    = input("  New Sport    (Enter to keep): ").strip()
                new_quantity    = input(" New Quantity    (Enter to keep): ").strip()

                if new_name: equipment['name'] = new_name
                if new_category: equipment['category'] = new_category
                if new_sport: equipment['sport'] = new_sport
                if new_quantity: equipment['Quantity'] =  new_quantity
        
        if not found:
            print(f"\n {RED} [!] Equipment ID {equipment_id} not found. {RESET}")
            return
        
        saveEquipmentList(get_all_equipments)
        
        print(f"\n {GREEN} \n  [✓] Equipment '{equipment_id}' updated successfully. {RESET}")
        


#get list of users in the system
def getSystemUsers():
    userData = {}

    try:
        with open(USERS_FILE, 'r') as file:
            userData = json.load(file)
    
    except FileNotFoundError:
        print(f"\n {RED} [!] '{USERS_FILE}' not found. Please create the file. {RESET}")
    except IOError as e:
        print(f"\n  {RED} [!] Error reading users file: {e} {RESET}")
    
    return userData

#get list of equipment list in the system
def getEquipmentLists():
    equipment_lists =  []

    try:
        with open(EQUIPMENT_LIST_FILE, 'r') as eq_file:
            content = eq_file.read().strip()

            if content:
                equipment_lists = json.loads(content)
                
    except FileNotFoundError:
        print(f"\n {RED} [!] '{EQUIPMENT_LIST_FILE}' not found. Please create the file. {RESET}")
    except IOError as e:
        print(f"\n  {RED} [!] Error reading equipment list file: {e} {RESET}")

    return equipment_lists

# Save equipment lists
def saveEquipmentList(equipment_lists):
    try:
        with open(EQUIPMENT_LIST_FILE, 'w') as list:
            json.dump(equipment_lists, list, indent=4)
    except IOError as e:
        print(f"\n  {RED} [!] Error writing to equipment list file: {e} {RESET}")


#User Authentication
def authenticate():
    print("\n  ── Login into your account ──")
    request_username = input("  Username: ").strip()
    request_password = input("  Password: ").strip()

    if not request_username or not request_password:
        print("\n  [!] Username and password cannot be empty.")

        return None
    

    #get list of users in the system
    system_users = getSystemUsers()

    #Check user credentials
    for user in system_users:

        if request_username == user["username"] and request_password == user["password"]:
            
            if user["role"] == "coordinator":
                print(f"{GREEN}\n  Welcome, Coordinator {request_username}! {RESET}")
                
                return Coordinator(user['user_id'], user['username'], user['role'])

            elif user["role"] == "student":
                print(f"{GREEN}\n  Welcome, Student {request_username}! {RESET}")
    
    print(f"\n {RED} [!] Invalid username or password. Please try again. {RESET}")

    


def main():
    print("\n" + "═" * 50)
    print("   SPORTS EQUIPMENT LOAN SYSTEM  ")
    print("═" * 50)

    while True:
        print("\n  [1] Login")
        print("  [0] Exit")
        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            user = None
            # Allow up to 3 login attempts per session
            for attempt in range(3):
                user = authenticate()
                if user:
                    break
                remaining = 2 - attempt
                if remaining > 0:
                    print(f"\n  {remaining} attempt(s) remaining.")

            if user:
                user.load_user_menu()
            else:
                print("\n  [!] Too many failed attempts. Returning to main menu.")

        elif choice == "0":
            print("\n  Thank you for using the Sports Equipment Loan System. Goodbye!\n")
            break
        else:
            print("\n  [!] Invalid choice. Enter 1 to login or 0 to exit.")


main()   