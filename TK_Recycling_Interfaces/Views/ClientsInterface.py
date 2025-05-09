
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk 
import os
import re

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from TK_Recycling_Database.crud_operations import (
    Insert_Data_Client,
    Read_All_Clients,
    Update_Client,
    Delete_Client
)

class ClientInterface(ctk.CTkFrame):
    def __init__(self, master, user_name="" ,**kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=935, height=650, fg_color="#ffffff", corner_radius=10)
        self.current_client_id = None
        
        # Main container (same structure as TeamInterface)
        page_view_container = ctk.CTkFrame(
            master=self,
            width=950,  
            height=650,
            corner_radius=0,
            fg_color="#fefeff"
        )
        page_view_container.place(x=0, y=0)  

        # Content container
        self.content_container = ctk.CTkFrame(
            master=page_view_container,
            width=950 - 6,  
            height=650 - 30,  
            corner_radius=0,
            fg_color="#fefeff"
        )
        self.content_container.place(x=3, y=15)  

        # Header section (aligned with TeamInterface)
        section_1 = ctk.CTkFrame(
            master=self.content_container,
            width=938,  
            height=150,
            corner_radius=0,
            fg_color="#fefeff",   
        )
        section_1.place(x=3, y=0)  

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
            text=" 🫱🏼‍🫲🏽 GÉRER LES CLIENTS ",
            font=("Nunito ExtraBold", 19, "bold"),
            fg_color="#fefeff",
            text_color="#2d2d30",  
        )
        welcome_msg_3.place(x=2, y=100)

        # Add client button (same style as TeamInterface)
        add_button = ctk.CTkButton(
            master=self.content_container,
            text="Ajouter Client",
            font=("Nunito", 16, "bold"),
            text_color="white",
            fg_color="#b6d48e",
            hover_color="#fff",
            corner_radius=6,
            width=140,
            height=35,
            border_width=1,  
            border_color="#b6d48e",
            command=self.add_client
        )
        add_button.place(x=770, y=100)
        # Create the button that triggers the `add_member` function
        # Button: Ajouter Membre
        def on_enter(event):
            add_button.configure(text_color="#b6d48e" , fg_color="#fff")  
            add_button.configure(cursor="hand2") 

        def on_leave(event):
            add_button.configure(text_color="white" , fg_color="#b6d48e")
            add_button.configure(cursor="")

        add_button.bind("<Enter>", on_enter)
        add_button.bind("<Leave>", on_leave)
        # Load existing clients
        self.load_existing_clients()

    def create_client_card(self, parent, client_data):
        card = ctk.CTkFrame(
            master=parent,
            width=280,  # Same width as TeamInterface cards
            height=217, # Same height as TeamInterface cards
            corner_radius=15,
            fg_color="white",
            border_width=1,
            border_color="#ebe9e9"
        )

        # Badge (same style as TeamInterface)
        badge_frame = ctk.CTkFrame(
            master=card,
            fg_color="#e6f0d9",  
            border_width=1,      
            border_color="#e6f0d9",  
            corner_radius=4,     
            width=60,            
            height=23            
        )
        badge_frame.place(x=10, y=12)

        badge = ctk.CTkLabel(
            master=badge_frame,
            text=client_data['company'],
            font=("Nunito", 11, "bold"),
            text_color="#228e22",  
            fg_color="transparent",
            width=55,   
            height=15,  
            anchor="center"  
        )
        badge.place(relx=0.5, rely=0.45, anchor="center")

        # Profile image (same as TeamInterface)
        profile_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Assets", "Profile_avatar1.png"))
        profile_image = Image.open(profile_image_path)  
        profile_image = profile_image.resize((50, 47)) 
        profile_image_tk = ImageTk.PhotoImage(profile_image)  

        profile_icon = ctk.CTkLabel(
            master=card,
            image=profile_image_tk,
            text=""  
        )
        profile_icon.place(x=9, y=65, anchor="w") 
        profile_icon.image = profile_image_tk

        # Client details (aligned with TeamInterface layout)
        name_label = ctk.CTkLabel(
            master=card,
            text=client_data['name'],
            font=("Nunito ExtraBold", 15, "bold"),
            text_color="#2d2d30"
        )
        name_label.place(x=63, y=43)

        id_label = ctk.CTkLabel(
            master=card,
            text=client_data['matricule'],
            font=("Nunito Medium", 13),
            text_color="#aeacac"
        )
        id_label.place(x=63, y=63)

        # Email (same style as TeamInterface)
        email_prefix_label = ctk.CTkLabel(
            master=card,
            text="📧 Email : ",
            font=("Nunito", 13, "bold"), 
            text_color="#aeacac"
        )
        email_prefix_label.place(x=15, y=95)

        email_value_label = ctk.CTkLabel(
            master=card,
            text=client_data['email'],
            font=("Nunito", 14),  
            text_color="#aeacac"
        )
        email_value_label.place(x=85, y=95)

        # Phone (same style as TeamInterface)
        phone_prefix_label = ctk.CTkLabel(
            master=card,
            text="📞 Telephone : ",
            font=("Nunito", 13, "bold"), 
            text_color="#aeacac"
        )
        phone_prefix_label.place(x=15, y=117)

        phone_value_label = ctk.CTkLabel(
            master=card,
            text=client_data['phone'],
            font=("Nunito", 14),  
            text_color="#aeacac"
        )
        phone_value_label.place(x=115, y=117)

        # Role (same style as TeamInterface)
        role_prefix_label = ctk.CTkLabel(
            master=card,
            text="⚙️ Rôle : ",
            font=("Nunito", 13, "bold"), 
            text_color="#aeacac"
        )
        role_prefix_label.place(x=15, y=140)

        role_value_label = ctk.CTkLabel(
            master=card,
            text=client_data['role'],
            font=("Nunito", 14),  
            text_color="#aeacac"
        )
        role_value_label.place(x=77, y=140)

        # Buttons (same style as TeamInterface)
        edit_button = ctk.CTkButton(
            master=card,
            text="Editer",
            fg_color="#a9d9fa",
            text_color="#199ff3",
            font=("Nunito Medium", 13),
            width=50,
            height=20,
            corner_radius=5,
            hover_color="#fff",
            border_width=1,  
            border_color="#a9d9fa",
            command=lambda: self.edit_client_popup(client_data)
        )
        edit_button.place(x=12, y=180)

        delete_button = ctk.CTkButton(
            master=card,
            text="Supprimer",
            fg_color="#ffceca",
            text_color="#ff3e2b",
            font=("Nunito Medium", 13),
            width=75,
            height=20,
            corner_radius=5,
            hover_color="#fff",
            border_width=1,  
            border_color="#ffceca",
            command=lambda: self.delete_client(client_data['id'])
        )
        delete_button.place(x=193, y=180)

        card.is_client_card = True
        return card

    def load_existing_clients(self):
        # Clear existing cards first
        for widget in self.content_container.winfo_children():
            if hasattr(widget, "is_client_card"):
                widget.destroy()

        clients = Read_All_Clients()
        if clients:
            START_X = 10
            START_Y = 160
            CARD_WIDTH = 280  # Same as TeamInterface
            CARD_HEIGHT = 217 # Same as TeamInterface
            CARD_SPACING_X = 20
            CARD_SPACING_Y = 20
            
            # Calculate the number of cards per row
            cards_per_row = max(1, (self.content_container.winfo_width() - START_X) // (CARD_WIDTH + CARD_SPACING_X))
            
            for i, client in enumerate(clients):
                row = i // cards_per_row
                col = i % cards_per_row
                
                x = START_X + col * (CARD_WIDTH + CARD_SPACING_X)
                y = START_Y + row * (CARD_HEIGHT + CARD_SPACING_Y)
                
                card = self.create_client_card(
                    parent=self.content_container,
                    client_data=client
                )
                card.place(x=x, y=y)

    def edit_client_popup(self, client_data):
        self.current_client_id = client_data['id']
        popup = ctk.CTkToplevel(self) 
        popup.title("✏️ Modifier Client")
        popup.transient(self)
        popup.grab_set()

        popup_width = 320
        popup_height = 500
        position_top = 240
        position_right = 900
        popup.geometry(f'{popup_width}x{popup_height}+{position_right}+{position_top}')

        # Name field
        name_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        name_frame.pack(padx=(10, 10), pady=(10, 7), anchor="w", fill="x")
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Nom",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=45,
            fg_color="#B6D48E",
            corner_radius=6
        )
        name_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        self.name_entry = ctk.CTkEntry(
            name_frame, 
            width=235 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        self.name_entry.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        self.name_entry.insert(0, client_data['name'])

        # Email field
        email_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        email_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        email_label = ctk.CTkLabel(
            email_frame,
            text="Email",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=50,
            fg_color="#B6D48E",
            corner_radius=6
        )
        email_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        self.email_entry = ctk.CTkEntry(
            email_frame, 
            width=230 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        self.email_entry.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        self.email_entry.insert(0, client_data['email'])

        # Role field
        role_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        role_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        role_label = ctk.CTkLabel(
            role_frame,
            text="Rôle",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=60,
            fg_color="#B6D48E",
            corner_radius=6
        )
        role_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        role_options = ["Employé", "Vente", "Ressource Humaine", "Administrateur"]
        self.role_menu = ctk.CTkOptionMenu(
            role_frame, 
            values=role_options,
            fg_color="#fff",  
            button_color="#B6D48E",  
            width=220,  
            height=28,
        )
        self.role_menu.set(client_data['role'])
        self.role_menu.configure(button_hover_color="white")
        self.role_menu.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # Country field
        country_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        country_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        country_label = ctk.CTkLabel(
            country_frame,
            text="Pays",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=60,
            fg_color="#B6D48E",
            corner_radius=6
        )
        country_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        country_options = ["Tunisie", "France", "USA", "Allemagne", "Canada"]
        self.country_menu = ctk.CTkOptionMenu(
            country_frame, 
            values=country_options,
            fg_color="#fff",  
            button_color="#B6D48E",  
            width=220,  
            height=28,
        )
        self.country_menu.set(client_data['pays'])
        self.country_menu.configure(button_hover_color="white")
        self.country_menu.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # ID field
        id_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        id_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        id_label = ctk.CTkLabel(
            id_frame,
            text="Matricule",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=75,
            fg_color="#B6D48E",
            corner_radius=6
        )
        id_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        self.id_entry = ctk.CTkEntry(
            id_frame, 
            width=205 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        self.id_entry.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        self.id_entry.insert(0, client_data['matricule'])

        # Phone field
        phone_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        phone_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        phone_label = ctk.CTkLabel(
            phone_frame,
            text="Téléphone",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=80,
            fg_color="#B6D48E",
            corner_radius=6
        )
        phone_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        self.phone_entry = ctk.CTkEntry(
            phone_frame, 
            width=200 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        self.phone_entry.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        self.phone_entry.insert(0, client_data['phone'])

        # Company field
        company_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        company_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        company_label = ctk.CTkLabel(
            company_frame,
            text="Entreprise",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=80,
            fg_color="#B6D48E",
            corner_radius=6
        )
        company_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        company_options = ["Ecoplast", "Medex", "Genoil", "Autre"]
        self.company_menu = ctk.CTkOptionMenu(
            company_frame, 
            values=company_options,
            fg_color="#fff",  
            button_color="#B6D48E",  
            width=200,  
            height=28,
        )
        self.company_menu.set(client_data['company'])
        self.company_menu.configure(button_hover_color="white")
        self.company_menu.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # Error label
        self.error_label = ctk.CTkLabel(
            popup, 
            text="", 
            text_color="red", 
            font=("Nunito", 10)
        )
        self.error_label.pack(pady=(10, 0))

        # Submit button
        submit_btn = ctk.CTkButton(
            popup, 
            text="Modifier", 
            fg_color="#a7c8f0",  
            hover_color="#a7c8f0",  
            text_color="white",  
            font=("Nunito ExtraBold", 15, "bold"),   
            border_width=1,  
            border_color="#a7c8f0",
            width=90, 
            height=36, 
            command=self.update_client
        )
        submit_btn.pack(pady=15, padx=(0, 10), anchor="e")

    def update_client(self):
        # Get input values
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        role = self.role_menu.get().strip()
        pays = self.country_menu.get().strip()
        user_id = self.id_entry.get().strip()
        phone = self.phone_entry.get().strip()
        company = self.company_menu.get().strip()

        # Validate inputs
        if not all([name, user_id, email, phone, role, pays, company]):
            self.error_label.configure(text="❌ Tous les champs sont obligatoires !")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.error_label.configure(text="❌ Adresse email invalide !")
            return

        if not phone.isdigit() or len(phone) != 8:
            self.error_label.configure(text="❌ Numéro de téléphone invalide !")
            return

        # Update the client
        Update_Client(
            client_id=self.current_client_id,
            name=name,
            email=email,
            role=role,
            pays=pays,
            matricule=user_id,
            phone=phone,
            company=company
        )

        # Refresh the interface
        self.load_existing_clients()
        
        # Close the popup
        self.name_entry.master.master.destroy()

    def delete_client(self, client_id):
        # Confirm deletion
        confirm = ctk.CTkToplevel(self)
        confirm.title("Confirmation")
        confirm.transient(self)
        confirm.grab_set()

        label = ctk.CTkLabel(
            confirm,
            text="Êtes-vous sûr de vouloir supprimer ce client?",
            font=("Nunito", 14)
        )
        label.pack(pady=20, padx=20)

        def confirm_delete():
            Delete_Client(client_id)
            self.load_existing_clients()
            confirm.destroy()

        yes_btn = ctk.CTkButton(
            confirm,
            text="Oui",
            command=confirm_delete,
            fg_color="#ff3e2b",
            hover_color="#ff6b5b"
        )
        yes_btn.pack(side="left", padx=10, pady=10)

        no_btn = ctk.CTkButton(
            confirm,
            text="Non",
            command=confirm.destroy,
            fg_color="#b6d48e"
        )
        no_btn.pack(side="right", padx=10, pady=10)

    def add_client(self):
        popup = ctk.CTkToplevel(self) 
        popup.title("👥 Ajouter un Client")
        popup.transient(self)
        popup.grab_set()

        popup_width = 320
        popup_height = 500
        position_top = 240
        position_right = 900
        popup.geometry(f'{popup_width}x{popup_height}+{position_right}+{position_top}')

        # Name field
        name_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        name_frame.pack(padx=(10, 10), pady=(10, 7), anchor="w", fill="x")
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Nom",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=45,
            fg_color="#B6D48E",
            corner_radius=6
        )
        name_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        name_entry = ctk.CTkEntry(
            name_frame, 
            width=235 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        name_entry.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # Email field
        email_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        email_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        email_label = ctk.CTkLabel(
            email_frame,
            text="Email",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=50,
            fg_color="#B6D48E",
            corner_radius=6
        )
        email_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        email_entry = ctk.CTkEntry(
            email_frame, 
            width=230 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        email_entry.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # Role field
        role_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        role_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        role_label = ctk.CTkLabel(
            role_frame,
            text="Rôle",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=60,
            fg_color="#B6D48E",
            corner_radius=6
        )
        role_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        role_options = ["Employé", "Vente", "Ressource Humaine", "Administrateur"]
        role_menu = ctk.CTkOptionMenu(
            role_frame, 
            values=role_options,
            fg_color="#fff",  
            button_color="#B6D48E",  
            width=220,  
            height=28,
        )
        role_menu.set("Employé")
        role_menu.configure(button_hover_color="white")
        role_menu.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # Country field
        country_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        country_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        country_label = ctk.CTkLabel(
            country_frame,
            text="Pays",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=60,
            fg_color="#B6D48E",
            corner_radius=6
        )
        country_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        country_options = ["Tunisie", "France", "USA", "Allemagne", "Canada"]
        country_menu = ctk.CTkOptionMenu(
            country_frame, 
            values=country_options,
            fg_color="#fff",  
            button_color="#B6D48E",  
            width=220,  
            height=28,
        )
        country_menu.set("Tunisie")
        country_menu.configure(button_hover_color="white")
        country_menu.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # ID field
        id_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        id_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        id_label = ctk.CTkLabel(
            id_frame,
            text="Matricule",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=75,
            fg_color="#B6D48E",
            corner_radius=6
        )
        id_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        id_entry = ctk.CTkEntry(
            id_frame, 
            width=205 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        id_entry.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # Phone field
        phone_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        phone_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        phone_label = ctk.CTkLabel(
            phone_frame,
            text="Téléphone",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=80,
            fg_color="#B6D48E",
            corner_radius=6
        )
        phone_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        phone_entry = ctk.CTkEntry(
            phone_frame, 
            width=200 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        phone_entry.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # Company field
        company_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        company_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        company_label = ctk.CTkLabel(
            company_frame,
            text="Entreprise",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=80,
            fg_color="#B6D48E",
            corner_radius=6
        )
        company_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        company_options = ["Ecoplast", "Medex", "Genoil", "Autre"]
        company_menu = ctk.CTkOptionMenu(
            company_frame, 
            values=company_options,
            fg_color="#fff",  
            button_color="#B6D48E",  
            width=200,  
            height=28,
        )
        company_menu.set("Ecoplast")
        company_menu.configure(button_hover_color="white")
        company_menu.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # Password field
        password_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        password_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        password_label = ctk.CTkLabel(
            password_frame,
            text="Mot de passe",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=100,
            fg_color="#B6D48E",
            corner_radius=6
        )
        password_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        password_entry = ctk.CTkEntry(
            password_frame, 
            width=180 , 
            height=28 ,
            border_width=0,  
            fg_color="#fff",
            show="*"
        )  
        password_entry.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # Confirm password field
        confirm_password_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        confirm_password_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        
        confirm_password_label = ctk.CTkLabel(
            confirm_password_frame,
            text="Confirmer MDP",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=110,
            fg_color="#B6D48E",
            corner_radius=6
        )
        confirm_password_label.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        
        confirm_password_entry = ctk.CTkEntry(
            confirm_password_frame, 
            width=170 , 
            height=28 ,
            border_width=0,  
            fg_color="#fff",
            show="*"
        )  
        confirm_password_entry.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

        # Error label
        error_label = ctk.CTkLabel(
            popup, 
            text="", 
            text_color="red", 
            font=("Nunito", 10)
        )
        error_label.pack(pady=(10, 0))

        def submit_client():
            # Get input values
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            role = role_menu.get().strip()
            pays = country_menu.get().strip()
            matricule = id_entry.get().strip()
            phone = phone_entry.get().strip()
            company = company_menu.get().strip()
            password = password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()

            # Validate inputs
            if not all([name, email, role, pays, matricule, phone, company, password, confirm_password]):
                error_label.configure(text="❌ Tous les champs sont obligatoires !")
                return

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                error_label.configure(text="❌ Adresse email invalide !")
                return

            if not phone.isdigit() or len(phone) != 8:
                error_label.configure(text="❌ Numéro de téléphone invalide !")
                return

            if password != confirm_password:
                error_label.configure(text="❌ Les mots de passe ne correspondent pas !")
                return

            # Clear the error label if everything is correct
            error_label.configure(text="")

            # Insert new client
            Insert_Data_Client(
                name=name,
                email=email,
                role=role,
                pays=pays,
                mission=role,  # Using role as mission for now
                matricule=matricule,
                phone=int(phone),
                company=company,
                password=password,
                confirmPasword=confirm_password
            )

            # Refresh the interface
            self.load_existing_clients()
            
            # Close the popup
            popup.destroy()

        submit_btn = ctk.CTkButton(
            popup, 
            text="Ajouter", 
            fg_color="#a7c8f0",  
            hover_color="#a7c8f0",  
            text_color="white",  
            font=("Nunito ExtraBold", 15, "bold"),   
            border_width=1,  
            border_color="#a7c8f0",
            width=90, 
            height=36, 
            command=submit_client
        )

        def on_enter(event):
            submit_btn.configure(text_color="#a7c8f0", fg_color="#fff")  
            submit_btn.configure(cursor="hand2") 
        
        def on_leave(event):
            submit_btn.configure(text_color="white", fg_color="#a7c8f0")
            submit_btn.configure(cursor="")
        
        submit_btn.bind("<Enter>", on_enter)
        submit_btn.bind("<Leave>", on_leave)
        submit_btn.pack(pady=15, padx=(0, 10), anchor="e")

    def refresh_interface(self):
        """Refresh the client interface by reloading all clients"""
        self.load_existing_clients()


