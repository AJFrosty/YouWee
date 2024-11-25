from datetime import datetime

class Receipt:
    def __init__ (self, items:dict[dict]):
        self.__items = items

    #Return Item Totals, Item Details and Grand Total
    def calculateItemTotals (self, memberID: str, discount: float, cart: dict[dict]) -> tuple:
        totalCost = 0
        itemDetails = []
        for item in cart[memberID]:
            itemName = self.__items[item]["name"]
            unitprice = self.__items[item]["price"]
            quantity = cart[memberID][item]
            itemTotal = unitprice * quantity
            totalCost += itemTotal
            itemDetails.append((itemName, unitprice,quantity,itemTotal))
        grandTotal = totalCost - discount
        return itemDetails, totalCost, grandTotal

    #Returns the customer's receipt
    def generateReceipt(self, memberID: str, discount: float, cart: dict[dict], points: int) -> str:
        receipt = []
        receipt.append(f"\t\t\tYOUWEE\n\t\t\tRECEIPT\nMember ID: {memberID}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        receipt.append("\t\t\t\t\tUnit Price\t\tQuantity\t\tTotal")
        itemDetails, totalCost, grandTotal = self.calculateItemTotals(memberID, discount, cart)
        for itemName, unitprice, quantity, itemTotal in itemDetails:
            receipt.append(f"{itemName}\t\t\t\t${unitprice:.2f}\t\t\t{quantity}\t\t\t${itemTotal:.2f}")
        receipt.append(f"\nTOTAL: ${totalCost:.2f}\nDiscount: ${discount:.2f}\nGRAND TOTAL: ${grandTotal:.2f}\n\nPOINTS EARNED:{points}")
        return "\n".join(receipt)
    
class POS:
    def __init__ (self, member: str, items: dict[dict]):
        self.__member = member
        self.__items = items
        self.__cart = {self.__member:{}}
        self.__receipt = Receipt(items)
    
    #Checks if cart is empty
    def isEmpty(self) -> bool:
        cart = self.getCart()
        return len(cart) == 0
    
    #Checks if an item is in the cart
    def isInCart(self, itemID: str) -> bool:
        if itemID in self.__cart[self.__member]:
            return True
        return False
    
    #Remove item from cart
    def removeFromCart(self, itemID: str, quantity: int) -> None:
        if quantity < 1:
            print("Quantity can't be less than 1.")
            return
        if quantity < self.__cart[self.__member][itemID]:
            self.__cart[self.__member][itemID] -= quantity
        elif quantity == self.__cart[self.__member][itemID]:
            del self.__cart[self.__member][itemID]
        else:
            print("Quantity cant be more than what's in the cart.")
            return

    #Returns the current customer cart
    def getCart(self) -> dict:
        if self.__cart[self.__member]:
            return self.__cart
        return {}
    
    #List information on all current items in the cart
    def listCartItems(self) -> None:
        if self.isEmpty():
            print("Your cart is empty.")
            return

        print(f"\nItems in your cart({self.__member}):")
        for item_id, quantity in self.__cart[self.__member].items():
            itemName = self.__items[item_id]["name"]
            price = self.__items[item_id]["price"]
            itemTotal = price * quantity
            print(f"ID: {item_id}, Name: {itemName}, Price: ${price:.2f}, Quantity: {quantity}, Total: ${itemTotal:.2f}")

    #Adds an item to the customer's cart
    def addToCart(self, itemID: str, quantity: int) -> None: 
        if itemID in self.__cart[self.__member]:
            self.__cart[self.__member][itemID] += quantity
        else:
            self.__cart[self.__member][itemID] = quantity
    
    #Calculate the total of a customer's cart
    def calculateTotal(self, discount:int = 0) -> float:
        total = 0
        for item in self.__cart[self.__member]:
            price =  self.__items[item]["price"]
            quantity = self.__cart[self.__member][item]
            total += (quantity*price)
        return total - discount

    #Get the value of the stock value after purchase
    def getUpdatedStock(self) -> dict:
        updatedStockInfo = {}

        for itemID in self.__cart[self.__member]:
            if itemID not in self.__items:
                print(f"Item {itemID} does not exist.")
                continue
            
            quantity = self.__cart[self.__member][itemID]
            currentStock = self.__items[itemID]["stock"]
            
            if quantity > currentStock:
                print(f"Insufficient stock for {itemID}.")
            
            updatedStock = max(0, currentStock - quantity)
            updatedStockInfo[itemID] = updatedStock

        return updatedStockInfo
        
    #Finalize the purchase and generates a receipt
    def finalizePurchase(self, discount:float, points: int) -> str:
        if self.__member not in self.__cart or not self.__cart[self.__member]:
            print("Cart is empty. Cannot finalize purchase.")
            return None
        #generate receipt
        receipt = self.__receipt.generateReceipt(self.__member, discount, self.__cart, points)
        self.__cart = {}
        return receipt 
