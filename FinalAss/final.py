from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

# Create the main application window
menu = Tk()
menu.title("Fent Store")  # Set the title of the window
menu.geometry("1000x500")  # Set the size of the window

# Create a label at the top with the store name
label = Label(menu, text="𝓕𝓮𝓷𝓽 𝓢𝓽𝓸𝓻𝓮", font=("Arial", 69))
label.pack(pady=20)  # Add some space around the label

# Error message pop-up
def show_error(title="Error", message="An error has occurred.", severity="error"):
    """
    Displays a customizable error message popup.
    FORMAT
    title, message, severity (colour)
    """
    errorMessage = Tk()
    errorMessage.withdraw()  # Hide the root window

    popup = Toplevel()

    # Adjust the appearance based on severity
    if severity == "error":
        popup.title("Error")
        bg_color = "red"
    elif severity == "warning":
        popup.title("Warning")
        bg_color = "orange"
    elif severity == "info":
        popup.title("Information")
        bg_color = "blue"
    else:
        popup.title("Notice")
        bg_color = "gray"

    popup.configure(bg=bg_color)  # Set background color based on severity

    Label(popup, text=message, padx=20, pady=10, wraplength=300, bg=bg_color, fg="white").pack()

    Button(popup, text="OK", command=popup.destroy, padx=10, pady=5, bg="white").pack(pady=10)

    popup.geometry("300x150")  # Set a default size
    popup.mainloop()

# Function to handle "Add a new product" button click
def add_new_product():
    # Create a new window for adding a product
    addProductWindow = Toplevel(menu)
    addProductWindow.title("Add a New Product")
    addProductWindow.geometry("1200x200")

    # Create table headers
    headers = ["Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"]

    for col, header in enumerate(headers):
        Label(addProductWindow, text=header, font=("Arial", 12, "bold"), borderwidth=2, relief="solid", padx=5, pady=5).grid(row=0, column=col, sticky="nsew")

    # Create entry fields for table rows
    addNewProductEntries = []

    # Add entries for all fields except Supplier
    for col in range(len(headers)):
        if col != 3:  # Supplier column will be a dropdown
            addNewProductEntry = Entry(addProductWindow, font=("Arial", 12))
            addNewProductEntry.grid(row=1, column=col, padx=5, pady=5)
            addNewProductEntries.append(addNewProductEntry)

    # Load suppliers from supplier.txt
    try:
        with open("suppliers.txt", "r") as file:
            suppliers = [line.strip().split(",")[1] for line in file.readlines()]  #2nd column is the supplier name
    except FileNotFoundError:
        suppliers = []

    # Check if suppliers exist
    if not suppliers:
        addProductWindow.destroy()
        show_error(title="No Suppliers Found", message="No suppliers found. Please add a supplier first.", severity="error")
        return

    # Create a dropdown menu for Supplier
    supplier_var = StringVar()
    supplier_var.set("Select Supplier")  # Default value

    supplier_dropdown = OptionMenu(addProductWindow, supplier_var, *suppliers)
    supplier_dropdown.config(font=("Arial", 12))
    supplier_dropdown.grid(row=1, column=3, padx=5, pady=5)

    # Function to save data to a text file
    def save_product():
        # Validate that Product ID, Price, and Quantity contain only numbers
        if not addNewProductEntries[0].get().isdigit():
            show_error(title="Value Error!", message="Product ID must be a number!", severity="error")
            return

        if not addNewProductEntries[3].get().replace('.', '', 1).isdigit():  # Allow decimal for Price
            show_error(title="Value Error!", message="Price must be a number!", severity="error")
            return

        if not addNewProductEntries[4].get().isdigit():
            show_error(title="Value Error!", message="Quantity must be a number!", severity="error")
            return

        # Check if a supplier is selected
        if supplier_var.get() == "Select Supplier":
            show_error(title="Value Error!", message="Please select a supplier.", severity="error")
            return

        # Save valid data to the file
        with open("product.txt", "a") as file:
            data = [
                addNewProductEntries[0].get(),
                addNewProductEntries[1].get(),
                addNewProductEntries[2].get(),
                supplier_var.get(),  # Selected supplier name
                addNewProductEntries[3].get(),
                addNewProductEntries[4].get(),
            ]
            file.write(",".join(data) + "\n")  # Write the data as a comma-separated line

        for addNewProductEntry in addNewProductEntries:
            addNewProductEntry.delete(0, END)  # Clear entry fields
        supplier_var.set("Select Supplier")  # Reset supplier dropdown

        show_error(title="Success!", message="Product has been added!", severity="info")  # Provide user feedback

    # Add Save and Exit to Menu buttons
    save_button = Button(addProductWindow, text="Save Product", font=("Arial", 12), command=save_product)
    save_button.grid(row=2, column=1, columnspan=2, pady=10, sticky="ew")

    def exit_to_menu():
        addProductWindow.destroy()

    exit_button = Button(addProductWindow, text="Exit to Menu", font=("Arial", 12), command=exit_to_menu)
    exit_button.grid(row=2, column=3, columnspan=2, pady=10, sticky="ew")

# Function to handle "Update product details" button click
def update_product_details():
    # Create a new window for updating product details
    update_window = Toplevel(menu)
    update_window.title("Update Product Details")
    update_window.geometry("800x600")

    # Label for the section
    Label(update_window, text="Update Product Details", font=("Arial", 14, "bold")).pack(pady=10)

    # Frame for Treeview
    frame = Frame(update_window)
    frame.pack(pady=10)

    # Treeview to display existing products
    tree = ttk.Treeview(frame, columns=("Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"), show="headings", height=10)
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    # Scrollbar for Treeview
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Define Treeview columns
    columns = ["Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"]
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Function to load products from file
    def load_products():
        try:
            with open("product.txt", "r") as file:
                products = [line.strip().split(",") for line in file.readlines()]
                # Clear the Treeview
                tree.delete(*tree.get_children())
                # Add products to Treeview
                for product in products:
                    tree.insert("", "end", values=product)
        except FileNotFoundError:
            show_error(title="File Not Found", message="The product file was not found.", severity="error")

    # Load products initially
    load_products()

    # Function to delete the selected product
    def delete_selected_product():
        selected_item = tree.selection()
        if not selected_item:
            show_error(title="No Selection", message="Please select a product to delete.", severity="warning")
            return

        # Get selected product details
        product_values = tree.item(selected_item, "values")

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Product ID: {product_values[0]}?")
        if not confirm:
            return

        # Remove the product from the file
        try:
            with open("product.txt", "r") as file:
                products = [line.strip().split(",") for line in file.readlines()]

            # Filter out the selected product
            products = [product for product in products if product[0] != product_values[0]]

            # Save updated products back to the file
            with open("product.txt", "w") as file:
                for product in products:
                    file.write(",".join(product) + "\n")

            # Refresh the Treeview
            load_products()

            show_error(title="Success!", message="Product deleted successfully!", severity="info")

        except Exception as e:
            show_error(title="Error", message=f"An error occurred: {e}", severity="error")

    # Function to edit a selected product (unchanged from before)
    def edit_selected_product():
        selected_item = tree.selection()
        if not selected_item:
            show_error(title="No Selection", message="Please select a product to update.", severity="warning")
            return

        # Get selected product details
        product_values = tree.item(selected_item, "values")

        # Create a new window for editing product details
        edit_window = Toplevel(update_window)
        edit_window.title("Edit Product Details")
        edit_window.geometry("500x400")

        # Labels and entry fields for editing product details
        labels = ["Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"]
        entries = []

        # Load suppliers for dropdown
        try:
            with open("suppliers.txt", "r") as file:
                suppliers = [line.strip().split(",") for line in file.readlines()]
            supplier_names = [supplier[1] for supplier in suppliers]  # Use supplier names
        except FileNotFoundError:
            show_error(title="File Not Found", message="The suppliers file was not found.", severity="error")
            edit_window.destroy()
            return

        # Create entry fields or dropdowns
        for i, (label, value) in enumerate(zip(labels, product_values)):
            Label(edit_window, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=10, sticky=W)

            if label == "Supplier":
                # Create a dropdown menu for suppliers
                supplier_dropdown = ttk.Combobox(edit_window, values=supplier_names, font=("Arial", 12), state="readonly")
                supplier_dropdown.set(value)  # Set the current supplier as default
                supplier_dropdown.grid(row=i, column=1, padx=10, pady=10, sticky=W)
                entries.append(supplier_dropdown)
            else:
                # Create entry for other fields
                entry = Entry(edit_window, font=("Arial", 12))
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=10, pady=10, sticky=W)
                entries.append(entry)

        # Function to save updated product details
        def save_updated_product():
            updated_values = [entry.get() for entry in entries]

            # Validate inputs
            if not updated_values[0].isdigit():
                show_error(title="Invalid Value", message="Product ID must be a number.", severity="error")
                return
            if not updated_values[4].replace('.', '', 1).isdigit():
                show_error(title="Invalid Value", message="Price must be a number.", severity="error")
                return
            if not updated_values[5].isdigit():
                show_error(title="Invalid Value", message="Quantity must be a number.", severity="error")
                return

            # Update product in file
            try:
                with open("product.txt", "r") as file:
                    products = [line.strip().split(",") for line in file.readlines()]

                # Find and update the product
                for product in products:
                    if product[0] == product_values[0]:  # Match by Product ID
                        products[products.index(product)] = updated_values

                # Save updated products back to file
                with open("product.txt", "w") as file:
                    for product in products:
                        file.write(",".join(product) + "\n")

                # Refresh the Treeview
                load_products()

                # Close the edit window
                edit_window.destroy()

                show_error(title="Success!", message="Product details updated successfully!", severity="info")

            except Exception as e:
                show_error(title="Error", message=f"An error occurred: {e}", severity="error")

        # Save button
        save_button = Button(edit_window, text="Save Changes", font=("Arial", 12), command=save_updated_product)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

        # Exit button
        exit_button = Button(edit_window, text="Exit to Main Menu", font=("Arial", 12), command=edit_window.destroy)
        exit_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

        # Function to save updated product details
        def save_updated_product():
            updated_values = [entry.get() for entry in entries]

            # Validate inputs
            if not updated_values[0].isdigit():
                show_error(title="Invalid Value", message="Product ID must be a number.", severity="error")
                return
            if not updated_values[4].replace('.', '', 1).isdigit():
                show_error(title="Invalid Value", message="Price must be a number.", severity="error")
                return
            if not updated_values[5].isdigit():
                show_error(title="Invalid Value", message="Quantity must be a number.", severity="error")
                return

            # Update product in file
            try:
                with open("product.txt", "r") as file:
                    products = [line.strip().split(",") for line in file.readlines()]

                # Find and update the product
                for product in products:
                    if product[0] == product_values[0]:  # Match by Product ID
                        products[products.index(product)] = updated_values

                # Save updated products back to file
                with open("product.txt", "w") as file:
                    for product in products:
                        file.write(",".join(product) + "\n")

                # Refresh the Treeview
                load_products()

                # Close the edit window
                edit_window.destroy()

                show_error(title="Success!", message="Product details updated successfully!", severity="info")

            except Exception as e:
                show_error(title="Error", message=f"An error occurred: {e}", severity="error")

        # Save button
        save_button = Button(edit_window, text="Save Changes", font=("Arial", 12), command=save_updated_product)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

        # Exit button
        exit_button = Button(edit_window, text="Exit to Main Menu", font=("Arial", 12), command=edit_window.destroy)
        exit_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

    # Button to edit the selected product
    edit_button = Button(update_window, text="Edit Selected Product", font=("Arial", 12), command=edit_selected_product)
    edit_button.pack(pady=10)

    # Button to delete the selected product
    delete_button = Button(update_window, text="Delete Selected Product", font=("Arial", 12), command=delete_selected_product)
    delete_button.pack(pady=10)

    # Exit button to return to the main menu
    def exit_update_window():
        update_window.destroy()

    exit_button = Button(update_window, text="Exit to Main Menu", font=("Arial", 12), command=exit_update_window)
    exit_button.pack(pady=10)

#Function to handle "Add a supplier" button click
def add_new_supplier():
    # Create a new window for adding a supplier
    supplier_window = Toplevel(menu)
    supplier_window.title("Add a Supplier")
    supplier_window.geometry("800x700")

    # Label for the section
    Label(supplier_window, text="Add or Manage Suppliers", font=("Arial", 14, "bold")).pack(pady=10)

    # Frame for Treeview
    frame = Frame(supplier_window)
    frame.pack(pady=10)

    # Treeview to display existing suppliers
    tree = ttk.Treeview(frame, columns=("Supplier ID", "Supplier Name", "Supplier Contact"), show="headings", height=10)
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    # Scrollbar for Treeview
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Define Treeview columns
    columns = ["Supplier ID", "Supplier Name", "Supplier Contact"]
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    # Function to load suppliers from file
    def load_suppliers():
        try:
            with open("suppliers.txt", "r") as file:
                suppliers = [line.strip().split(",") for line in file.readlines()]
                # Clear the Treeview
                tree.delete(*tree.get_children())
                # Add suppliers to Treeview
                for supplier in suppliers:
                    tree.insert("", "end", values=supplier)
        except FileNotFoundError:
            # If file doesn't exist, create an empty file
            with open("suppliers.txt", "w") as file:
                pass  # Simply create the file without writing anything

    # Load suppliers initially
    load_suppliers()

    # Frame for adding new supplier
    entry_frame = Frame(supplier_window)
    entry_frame.pack(pady=20)

    # Labels and entry fields for Supplier ID, Name, and Contact
    labels = ["Supplier ID", "Supplier Name", "Supplier Contact"]
    entries = []

    for i, label in enumerate(labels):
        Label(entry_frame, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=10, sticky=W)
        entry = Entry(entry_frame, font=("Arial", 12))
        entry.grid(row=i, column=1, padx=10, pady=10, sticky=W)
        entries.append(entry)

    # Function to save the supplier
    def save_supplier():
        supplier_id, supplier_name, supplier_contact = [entry.get().strip() for entry in entries]

        # Validate that supplier ID is filled
        if not supplier_id:
            show_error(title="Incomplete Details", message="Supplier ID must be filled.", severity="error")
            return
        
        # Validate that supplier name is filled
        elif not supplier_name :
            show_error(title="Incomplete Details", message="Supplier name must be filled.", severity="error")
            return
        
        # Validate that supplier contact is filled
        elif not supplier_contact:
            show_error(title="Incomplete Details", message="Supplier contact must be filled.", severity="error")
            return

        # Validate Supplier ID
        elif not supplier_id.isdigit():
            show_error(title="Invalid Value", message="Supplier ID must contain only numbers.", severity="error")
            return
        
        # Save the supplier to the file
        try:
            with open("suppliers.txt", "a") as file:
                file.write(f"{supplier_id},{supplier_name},{supplier_contact}\n")

            # Clear entry fields after saving
            for entry in entries:
                entry.delete(0, END)

            # Refresh the Treeview
            load_suppliers()

            show_error(title="Success!", message="Supplier added successfully!", severity="info")

        except Exception as e:
            show_error(title="Error", message=f"An error occurred: {e}", severity="error")

    # Button to save the supplier
    save_button = Button(supplier_window, text="Save Supplier", font=("Arial", 12), command=save_supplier)
    save_button.pack(pady=10)

    # Function to delete the selected supplier
    def delete_selected_supplier():
        selected_item = tree.selection()
        if not selected_item:
            show_error(title="No Selection", message="Please select a supplier to delete.", severity="warning")
            return

        # Get selected supplier details
        supplier_values = tree.item(selected_item, "values")

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Supplier ID: {supplier_values[0]}?")
        if not confirm:
            return

        # Remove the supplier from the file
        try:
            with open("suppliers.txt", "r") as file:
                suppliers = [line.strip().split(",") for line in file.readlines()]

            # Filter out the selected supplier
            suppliers = [supplier for supplier in suppliers if supplier[0] != supplier_values[0]]

            # Save updated suppliers back to the file
            with open("suppliers.txt", "w") as file:
                for supplier in suppliers:
                    file.write(",".join(supplier) + "\n")

            # Refresh the Treeview
            load_suppliers()

            show_error(title="Success!", message="Supplier deleted successfully!", severity="info")

        except Exception as e:
            show_error(title="Error", message=f"An error occurred: {e}", severity="error")

    # Function to update the selected supplier
    def update_supplier():
        selected_item = tree.selection()
        if not selected_item:
            show_error(title="No Selection", message="Please select a supplier to update.", severity="warning")
            return

        # Get selected supplier details
        supplier_values = tree.item(selected_item, "values")

        # Create a new window for updating the supplier
        update_window = Toplevel(supplier_window)
        update_window.title("Update Supplier")
        update_window.geometry("400x300")

        # Labels and entry fields for updating Supplier ID, Name, and Contact
        labels = ["Supplier ID", "Supplier Name", "Supplier Contact"]
        update_entries = []

        for i, label in enumerate(labels):
            Label(update_window, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=10, sticky=W)
            entry = Entry(update_window, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=10, sticky=W)
            entry.insert(0, supplier_values[i])  # Populate fields with current supplier details
            update_entries.append(entry)

        # Function to save the updated supplier details
        def save_updated_supplier():
            supplier_id, supplier_name, supplier_contact = [entry.get().strip() for entry in update_entries]

            # Validate that supplier ID is filled
            if not supplier_id:
                show_error(title="Incomplete Details", message="Supplier ID must be filled.", severity="error")
                return

            # Validate that supplier name is filled
            elif not supplier_name:
                show_error(title="Incomplete Details", message="Supplier name must be filled.", severity="error")
                return

            # Validate that supplier contact is filled
            elif not supplier_contact:
                show_error(title="Incomplete Details", message="Supplier contact must be filled.", severity="error")
                return

            # Validate Supplier ID
            elif not supplier_id.isdigit():
                show_error(title="Invalid Value", message="Supplier ID must contain only numbers.", severity="error")
                return

            # Update the supplier in the file
            try:
                with open("suppliers.txt", "r") as file:
                    suppliers = [line.strip().split(",") for line in file.readlines()]

                # Find and update the selected supplier
                for supplier in suppliers:
                    if supplier[0] == supplier_values[0]:  # Match the original Supplier ID
                        supplier[0] = supplier_id
                        supplier[1] = supplier_name
                        supplier[2] = supplier_contact
                        break

                # Write the updated list back to the file
                with open("suppliers.txt", "w") as file:
                    for supplier in suppliers:
                        file.write(",".join(supplier) + "\n")

                # Refresh the Treeview
                load_suppliers()

                # Close the update window
                update_window.destroy()

                show_error(title="Success!", message="Supplier updated successfully!", severity="info")
                  
            except Exception as e:
                show_error(title="Error", message=f"An error occurred: {e}", severity="error")

        # Button to save the updated supplier
        save_button = Button(update_window, text="Save Changes", font=("Arial", 12), command=save_updated_supplier)
        save_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Button to cancel the update and close the update window
        def cancel_update():
            update_window.destroy()

        cancel_button = Button(update_window, text="Cancel", font=("Arial", 12), command=cancel_update)
        cancel_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Button to update the selected supplier
    update_button = Button(supplier_window, text="Update Supplier", font=("Arial", 12), command=update_supplier)
    update_button.pack(pady=10)

    # Button to delete the selected supplier
    delete_button = Button(supplier_window, text="Delete Supplier", font=("Arial", 12), command=delete_selected_supplier)
    delete_button.pack(pady=10)

    # Button to close the window and return to the main menu
    def close_supplier_window():
        supplier_window.destroy()

    exit_button = Button(supplier_window, text="Exit to Menu", font=("Arial", 12), command=close_supplier_window)
    exit_button.pack(pady=10)

#Function to handle "Place A Customer's Order" button click
def place_an_order():
    # Create a new window for placing an order
    order_window = Toplevel(menu)
    order_window.title("Place an Order")
    order_window.geometry("900x750")

    # Top section for displaying existing orders
    Label(order_window, text="Existing Orders", font=("Arial", 14, "bold")).pack(pady=10)

    order_frame = Frame(order_window)
    order_frame.pack(pady=10)

    order_tree = ttk.Treeview(order_frame, columns=("Date/Time", "Order ID", "Product ID", "Product Name", "Quantity", "Total Price"), show="headings", height=10)
    order_tree.pack(side=LEFT, fill=BOTH, expand=True)

    order_scrollbar = Scrollbar(order_frame, orient=VERTICAL, command=order_tree.yview)
    order_tree.config(yscrollcommand=order_scrollbar.set)
    order_scrollbar.pack(side=RIGHT, fill=Y)

    # Define Order Treeview columns
    order_columns = ["Date/Time", "Order ID", "Product ID", "Product Name", "Quantity", "Total Price"]
    for col in order_columns:
        order_tree.heading(col, text=col)
        order_tree.column(col, width=120, anchor="center")

    # Load existing orders into the Treeview
    def load_orders():
        try:
            with open("order.txt", "r") as file:
                orders = [line.strip().split(",") for line in file.readlines()]
                # Sort orders by Product ID (index 2)
                orders.sort(key=lambda x: x[2])  # Product ID is at index 2 in the orders file
                order_tree.delete(*order_tree.get_children())
                for order in orders:
                    order_tree.insert("", "end", values=order)
        except FileNotFoundError:
             # If file doesn't exist, create an empty file
            with open("order.txt", "w") as file:
                pass  # Simply create the file without writing anything

    load_orders()

    # Middle section for placing a new order
    Label(order_window, text="Place an Order", font=("Arial", 14, "bold")).pack(pady=10)

    product_frame = Frame(order_window)
    product_frame.pack(pady=10)

    tree = ttk.Treeview(product_frame, columns=("Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"), show="headings", height=10)
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    product_scrollbar = Scrollbar(product_frame, orient=VERTICAL, command=tree.yview)
    tree.config(yscrollcommand=product_scrollbar.set)
    product_scrollbar.pack(side=RIGHT, fill=Y)

    # Define Product Treeview columns
    product_columns = ["Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"]
    for col in product_columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    def load_products():
        try:
            with open("product.txt", "r") as file:
                products = [line.strip().split(",") for line in file.readlines()]
                # Sort products by Product ID (index 0)
                products.sort(key=lambda x: x[0])  # Product ID is at index 0 in the products file
                tree.delete(*tree.get_children())
                for product in products:
                    tree.insert("", "end", values=product)
        except FileNotFoundError:
            show_error(title="File Not Found", message="The product file was not found.", severity="error")

    load_products()

    quantity_frame = Frame(order_window)
    quantity_frame.pack(pady=20)

    Label(quantity_frame, text="Enter Quantity:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
    quantity_entry = Entry(quantity_frame, font=("Arial", 12))
    quantity_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    # Place Order Functionality
    def place_order():
        selected_item = tree.selection()
        
        if not selected_item:
            show_error(title="No Selection", message="Please select a product to order.", severity="warning")
            return

        product_values = tree.item(selected_item, "values")
        product_id, product_name, description, supplier, price, available_quantity = product_values
        available_quantity = int(available_quantity)

        # Validate quantity
        try:
            # Check if the quantity entry is null or empty
            if not quantity_entry.get().strip():
                raise ValueError("Quantity cannot be left empty.")
            
            order_quantity = int(quantity_entry.get())
            if order_quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
            if order_quantity > available_quantity:
                raise ValueError("Quantity exceeds available stock.")
        except ValueError as e:
            show_error(title="Invalid Quantity", message=str(e), severity="error")
            return

        def get_next_order_id():
            try:
                with open("order.txt", "r") as file:
                    orders = file.readlines()
                    if orders:
                        last_order = orders[-1].strip().split(",")
                        return int(last_order[1][3:]) + 1  # Extract the numeric part of the Order ID and increment
                    else:
                        return 1  # Start with 01if the file is empty
            except FileNotFoundError:
                return 1 # Start with 1 if the file does not exist

        order_id = f"ORD{get_next_order_id()}"
        total_price = float(price) * order_quantity
        new_quantity = available_quantity - order_quantity

        # Update product quantity and save order
        try:
            with open("product.txt", "r") as file:
                products = [line.strip().split(",") for line in file.readlines()]
            for product in products:
                if product[0] == product_id:
                    product[5] = str(new_quantity)
            with open("product.txt", "w") as file:
                for product in products:
                    file.write(",".join(product) + "\n")

            from datetime import datetime
            order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("order.txt", "a") as file:
                file.write(f"{order_time},{order_id},{product_id},{product_name},{order_quantity},{total_price}\n")

            load_products()
            load_orders()
            quantity_entry.delete(0, END)

            show_error(title="Success!", message="Order placed successfully!", severity="info")

        except Exception as e:
            show_error(title="Error", message=f"An error occurred: {e}", severity="error")

    # Update Order Functionality
    def update_order():
        selected_item = order_tree.selection()
        if not selected_item:
            show_error(title="No Selection", message="Please select an order to update.", severity="warning")
            return

        order_values = order_tree.item(selected_item, "values")
        order_id, product_id, product_name, old_quantity, total_price = order_values[1], order_values[2], order_values[3], int(order_values[4]), float(order_values[5])

        # Create a new window for editing order details
        edit_window = Toplevel(order_window)
        edit_window.title(f"Edit Order {order_id}")
        edit_window.geometry("400x300")

        Label(edit_window, text=f"Editing Order: {order_id}", font=("Arial", 14, "bold")).pack(pady=10)
        Label(edit_window, text=f"Product: {product_name} (ID: {product_id})", font=("Arial", 12)).pack(pady=5)

        Label(edit_window, text="Enter New Quantity:", font=("Arial", 12)).pack(pady=10)
        new_quantity_entry = Entry(edit_window, font=("Arial", 12))
        new_quantity_entry.pack(pady=5)
        new_quantity_entry.insert(0, old_quantity)  # Pre-fill with the current quantity

        def save_updated_order():
            try:
                new_quantity = int(new_quantity_entry.get())
                if new_quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")

                # Load the products and find the relevant product
                with open("product.txt", "r") as file:
                    products = [line.strip().split(",") for line in file.readlines()]
                
                for product in products:
                    if product[0] == product_id:
                        available_quantity = int(product[5])
                        updated_stock = available_quantity + old_quantity - new_quantity

                        if updated_stock < 0:
                            raise ValueError("New quantity exceeds available stock.")
                        
                        product[5] = str(updated_stock)
                        break

                # Update the products file
                with open("product.txt", "w") as file:
                    for product in products:
                        file.write(",".join(product) + "\n")

                # Update the orders file
                with open("order.txt", "r") as file:
                    orders = [line.strip().split(",") for line in file.readlines()]

                for order in orders:
                    if order[1] == order_id:  # Match Order ID
                        order[4] = str(new_quantity)
                        order[5] = str(float(order[5]) / old_quantity * new_quantity)  # Update total price
                        break

                with open("order.txt", "w") as file:
                    for order in orders:
                        file.write(",".join(order) + "\n")

                # Reload UI data and close the edit window
                load_orders()
                load_products()
                edit_window.destroy()
                show_error(title="Success!", message="Order updated successfully!", severity="info")

            except ValueError as e:
                show_error(title="Invalid Quantity", message=str(e), severity="error")
            except Exception as e:
                show_error(title="Error", message=f"An error occurred: {e}", severity="error")

        Button(edit_window, text="Save Changes", font=("Arial", 12), command=save_updated_order).pack(pady=20)
        Button(edit_window, text="Cancel", font=("Arial", 12), command=edit_window.destroy).pack(pady=10)

    # Delete Order Functionality
    def delete_order():
        selected_item = order_tree.selection()
        if not selected_item:
            show_error(title="No Selection", message="Please select an order to delete.", severity="warning")
            return

        order_values = order_tree.item(selected_item, "values")
        order_id, product_id, product_name, order_quantity = order_values[1], order_values[2], order_values[3], int(order_values[4])

        try:
            # Remove the order from the orders file
            with open("order.txt", "r") as file:
                orders = [line.strip().split(",") for line in file.readlines()]
            orders = [order for order in orders if order[1] != order_id]
            with open("order.txt", "w") as file:
                for order in orders:
                    file.write(",".join(order) + "\n")

            # Update the product's quantity in the products file
            with open("product.txt", "r") as file:
                products = [line.strip().split(",") for line in file.readlines()]
            for product in products:
                if product[0] == product_id:  # Match the Product ID
                    product[5] = str(int(product[5]) + order_quantity)  # Add the ordered quantity back to available stock
            with open("product.txt", "w") as file:
                for product in products:
                    file.write(",".join(product) + "\n")

            # Reload data into the UI
            load_orders()
            load_products()
            show_error(title="Success!", message="Order deleted and product quantity updated successfully!", severity="info")

        except Exception as e:
            show_error(title="Error", message=f"An error occurred: {e}", severity="error")

    

    # Exit Button
    def close_order_window():
        order_window.destroy()


    # Create a frame to hold the buttons
    button_frame = Frame(order_window)
    button_frame.pack(pady=10, anchor="center")

    # Add buttons to the frame
    Button(button_frame, text="Place Order", font=("Arial", 12), command=place_order).pack(side=LEFT, padx=10)
    Button(button_frame, text="Update Order Details", font=("Arial", 12), command=update_order).pack(side=LEFT, padx=10)
    Button(button_frame, text="Delete Order", font=("Arial", 12), command=delete_order).pack(side=LEFT, padx=10)
    Button(button_frame, text="Exit to Menu", font=("Arial", 12), command=close_order_window).pack(side=LEFT, padx=10)

# Function to handle "Buy Stock From Supplier" button click
def buy_stock_from_supplier():
    # Create a new window for buying stock
    buy_window = Toplevel(menu)
    buy_window.title("Buy Stock from Supplier")
    buy_window.geometry("800x850")

    # Label for the section
    Label(buy_window, text="Buy Stock from Supplier", font=("Arial", 14, "bold")).pack(pady=10)

    def generate_order_id():
        try:
            with open("supplier_order.txt", "r") as file:
                orders = [line.strip().split(",")[0] for line in file.readlines()]
                if not orders:
                    return "SORD1"

                valid_ids = [int(order_id[4:]) for order_id in orders if order_id.startswith("SORD") and order_id[4:].isdigit()]
                if not valid_ids:
                    return "SORD1"

                max_id = max(valid_ids)
                return f"SORD{max_id + 1}"
        except FileNotFoundError:
            return "SORD1"

    # Load existing products
    products = []
    try:
        with open("product.txt", "r") as file:
            products = [line.strip().split(",") for line in file.readlines()]
    except FileNotFoundError:
        show_error(title="File Not Found", message="The product file was not found. Add product first", severity="error")
        buy_window.destroy()
        return

    # Load existing suppliers
    suppliers = []
    try:
        with open("suppliers.txt", "r") as file:
            suppliers = [line.strip().split(",") for line in file.readlines()]
    except FileNotFoundError:
        show_error(title="File Not Found", message="The supplier file was not found. Add Supplier first", severity="error")
        buy_window.destroy()
        return

    # Create a mapping of product ID to supplier for auto-selection
    product_to_supplier = {product[0]: product[3] for product in products}

    # Frame for Treeview (Products)
    frame_products = Frame(buy_window)
    frame_products.pack(pady=10)

    # Treeview to display existing products
    tree_products = ttk.Treeview(
        frame_products, columns=("Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"), show="headings", height=10
    )
    tree_products.pack(side=LEFT, fill=BOTH, expand=True)

    # Scrollbar for Treeview (Products)
    scrollbar_products = Scrollbar(frame_products, orient=VERTICAL, command=tree_products.yview)
    tree_products.config(yscrollcommand=scrollbar_products.set)
    scrollbar_products.pack(side=RIGHT, fill=Y)

    # Define Treeview columns (Products)
    product_columns = ["Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"]
    for col in product_columns:
        tree_products.heading(col, text=col)
        tree_products.column(col, width=100, anchor="center")

    # Populate Treeview with products
    for product in products:
        tree_products.insert("", "end", values=product)

    # Section for input: Quantity
    Label(buy_window, text="Enter Quantity:", font=("Arial", 12)).pack(pady=5)
    quantity_entry = Entry(buy_window, font=("Arial", 12))
    quantity_entry.pack(pady=5)

    # Section for displaying orders
    Label(buy_window, text="Existing Orders", font=("Arial", 12, "bold")).pack(pady=10)
    frame_orders = Frame(buy_window)
    frame_orders.pack(pady=10)

    # Treeview for orders
    tree_orders = ttk.Treeview(
        frame_orders, columns=("Order ID", "Supplier ID", "Supplier Name", "Product ID", "Product Name", "Quantity", "Order Time"), show="headings", height=10
    )
    tree_orders.pack(side=LEFT, fill=BOTH, expand=True)

    # Scrollbar for Treeview (Orders)
    scrollbar_orders = Scrollbar(frame_orders, orient=VERTICAL, command=tree_orders.yview)
    tree_orders.config(yscrollcommand=scrollbar_orders.set)
    scrollbar_orders.pack(side=RIGHT, fill=Y)

    # Define Treeview columns (Orders)
    order_columns = ["Order ID", "Supplier Name", "Supplier ID", "Product ID", "Product Name", "Quantity", "Order Time"]
    for col in order_columns:
        tree_orders.heading(col, text=col)
        tree_orders.column(col, width=100, anchor="center")

    # Load existing orders
    def load_orders():
        try:
            with open("supplier_order.txt", "r") as file:
                orders = [line.strip().split(",") for line in file.readlines()]
                tree_orders.delete(*tree_orders.get_children())  # Clear existing data
                for order in orders:
                    tree_orders.insert("", "end", values=order)
        except FileNotFoundError:
             # If file doesn't exist, create an empty file
            with open("supplier_order.txt", "w") as file:
                pass  # Simply create the file without writing anything

    load_orders()

    # Function to handle product selection
    selected_product = {}

    def handle_product_selection(event):
        selected_item = tree_products.selection()
        if not selected_item:
            return

        product_values = tree_products.item(selected_item, "values")
        selected_product["product_id"] = product_values[0]
        selected_product["product_name"] = product_values[1]

        # Automatically set the supplier name
        supplier_name = product_values[3]
        selected_product["supplier_name"] = supplier_name

    # Bind selection event
    tree_products.bind("<<TreeviewSelect>>", handle_product_selection)

    # Function to save the order
    def save_order():
        if not selected_product:
            show_error(title="No Selection", message="Please select a product to buy stock for.", severity="error")
            return

        quantity = quantity_entry.get()

        # Validate inputs
        if not quantity.isdigit() or int(quantity) <= 0:
            show_error(title="Invalid Quantity", message="Quantity must be a positive integer.", severity="error")
            return

        # Generate Order ID
        order_id = generate_order_id()

        # Get current date and time
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Automatically retrieve supplier ID based on name
        supplier_id = ""
        supplier_name = selected_product.get("supplier_name", "")
        for supplier in suppliers:
            if supplier[1] == supplier_name:
                supplier_id = supplier[0]
                break

        # Save the order to a file
        try:
            with open("supplier_order.txt", "a") as file:
                file.write(
                    f"{order_id},{supplier_id if supplier_id else 'UNKNOWN'},{supplier_name},"
                    f"{selected_product['product_id']},{selected_product['product_name']},{quantity},{order_time}\n"
                )

            # Reset fields
            tree_products.selection_remove(*tree_products.selection())
            quantity_entry.delete(0, END)

            # Reload orders
            load_orders()

            show_error(title="Success!", message="Order placed successfully!", severity="info")

        except Exception as e:
            show_error(title="Error", message=f"An error occurred: {e}", severity="error")

    # Function to edit an order
    def edit_order():
        selected_item = tree_orders.selection()
        if not selected_item:
            show_error(title="No Selection", message="Please select an order to edit.", severity="error")
            return

        # Get selected order details
        order_values = tree_orders.item(selected_item, "values")

        # Allow editing quantity
        new_quantity = simpledialog.askstring("Edit Order", f"Edit quantity for Order ID {order_values[0]}:", initialvalue=order_values[5])
        if not new_quantity or not new_quantity.isdigit() or int(new_quantity) <= 0:
            show_error(title="Invalid Quantity", message="Quantity must be a positive integer.", severity="error")
            return

        # Update the order
        try:
            with open("supplier_order.txt", "r") as file:
                orders = [line.strip().split(",") for line in file.readlines()]

            with open("supplier_order.txt", "w") as file:
                for order in orders:
                    if order[0] == order_values[0]:  # Match by Order ID
                        order[5] = new_quantity
                    file.write(",".join(order) + "\n")

            load_orders()
            show_error(title="Success!", message="Order updated successfully!", severity="info")
        except Exception as e:
            show_error(title="Error", message=f"An error occurred: {e}", severity="error")

    # Function to delete an order
    def delete_order():
        selected_item = tree_orders.selection()
        if not selected_item:
            show_error(title="No Selection", message="Please select an order to delete.", severity="error")
            return

        # Get selected order details
        order_values = tree_orders.item(selected_item, "values")

        # Confirm deletion
        confirm = messagebox.askyesno("Delete Order", f"Are you sure you want to delete Order ID {order_values[0]}?")
        if not confirm:
            return

        # Delete the order
        try:
            with open("supplier_order.txt", "r") as file:
                orders = [line.strip().split(",") for line in file.readlines()]

            with open("supplier_order.txt", "w") as file:
                for order in orders:
                    if order[0] != order_values[0]:  # Skip the order to delete
                        file.write(",".join(order) + "\n")

            load_orders()
            show_error(title="Success!", message="Order deleted successfully!", severity="info")
        except Exception as e:
            show_error(title="Error", message=f"An error occurred: {e}", severity="error")

    # Create a frame for buttons
    button_frame = Frame(buy_window)
    button_frame.pack(pady=10, anchor="center")

    # Button to save the order
    Button(button_frame, text="Place Order", font=("Arial", 12), command=save_order).pack(side=LEFT, padx=10)
    
    # Button to edit an order
    Button(button_frame, text="Edit Order", font=("Arial", 12), command=edit_order).pack(side=LEFT, padx=10)
   
    # Button to delete an order
    Button(button_frame, text="Delete Order", font=("Arial", 12), command=delete_order).pack(side=LEFT, padx=10)
    
    # Button to exit to menu
    def exit_to_menu():
        buy_window.destroy()

    Button(button_frame, text="Exit to Menu", font=("Arial", 12), command=exit_to_menu).pack(side=LEFT, padx=10)

# Function to handle "View inventory" button click
def view_inventory():
    inventory_window = Toplevel(menu)
    inventory_window.title("View Inventory")
    inventory_window.geometry("900x400")  # Adjusted the size to fit new column

    # Create a frame for the Treeview and scrollbar
    frame = Frame(inventory_window)
    frame.pack(pady=20)

    # Add a scrollbar
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Create a Treeview to display inventory as a table with an additional Supplier column
    tree = ttk.Treeview(frame, columns=("Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"), 
                        show="headings", height=10)
    tree.pack()

    # Define columns and headings
    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Description", text="Description")
    tree.heading("Supplier", text="Supplier")
    tree.heading("Price", text="Price")
    tree.heading("Quantity", text="Quantity")

    # Set column widths
    tree.column("Product ID", width=100, anchor="center")
    tree.column("Product Name", width=200, anchor="center")
    tree.column("Description", width=250, anchor="center")
    tree.column("Supplier", width=150, anchor="center")
    tree.column("Price", width=100, anchor="center")
    tree.column("Quantity", width=100, anchor="center")

    # Load inventory data from file
    try:
        with open("product.txt", "r") as file:
            inventory_items = file.readlines()

        # Parse and sort inventory items by Product ID
        sorted_items = sorted(
            (line.strip().split(",") for line in inventory_items),  # Parse each line
            key=lambda item: int(item[0])  # Sort by Product ID (assuming it's the first column and numeric)
        )

        # Populate the Treeview with sorted product data
        for item in sorted_items:
            tree.insert("", "end", values=item)

    except FileNotFoundError:
        show_error(title="File Not Found", message="The inventory file was not found.", severity="error")
        return
    except ValueError:
        show_error(title="Data Error", message="Invalid Product ID format in the inventory file.", severity="error")
        return

    # Configure the scrollbar
    scrollbar.config(command=tree.yview)
    tree.config(yscrollcommand=scrollbar.set)

    # Add an Exit button to the inventory window
    def exit_inventory_window():
        inventory_window.destroy()

    exit_button = Button(inventory_window, text="Exit", font=("Arial", 12), command=exit_inventory_window)
    exit_button.pack(pady=10)

# Function to handle "Generate Report" button click
def generate_report():
    # Create a new window for the report
    report_window = Toplevel(menu)
    report_window.title("Sales, Low Stock, and Supplier Orders Report")
    report_window.geometry("1650x650")  # You can remove this line if you want automatic resizing

    # Configure grid to allow resizing
    report_window.grid_rowconfigure(0, weight=0)  # Header row (titles like "Sales Report")
    report_window.grid_rowconfigure(1, weight=1)  # Sales frame (expands with content)
    report_window.grid_rowconfigure(2, weight=0)  # Total sales profit label row
    report_window.grid_rowconfigure(3, weight=1)  # Low stock frame (expands with content)
    report_window.grid_rowconfigure(4, weight=1)  # Supplier orders frame (expands with content)
    report_window.grid_columnconfigure(0, weight=1)  # Allow first column to expand
    report_window.grid_columnconfigure(1, weight=1)  # Allow second column to expand

    # Section for Sales Report
    Label(report_window, text="Sales Report", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10)

    sales_frame = Frame(report_window)
    sales_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Ensure it expands

    sales_tree = ttk.Treeview(sales_frame, columns=("Date/Time", "Order ID", "Product ID", "Product Name", "Quantity", "Total Price"), show="headings", height=10)
    sales_tree.pack(side=LEFT, fill=BOTH, expand=True)

    sales_scrollbar = Scrollbar(sales_frame, orient=VERTICAL, command=sales_tree.yview)
    sales_tree.config(yscrollcommand=sales_scrollbar.set)
    sales_scrollbar.pack(side=RIGHT, fill=Y)

    # Define Sales Treeview columns
    sales_columns = ["Date/Time", "Order ID", "Product ID", "Product Name", "Quantity", "Total Price"]
    for col in sales_columns:
        sales_tree.heading(col, text=col)
        sales_tree.column(col, width=120, anchor="center")

    # Total Sales Profit
    total_sales_profit_label = Label(report_window, text="Total Sales Profit: $0.00", font=("Arial", 12, "bold"), fg="green")
    total_sales_profit_label.grid(row=2, column=0, padx=10, pady=5)

    # Load sales data into the Sales Treeview and calculate total sales profit
    def load_sales():
        total_profit = 0.0
        try:
            with open("order.txt", "r") as file:
                sales = [line.strip().split(",") for line in file.readlines()]
                sales_tree.delete(*sales_tree.get_children())
                for sale in sales:
                    total_profit += float(sale[5])  # Add the total price of each order
                    sales_tree.insert("", "end", values=sale)
            total_sales_profit_label.config(text=f"Total Sales Profit: ${total_profit:.2f}")
        except FileNotFoundError:
            show_error(title="File Not Found", message="The order file was not found.", severity="error")

    load_sales()

    # Section for Low Stock Report
    Label(report_window, text="Low Stock Products (Threshold: 10)", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=10)

    low_stock_frame = Frame(report_window)
    low_stock_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")  # Ensure it expands

    low_stock_tree = ttk.Treeview(low_stock_frame, columns=("Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"), show="headings", height=10)
    low_stock_tree.pack(side=LEFT, fill=BOTH, expand=True)

    low_stock_scrollbar = Scrollbar(low_stock_frame, orient=VERTICAL, command=low_stock_tree.yview)
    low_stock_tree.config(yscrollcommand=low_stock_scrollbar.set)
    low_stock_scrollbar.pack(side=RIGHT, fill=Y)

    # Define Low Stock Treeview columns
    low_stock_columns = ["Product ID", "Product Name", "Description", "Supplier", "Price", "Quantity"]
    for col in low_stock_columns:
        low_stock_tree.heading(col, text=col)
        low_stock_tree.column(col, width=120, anchor="center")

    # Load low stock data into the Low Stock Treeview
    def load_low_stock():
        try:
            with open("product.txt", "r") as file:
                products = [line.strip().split(",") for line in file.readlines()]
                low_stock_tree.delete(*low_stock_tree.get_children())
                for product in products:
                    if int(product[5]) <= 10:  # Check if quantity is below the threshold
                        low_stock_tree.insert("", "end", values=product)
        except FileNotFoundError:
            show_error(title="File Not Found", message="The product file was not found.", severity="error")

    load_low_stock()

    # Section for Supplier Orders Report
    Label(report_window, text="Supplier Orders Report", font=("Arial", 14, "bold")).grid(row=2, column=1, padx=10, pady=10)

    supplier_frame = Frame(report_window)
    supplier_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")  # Align to the left (west)

    supplier_tree = ttk.Treeview(
        supplier_frame,
        columns=("Order ID", "Supplier ID", "Supplier Name", "Product ID", "Product Name", "Quantity", "Order Date"),
        show="headings",
        height=10
    )
    supplier_tree.pack(side=LEFT, fill=BOTH, expand=True)

    supplier_scrollbar = Scrollbar(supplier_frame, orient=VERTICAL, command=supplier_tree.yview)
    supplier_tree.config(yscrollcommand=supplier_scrollbar.set)
    supplier_scrollbar.pack(side=RIGHT, fill=Y)

    # Define Supplier Orders Treeview columns
    supplier_columns = ["Order ID", "Supplier ID", "Supplier Name", "Product ID", "Product Name", "Quantity", "Order Date"]
    for col in supplier_columns:
        supplier_tree.heading(col, text=col)
        supplier_tree.column(col, width=120, anchor="center")

    # Load supplier orders data into the Supplier Orders Treeview
    def load_supplier_orders():
        try:
            with open("supplier_order.txt", "r") as file:
                orders = [line.strip().split(",") for line in file.readlines()]
                supplier_tree.delete(*supplier_tree.get_children())
                for order in orders:
                    supplier_tree.insert("", "end", values=order)
        except FileNotFoundError:
            show_error(title="File Not Found", message="The supplier orders file was not found.", severity="error")

    load_supplier_orders()

    # Exit button
    exit_button = Button(report_window, text="Exit", command=report_window.destroy, font=("Arial", 12))
    exit_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

    report_window.mainloop()

# Function to handle exit button click
def exit_application():
    menu.destroy()  # Close the application window
    exit()

# Button texts and corresponding commands
button_texts_and_commands = [
    ("Add a new product", add_new_product),
    ("Update product details", update_product_details),
    ("Add/ manage supplier", add_new_supplier),
    ("Place a customer's order", place_an_order),
    ("Buy stock from supplier", buy_stock_from_supplier),
    ("View inventory", view_inventory),
    ("Generate report", generate_report),
    ("Exit", exit_application)
]

# Create and pack buttons
for text, command in button_texts_and_commands:
    button = Button(menu, text=text, font=("Arial", 12), command=command)  # Changed Tk.Button to Button
    button.pack(pady=5, fill=X, padx=20)  # Add some space around the button and make it stretch horizontally

# Run the application
menu.mainloop()