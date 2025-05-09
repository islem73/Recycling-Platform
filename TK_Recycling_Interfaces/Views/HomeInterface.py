
import customtkinter as ctk
from PIL import Image, ImageTk
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from TK_Recycling_Database.crud_operations import (
    count_employees, 
    count_clients,
    count_suppliers,
    count_products,
    count_orders,
    count_services
)

class HomeInterface(ctk.CTkFrame):
    def __init__(self, master, user_name="" ,**kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=935, height=650, fg_color="#ffffff", corner_radius=10)

        self.employee_count = count_employees()
        self.client_count = count_clients()
        self.supplier_count = count_suppliers()
        self.product_count = count_products()
        self.order_count = count_orders()
        self.service_count = count_services()
        
        
        # Page view container
        page_view_container = ctk.CTkFrame(
            master=self,
            width=950,
            height=650,
            corner_radius=0,
            fg_color="#fefeff"
        )
        page_view_container.place(x=0, y=0)

        # Content container
        content_container = ctk.CTkFrame(
            master=page_view_container,
            width=944,
            height=620,
            corner_radius=0,
            fg_color="#fefeff"
        )
        content_container.place(x=3, y=15)

        # Section 1: Welcome
        section_1 = ctk.CTkFrame(
            master=content_container,
            width=938,
            height=55,
            corner_radius=0,
            fg_color="#fefeff"
        )
        section_1.place(x=3, y=0)

        welcome_msg_1 = ctk.CTkLabel(
            master=section_1,
            text=f"Bienvenue De Retour {user_name} !",
            font=("Nunito ExtraBold", 19, "bold"),
            fg_color="#fefeff",
            text_color="#2d2d30"
        )
        welcome_msg_1.place(x=2, y=2)

        welcome_msg_2 = ctk.CTkLabel(
            master=section_1,
            text="Qu'aimeriez-vous faire aujourd'hui ?",
            font=("Nunito ExtraBold", 14, "bold"),
            fg_color="#fefeff",
            text_color="#aeacac"
        )
        welcome_msg_2.place(x=2, y=25)

        # Section 2: Cards layout
        section_2 = ctk.CTkFrame(
            master=content_container,
            width=938,
            height=600,
            corner_radius=0,
            fg_color="#fefeff"
        )
        section_2.place(x=3, y=95)

        # Data for cards (icon, title, count)
        card_data = [
            ("👥", "Total Employés", self.employee_count),
            ("🧑‍💼", "Total Clients", self.client_count),
            ("📦", "Total Fournisseurs", self.supplier_count),
            ("🛒", "Total Produits", self.product_count),
            ("🧾", "Total Commandes", self.order_count),
            ("💼", "Total Services", self.service_count)
        ]

        def create_card(master, icon_text, title, count, x_pos, y_pos):
            card_width = 280
            card_height = 120
            card = ctk.CTkFrame(
                master=master,
                width=card_width,
                height=card_height,
                corner_radius=8,
                fg_color="white",
                border_width=1,
                border_color="#edf5e4"
            )
            card.place(x=x_pos, y=y_pos)

            # Grey square icon background
            icon_container = ctk.CTkFrame(
                master=card,
                width=40,
                height=40,
                corner_radius=8,
                fg_color="#f6f7f5"
            )
            icon_container.place(x=10, y=10)

            icon_label = ctk.CTkLabel(
                master=icon_container,
                text=icon_text,
                font=("Nunito", 24, "bold"),
                text_color="#4d4d4d"
            )
            icon_label.place(relx=0.5, rely=0.5, anchor="center")

            # Title
            title_label = ctk.CTkLabel(
                master=card,
                text=title,
                font=("Nunito Black", 15, "bold"),
                text_color="#2d2d30",
                anchor="w"
            )
            title_label.place(x=13, y=60)

            # Count
            count_label = ctk.CTkLabel(
                master=card,
                text=str(count),
                font=("Nunito", 20, "bold"),
                text_color="#1c1c1c"
            )
            count_label.place(x=13, y=86)

            # Voir Tous
            link_label = ctk.CTkLabel(
                master=card,
                text="Voir Tous →",
                font=("Nunito", 12, "bold"),
                text_color="#b0b0b0"
            )
            link_label.place(x=205, y=86)

        # Layout variables
        x_start = 0
        y_start = 0
        x_gap = 20
        y_gap = 20
        card_width = 280
        cards_per_row = 3

        for i, (icon, title, count) in enumerate(card_data):
            row = i // cards_per_row
            col = i % cards_per_row
            x_pos = x_start + col * (card_width + x_gap)
            y_pos = y_start + row * (120 + y_gap)
            create_card(section_2, icon, title, count, x_pos, y_pos)
