import random
import datetime

class RoyaltyProgram:
    def __init__(self, memberID: str, cartInfo: dict[dict], itemInfo: dict, purchaseHist: dict[dict]):
        self.__member = memberID
        self.__cart = cartInfo
        self.__items = itemInfo
        self.__currentDay = datetime.datetime.now().strftime("%A")
        self.__roles = ["Apprentice", "Explorer", "Expert", "Master", "Legend"]
        self.__multipliers = {
            "Monday": {"KIT": 2},
            "Tuesday": {"FRU": 2, "VEG": 2},
            "Wednesday": {"TEC": 3},
            "Thursday": {"CLO": 2, "SPT": 2},
            "Friday": {"BEV": 3, "HOM": 2},
            "Saturday": {"AUT": 3, "JWL": 2},
            "Sunday": {"TOY": 3, "ART": 2},
        }

        if self.__member in purchaseHist:
            self.__history = purchaseHist[self.__member]
        else:
            self.__history = {}

    #Get multiplier for a given category on the current day
    def getMultiplier(self, category: str) -> int:
        return self.__multipliers.get(self.__currentDay, {}).get(category, 1)

    #Calculate base points for an item
    def calculateBasePoints(self, price: float) -> int:
        return int(price*0.2+1)

    #Checks if a role is valid
    def isRole(self, role: str) -> bool:
        return role in self.__roles
    
    #Validate the role entered
    def validateRole(self, role: str) -> str:
        while not self.isRole(role):
            print(f"Invalid role entered. Available roles: {', '.join(self.__roles)}.")
            role = input("Enter a valid role or '0' to cancel: ").strip()
            
            #Customer opts out of using a reward
            if role == "0":
                return "0"
        
        return role

    #Calculate points for the entire cart
    def getPoints(self,points=0) -> int:
        totalPoints = 0

        for itemID, quantity in self.__cart[self.__member].items():
            category = itemID[:3]
            itemPrice = self.__items[itemID]['price']
            multiplier = self.getMultiplier(category)
            basePoints = self.calculateBasePoints(itemPrice)
            totalPoints += basePoints*multiplier*quantity

        return totalPoints + points

    #Check eligibility for a reward
    def isEligible(self,role:str, total:int, reward:str ="Apprentice") -> bool:
        if reward == "Apprentice":
            return total > 200

        if reward == "Explorer":
            if not self.__history:
                return False
            for item_id in self.__cart[self.__member]:
                for history_date, history_cart in self.__history.items():
                    if item_id in history_cart:
                        return role in ["Explorer", "Expert", "Master", "Legend"]

        if reward == "Expert":
            return len(self.__cart[self.__member]) >= 4 and role in ["Expert", "Master", "Legend"]

        if reward == "Master":
            return len(self.__cart[self.__member]) >= 3 and role in ["Master", "Legend"]

        if reward == "Legend":
            for itemID in self.__cart[self.__member]:
                if self.__items[itemID]["seasonal"]:
                    return role == "Legend"
                
        return False

    #Checking reward entered is valid before further checks
    def isEligibleForReward(self, role: str, total: float, reward: str) -> bool:
        reward = self.validateRole(reward)
    
        #User opted to not use a reward
        if reward == "0":
            return False

        # Check eligibility
        if not self.isEligible(role, total, reward):
            print(f"You are not eligible for the '{reward}' reward with your current role '{role}' or purchase total ${total:.2f}.")
            return False

        return True
    
    #Finds the highest-costing seasonal item in the cart and returns its ID and cost
    def getHighestCostSeasonalItem(self) -> tuple:
        highestCost = 0
        highestItemID = None

        for itemID, quantity in self.__cart[self.__member].items():
            if self.__items[itemID]["seasonal"] == True:
                itemCost = self.__items[itemID]["price"] * quantity
                if itemCost > highestCost:
                    highestCost = itemCost
                    highestItemID = itemID

        return highestItemID, highestCost
    
    #Display eligible rewards for a role
    def displayAbilities(self, role: str, total: int) -> None:
        eligibleRewards = [r for r in self.__roles if self.isEligible(role, total, r)]
        if eligibleRewards:
            for reward in eligibleRewards:
                print(f"Customer is eligible for {reward} reward")
        else:
            print("Customer isn't eligible for a reward!")

    #Use abilities based on the role and reward
    def useAbilities(self, role: str, reward: str, total: float = 0) -> float:
        role = self.validateRole(role)

        if not self.isEligible(role, total, reward):
            print(f"Customer is not eligible for {reward} reward.")
            return 0.0

        if reward == "Apprentice":
            return self.apprenticePerks(total)
        if reward == "Explorer":
            return self.explorerPerks()
        if reward == "Expert":
            return self.expertPerks()
        if reward == "Master":
            return self.masterPerks()
        if reward == "Legend":
            return self.legendPerks()

    #Customers with an Apprentice role shall get a 15% discount if they spend more than $200
    def apprenticePerks(self, totalSpent: float)-> float:
        return totalSpent*0.15

    #Apply a 25% discount on a random item the customer has bought before.
    def explorerPerks(self) -> float:
        userHistory = self.__history
        uniqueItems = set(item for purchases in userHistory.values() for item in purchases.keys())
        boughtBefore = [item for item in self.__cart[self.__member] if item in uniqueItems]

        if not boughtBefore:
            return 0

        discountedItem = random.choice(boughtBefore)
        itemQuantity = self.__cart[self.__member][discountedItem]
        itemPrice = self.__items[discountedItem]['price']
        discountAmt = 0.25 * itemPrice * itemQuantity

        print(f"Discounted Item: {self.__items[discountedItem]['name']} @25%. NetPrice: {(itemPrice - discountAmt):.2f}")
        return discountAmt

    #Appy a 25-40% discount to at least 0 items. Then for every 4 items they have a chance of another item.
    def expertPerks(self) -> float:
        perkAmount = random.randint(0, len(self.__cart[self.__member])//4)
        percentageAmount = random.randint(25, 40)/100
        discountedItems = random.sample(sorted(self.__cart[self.__member].keys()), perkAmount)
        discountAmt = 0

        for x in discountedItems:
            discountVal = self.__items[x]['price'] * percentageAmount
            discountAmt += discountVal
            print(f"Discounted Item: {x} @{percentageAmount*100:.0f}%. NetPrice: {(self.__items[x]['price'] - discountVal):.2f}")

        return discountAmt

    #Apply a 40-80% discount to at least 0 items. Then for every 3 items they have a chance of another item.
    def masterPerks(self) -> float:
        perkAmount = random.randint(0, len(self.__cart[self.__member])//3)
        percentageAmount = random.randint(40, 80)/100
        discountedItems = random.sample(sorted(self.__cart[self.__member]), perkAmount)
        discountAmt = 0

        for x in discountedItems:
            discountVal = self.__items[x]['price']*percentageAmount
            discountAmt += discountVal
            print(f"Discounted Item: {x} @{percentageAmount*100:.0f}%. NetPrice: {(self.__items[x]['price'] - discountVal):.2f}")

        self.getPoints()
        return discountAmt

    #Allow a customer to remove the entire cost of a single quantity of a seasonal item of highest value.
    def legendPerks(self) -> float:
        itemID, highestCost = self.getHighestCostSeasonalItem()
        if itemID:
            print(f"Legend Perk Applied: {self.__items[itemID]['name']} (ID: {itemID}) @ ${highestCost:.2f}")
            self.getPoints(-1000)
        return highestCost