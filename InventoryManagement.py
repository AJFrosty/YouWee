class Item:
    def __init__(self, itemID: str, name: str, price: float, stock: int,seasonal: bool):
        self.__itemID = itemID
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__seasonal = seasonal  

    def getItemId(self) -> str:
        return self.__itemID

    def getName(self) -> str:
        return self.__name

    def getPrice(self) -> float:
        return self.__price

    def getStock(self) -> int:
        return self.__stock

    def isSeasonal(self) -> bool:
        return self.__seasonal

    def setStock(self, quantity: int) -> None:
        if quantity >= 0:
            self.__stock = quantity
        else:
            print("Quantity cannot be negative.")
    
    def setSeasonal(self, seasonal: bool) -> None:
        self.__seasonal = seasonal

class Inventory:
    def __init__(self, inventoryFile: str = 'Storage\\INVENTORY.txt'):
        self.__inventoryFile = inventoryFile
        self.__items = {}
        self.loadItems()

    #Load in all item information from the Inventory
    def loadItems(self) -> None:
        try:
            with open(self.__inventoryFile, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:    
                        itemID, name, price, quantity, seasonal = line.split(':')
                        self.__items[itemID] = Item(itemID, name, float(price), int(quantity), seasonal == "SEASONAL")
        except FileNotFoundError:
            print(f"File '{self.__inventoryFile}' not found. Starting with an empty inventory.")

    #Returns a dictionary of all the inventory items
    def getInventory(self) -> dict[dict]:
        self.loadItems()
        data = {}
        for itemID, item in self.__items.items():
            data[itemID] = {
                "name": item._Item__name,
                "price": item._Item__price,
                "stock": item._Item__stock,
                "seasonal": item._Item__seasonal
            }
        return data
    
    #Returns a dictionary of all items and their price/stock level
    def getPrices(self) -> dict[dict]:
        self.loadItems()
        data = {}
        for itemID, item in self.__items.items():
            data[itemID] = {
                "price": item._Item__price,
                "stock": item._Item__stock,
                "seasonal": item._Item__seasonal
            }
        return data
    
    #Saves the current inventory back to the INVENTORY.txt file.
    def saveItems(self) -> None:
        with open(self.__inventoryFile, 'w') as file:
            for item in self.__items.values():
                # Check if the item is seasonal and write to file
                seasonalStatus = "SEASONAL" if item.isSeasonal() else "NOTSEASONAL"
                file.write(f"{item.getItemId()}:{item.getName()}:{item.getPrice():.2f}:{item.getStock()}:{seasonalStatus}\n")
        print("Items saved successfully!")

    #Edits the seasonal status of an item.
    def editSeasonalStatus(self, itemID: str, seasonal: bool) -> None:
        if itemID in self.__items:
            self.__items[itemID].setSeasonal(seasonal)
            self.saveItems()
            print(f"Seasonal status of item {itemID} updated to {'SEASONAL' if seasonal else 'NOTSEASONAL'}.")
        else:
            print(f"Item with ID {itemID} does not exist.")

    #Adds a new item to the inventory.
    def addItem(self, item: Item) -> None:
        if item._Item__itemID in self.__items:
            print(f"Item with ID {item._Item__itemID} already exists.")
        else:
            self.__items[item._Item__itemID] = item
            self.saveItems()
            print(f"Item {item._Item__name} added successfully.")

    #Removes an item from the inventory based on the item ID.
    def removeItem(self, itemID: str) -> None:
        if itemID in self.__items:
            del self.__items[itemID]
            self.saveItems()
            print(f"Item with ID {itemID} removed successfully.")
        else:
            print(f"Item with ID {itemID} does not exist.")

    #Updates the stock level for a specified item.
    def updateStock(self, updatedStockInfo: dict) -> None:
        for itemID, updatedStock in updatedStockInfo.items():
            if itemID in self.__items:
                self.__items[itemID].setStock(updatedStock)
                print(f"Stock for item with ID {itemID} updated successfully to {updatedStock}.")
            else:
                print(f"Item with ID {itemID} does not exist.")
        
        self.saveItems()

    #Lists all items with their current stock levels.
    def listItems(self) -> None:
        if self.__items:
            print("Inventory Items:")
            for item in self.__items.values():
                print(f"ID: {item.getItemId()}, Name: {item.getName()}, Price: {item.getPrice():.2f}, Stock: {item.getStock()}")
        else:
            print("No items in inventory.")

    #Checks if an item is in invrntory
    def isItem(self, itemID: str) -> bool:
        return itemID in self.__items
    
    #Checks if an item is in stock
    def isInStock(self, itemID: str, quantity: int) -> bool:
        if itemID in self.__items:
            return self.__items[itemID].getStock() >= quantity
        else:
            return False