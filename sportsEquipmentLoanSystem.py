# Sports Equipment Loan System
# Group: 1

# FILE PATH 
USERS_FILE = "files/users.txt"
EQUIPMENT_LIST_FILE = "files/equipment_lists.txt"
BORROWING_HISTORY_FILE = "files/loan_history.txt"


# system color code
# ───
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


from datetime import datetime
import json
import pandas as pd

class User:
    def __init__(self, user_id, username, role) -> None:
        self.user_id =  user_id
        self.username = username
        self.role = role

    def getUsername(self):
        return self.username

    def getUserId(self):
        return self.user_id

class Coordinator(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "Coordinator")

    def loadUserMenu (self):
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
            elif choice == "3": self.removeEquipment()
            elif choice == "4": viewAllEquipment()
            elif choice == "5": self.viewAllLoans()
            elif choice == "6": self.viewLoansByStudent()
            elif choice == "0":
                print("\n  Logging out...")
                break
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

    def removeEquipment (self):
        print("\n ---- Remove Equipment ---- ")

        equipment_id = input("Enter the equipment id: ").strip().upper()

        get_all_equipments = getEquipmentLists()
        found = False

        for equipment in  get_all_equipments:
            if equipment['eq_id'] == equipment_id:
                found = True
                get_all_equipments.remove(equipment)
        
        if not found:
            print(f"\n {RED} [!] Equipment ID {equipment_id} not found. {RESET}")
            return
        
        saveEquipmentList(get_all_equipments)

        print(f"\n {GREEN} \n  [✓] Equipment '{equipment_id}' removed successfully. {RESET}")

        
    def viewAllLoans(self):
        print("\n  ── All Loan Records ── \n")

        load_loan_history = getLoanHistory()

        if not load_loan_history:
            print(f"\n {RED} [!] No loan records found in the system. {RESET}")
            return
        
        print(pd.DataFrame(load_loan_history))

        print(f"\n {GREEN} [✓] Total loan records: {len(load_loan_history)} {RESET}")
    

    def viewLoansByStudent(self):
        print("\n  ── View Loan History by Student ── \n")

        student_id = input("  Enter Student ID (e.g. S001): ").strip().upper()

        load_loan_history = getLoanHistory()

        student_loans = []

        for loan in load_loan_history:
            if loan['student_id'] == student_id:
                student_loans.append(loan)

        if not student_loans:
            print(f"\n {RED} [!] No loan records found for Student ID {student_id}. {RESET}")
            return
        
        print(pd.DataFrame(student_loans))

        print(f"\n {GREEN} [✓] Total loans for Student ID {student_id}: {len(student_loans)} {RESET}")

class Student(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "Student")

    def loadUserMenu(self):
        while True:
            print("\n" + "═" * 50)
            print("   STUDENT MENU")
            print("═" * 50)
            print("  [1] View Available Equipment")
            print("  [2] Borrow Equipment")
            print("  [3] Return Equipment")
            print("  [4] View My Loan History")
            print("  [0] Logout")
            print("═" * 50)

            choice = input("  Enter choice: ").strip()

            if   choice == "1": self.viewEquipmentList()
            elif choice == "2": self.borrowEquipment()
            elif choice == "3": self.returnEquipment()
            elif choice == "4": self.viewMyHistory()
            elif choice == "0":
                print("\n  Logging out...")
                break
            else:
                print("\n  [!] Invalid choice. Please try again.")
    

    def viewEquipmentList(self):
        print("\n  ── Available Equipment List ── \n")

        equipment_lists = getEquipmentLists()

        if not equipment_lists:
            print(f"\n {RED} [!] No equipment found in the system. {RESET}")
            return
        
        print(pd.DataFrame(equipment_lists))
        print(f"\n {GREEN} [✓] Total equipment: {len(equipment_lists)} {RESET}")
    

    def borrowEquipment(self):
        print("\n  ── Borrow Equipment ── \n")

        user_loans = self.getLoggedInUserBorrowHistory()

        print(f"\n You have currently borrowed {len(user_loans)} equipment(s).")

        if len(user_loans) >=2:
            print(f"\n {RED} [!] You have already borrowed 2 equipment. Please return them before borrowing more. {RESET}")

            print("\n Your current borrowings: \n")
            print(pd.DataFrame(user_loans))
            return
        
        print("\n Please select the equipment you want to borrow: \n")
        print(pd.DataFrame(getEquipmentLists()))

        equipment_id = input(" \n \n Enter Equipment ID to borrow: ").strip().upper()

        equipment_lists = getEquipmentLists()
        loan_record = {}

        for equipment in equipment_lists:
            if equipment['eq_id'] == equipment_id:
                loan_record['loan_id'] = f"LR-00{len(getLoanHistory()) + 1}"
                loan_record ['student_id'] = self.getUserId()
                loan_record ['equipment_id'] = equipment_id
                loan_record ['status'] = "Borrowed"
                loan_record ['borrowed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                #reduce the quantity of the equipment by 1
                equipment['Quantity'] = str(int(equipment['Quantity']) - 1)
                saveEquipmentList(equipment_lists)

                self.storeBorrowedHistoryData(loan_record)
                print(f"\n {GREEN} [✓] You have successfully borrowed '{equipment['name']}'. Please return it on time. {RESET}")
                return
        
        print(f"\n {RED} [!] Equipment ID {equipment_id} not found. {RESET}")

    
    def returnEquipment(self):
        print("\n  ── Return Equipment ── \n")

        user_loans = self.getLoggedInUserBorrowHistory()

        if not user_loans:
            print(f"\n {RED} [!] You have no borrowed equipment to return. {RESET}")
            return
        
        print("\n Your current borrowings: \n")
        print(pd.DataFrame(user_loans))

        loan_id = input("\n Enter Loan ID to return: ").strip().upper()

        loan_history = getLoanHistory()
        found = False

        for loan in loan_history:
            if loan['loan_id'] == loan_id and loan['student_id'] == self.getUserId() and loan['status'] == "Borrowed":
                found = True
                loan['status'] = "Returned"
                loan['return_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        
        if not found:
            print(f"\n {RED} [!] Loan ID {loan_id} not found in your borrowings. {RESET}")
            return
        
        try:
            with open(BORROWING_HISTORY_FILE, 'w') as file:
                json.dump(loan_history, file, indent=4)
            print(f"\n {GREEN} [✓] You have successfully returned the equipment. Thank you! {RESET}")
        except IOError as e:
            print(f"\n {RED} [!] Error writing to loan history file: {e} {RESET}")
        
    def viewMyHistory(self):
        print("\n  ── My Loan History ── \n")

        user_loans = self.getAllAuthUserHistory()

        if not user_loans:
            print(f"\n {RED} [!] You have no loan history. {RESET}")
            return
        
        print(pd.DataFrame(user_loans))


    def storeBorrowedHistoryData(self, loan_record):
        loan_history = getLoanHistory()

        loan_history.append(loan_record)

        try:
            with open(BORROWING_HISTORY_FILE, 'w') as file:
                json.dump(loan_history, file, indent=4)
        except IOError as e:
            print(f"\n {RED} [!] Error writing to loan history file: {e} {RESET}")


    def getLoggedInUserBorrowHistory(self):
        loan_history = getLoanHistory()
        user_id = self.getUserId()

        user_loans = []

        for loan in loan_history:
            if loan['student_id'] == user_id and loan['status'] == "Borrowed":
                user_loans.append(loan)

        return user_loans
    
    def getAllAuthUserHistory(self):
        loan_history = getLoanHistory()
        user_id = self.getUserId()

        user_loans = []

        for loan in loan_history:
            if loan['student_id'] == user_id:
                user_loans.append(loan)

        return user_loans

    

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

# View all equipment in the system
def viewAllEquipment():
    print("\n  ── All Equipment List ── \n")

    equipment_lists = getEquipmentLists()

    if not equipment_lists:
        print(f"\n {RED} [!] No equipment found in the system. {RESET}")
        return
    
    print(pd.DataFrame(equipment_lists))
    print(f"\n {GREEN} [✓] Total equipment: {len(equipment_lists)} {RESET}")

# Save equipment lists
def saveEquipmentList(equipment_lists):
    try:
        with open(EQUIPMENT_LIST_FILE, 'w') as list:
            json.dump(equipment_lists, list, indent=4)
    except IOError as e:
        print(f"\n  {RED} [!] Error writing to equipment list file: {e} {RESET}")

def getLoanHistory():
    loan_history = []

    try:
        with open(BORROWING_HISTORY_FILE, 'r') as file:
            content = file.read().strip()

            if content:
                loan_history = json.loads(content)
                
    except FileNotFoundError:
        print(f"\n {RED} [!] '{BORROWING_HISTORY_FILE}' not found. Please create the file. {RESET}")
    except IOError as e:
        print(f"\n  {RED} [!] Error reading loan history file: {e} {RESET}")

    return loan_history


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
                
                return Coordinator(user['user_id'], user['username'])

            elif user["role"] == "student":
                print(f"{GREEN}\n  Welcome, Student {request_username}! {RESET}")

                return Student(user['user_id'], user['username'])
    
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
                user.loadUserMenu()
            else:
                print("\n  [!] Too many failed attempts. Returning to main menu.")

        elif choice == "0":
            print("\n  Thank you for using the Sports Equipment Loan System. Goodbye!\n")
            break
        else:
            print("\n  [!] Invalid choice. Enter 1 to login or 0 to exit.")


main()   