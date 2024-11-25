[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/NWFDurr0)
# COMP1205-GroupProject

## **Project Specifications**

### **Overview**
The **YouWee Society Members Only Club** mantains a high-end supermarket chain operating in Antigua and Barbuda. The management team is focused on elevating the shopping experience for its exclusive members. They aim to create a Python-based Inventory and Point of Sale (POS) system to manage stock, facilitate efficient checkout, and implement a unique royalty program that enhances member loyalty. After consulting Python programmers attending COMP1205, the chain has defined the following requirements for the programmers to implement a software solution to manage their supermarket.

### **Requirements**

1. **Inventory Management Module**
   - Tracks and manages stock levels for items available in the supermarket.
   - Allows staff to add, remove, or update items in the inventory.

2. **Point of Sale (POS) Module**
   - Provides an interface for cashiers to process purchases for members.
   - Calculates totals, applies discounts, and updates inventory upon sale.

3. **Membership System**
   - Registers new members and maintains a member database.
   - Allows members to log in and view their purchase history and royalty points.

4. **Royalty Program**
   - A unique and engaging royalty program for frequent shoppers.
   - Encourages repeat purchases by offering benefits such as discounts, points, or exclusive member rewards.
   - Programmers are encouraged to creatively define how points are earned and redeemed.

---

## **Project Breakdown**

### **Modules**

#### **1. Inventory Management Module**
- **Description**: Manages items in the supermarket's stock. Supports operations to add, update, or delete items in the inventory.

  - **Classes**
    - `Item`: Represents an item in the inventory.
    - `Inventory`: Manages a collection of `Item` objects, including stock control and item search.

  - **Functions**
    - `add_item(self, item: Item)`: Adds a new item to the inventory.
    - `remove_item(self, item_id: str)`: Removes an item based on the item ID.
    - `update_item(self, item_id: str, quantity: int)`: Updates the stock level for a specified item.
    - `list_items(self)`: Lists all items with their current stock levels.

#### **2. Point of Sale (POS) Module**
- **Description**: Handles customer transactions, calculates totals, and adjusts inventory after sales.

  - **Classes**
    - `POS`: Manages the checkout process and receipt generation.
    - `Receipt`: Represents a customer’s receipt, with details of purchased items, total cost, and applied discounts.

  - **Functions**
    - `start_transaction(self, member_id: str)`: Begins a transaction for a member.
    - `add_to_cart(self, item_id: str, quantity: int)`: Adds an item to the member’s shopping cart.
    - `calculate_total(self)`: Calculates the total cost of items in the cart, including discounts.
    - `finalize_purchase(self)`: Completes the transaction, updates inventory, and generates a receipt.
    - `generate_receipt(self)`: Prints or returns a summary of purchased items and the final amount due.

#### **3. Membership System**
- **Description**: Manages member registration, login, and profile details. Keeps track of members' purchase history and royalty points.

  - **Classes**
    - `Member`: Stores member information, including personal details and royalty points.
    - `MemberDatabase`: Manages the collection of `Member` objects, supporting registration, lookup, and updates.

  - **Functions**
    - `register_member(self, name: str, email: str)`: Registers a new member, adding them to the member database.
    - `update_member_details(self, member_id: str, **details)`: Updates the personal information of a member.
    - `view_purchase_history(self, member_id: str)`: Retrieves a member’s past purchases.
    - `view_royalty_points(self, member_id: str)`: Shows the current royalty points for a member.

#### **4. Royalty Program**
- **Description**: Implements a unique royalty program where members earn points for each purchase. Points can be redeemed for discounts or exclusive rewards. Creativity is encouraged in how points are earned and redeemed.

  - **Classes**
    - `RoyaltyProgram`: Manages the point-earning and redemption system.

  - **Functions**
    - `add_points(self, member_id: str, amount_spent: float)`: Adds points to a member's account based on purchase value.
    - `redeem_points(self, member_id: str, points: int)`: Redeems points for discounts or rewards.
    - `check_eligibility_for_rewards(self, member_id: str)`: Checks if a member qualifies for special rewards or discounts.

---

### **Additional Specifications**

1. **Data Storage**: 
   - Implement data storage using txt files to persist member and inventory information.

2. **User Interface**:
   - The interface should be text-based for ease of use, with clear prompts for each action.

### **Documentation**:
   - Provide clear comments in the code.
   - Include a README file explaining how to set up and use the system.


### **Deliverables**

- A fully functioning Python program structured according to the specifications.
- Documentation including a README and code comments.
- Example data files (txt) for inventory and members.

### **Grading Rubric**

Functionality: Completeness and accuracy of required functions.
Creativity: Unique implementation of the royalty program.
Code Quality: Code readability, comments, and adherence to Python standards.
Documentation: Clarity and completeness of the README file.

### **Conclusion**

The YouWee Society expects a robust system that not only simplifies inventory management and sales but also deepens customer loyalty through an innovative royalty program.
