items = [
    {"name": "Apples", "quantity": 50},
    {"name": "Bananas", "quantity": 30},
    {"name": "Oranges", "quantity": 20}
]

while True:
    print("\nInventory Menu")
    print("1. View Inventory")
    print("2. Update Stock")
    print("3. Add New Item")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\nCurrent Inventory:")
        for item in items:
            print(item["name"] + ": " + str(item["quantity"]))
    
    elif choice == "2":
        item_name = input("Enter item name to update: ")
        found = False
        for item in items:
            if item["name"].lower() == item_name.lower():
                qty = input("Enter new quantity: ")
                if qty.isdigit():
                    item["quantity"] = int(qty)
                    print("Stock updated.")
                else:
                    print("Invalid quantity.")
                found = True
                break
        if not found:
            print("Item not found.")

    elif choice == "3":
        new_name = input("Enter new item name: ")
        new_qty = input("Enter quantity: ")
        exists = False
        for item in items:
            if item["name"].lower() == new_name.lower():
                exists = True
                break
        if exists:
            print("Item already exists.")
        elif new_qty.isdigit():
            items.append({"name": new_name, "quantity": int(new_qty)})
            print("Item added.")
        else:
            print("Invalid quantity.")

    elif choice == "4":
        print("Exiting program.")
        break
    else:
        print("Invalid choice.")
