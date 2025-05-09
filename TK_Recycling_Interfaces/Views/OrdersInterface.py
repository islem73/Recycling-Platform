import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import os
import tkinter as tk
import re
from datetime import datetime
import sys
from pathlib import Path
from mysql.connector import Error

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from TK_Recycling_Database.crud_operations import (
    Insert_Data_Order,
    Read_All_Orders,
    Update_Order,
    Delete_Order
)

from TK_Recycling_Database.connexion_DB import (
    create_connection
)

class OrdersInterface(ctk.CTkFrame):
    def __init__(self, master, user_name="" ,**kwargs):
        super().__init__(master, **kwargs)
        self.commandes = []  
        self.current_order_id = self.get_max_order_id()  
        
        # Configure the frame
        self.configure(width=935, height=650, fg_color="#ffffff", corner_radius=10)

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
            width=944,  
            height=620,  
            corner_radius=0,
            fg_color="#fefeff"
        )
        content_container.place(x=3, y=15)  

        # SECTION 1 (Top Header)
        section_1 = ctk.CTkFrame(
            master=content_container,
            width=938,  
            height=50,
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

        # SECTION 2 (Below section 1)
        section_2_height = 620 - 90  # 620 content height - 150 section_1 height
        section_2 = ctk.CTkFrame(
            master=content_container,
            width=938,
            height=section_2_height,
            corner_radius=0,
            fg_color="#ffffff",
        )
        section_2.place(x=3, y=80)

        # Divide Section 2 Vertically: TOP and BOTTOM
        top_half = ctk.CTkFrame(
            master=section_2,
            width=938,
            height=50,
            corner_radius=0,
            fg_color="#ffffff",
        )
        top_half.place(x=0, y=2)

        # LEFT SIDE: welcome_msg_3
        welcome_msg_3 = ctk.CTkLabel(
            master=top_half,
            text="📦 GÉRER LES COMMANDES",
            font=("Nunito ExtraBold", 17, "bold"),
            fg_color="#ffffff",
            text_color="#2d2d30",  
        )
        welcome_msg_3.place(x=2, y=10)

        # Button Frame
        button_frame = ctk.CTkFrame(
            master=top_half,
            height=32,
            width=170,
            fg_color="transparent",
            corner_radius=0,
            border_width=0
        )
        button_frame.place(x=755, y=10)

        # Button
        passer_commande_btn = ctk.CTkButton(
            button_frame,
            text="🛒 Passer Commande",
            font=("Nunito", 14, "bold"),
            text_color="white",
            fg_color="#b6d48e",
            hover_color="#9bc06c",
            corner_radius=5,
            width=170,
            height=32,
            border_width=0,
            command=self.create_order_popup
        )
        passer_commande_btn.pack(fill="both", expand=True)

        bottom_half = ctk.CTkFrame(
            master=section_2,
            width=938,
            height=section_2_height - 50 -25,
            corner_radius=0,
            fg_color="#ffffff",
        )
        bottom_half.place(x=0, y=70)

        # SECTION BOTTOM_HALF DIVIDED INTO LEFT AND RIGHT
        right_width = 250
        spacing = 20
        bottom_half_width = 938  
        bottom_half_height = section_2_height - 50 - 25

        # Right Section
        right_section = ctk.CTkFrame(
            master=bottom_half,
            width=right_width,
            height=bottom_half_height,
            corner_radius=0,
            fg_color="#ffffff",
        )
        right_section.place(x=bottom_half_width - right_width, y=0)

        # Left Section with Scrollable Canvas
        left_section_width = bottom_half_width - right_width - spacing

        # Create a canvas and scrollbar
        self.canvas = ctk.CTkCanvas(
            master=bottom_half,
            width=left_section_width,
            height=bottom_half_height,
            bg="#ffffff",
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0)

        scrollbar = ctk.CTkScrollbar(
            master=bottom_half,
            orientation="vertical",
            command=self.canvas.yview,
            height=bottom_half_height,
            fg_color="transparent",  
            button_color="#f5f6f5",  
            button_hover_color="#f5f6f5" 
        )
        scrollbar.place(x=left_section_width, y=0)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame inside canvas
        self.scrollable_frame = ctk.CTkFrame(
            master=self.canvas,
            width=left_section_width,
            height=bottom_half_height,
            fg_color="#ffffff",
            corner_radius=0
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Load orders from database
        self.load_orders_from_db()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def get_max_order_id(self):
        """Get the highest order ID from database to continue numbering"""
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT MAX(id) FROM `order`")
                max_id = cursor.fetchone()[0]
                return max_id + 1 if max_id else 1  # Start from 1 if no orders exist
        except Error as e:
            print(f"Error getting max order ID: {e}")
            return 1  # Default starting point if error occurs
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def load_orders_from_db(self):
        """Load all orders from database and display them"""
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                query = """
                SELECT o.id, o.product, o.quantity, o.total, o.createdAtFormatted as date, 
                       c.name as client, c.company as entreprise
                FROM `order` o
                JOIN client c ON o.client_id = c.id
                ORDER BY o.id DESC
                """
                cursor.execute(query)
                orders = cursor.fetchall()
                
                for order in orders:
                    self.add_order_card(
                        order_id=str(order['id']),
                        date=order['date'],
                        client=order['client'],
                        entreprise=order['entreprise'],
                        produit=order['product'],
                        quantite=str(order['quantity']),
                        total=str(order['total'])
                    )
        except Error as e:
            print(f"Error loading orders: {e}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def add_order_card(self, order_id, date, client, entreprise, produit, quantite, total):
        """Add a new order card to the scrollable frame"""
        right_width = 250
        spacing = 20
        bottom_half_width = 938  
        section_2_height = 620 - 90 
        bottom_half_height = section_2_height - 50 - 25
        left_section_width = bottom_half_width - right_width - spacing
        
        card = ctk.CTkFrame(
            master=self.scrollable_frame,
            width=left_section_width - 20,
            height=115,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#f5f6f5"
        )
        card.pack(pady=10, padx=10, fill="x")

        # Store card reference in the commande dictionary
        card_data = {
            "frame": card,
            "id": order_id
        }
        self.commandes.append(card_data)

        # Wrapper Frame with background and rounded corners
        commande_id_wrapper = ctk.CTkFrame(card, fg_color="#f5f6f5", corner_radius=4, width=125, height=26)
        commande_id_wrapper.place(x=10, y=10)

        # Commande ID Label
        commande_id = ctk.CTkLabel(commande_id_wrapper, text=f"## Commande-{order_id}", text_color="#a1a1a1", font=("Nunito", 12, "bold"), fg_color="transparent")
        commande_id.place(x=10, y=-1)

        commande_date_wrapper = ctk.CTkFrame(card, fg_color="#f5f6f5", corner_radius=4, width=120, height=26)
        commande_date_wrapper.place(x=145, y=10)

        # Commande DATE Label
        commande_date = ctk.CTkLabel(commande_date_wrapper, text=f"Date : {date}", text_color="#a1a1a1", font=("Nunito", 12, "bold"), fg_color="transparent")
        commande_date.place(x=10, y=-1)

        supprimer_commande_wrapper = ctk.CTkFrame(
            card, 
            fg_color="#ffe3e0", 
            corner_radius=4, 
            width=65, 
            height=24
        )
        supprimer_commande_wrapper.place(x=575, y=10)
    
        # Make the label clickable
        supprimer_commande_label = ctk.CTkLabel(
            supprimer_commande_wrapper, 
            text="Supprimer", 
            text_color="#ff3e2b", 
            font=("Nunito", 10, "bold"), 
            fg_color="transparent",
            cursor="hand2"
        )
        supprimer_commande_label.place(x=6, y=-3)

        # Bind click event to delete the card
        supprimer_commande_label.bind("<Button-1>", lambda e, card=card, order_id=order_id: self.delete_card(card, order_id))
        supprimer_commande_wrapper.bind("<Button-1>", lambda e, card=card, order_id=order_id: self.delete_card(card, order_id))

        # Client and Entreprise (Middle Row)
        client_label = ctk.CTkLabel(card, text=f"👨🏻‍💼 Client : {client}", text_color="#2e2e2e", font=("Nunito", 13, "bold"))
        client_label.place(x=10, y=45)

        entreprise_label = ctk.CTkLabel(card, text=f"🏢  Entreprise : {entreprise}", text_color="#2e2e2e", font=("Nunito", 13, "bold"))
        entreprise_label.place(x=230, y=45)

        # Produit Wrapper
        produit_wrapper = ctk.CTkFrame(card, fg_color="#d9e9c5", corner_radius=4 , width=115, height=27)
        produit_wrapper.place(x=10, y=80)

        produit_label = ctk.CTkLabel(produit_wrapper, text=f"♻️ Produit : {produit}", font=("Nunito", 12, "bold"), text_color="#4e944f", fg_color="transparent")
        produit_label.place(x=10, y=-2)

        # Quantité Wrapper
        quantite_wrapper = ctk.CTkFrame(card, fg_color="#e8f5ff", corner_radius=4 ,width=140, height=27)
        quantite_wrapper.place(x=160, y=80)

        quantite_label = ctk.CTkLabel(quantite_wrapper, text=f"📦  Quantité : {quantite} Kg", font=("Nunito", 12, "bold"), text_color="#2571c3", fg_color="transparent")
        quantite_label.place(x=5, y=-2)

        # Total Wrapper
        total_wrapper = ctk.CTkFrame(card, fg_color="#ffe8cc", corner_radius=4 , width=125, height=27)
        total_wrapper.place(x=340, y=80)

        total_label = ctk.CTkLabel(total_wrapper, text=f"🧾 Total : {total} TND", font=("Nunito", 12, "bold"), text_color="#d36315", fg_color="transparent")
        total_label.place(x=5, y=-2)

    def delete_card(self, card, order_id):
        """Remove the card from the interface and database"""
        # Delete from database first
        try:
            Delete_Order(order_id)
            
            # Destroy the card widget
            card.destroy()
        
            # Remove from commands list
            self.commandes = [cmd for cmd in self.commandes if cmd["id"] != order_id]
        
            # Update the scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            print(f"Order {order_id} deleted successfully")
        except Error as e:
            print(f"Error deleting order: {e}")

    def create_order_popup(self):
        popup = ctk.CTkToplevel(self) 
        popup.title("Commande")
        popup.transient(self)

        # Center the popup window
        popup_width = 240
        popup_height = 355
        position_top = 260
        position_right = 980
        popup.geometry(f'{popup_width}x{popup_height}+{position_right}+{position_top}')

        # Client Frame
        client_frame = ctk.CTkFrame(
                    popup,
                    fg_color="#FFF",  
                    border_width=1, 
                    border_color="#B6D48E",  
                    corner_radius=7,  
                    height=34, 
                    width=200
        )
        client_frame.pack(padx=(10, 10), pady=(10, 7), anchor="w", fill="x")
        left_frame_client = ctk.CTkFrame(
                    client_frame,
                    fg_color="#B6D48E",  
                    corner_radius=6,  
                    height=30,
                    width=100  
        )
        left_frame_client.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        client_label = ctk.CTkLabel(
                    left_frame_client,
                    text="Client",  
                    font=("Nunito ExtraBold", 14, "bold"),
                    text_color="white",
                    anchor="w",
                    width=50
        )
        client_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_client = ctk.CTkFrame(
                    client_frame,
                    fg_color="#fff",  
                    corner_radius=7, 
                    height=30
        )
        right_frame_client.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        
        # Get clients from database for dropdown
        client_options = self.get_clients_from_db()
        self.client_menu = ctk.CTkOptionMenu(
                    right_frame_client, 
                    values=client_options['names'],
                    fg_color="#fff",  
                    button_color="#B6D48E",  
                    width=235,  
                    height=30,
        )
        self.client_menu.set("Sélectionner")  
        self.client_menu.pack(padx=0, pady=0, fill="y", expand=True)
        self.client_ids = client_options['ids']  # Store client IDs for reference

        # Produit Frame
        produit_frame = ctk.CTkFrame(
                    popup,
                    fg_color="#FFF",  
                    border_width=1, 
                    border_color="#B6D48E",  
                    corner_radius=7,  
                    height=34, 
                    width=200
        )
        produit_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        left_frame_produit = ctk.CTkFrame(
                    produit_frame,
                    fg_color="#B6D48E",  
                    corner_radius=6,  
                    height=30,
                    width=110  
        )
        left_frame_produit.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        produit_label = ctk.CTkLabel(
                    left_frame_produit,
                    text="Produit",  
                    font=("Nunito ExtraBold", 14, "bold"),
                    text_color="white",
                    anchor="w",
                    width=60
        )
        produit_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_produit = ctk.CTkFrame(
                    produit_frame,
                    fg_color="#fff",  
                    corner_radius=7, 
                    height=30
        )
        right_frame_produit.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        produit_options = ["ABS", "PP", "PEHD", "PET"]
        self.produit_menu = ctk.CTkOptionMenu(
                    right_frame_produit, 
                    values=produit_options,
                    fg_color="#fff",  
                    button_color="#B6D48E",  
                    width=230,  
                    height=30,
        )
        self.produit_menu.set("Sélectionner")  
        self.produit_menu.pack(padx=0, pady=0, fill="y", expand=True)

        # Quantité Frame
        quantite_frame = ctk.CTkFrame(
                    popup,
                    fg_color="#FFF",  
                    border_width=1, 
                    border_color="#B6D48E",  
                    corner_radius=7,  
                    height=34, 
                    width=190
        )
        quantite_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        left_frame_quantite = ctk.CTkFrame(
                    quantite_frame,
                    fg_color="#B6D48E",  
                    corner_radius=6,  
                    height=30,
                    width=100  
        )
        left_frame_quantite.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        quantite_label = ctk.CTkLabel(
                    left_frame_quantite,
                    text="Quantité",  
                    font=("Nunito ExtraBold", 14, "bold"),
                    text_color="white",
                    anchor="w",
                    width=75
        )
        quantite_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_quantite = ctk.CTkFrame(
                    quantite_frame,
                    fg_color="#fff",  
                    corner_radius=7, 
                    height=30
        )
        right_frame_quantite.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        self.input_field_quantite = ctk.CTkEntry(
                    right_frame_quantite, 
                    width=205, 
                    height=30,
                    border_width=0,  
                    fg_color="#fff"
        )  
        self.input_field_quantite.pack(padx=0, pady=0, fill="y", expand=True)

        # Entreprise Frame
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
                    width=105
        )
        left_frame_entreprise.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
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
        right_frame_entreprise.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        self.input_field_entreprise = ctk.CTkEntry(
                    right_frame_entreprise, 
                    width=200, 
                    height=30,
                    border_width=0,  
                    fg_color="#fff"
        )  
        self.input_field_entreprise.pack(padx=0, pady=0, fill="y", expand=True)

        # Prix Frame
        prix_frame = ctk.CTkFrame(
                    popup,
                    fg_color="#FFF",  
                    border_width=1, 
                    border_color="#B6D48E",  
                    corner_radius=7,  
                    height=34, 
                    width=200
        )
        prix_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        left_frame_prix = ctk.CTkFrame(
                    prix_frame,
                    fg_color="#B6D48E",  
                    corner_radius=6,  
                    height=30,
                    width=100
        )
        left_frame_prix.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        prix_label = ctk.CTkLabel(
                    left_frame_prix,
                    text="Prix Unitaire",  
                    font=("Nunito ExtraBold", 14, "bold"),
                    text_color="white",
                    anchor="w",
                    width=95
        )
        prix_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_prix = ctk.CTkFrame(
                    prix_frame,
                    fg_color="#fff",  
                    corner_radius=7, 
                    height=30
        )
        right_frame_prix.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        self.input_field_prix = ctk.CTkEntry(
                    right_frame_prix, 
                    width=200, 
                    height=30,
                    border_width=0,  
                    fg_color="#fff"
        )  
        self.input_field_prix.pack(padx=0, pady=0, fill="y", expand=True)

        # Date Frame
        date_frame = ctk.CTkFrame(
                    popup,
                    fg_color="#FFF",  
                    border_width=1, 
                    border_color="#B6D48E",  
                    corner_radius=7,  
                    height=34, 
                    width=200
        )
        date_frame.pack(padx=(10, 10), pady=(0, 7), anchor="w", fill="x")
        left_frame_date = ctk.CTkFrame(
                    date_frame,
                    fg_color="#B6D48E",  
                    corner_radius=6,  
                    height=30,
                    width=60  
        )
        left_frame_date.pack(side="left", padx=(2.5,0), pady=2.5, fill="y")
        date_label = ctk.CTkLabel(
                    left_frame_date,
                    text="Date",  
                    font=("Nunito ExtraBold", 14, "bold"),
                    text_color="white",
                    anchor="w",
                    width=50
        )
        date_label.pack(side="left", padx=(10, 0), pady=0, anchor="w", fill="y")
        right_frame_date = ctk.CTkFrame(
                    date_frame,
                    fg_color="#fff",  
                    corner_radius=7, 
                    height=30
        )
        right_frame_date.pack(side="left", padx=(0,2), pady=2, fill="y", expand=True)
        self.input_field_date = ctk.CTkEntry(
                    right_frame_date, 
                    width=220, 
                    height=30,
                    border_width=0,  
                    fg_color="#fff",
                    placeholder_text="JJ-MM-AAAA"
        )  
        self.input_field_date.pack(padx=0, pady=0, fill="y", expand=True)

        self.error_label = ctk.CTkLabel(
                    popup, 
                    text="", 
                    text_color="red", 
                    font=("Nunito", 10)
        )
        self.error_label.pack(pady=(10, 0))

        submit_btn = ctk.CTkButton(
                    popup, 
                    text="Confirmer", 
                    fg_color="#a7c8f0",  
                    hover_color="#a7c8f0",  
                    text_color="white",  
                    font=("Nunito ExtraBold", 15, "bold"),   
                    border_width=1,  
                    border_color="#a7c8f0",
                    width=90, 
                    height=36, 
                    command=lambda: self.submit_order(popup)
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

    def get_clients_from_db(self):
        """Get list of clients from database for dropdown"""
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name FROM client")
                clients = cursor.fetchall()
                return {
                    'ids': [client[0] for client in clients],
                    'names': [client[1] for client in clients]
                }
        except Error as e:
            print(f"Error getting clients: {e}")
            return {'ids': [], 'names': []}
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def validate_date(self, date_str):
        """Validate date format (DD-MM-YYYY)"""
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    def submit_order(self, popup):
        """Handle order submission"""
        # Get input values
        client_name = self.client_menu.get()
        client_index = self.client_menu._values.index(client_name) if client_name in self.client_menu._values else -1
        client_id = self.client_ids[client_index] if client_index >= 0 else None
        
        produit = self.produit_menu.get()
        quantite = self.input_field_quantite.get().strip()
        entreprise = self.input_field_entreprise.get().strip()
        prix = self.input_field_prix.get().strip()
        date = self.input_field_date.get().strip()

        # Validate inputs
        if not all([client_name, produit, quantite, prix, date, entreprise]):
            self.error_label.configure(text="❌ Tous les champs sont obligatoires !")
            return

        if client_name == "Sélectionner" or client_index == -1:
            self.error_label.configure(text="❌ Veuillez sélectionner un client !")
            return

        if produit == "Sélectionner":
            self.error_label.configure(text="❌ Veuillez sélectionner un produit !")
            return

        if not quantite.isdigit() or float(quantite) <= 0:
            self.error_label.configure(text="❌ Quantité invalide !")
            return

        if not prix.replace('.', '').isdigit() or float(prix) <= 0:
            self.error_label.configure(text="❌ Prix invalide !")
            return

        if not self.validate_date(date):
            self.error_label.configure(text="❌ Date invalide (JJ-MM-AAAA) !")
            return

        if not entreprise:
            self.error_label.configure(text="❌ Veuillez entrer une entreprise !")
            return

        # Clear the error label if everything is correct
        self.error_label.configure(text="")

        # Calculate total with 1 decimal place
        total = round(float(quantite) * float(prix), 1)
        
        # Generate order ID
        order_id = self.current_order_id
        self.current_order_id += 1

        # Insert into database
        try:
            Insert_Data_Order(
                client_id=client_id,
                product=produit,
                quantity=quantite,
                total=total,
                status="pending",  # Default status
                createdAtFormatted=date
            )
            
            # Add new card to the interface
            self.add_order_card(
                order_id=str(order_id),
                date=date,
                client=client_name,
                entreprise=entreprise,
                produit=produit,
                quantite=quantite,
                total=f"{total:.1f}"
            )

            # Close the popup
            popup.destroy()
            
        except Error as e:
            self.error_label.configure(text=f"❌ Erreur base de données: {e}")