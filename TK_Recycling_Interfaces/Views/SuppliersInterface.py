import re
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from mysql.connector import Error
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from TK_Recycling_Database.crud_operations import (
    Insert_Data_Supplier,
    Read_All_Suppliers,
    Update_Supplier,
    Delete_Supplier
)
from TK_Recycling_Database.connexion_DB import (
    create_connection
)

class SuppliersInterface(ctk.CTkFrame):
    def __init__(self, master, user_name="" ,**kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=935, height=650, fg_color="#ffffff", corner_radius=10)
        self.suppliers_data = []  # To store supplier data from database
        self.current_supplier_id = self.get_max_supplier_id()  # Get the highest ID from database

        # PAGE VIEW CONTAINER
        page_view_container = ctk.CTkFrame(
            master=self,
            width=950,  
            height=650,
            corner_radius=0,
            fg_color="#fefeff"
        )
        page_view_container.place(x=0, y=0)  

        # CONTENT CONTAINER
        content_container = ctk.CTkFrame(
            master=page_view_container,
            width=950 - 6,  
            height=650 - 30,  
            corner_radius=0,
            fg_color="#fefeff"
        )
        content_container.place(x=3, y=15)  

        # SECTION 1 (Top Header)
        section_1 = ctk.CTkFrame(
            master=content_container,
            width=938,  
            height=150,
            corner_radius=0,
            fg_color="#fefeff",  
        )
        section_1.place(x=3, y=0)  

        # Welcome Labels
        welcome_msg_1 = ctk.CTkLabel(
            master=section_1,
            text=f"Bienvenue De Retour {user_name} !",
            font=("Nunito ExtraBold", 19, "bold"),
            fg_color="#fefeff",
            text_color="#2d2d30",  
        )
        welcome_msg_1.place(x=2, y=2)  

        welcome_msg_2 = ctk.CTkLabel(
            master=section_1,
            text="Qu aimeriez-vous faire aujourd'hui ?",
            font=("Nunito ExtraBold", 14, "bold"),
            fg_color="#fefeff",
            text_color="#aeacac",  
        )
        welcome_msg_2.place(x=2, y=25)  

        welcome_msg_3 = ctk.CTkLabel(
            master=section_1,
            text="🚚 GÉRER LES FOURNISSEURS",
            font=("Nunito ExtraBold", 18, "bold"),
            fg_color="#fefeff",
            text_color="#2d2d30",  
        )
        welcome_msg_3.place(x=2, y=100) 

        # Create table
        self.create_table(content_container)

        # Add Supplier Button
        def on_enter(event):
            add_button.configure(text_color="#b6d48e", fg_color="#fff")  
            add_button.configure(cursor="hand2") 

        def on_leave(event):
            add_button.configure(text_color="white", fg_color="#b6d48e")
            add_button.configure(cursor="")

        add_button = ctk.CTkButton(
            master=content_container,
            text="Ajouter Fournisseur",
            font=("Nunito", 16, "bold"),
            text_color="white",
            fg_color="#b6d48e",
            hover_color="#fff",
            corner_radius=6,
            width=160,
            height=35,
            border_width=1,  
            border_color="#b6d48e",
            command=self.add_supplier_dialog
        )

        add_button.bind("<Enter>", on_enter)
        add_button.bind("<Leave>", on_leave)
        add_button.place(x=740, y=100)

        # Load suppliers from database
        self.load_suppliers_from_db()

    def get_max_supplier_id(self):
        """Get the highest supplier ID from database"""
        connection = None
        cursor = None
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT MAX(id) FROM supplier")
                max_id = cursor.fetchone()[0]
                return max_id + 1 if max_id else 1  # Start from 1 if no suppliers exist
        except Error as e:
            print(f"Error getting max supplier ID: {e}")
            return 1
        finally:
            if connection and connection.is_connected():
                if cursor:
                    cursor.close()
                connection.close()

    def load_suppliers_from_db(self):
        """Load all suppliers from database and display them"""
        connection = None
        cursor = None
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT id, matricule, firstname, lastname, phone FROM supplier WHERE active = TRUE"
                cursor.execute(query)
                suppliers = cursor.fetchall()
                
                for supplier in suppliers:
                    self.add_supplier_to_table(
                        supplier_id=supplier['id'],
                        matricule=supplier['matricule'],
                        firstname=supplier['firstname'],
                        lastname=supplier['lastname'],
                        phone=supplier['phone']
                    )
        except Error as e:
            print(f"Error loading suppliers: {e}")
        finally:
            if connection and connection.is_connected():
                if cursor:
                    cursor.close()
                connection.close()

    def create_table(self, parent):
        """Create the suppliers table"""
        table_frame = ctk.CTkFrame(
            master=parent,
            width=920,
            height=400,
            fg_color="#F8FCF4",   
            corner_radius=15,          
            border_width=5,             
            border_color="#ebe9e9"            
        )
        table_frame.place(x=3, y=160)
        
        columns = ("ID", "Matricule", "Nom", "Prénom", "Téléphone", "Opération")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        # Apply table style
        style = ttk.Style()
        style.theme_use("default")  
        
        style.configure("Treeview.Heading", 
            font=("Nunito Medium", 11), 
            background="#f8fcf4", 
            foreground="black",
            padding=(4, 8), 
            borderwidth=1, 
            relief="ridge"
        )  

        style.configure("Treeview", 
            font=("Nunito Medium", 11), 
            background="#ffffff",  
            foreground="black",
            rowheight=40,  
            borderwidth=1,  
            relief="ridge"
        )

        style.configure("Treeview.Item", 
            borderwidth=1,
            relief="solid"
        )

        style.configure("Treeview", rowheight=30) 

        style.map("Treeview", 
            background=[("selected", "#b6d48e")],  
            foreground=[("selected", "black")]   
        )

        # Define columns
        self.tree.heading("ID", text="🆔 ID")
        self.tree.heading("Matricule", text="🔢 Matricule")
        self.tree.heading("Nom", text="👤 Nom")
        self.tree.heading("Prénom", text="👤 Prénom")
        self.tree.heading("Téléphone", text="📞 Téléphone")
        self.tree.heading("Opération", text="⚙️ Opération")

        # Column widths
        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Matricule", width=120, anchor='center')
        self.tree.column("Nom", width=150, anchor='center')
        self.tree.column("Prénom", width=150, anchor='center')
        self.tree.column("Téléphone", width=150, anchor='center')
        self.tree.column("Opération", width=200, anchor='center')

        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<Button-1>", self.on_tree_click)

    def add_supplier_to_table(self, supplier_id, matricule, firstname, lastname, phone):
        """Add a supplier to the table"""
        self.tree.insert("", "end", values=(
            supplier_id,
            matricule,
            lastname,
            firstname,
            phone,
            "[Modifier]  [Supprimer]"
        ))

    def add_supplier_dialog(self):
        """Show dialog to add new supplier"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ajouter Fournisseur")
        dialog.transient(self)
        dialog.grab_set()

        # Center the dialog
        dialog_width = 400
        dialog_height = 350
        position_top = int(self.winfo_y() + (self.winfo_height() / 2) - (dialog_height / 2))
        position_right = int(self.winfo_x() + (self.winfo_width() / 2) - (dialog_width / 2))
        dialog.geometry(f"{dialog_width}x{dialog_height}+{position_right}+{position_top}")

        # Form fields
        fields = [
            ("Matricule", "", False),
            ("Nom", "", False),
            ("Prénom", "", False),
            ("Téléphone", "", False)
        ]

        entries = {}
        for i, (label, placeholder, disabled) in enumerate(fields):
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(pady=5, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"{label}:").pack(side="left", padx=(0, 10))
            
            entry = ctk.CTkEntry(frame)
            entry.pack(side="right", expand=True, fill="x")
            
            if placeholder:
                entry.insert(0, placeholder)
            if disabled:
                entry.configure(state="disabled")
            
            entries[label.lower()] = entry

        # Error label
        error_label = ctk.CTkLabel(dialog, text="", text_color="red")
        error_label.pack(pady=5)

        # Submit button
        def submit():
            # Get values
            matricule = entries['matricule'].get()
            lastname = entries['nom'].get()
            firstname = entries['prénom'].get()
            phone = entries['téléphone'].get()

            # Validate
            if not all([matricule, lastname, firstname, phone]):
                error_label.configure(text="Tous les champs sont obligatoires!")
                return

            if not re.match(r"^[A-Za-zÀ-ÿ -]+$", lastname) or not re.match(r"^[A-Za-zÀ-ÿ -]+$", firstname):
                error_label.configure(text="Nom et prénom doivent contenir uniquement des lettres!")
                return

            if not re.match(r"^\d{8}$", phone):
                error_label.configure(text="Le téléphone doit contenir 8 chiffres!")
                return

            # Insert to database
            try:
                Insert_Data_Supplier(
                    firstname=firstname,
                    lastname=lastname,
                    matricule=matricule,
                    phone=phone,
                    active=True
                )

                # Add to table
                supplier_id = self.current_supplier_id
                self.current_supplier_id += 1
                self.add_supplier_to_table(
                    supplier_id=supplier_id,
                    matricule=matricule,
                    firstname=firstname,
                    lastname=lastname,
                    phone=phone
                )

                dialog.destroy()
            except Error as e:
                error_label.configure(text=f"Erreur base de données: {e}")

        submit_btn = ctk.CTkButton(
            dialog,
            text="Ajouter",
            command=submit
        )
        submit_btn.pack(pady=10)

    def on_tree_click(self, event):
        """Handle clicks on the table"""
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        col_index = int(column[1:]) - 1

        if not item:
            return

        values = self.tree.item(item, "values")
        supplier_id = values[0]

        if col_index < 5:  # If click in data columns
            self.edit_supplier(item, col_index, supplier_id)
        elif col_index == 5:  # Operation column
            x, y, width, height = self.tree.bbox(item, column)
            click_x = event.x
            
            if click_x < x + width / 2:
                self.edit_supplier_dialog(supplier_id)  # Modify
            else:
                self.delete_supplier(supplier_id, item)  # Delete

    def edit_supplier_dialog(self, supplier_id):
        """Show dialog to edit supplier"""
        # Get supplier data
        connection = None
        cursor = None
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM supplier WHERE id = %s", (supplier_id,))
                supplier = cursor.fetchone()
        except Error as e:
            print(f"Error getting supplier: {e}")
            return
        finally:
            if connection and connection.is_connected():
                if cursor:
                    cursor.close()
                connection.close()

        if not supplier:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Modifier Fournisseur")
        dialog.transient(self)
        dialog.grab_set()

        # Center the dialog
        dialog_width = 400
        dialog_height = 350
        position_top = int(self.winfo_y() + (self.winfo_height() / 2) - (dialog_height / 2))
        position_right = int(self.winfo_x() + (self.winfo_width() / 2) - (dialog_width / 2))
        dialog.geometry(f"{dialog_width}x{dialog_height}+{position_right}+{position_top}")

        # Form fields
        fields = [
            ("Matricule", supplier['matricule'], True),
            ("Nom", supplier['lastname'], False),
            ("Prénom", supplier['firstname'], False),
            ("Téléphone", supplier['phone'], False)
        ]

        entries = {}
        for i, (label, value, disabled) in enumerate(fields):
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(pady=5, padx=10, fill="x")

            ctk.CTkLabel(frame, text=f"{label}:").pack(side="left", padx=(0, 10))
            
            entry = ctk.CTkEntry(frame)
            entry.insert(0, value)
            entry.pack(side="right", expand=True, fill="x")
            
            if disabled:
                entry.configure(state="disabled")
            
            entries[label.lower()] = entry

        # Error label
        error_label = ctk.CTkLabel(dialog, text="", text_color="red")
        error_label.pack(pady=5)

        # Submit button
        def submit():
            # Get values
            matricule = entries['matricule'].get()
            lastname = entries['nom'].get()
            firstname = entries['prénom'].get()
            phone = entries['téléphone'].get()

            # Validate
            if not all([matricule, lastname, firstname, phone]):
                error_label.configure(text="Tous les champs sont obligatoires!")
                return

            if not re.match(r"^[A-Za-zÀ-ÿ -]+$", lastname) or not re.match(r"^[A-Za-zÀ-ÿ -]+$", firstname):
                error_label.configure(text="Nom et prénom doivent contenir uniquement des lettres!")
                return

            if not re.match(r"^\d{8}$", phone):
                error_label.configure(text="Le téléphone doit contenir 8 chiffres!")
                return

            # Update in database
            try:
                Update_Supplier(
                    supplier_id=supplier_id,
                    firstname=firstname,
                    lastname=lastname,
                    phone=phone
                )

                # Update in table
                for item in self.tree.get_children():
                    if self.tree.item(item, "values")[0] == str(supplier_id):
                        self.tree.item(item, values=(
                            supplier_id,
                            matricule,
                            lastname,
                            firstname,
                            phone,
                            "[Modifier]  [Supprimer]"
                        ))
                        break

                dialog.destroy()
            except Error as e:
                error_label.configure(text=f"Erreur base de données: {e}")

        submit_btn = ctk.CTkButton(
            dialog,
            text="Enregistrer",
            command=submit
        )
        submit_btn.pack(pady=10)

    def delete_supplier(self, supplier_id, item):
        """Delete a supplier from database and table"""
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce fournisseur?"):
            try:
                Delete_Supplier(supplier_id)
                self.tree.delete(item)
            except Error as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer le fournisseur: {e}")

    def edit_supplier(self, item, col_index, supplier_id):
        """Edit supplier data directly in the table"""
        if col_index < 1 or col_index > 4:
            return  # Only allow editing columns 1-4 (Matricule to Téléphone)

        values = list(self.tree.item(item, "values"))
        x, y, width, height = self.tree.bbox(item, f"#{col_index+1}")
        entry = ttk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, values[col_index])
        entry.focus()

        def save_edit(event=None):
            new_value = entry.get()
            
            # Validation based on column
            if col_index in [2, 3]:  # Nom and Prénom
                if not re.match(r"^[A-Za-zÀ-ÿ -]+$", new_value):
                    messagebox.showerror("Erreur", "Nom et prénom doivent contenir uniquement des lettres.")
                    entry.focus()
                    return
            elif col_index == 4:  # Téléphone
                if not re.match(r"^\d{8}$", new_value):
                    messagebox.showerror("Erreur", "Le téléphone doit contenir 8 chiffres.")
                    entry.focus()
                    return

            values[col_index] = new_value
            self.tree.item(item, values=values)
            entry.destroy()

            # Update database
            try:
                if col_index == 1:  # Matricule
                    Update_Supplier(supplier_id, matricule=new_value)
                elif col_index == 2:  # Nom (lastname)
                    Update_Supplier(supplier_id, lastname=new_value)
                elif col_index == 3:  # Prénom (firstname)
                    Update_Supplier(supplier_id, firstname=new_value)
                elif col_index == 4:  # Téléphone
                    Update_Supplier(supplier_id, phone=new_value)
            except Error as e:
                messagebox.showerror("Erreur", f"Impossible de mettre à jour: {e}")

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())