# =============================================================================
# Sports Equipment Loan System
# Group: XX
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# FILE PATH CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
USERS_FILE = "users.txt"

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


#User Authentication
def authenticate():
    print("\n  ── Login into your account ──")
    request_username = input("  Username: ").strip()
    request_password = input("  Password: ").strip()

    if not request_username or not request_password:
        print("\n  [!] Username and password cannot be empty.")

        return None
    

    #get list of users in the system
    systemUsers = getSystemUsers()

    #Check user credentials
    for user in systemUsers:

        if request_username == user["username"] and request_password == user["password"]:
            print(f"{GREEN}Login successful!{RESET}")
            break
    
    print(f"\n {RED} [!] Invalid username or password. Please try again. {RESET}")

    


authenticate()