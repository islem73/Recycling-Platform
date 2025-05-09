import customtkinter as ctk
from PIL import Image, ImageTk
import os
import re

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from TK_Recycling_Database.crud_operations import (
    Insert_Data_User,
    Read_All_Users,
    Update_User,
    Delete_User
)

class TeamInterface(ctk.CTkFrame):
    def __init__(self, master, user_name="" ,**kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=935, height=650, fg_color="#ffffff", corner_radius=10)
        self.current_user_id = None
        
        # Main container
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

        # Header section
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
            text=" 👨‍👧‍👦 GÉRER L'ÉQUIPE",
            font=("Nunito ExtraBold", 19, "bold"),
            fg_color="#fefeff",
            text_color="#2d2d30",  
        )
        welcome_msg_3.place(x=2, y=100)

        # Add member button
        button_frame = ctk.CTkFrame(
            master=self.content_container,
            fg_color="#b6d48e",
            corner_radius=6,
            width=230
        )

        plus_label = ctk.CTkLabel(button_frame, text="➕", font=("Nunito", 12, "bold"), text_color="white")
        plus_label.pack(side="left", padx=(7, 3), pady=1.5)

        text_label = ctk.CTkLabel(button_frame, text="Ajouter Membre", font=("Nunito", 16, "bold"), text_color="white")
        text_label.pack(side="left", padx=(3, 12), pady=1.5)

        self.add_button = ctk.CTkButton(
            master=self.content_container,
            text="Ajouter Membre",
            font=("Nunito", 16, "bold"),
            text_color="white",
            fg_color="#b6d48e",
            hover_color="#fff",
            corner_radius=6,
            width=140,
            height=35,
            border_width=1,  
            border_color="#b6d48e",
            command=self.add_member
        )

        def on_enter(event):
            self.add_button.configure(text_color="#b6d48e", fg_color="#fff")  
            self.add_button.configure(cursor="hand2") 

        def on_leave(event):
            self.add_button.configure(text_color="white", fg_color="#b6d48e")
            self.add_button.configure(cursor="")

        self.add_button.bind("<Enter>", on_enter)
        self.add_button.bind("<Leave>", on_leave)
        self.add_button.place(x=770, y=100)

        # Load existing users
        self.load_existing_users()

    def create_member_card(self, parent, user_data):
        card = ctk.CTkFrame(
            master=parent,
            width=280,
            height=217,
            corner_radius=15,
            fg_color="white",
            border_width=1,
            border_color="#ebe9e9"
        )

        # Badge
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
            text="Ecoplast",
            font=("Nunito", 11, "bold"),
            text_color="#228e22",  
            fg_color="transparent",
            width=55,   
            height=15,  
            anchor="center"  
        )
        badge.place(relx=0.5, rely=0.45, anchor="center")

        # Profile image
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

        # User details
        name_label = ctk.CTkLabel(
            master=card,
            text=user_data['name'],
            font=("Nunito ExtraBold", 15, "bold"),
            text_color="#2d2d30"
        )
        name_label.place(x=63, y=43)

        id_label = ctk.CTkLabel(
            master=card,
            text=user_data['matricule'],
            font=("Nunito Medium", 13),
            text_color="#aeacac"
        )
        id_label.place(x=63, y=63)

        # Email
        email_prefix_label = ctk.CTkLabel(
            master=card,
            text="📧 Email : ",
            font=("Nunito", 13, "bold"), 
            text_color="#aeacac"
        )
        email_prefix_label.place(x=15, y=95)

        email_value_label = ctk.CTkLabel(
            master=card,
            text=user_data['email'],
            font=("Nunito", 14),  
            text_color="#aeacac"
        )
        email_value_label.place(x=85, y=95)

        # Phone
        phone_prefix_label = ctk.CTkLabel(
            master=card,
            text="📞 Telephone : ",
            font=("Nunito", 13, "bold"), 
            text_color="#aeacac"
        )
        phone_prefix_label.place(x=15, y=117)

        phone_value_label = ctk.CTkLabel(
            master=card,
            text=user_data['phone'],
            font=("Nunito", 14),  
            text_color="#aeacac"
        )
        phone_value_label.place(x=115, y=117)

        # Role
        role_prefix_label = ctk.CTkLabel(
            master=card,
            text="⚙️ Rôle : ",
            font=("Nunito", 13, "bold"), 
            text_color="#aeacac"
        )
        role_prefix_label.place(x=15, y=140)

        role_value_label = ctk.CTkLabel(
            master=card,
            text=user_data['role'],
            font=("Nunito", 14),  
            text_color="#aeacac"
        )
        role_value_label.place(x=77, y=140)  

        # Buttons
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
            command=lambda: self.edit_member_popup(user_data)
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
            command=lambda: self.delete_member(user_data['id'])
        )
        delete_button.place(x=193, y=180)

        card.is_member_card = True
        return card

    def load_existing_users(self):
        # Clear existing cards first
        for widget in self.content_container.winfo_children():
            if hasattr(widget, "is_member_card"):
                widget.destroy()

        users = Read_All_Users()
        if users:
            START_X = 10
            START_Y = 160
            CARD_WIDTH = 280
            CARD_HEIGHT = 217
            CARD_SPACING_X = 20
            CARD_SPACING_Y = 20
            
            # Calculate the number of cards per row
            cards_per_row = max(1, (self.content_container.winfo_width() - START_X) // (CARD_WIDTH + CARD_SPACING_X))
            
            for i, user in enumerate(users):
                row = i // cards_per_row
                col = i % cards_per_row
                
                x = START_X + col * (CARD_WIDTH + CARD_SPACING_X)
                y = START_Y + row * (CARD_HEIGHT + CARD_SPACING_Y)
                
                card = self.create_member_card(
                    parent=self.content_container,
                    user_data=user
                )
                card.place(x=x, y=y)

    def edit_member_popup(self, user_data):
        self.current_user_id = user_data['id']
        popup = ctk.CTkToplevel(self) 
        popup.title("✏️ Modifier Membre")
        popup.transient(self)
        popup.grab_set()

        popup_width = 320
        popup_height = 440
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
        self.name_entry.insert(0, user_data['name'])

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
        self.email_entry.insert(0, user_data['email'])

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
        self.id_entry.insert(0, user_data['matricule'])

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
        self.phone_entry.insert(0, user_data['phone'])

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
        self.role_menu.set(user_data['role'])
        self.role_menu.configure(button_hover_color="white")
        self.role_menu.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)

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
            command=self.update_member
        )
        submit_btn.pack(pady=15, padx=(0, 10), anchor="e")

    def update_member(self):
        # Get input values
        name = self.name_entry.get().strip()
        user_id = self.id_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        role = self.role_menu.get().strip()

        # Validate inputs
        if not all([name, user_id, email, phone, role]):
            self.error_label.configure(text="❌ Tous les champs sont obligatoires !")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.error_label.configure(text="❌ Adresse email invalide !")
            return

        if not phone.isdigit() or len(phone) != 8:
            self.error_label.configure(text="❌ Numéro de téléphone invalide !")
            return

        # Update the user
        Update_User(
            user_id=self.current_user_id,
            name=name,
            email=email,
            role=role,
            matricule=user_id,
            phone=phone
        )

        # Refresh the interface
        self.load_existing_users()
        
        # Close the popup
        self.name_entry.master.master.destroy()

    def delete_member(self, user_id):
        # Confirm deletion
        confirm = ctk.CTkToplevel(self)
        confirm.title("Confirmation")
        confirm.transient(self)
        confirm.grab_set()

        label = ctk.CTkLabel(
            confirm,
            text="Êtes-vous sûr de vouloir supprimer ce membre?",
            font=("Nunito", 14)
        )
        label.pack(pady=20, padx=20)

        def confirm_delete():
            Delete_User(user_id)
            self.load_existing_users()
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

    def add_member(self):
        popup = ctk.CTkToplevel(self) 
        popup.title("👥 Ajouter un Membre")
        popup.transient(self)
        popup.grab_set()

        # Center the popup window
        popup_width = 320
        popup_height = 440
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = 240
        position_right = 900
        popup.geometry(f'{popup_width}x{popup_height}+{position_right}+{position_top}')
        
        # Create the name_frame with border and other properties
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
        left_frame_name = ctk.CTkFrame(
            name_frame,
            fg_color="#B6D48E",  
            corner_radius=6,  
            height=30,
            width=100  
        )
        left_frame_name.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        name_label = ctk.CTkLabel(
            left_frame_name,
            text="Nom",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=45
        )
        name_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_name = ctk.CTkFrame(
            name_frame,
            fg_color="#fff",  
            corner_radius=7, 
            height=30
        )
        right_frame_name.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        input_field_name = ctk.CTkEntry(
            right_frame_name, 
            width=235 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        input_field_name.pack(padx=0, pady=0, fill="y", expand=True)

        # Create the email_frame with border and other properties
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
        left_frame_email = ctk.CTkFrame(
            email_frame,
            fg_color="#B6D48E",  
            corner_radius=6,  
            height=30,
            width=100  
        )
        left_frame_email.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        email_label = ctk.CTkLabel(
            left_frame_email,
            text="Email",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=50
        )
        email_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_email = ctk.CTkFrame(
            email_frame,
            fg_color="#fff",  
            corner_radius=7, 
            height=30
        )
        right_frame_email.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        input_field_email = ctk.CTkEntry(
            right_frame_email, 
            width=230 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        input_field_email.pack(padx=0, pady=0, fill="y", expand=True)

        # Create the ID_frame with border and other properties
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
        left_frame_id = ctk.CTkFrame(
            id_frame,
            fg_color="#B6D48E",  
            corner_radius=6,  
            height=30,
            width=100  
        )
        left_frame_id.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        id_label = ctk.CTkLabel(
            left_frame_id,
            text="Matricule",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=75
        )
        id_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_id = ctk.CTkFrame(
            id_frame,
            fg_color="#fff",  
            corner_radius=7, 
            height=30
        )
        right_frame_id.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        input_field_id = ctk.CTkEntry(
            right_frame_id, 
            width=205 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        input_field_id.pack(padx=0, pady=0, fill="y", expand=True)

        # Create the Phone_frame with border and other properties
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
        left_frame_phone = ctk.CTkFrame(
            phone_frame,
            fg_color="#B6D48E",  
            corner_radius=6,  
            height=30,
            width=100  
        )
        left_frame_phone.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        phone_label = ctk.CTkLabel(
            left_frame_phone,
            text="Téléphone",  
            font=("Nunito ExtraBold", 14, "bold"),
            text_color="white",
            anchor="w" ,
            width=80
        )
        phone_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_phone = ctk.CTkFrame(
            phone_frame,
            fg_color="#fff",  
            corner_radius=7, 
            height=30
        )
        right_frame_phone.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        input_field_phone = ctk.CTkEntry(
            right_frame_phone, 
            width=200 , 
            height=30 ,
            border_width=0,  
            fg_color="#fff"
        )  
        input_field_phone.pack(padx=0, pady=0, fill="y", expand=True)

        # Create the mission_frame with border and other properties
        mission_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        mission_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        left_frame_mission = ctk.CTkFrame(
            mission_frame,
            fg_color="#B6D48E",  
            corner_radius=6,  
            height=30,
            width=100  
        )
        left_frame_mission.pack(side="left", padx=(2.5, 0), pady=2.5, fill="y")
        mission_label = ctk.CTkLabel(
            left_frame_mission,
            text="Mission",  
            font=("Nunito ExtraBold", 14, "bold"),  
            text_color="white", 
            anchor="w", 
            width=60
        )
        mission_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_mission = ctk.CTkFrame(
            mission_frame,
            fg_color="#fff",  
            corner_radius=7,  
            height=30  
        )
        right_frame_mission.pack(side="left", padx=(0, 2), pady=2, fill="y", expand=True)
        mission_options = ["Employé", "Vente", "Ressource Humaine"]
        mission_menu = ctk.CTkOptionMenu(
            right_frame_mission, 
            values=mission_options,
            fg_color="#fff",  
            button_color="#B6D48E",  
            width=220,  
            height=28,
        )
        mission_menu.set("Employé")  
        mission_menu.configure(
            button_hover_color="white"  
        )
        mission_menu.pack(padx=2, pady=1, fill="y", expand=True)

        # Create the entreprise_frame with border and other properties
        entreprise_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        entreprise_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        left_frame_entreprise = ctk.CTkFrame(
            entreprise_frame,
            fg_color="#B6D48E",  
            corner_radius=6,  
            height=30,
            width=100  
        )
        left_frame_entreprise.pack(side="left", padx=(2.5, 0), pady=2.5, fill="y")
        entreprise_label = ctk.CTkLabel(
            left_frame_entreprise,
            text="Entreprise",  
            font=("Nunito ExtraBold", 14, "bold"),  
            text_color="white", 
            anchor="w", 
            width=80
        )
        entreprise_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_entreprise = ctk.CTkFrame(
            entreprise_frame,
            fg_color="#fff",  
            corner_radius=7,  
            height=30  
        )
        right_frame_entreprise.pack(side="left", padx=(0, 2), pady=2, fill="y", expand=True)
        entreprise_options = ["Ecoplast", "Medex", "Genoil"]
        entreprise_menu = ctk.CTkOptionMenu(
            right_frame_entreprise, 
            values=entreprise_options,
            fg_color="#fff",  
            button_color="#B6D48E",  
            width=200,  
            height=28,
        )
        entreprise_menu.set("Ecoplast")  
        entreprise_menu.configure(
            button_hover_color="white"  
        )
        entreprise_menu.pack(padx=2, pady=1, fill="y", expand=True)

        # Create the mot_de_passe_frame with border and other properties
        mot_de_passe_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        mot_de_passe_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        left_frame_mot_de_passe = ctk.CTkFrame(
            mot_de_passe_frame,
            fg_color="#B6D48E",  
            corner_radius=6,  
            height=30,
            width=100  
        )
        left_frame_mot_de_passe.pack(side="left", padx=(2.5, 0), pady=2.5, fill="y")
        mot_de_passe_label = ctk.CTkLabel(
            left_frame_mot_de_passe,
            text="Mot de Passe",  
            font=("Nunito ExtraBold", 14, "bold"),  
            text_color="white", 
            anchor="w", 
            width=100
        )
        mot_de_passe_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_mot_de_passe = ctk.CTkFrame(
            mot_de_passe_frame,
            fg_color="#fff",  
            corner_radius=7,  
            height=30  
        )
        right_frame_mot_de_passe.pack(side="left", padx=(0, 2), pady=2, fill="y", expand=True)
        mot_de_passe_input = ctk.CTkEntry(
            right_frame_mot_de_passe, 
            width=180,  
            height=28,  
            show="*",  
            border_width=0,  
            fg_color="#fff"
        )
        mot_de_passe_input.pack(padx=2, pady=1, fill="y", expand=True)

        # Create the confirmer_mot_de_passe_frame with border and other properties
        confirmer_mot_de_passe_frame = ctk.CTkFrame(
            popup,
            fg_color="#FFF",  
            border_width=1, 
            border_color="#B6D48E",  
            corner_radius=7,  
            height=34, 
            width=200
        )
        confirmer_mot_de_passe_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        left_frame_confirmer_mot_de_passe = ctk.CTkFrame(
            confirmer_mot_de_passe_frame,
            fg_color="#B6D48E",  
            corner_radius=6,  
            height=30,
        )
        left_frame_confirmer_mot_de_passe.pack(side="left", padx=(2.5, 0), pady=2.5, fill="y")
        confirmer_mot_de_passe_label = ctk.CTkLabel(
            left_frame_confirmer_mot_de_passe,
            text="Confirmer MDP",  
            font=("Nunito ExtraBold", 14, "bold"),  
            text_color="white", 
            anchor="w", 
            width=110
        )
        confirmer_mot_de_passe_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_confirmer_mot_de_passe = ctk.CTkFrame(
            confirmer_mot_de_passe_frame,
            fg_color="#fff",  
            corner_radius=7,  
            height=30  
        )
        right_frame_confirmer_mot_de_passe.pack(side="left", padx=(0, 2), pady=2, fill="y", expand=True)
        confirmer_mot_de_passe_input = ctk.CTkEntry(
            right_frame_confirmer_mot_de_passe, 
            width=170,  
            height=28,  
            show="*",  
            border_width=0,  
            fg_color="#fff"
        )
        confirmer_mot_de_passe_input.pack(padx=2, pady=1, fill="y", expand=True)

        error_label = ctk.CTkLabel(
            popup, 
            text="", 
            text_color="red", 
            font=("Nunito", 10)
        )
        error_label.pack(pady=(10, 0))

        def validate_email(email):
            return re.match(r"[^@]+@[^@]+\.[^@]+", email)

        def submit_member():
            name = input_field_name.get().strip()
            user_id = input_field_id.get().strip()
            email = input_field_email.get().strip()
            phone = input_field_phone.get().strip()
            mission = mission_menu.get().strip()
            password = mot_de_passe_input.get().strip()
            confirmPassword = confirmer_mot_de_passe_input.get().strip()

            if not all([name, user_id, email, phone, mission, password, confirmPassword]):
                error_label.configure(text="❌ Tous les champs sont obligatoires !")
                return

            if not validate_email(email):
                error_label.configure(text="❌ Adresse email invalide !")
                return

            if not phone.isdigit() or len(phone) != 8:
                error_label.configure(text="❌ Numéro de téléphone invalide !")
                return

            if password != confirmPassword:
                error_label.configure(text="❌ Les mots de passe ne correspondent pas !")
                return

            error_label.configure(text="")
            
            Insert_Data_User(
                name=name,
                email=email,
                role=mission,
                mission=mission,
                matricule=user_id,
                phone=int(phone), 
                password=password,
                confirmPassword=confirmPassword,
                company=""
            )
            
            self.load_existing_users()
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
            command=submit_member
        )

        def on_enter(event):
            submit_btn.configure(text_color="#a7c8f0" , fg_color="#fff")  
            submit_btn.configure(cursor="hand2") 
        def on_leave(event):
            submit_btn.configure(text_color="white" , fg_color="#a7c8f0")
            submit_btn.configure(cursor="")
        
        submit_btn.bind("<Enter>", on_enter)
        submit_btn.bind("<Leave>", on_leave)
        submit_btn.pack(pady=15, padx=(0, 10), anchor="e")  

    def refresh_interface(self):
        """Refresh the user interface by reloading all users"""
        self.load_existing_users()