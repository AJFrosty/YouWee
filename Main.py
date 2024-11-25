from Modules.InventoryManagement import Inventory
from Modules.MembershipSystem import MemberDatabase
from Modules.POS import POS
from Modules.RoyaltyProgram import RoyaltyProgram

#Initialize and return all required classes.
def initializeClasses(memberID: str = None) -> tuple:
    inv = Inventory()
    memberDB = MemberDatabase()
    cashier = POS(memberID, inv.getInventory())
    return inv, memberDB, cashier

#Handles adding items to the cart.
def handleAddingToCart(inv: Inventory, cashier: POS):
    inv.listItems()
    while True:
        item = input("Enter Item ID To Add To Cart (or press Enter to stop adding): ").strip()
        if not item:
            break

        if not inv.isItem(item):
            print("The Item Entered Isn't Valid")
            continue

        try:
            quantity = int(input("How Many: "))
            if inv.isInStock(item, quantity):
                cashier.addToCart(item, quantity)
                updatedStock = cashier.getUpdatedStock()
                inv.updateStock(updatedStock)
            else:
                stock = inv.getInventory()[item]["stock"]
                print(f"Stock Level of {inv.getInventory()[item]['name']} is {stock}")
        except ValueError:
            print("Invalid quantity. Please enter a number.")

#Handles removing items from the cart.
def handleRemoveItemsFromCart(cashier: POS, memberID: str, inv: Inventory):
    if not cashier.getCart() or memberID not in cashier.getCart():
        print("Your cart is empty. Nothing to remove.")
        return

    cashier.listCartItems()
    while True:
        item = input("Enter the Item ID to remove (or press Enter to stop removing): ").strip()
        if not item:
            break

        if item not in cashier.getCart()[memberID]:
            print(f"The item {item} is not in your cart. Please enter a valid item ID.")
            continue

        try:
            quantity = int(input(f"How many of {item} do you want to remove? "))
            cashier.removeFromCart(item, quantity)
            currentStock = inv.getInventory()[item]["stock"]
            inv.updateStock({item:currentStock+quantity})
            break
        except ValueError:
            print("Invalid quantity. Please enter a valid number.")

#Manage adding and removing items in the cart.
def handleCartOperations(cashier: POS, inv: Inventory, memberID: str):
    while True:
        print("\nCart Operations: \n1. Add Items to Cart\n2. Remove Items from Cart\n0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handleAddingToCart(inv, cashier)
        elif choice == "2":
            handleRemoveItemsFromCart(cashier, memberID, inv)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

#Ensure the customer selects a valid ability to use.
def handleAbilitySelection(royaltySys: RoyaltyProgram, memberDB: MemberDatabase, memberID: str, total: float) -> str:
    while True:
        ability = input("Enter The Ability The Customer Would Like To Use (Enter '0' if Not Eligible): ").strip()
        
        if ability == "0":
            print("No reward selected. Finalizing without any discounts.")
            return ability

        if royaltySys.isEligibleForReward(memberDB.getRole(memberID), total, ability):
            return ability

#Finalize the purchase and apply any royalty program benefits.
def checkout(memberDB: MemberDatabase, cashier: POS, memberID: str, inv: Inventory):
    if cashier.isEmpty():
        print("Cart Empty! Get Out Of The Line!")
        return
    
    cart = cashier.getCart()
    total = cashier.calculateTotal()
    
    royaltySys = RoyaltyProgram(memberID, cart, inv.getInventory(), memberDB.loadHistory())
    royaltySys.displayAbilities(memberDB.getRole(memberID), total)
    
    ability = handleAbilitySelection(royaltySys,memberDB,memberID,total)
    if ability != "0":
        discount = royaltySys.useAbilities(memberDB.getRole(memberID), ability, total)
    else:
        discount = 0

    #Update Member Details
    pointsEarned = royaltySys.getPoints()
    memberDB.updateMemberDetails(memberID, points=pointsEarned)
    memberDB.savePurchases({memberID: cart[memberID]})

    #Update Inventory
    inv.updateStock(cashier.getUpdatedStock())

    #Receipt Generation
    receipt = cashier.finalizePurchase(discount, pointsEarned)
    print(receipt)
    print("\n" + "="*80 + "\n")

#Main Program
def main():
    inv, memberDB, cashier = initializeClasses()

    while True:
        memberID = input("Enter Customer ID (or -999 to exit): ").strip()
        if memberID == "-999":
            print("Closing for the day...")
            break
        
        if memberID not in memberDB.getAllMembers():
            memberID = memberDB.processNewMember()
        
        #Initialize a new POS instance for each customer
        inv, memberDB, cashier = initializeClasses(memberID)
        
        handleCartOperations(cashier, inv, memberID)
        checkout(memberDB, cashier, memberID, inv)

if __name__ == "__main__":
    main()