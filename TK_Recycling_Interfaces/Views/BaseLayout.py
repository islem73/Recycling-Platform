import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys

from HomeInterface import HomeInterface
from TeamInterface import TeamInterface
from ClientsInterface import ClientInterface
from SuppliersInterface import SuppliersInterface
from OrdersInterface import OrdersInterface
from ProductsInterface import ProductInterface

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def base_layout(user_name):
    # Setting the paths for the logo and bottom images
    logo_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Assets", "mainLogo.png"))
    bottom_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Assets", "bottle.png"))

    # Initializing the main root window
    root = ctk.CTk()
    root.title("Accueil")
    root.geometry("1200x650")

    # Creating the main container for the app
    main_container = ctk.CTkFrame(master=root, width=1200, height=650, corner_radius=10, fg_color="#ffffff")
    main_container.place(x=0, y=0)

    # Sidebar Container
    sidebarContainer = ctk.CTkFrame(master=main_container, width=250, height=650, corner_radius=0, fg_color="#ffffff")
    sidebarContainer.place(x=0, y=0)

    # Sidebar Content Box
    sidebarContentBox = ctk.CTkFrame(
        master=sidebarContainer,
        width=220,
        height=620,
        corner_radius=12,
        fg_color="#f8fcf4",
        border_width=1,
        border_color="#f8fcf4"
    )
    sidebarContentBox.place(x=14, y=15)

    # CREATING THE TOP SECTION INSIDE THE SIDEBAR CONTENT BOX
    top_section = ctk.CTkFrame(
        master=sidebarContentBox,
        width=190,
        height=40,
        corner_radius=8,
        fg_color="transparent",
    )
    top_section.pack(pady=(10, 0), padx=15, fill="x")

    # CREATING THE FLEXIBLE ROW INSIDE THE TOP SECTION
    flex_row = ctk.CTkFrame(master=top_section, width=190, height=40, corner_radius=0, fg_color="transparent")
    flex_row.pack(fill="x", padx=0)

    # CREATING THE LOGO FRAME
    logo_frame = ctk.CTkFrame(
        master=flex_row,
        width=40,
        height=40,
        corner_radius=8,
        fg_color="white",
        border_width=1,
        border_color="#edf5e4"
    )
    logo_frame.pack(side="left", padx=0, pady=8)

    # LOADING AND DISPLAYING THE LOGO IMAGE
    try:
        logo_image = Image.open(logo_image_path)
        width, height = logo_image.size
        new_width = int(width * 0.11)
        new_height = int(height * 0.11)
        logo_image_resized = logo_image.resize((new_width, new_height), Image.LANCZOS)
        logo_image_tk = ImageTk.PhotoImage(logo_image_resized)
        logo_label = ctk.CTkLabel(master=logo_frame, image=logo_image_tk, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception as e:
        print("Error loading image:", e)
        logo_label = ctk.CTkLabel(master=logo_frame, text="Logo Not Found", text_color="black", font=("Nunito", 10))
        logo_label.place(relwidth=1, relheight=1)

    # CREATING THE TITLE FRAME INSIDE THE FLEXIBLE ROW
    title_frame = ctk.CTkFrame(
        master=flex_row,
        width=140,
        height=40,
        corner_radius=8,
        fg_color="transparent",
        border_width=1,
        border_color="#00796b"
    )
    title_frame.pack(side="left", padx=10, pady=8)

    # CREATING THE TITLE LABELS FOR THE APPLICATION
    title_label_left = ctk.CTkLabel(
        master=title_frame,
        text="EcoPlast",
        font=("Nunito Black", 18, "bold"),
        text_color="#4d9f51"
    )
    title_label_left.pack(side="left", expand=True)

    title_label_right = ctk.CTkLabel(
        master=title_frame,
        text="Dash.",
        font=("Nunito Black", 18, "bold"),
        text_color="#a6cb75"
    )
    title_label_right.pack(side="left")

    # CREATING THE MIDDLE SECTION FOR THE MENU
    middle_section = ctk.CTkFrame(
        master=sidebarContentBox,
        width=250,
        height=620 - (40 + 200),
        corner_radius=8,
        fg_color="transparent",
    )
    middle_section.pack(pady=(15, 25), padx=15, fill="both", expand=True)

    # Function to create menu buttons with hover effects
    def create_menu_button(master, text, emoji, command):
        button = ctk.CTkButton(
            master=master,
            text=f"{emoji}   {text}",
            font=("Nunito ExtraBold", 13, "bold"),
            text_color="#aeacac",
            fg_color="#fefeff",
            hover_color="#e6f4e6",
            command=command,
            corner_radius=7,
            height=36,
            anchor="w",
            compound="left",
            border_width=1,
            border_color="#ffffff"
        )

        def on_enter(event):
            button.configure(border_color="#edf5e4", text_color="#b3d088")

        def on_leave(event):
            button.configure(border_color="#ffffff", text_color="#aeacac")

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        button.pack(pady=5, padx=10, fill="x")
        return button

    # Function to handle button clicks
    def on_button_click(page_name):
        if page_name == "Déconnexion":
            # Close the entire application
            root.destroy()
            sys.exit()
        else:
            show_page(page_name)

    # Creating page view container
    page_view_container = ctk.CTkFrame(
        master=main_container,
        width=950,
        height=650,
        corner_radius=0,
        fg_color="#fefeff"
    )
    page_view_container.place(x=250, y=0)

    # Pages dictionary
    pages = {}

    def create_page(master, page_name):
        if page_name == "Tableau de board":
            page = HomeInterface(master , user_name=user_name)
        elif page_name == "Equipe":
            page = TeamInterface(master, user_name=user_name)
        elif page_name == "Clients":
            page = ClientInterface(master , user_name=user_name)
        elif page_name == "Fournisseurs":
            page = SuppliersInterface(master , user_name=user_name)
        elif page_name == "Commandes":
            page = OrdersInterface(master , user_name=user_name)
        elif page_name == "Produits":
            page = ProductInterface(master ,user_name=user_name)
        else:
            page = ctk.CTkFrame(master=master, width=935, height=650, corner_radius=10, fg_color="#ffffff")
            label = ctk.CTkLabel(master=page, text=page_name, font=("Nunito Black", 24, "bold"), text_color="#4d9f51")
            label.place(relx=0.5, rely=0.5, anchor="center")
        pages[page_name] = page
        return page

    # Function to show the selected page
    def show_page(page_name):
        for page in pages.values():
            page.place_forget()
        if page_name not in pages:
            create_page(page_view_container, page_name)
        pages[page_name].place(x=0, y=0)

    # Creating menu sections and their buttons
    menu_sections = {
        "MENU RAPIDE": [("Tableau de board", "🧩")],
        "GESTION": [
            ("Equipe", "👨‍👧‍👦"),
            ("Clients", "🫱🏼‍🫲🏽"),
            ("Fournisseurs", "🚛"),
            ("Commandes", "📦"),
            ("Produits", "♻️"),
            ("Déconnexion", "🔚")
        ],
    }

    # Looping through the sections and items to create menu titles and buttons
    for section, items in menu_sections.items():
        menu_title = ctk.CTkLabel(
            master=middle_section,
            text=section,
            font=("Nunito ExtraBold", 13, "bold"),
            text_color="black"
        )
        menu_title.pack(pady=(8, 5), padx=8, anchor="w")
        for item, emoji in items:
            create_menu_button(middle_section, item, emoji, lambda item=item: on_button_click(item))

    # CREATING THE BOTTOM SECTION INSIDE THE SIDEBAR CONTENT BOX
    bottom_section = ctk.CTkFrame(
        master=sidebarContentBox,
        width=190,
        height=100,
        corner_radius=8,
        fg_color="transparent",
        border_width=0
    )
    bottom_section.pack(pady=(0, 10), padx=(20, 10), fill="x")

    # LOADING AND DISPLAYING THE BOTTOM IMAGE
    try:
        bottom_image = Image.open(bottom_image_path)
        width, height = bottom_image.size
        new_width = int(width * 0.33)
        new_height = int(height * 0.33)
        bottom_image_resized = bottom_image.resize((new_width, new_height), Image.LANCZOS)
        bottom_image_tk = ImageTk.PhotoImage(bottom_image_resized)

        bottom_label = ctk.CTkLabel(master=bottom_section, image=bottom_image_tk, text="")
        bottom_label.place(relx=0, rely=0.5, anchor="w")
    except Exception as e:
        print("Error loading image:", e)

    # Initially show the dashboard page
    show_page("Tableau de board")

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    base_layout()
