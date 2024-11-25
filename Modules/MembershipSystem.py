from datetime import datetime

class Member:
    def __init__(self, memberID: str, name: str, email: str, role: str, points: int=0):
        self.__memberId = memberID
        self.__name = name
        self.__email = email
        self.__history = {}
        self.__points = points
        self.__role = role
        self.__roles = ["Apprentice", "Explorer", "Expert", "Master", "Legend"]
    
    #Returns the Customer's ID
    def getId(self) -> str:
        return self.__memberId
    
    #Returns the Customer's Name
    def getName(self) -> str:
        return self.__name
    
    #Returns the Customer's Email
    def getEmail(self) -> str:
        return self.__email

    #Returns The Customer's Royalty Points
    def getPoints(self) -> int:
        return self.__points
    
    #Returns The Customer's Role
    def getRole(self) -> str:
        return self.__role
    
    #Returns The Customer's Full Information
    def getMember(self) -> dict:
        return {
            self.__memberId: { 
                "name": self.__name, 
                "email": self.__email, 
                "points": self.__points, 
                "role": self.__role, 
                "history": self.__history 
            }
        }
    
    # #Change Information For A Customer
    def setMemberDetails(self, name: str="", email: str="", role: str="", points: int=0) -> None:
        if name:
            self.__name = name
        if email:
            self.__email = email
        if role in self.__roles:
            self.__role = role
        #We Never Set Points Only Add
        if points:
            self.__points += points
        else:
            print(f"Error: The role '{role}' does not exist! Available roles are: {self.__roles}")
    
    #Edits The History For All Members
    def addPurchaseHistory(self, date: str, history: dict) -> None:
        if not (date in self.__history):
            self.__history[date] = history
        else:
            print("Error In Saving History")

    #Add A Recent Purchase To a Customer's History
    def addPurchase(self, cart: dict,points: int) -> None:
        for date, items in cart.items():
            if date not in self.__history:
                self.__history[date] = {}
            
            for item_id, quantity in items.items():
                if item_id in self.__history[date]:
                    self.__history[date][item_id] += quantity
                else:
                    self.__history[date][item_id] = quantity

        self.__points += points
    
    #Change The Current Member
    def updateMembers(self,data: dict) -> "Member":
        member = Member(member_id=data["id"], name=data["name"], email=data["email"], role=data["role"])
        self.__points = data["points"]
        self.__history = data["history"]
        return member       
    
class MemberDatabase:
    def __init__(self, filename: str="Storage\\MEMBERS.txt", historyFile: str="Storage\\PURCHASE_HISTORY.txt") -> None:
        self.__filename = filename
        self.__historyFile = historyFile
        self.__history = {}
        self.__members= {}
        self.loadMembers()
        self.loadHistory()
    
    #Load All Customers' From Database File
    def loadMembers(self) -> None:
        self.__members = {}
        try:
            with open(self.__filename, "r") as file:
                for line in file:
                    memberData = line.strip().split(":")
                    memberID = memberData[0]
                    name = memberData[1]
                    email = memberData[2]
                    points = int(memberData[3])
                    role = memberData[4]

                    self.__members[memberID] = Member(memberID, name, email, role, points)

        except FileNotFoundError:
            print(f"File '{self.__filename}' not found. Starting with an empty member list.")

    #Creates a New Customer on our system
    def processNewMember(self) -> str:
        print("Create New User:")
        while True:
            name = input("Enter Your First & Last Name: ").strip()
            if not self.isValidName(name):
                print("Invalid name. Please enter a first and last name separated by a space.")
                continue
            break

        while True:
            email = input("Enter Your Email: ").strip()
            if not self.isValidEmail(email):
                print("Invalid email. Please enter a valid email address (e.g., example@domain.com).")
                continue
            break

        return self.registerMember(name, email)
    
    #Checks if a name is valid
    def isValidName(self, name: str) -> bool:
        parts = name.split()
        return len(parts) == 2 and all(part.isalpha() for part in parts)
    
    #Checks if an email is valid
    def isValidEmail(self, email: str) -> bool:
        parts = email.split("@")
        return len(parts) == 2
    
    #parse a single line of history file into structured data
    def parseHeader(self, line: str) -> tuple[str, str, list]:
        historyData = line.strip().split(":")
        memberID = historyData[0]
        date = historyData[1]
        items = historyData[2:]
        return memberID, date, items
    
    #parse purchase item into dictionary of item ID and amount
    def parseItems(self, items: list) -> dict:
        history = {}
        for item in items:
            item = item.strip("()")
            itemID, amount = item.split(",")
            history[itemID.strip()] = int(amount.strip())
        return history
    
    #combines header and item parsing
    def parseHistoryLine(self, line: str) -> tuple[str, str, dict]:
        memberID, date, items = self.parseHeader(line)
        history = self.parseItems(items)
        return memberID, date, history 
    
    #Load All Customers' Purchase History
    def loadHistory(self) -> dict:
        self.__history = {}
        try:
            with open(self.__historyFile, "r") as file:
                for line in file:
                    memberID, date, history = self.parseHistoryLine(line)
                    if memberID not in self.__history:
                        self.__history[memberID] = {}
                    self.__history[memberID][date] = history
                
            print("History loaded successfully!")
        
        except FileNotFoundError:
            print(f"File '{self.__historyFile}' not found. Starting with an empty purchase history.")
        return self.__history

    #Display All Members Information from the Database File
    def getAllMembers(self) -> dict:
        self.loadMembers() 
        data = {}
        for memberID, member in self.__members.items():
            data[memberID] = {
                "name": member.getName(),
                "email": member.getEmail(),
                "role": member.getRole(),
                "points": member.getPoints(),
                "history": member._Member__history
            }
        return data

    #Save Current Member List In Database
    def saveMembers(self) -> None:
        with open(self.__filename, "w") as file:
            for memberID, member in sorted(self.__members.items()):
                #Automatically update the member's role based on their points if there are discrepancies
                points = member.getPoints()
                validRole = None
                if points < 500:
                    validRole = "Apprentice"
                elif points < 1000:
                    validRole = "Explorer"
                elif points < 1500:
                    validRole = "Expert"
                elif points < 2000:
                    validRole = "Master"
                else:
                    validRole = "Legend"
                
                #Check if role is valid or not
                if member.getRole() != validRole:
                    member.setMemberDetails(role=validRole)
                    print(f"Role for Member ID '{memberID}' updated to '{validRole}' based on points ({points}).")

                #Save The Members' Information correctly
                file.write(f"{memberID}:{member.getName()}:{member.getEmail()}:{member.getPoints()}:{member.getRole()}\n")

        print("\nAll members saved successfully!")

    #Updates History File
    def savePurchases(self, cart: dict) -> None:
        try:
            with open(self.__historyFile, "a") as file:
                for memberID, items in cart.items():
                    formattedItems = ":".join([f'({itemID},{quantity})' for itemID, quantity in items.items()])
                    file.write(f"{memberID}:{datetime.now().strftime('%Y-%m-%d')}:{formattedItems}\n")
            print("Purchases saved!")
        except Exception:
            print(f"Error saving purchase history")

    #Generates a Unique Customer ID For A User
    def generateID(self, name: str) -> str:
        initials = ''.join([word[0].upper() for word in name.split()[:2]])
        if len(initials) < 2:
            initials += "X"

        count = 0
        for memberID in self.__members:
            if memberID.startswith(initials):
                count += 1

        number = count + 1
        numberSTR = "00000" + str(number)
        numberSTR = numberSTR[-5:]
        return initials + numberSTR
    
    #Registers a new Customer On To The System
    def registerMember(self, name : str, email: str) -> str | None:
        for member in self.__members.values():
            if member.getName() == name and member.getEmail() == email:
                print("Member already exists. Registration skipped.")
                return None
        
        memberID = self.generateID(name)

        self.__members[memberID] = Member(memberID, name, email, role="Apprentice", points=0)
        self.saveMembers()

        #Prints The MemberID For Them To Keep/Know
        print(f"Registered Successfully! Member ID: {memberID}")
        return memberID

    #Update The Details of a Customer
    def updateMemberDetails(self, memberID: str, name: str=None, email: str=None, role: str=None, points: int=None) -> None:
        member = self.__members.get(memberID)
        if member:
            name = name if name else member.getName()
            email = email if email else member.getEmail()
            role = role if role else member.getRole()
            points = points if points else member.getPoints()
            
            member.setMemberDetails(name=name, email=email, role=role, points=points)
            self.saveMembers()
            print("Details updated!")
        else:
            print("Member does not exist.")
    
    #View Purchase History For Customer
    def viewPurchaseHistory(self, memberID: str) -> dict | None:
        return self.__history[memberID]
    
    #View Royalty Points For A Customer
    def viewRoyaltyPoints(self, memberID: str) -> int | None:
        member = self.__members.get(memberID)
        if member:
            return member.getPoints()
        else:
            print("Member does not exist.")
        return None
    
    #Get The Role of a Customer
    def getRole(self, memberID) -> str | None:
        member = self.__members.get(memberID)
        if member:
            return member.getRole()
        return None
    
    #Add Cart Purchases To a Member
    def addMemberPurchase(self, memberID: str, cart: dict) -> None:
        member = self.__members.get(memberID)
        if member:
            member.addPurchaseHistory(date=list(cart.keys())[0], history=cart[list(cart.keys())[0]])   
            print("Purchase added")
            self.savePurchases(cart)
        else:
            print("Member does not exist.")
        
    #Delete Member
