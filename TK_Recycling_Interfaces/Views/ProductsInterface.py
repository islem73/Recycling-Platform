import customtkinter as ctk
from PIL import Image, ImageTk
import os
import tkinter as tk

class ProductInterface(ctk.CTkFrame):
    def __init__(self, master , user_name="" ,**kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=935, height=650, fg_color="#ffffff", corner_radius=10)
        # self.user_name = user_name
   
        
        # Product data array 
        self.products = [
        {
                "name": "PLASTIQUE PP",
                "category": "PP",
                "price": "30 TND / KG",
                "description": "Le plastique PP (polypropylène) est un thermoplastique polyvalent utilisé dans\ndivers domaines. Sa résistance aux chocs, à la chaleur et aux produits chimiques\nen fait un matériau précieux. Léger et résistant à l'usure, il est idéal pour de\nnombreuses applications industrielles.\nIl est adapté aux emballages alimentaires grâce à sa non-toxicité. Son faible\ncoût de production en fait un choix économique pour de nombreuses industries.",
                "features": [
                        {"name": "Résistance aux chocs", "color": "#F25C05"},
                        {"name": "Facilité de façonnage", "color": "#4DA6FF"},
                        {"name": "Résistance à la chaleur", "color": "#B6E087"},
                        {"name": "Résistance chimique", "color": "#9C4DCC"}
                ],
                "stock": {"current": 800, "max": 4000},
                "color": "#4fc3f7",
                "bg_color": "#e3f7fd",
                "image": "granulesBlue.png"
        },
        {
                "name": "PLASTIQUE PET",
                "category": "PET",
                "price": "25 TND / KG",
                "description": "Le PET (polyéthylène téréphtalate) est largement utilisé pour les bouteilles \net emballages alimentaires. Il offre une excellente barrière aux gaz et est \n100% recyclable. Transparent et léger, il est idéal pour les applications \nnécessitant clarté et résistance.\nSa surface lisse permet une excellente impression pour le marquage et le branding.\nLe PET conserve bien les arômes et saveurs des produits qu'il contient.",
                "features": [
                        {"name": "Transparence", "color": "#4DA6FF"},
                        {"name": "Barrière aux gaz", "color": "#9C4DCC"},
                        {"name": "Recyclabilité", "color": "#B6E087"},
                        {"name": "Résistance mécanique", "color": "#F25C05"}
                ],
                "stock": {"current": 1500, "max": 3000},
                "color": "#f4b860",
                "bg_color": "#fdf5df",
                "image": "granulesJaunes.png"
        },
        {
                "name": "PLASTIQUE HDPE",
                "category": "HDPE",
                "price": "28 TND / KG",
                "description": "Le HDPE (polyéthylène haute densité) est connu pour sa rigidité et sa résistance \nchimique. Utilisé dans les contenants rigides, tuyaux et jouets, il offre une \nexcellente résistance aux impacts et est facile à mouler par injection.\nIl résiste particulièrement bien aux produits chimiques agressifs et aux solvants.\nSa surface semi-opaque permet une certaine visibilité du contenu tout en protégeant\nde la lumière.",
                "features": [
                        {"name": "Rigidité", "color": "#4DA6FF"},
                        {"name": "Résistance chimique", "color": "#9C4DCC"},
                        {"name": "Résistance aux impacts", "color": "#F25C05"},
                        {"name": "Facilité de moulage", "color": "#B6E087"}
                ],
                "stock": {"current": 2200, "max": 5000},
                "color": "#d0c2f8",
                "bg_color": "#ebe6fb",
                "image": "granulesMauve.png"
        },
        {
                "name": "PLASTIQUE ABS",
                "category": "ABS",
                "price": "35 TND / KG",
                "description": "L'ABS (acrylonitrile butadiène styrène) combine résistance, rigidité et résistance \naux chocs. Utilisé dans les pièces automobiles, les boîtiers électroniques et les \njouets, il offre une excellente finition de surface et peut être facilement peint ou\n collé. Il supporte bien les températures élevées sans perdre ses propriétés\nmécaniques. Sa surface lisse permet des finitions esthétiques de haute qualité.",
                "features": [
                        {"name": "Résistance aux chocs", "color": "#F25C05"},
                        {"name": "Rigidité", "color": "#4DA6FF"},
                        {"name": "Bonne finition", "color": "#B6E087"},
                        {"name": "Facilité d'usinage", "color": "#9C4DCC"}
                ],
                "stock": {"current": 600, "max": 2000},
                "color": "#f9cfcb",
                "bg_color": "#fbedeb",
                "image": "granulesRouge.png"
        }
    ]
                
        # Currently selected product index
        self.current_product = 0
        
        # Create UI
        self.create_ui(user_name)
        
        # Display first product by default
        self.display_product_details(self.products[self.current_product])
    
    def create_ui(self ,  user_name=""):
        # Main container
        page_view_container = ctk.CTkFrame(self, width=950, height=650, corner_radius=0, fg_color="#fefeff")
        page_view_container.place(x=0, y=0)
        
        # Content container with padding
        content_container = ctk.CTkFrame(page_view_container, width=950-6, height=650-30, corner_radius=0, fg_color="#fefeff")
        content_container.place(x=3, y=15)
        
        # Header section
        self.create_header_section(content_container , user_name)
        
        # Main content section
        section_2 = ctk.CTkFrame(content_container, width=938, height=650-30-55-15, corner_radius=0, fg_color="transparent")
        section_2.place(x=3, y=70)
        
        # Left sidebar with product cards
        self.create_product_cards(section_2)
        
        # Right section for product details
        self.create_product_details_section(section_2)
    
    def create_header_section(self, parent , user_name ):
        section_1 = ctk.CTkFrame(parent, width=938, height=55, corner_radius=0, fg_color="#fefeff")
        section_1.place(x=3, y=0)
        
        # Welcome message
        ctk.CTkLabel(section_1, text=f"Bienvenue De Retour {user_name} !", 
                    font=("Nunito ExtraBold", 19, "bold"), text_color="#2d2d30").place(x=2, y=2)
        ctk.CTkLabel(section_1, text="Qu aimeriez-vous faire aujourd'hui ?", 
                    font=("Nunito ExtraBold", 14, "bold"), text_color="#aeacac").place(x=2, y=25)
    
    def create_product_cards(self, parent):
        left_section = ctk.CTkFrame(parent, width=270, height=355, corner_radius=8, 
                                  fg_color="#ffffff", border_width=1, border_color="#ecf4e2")
        left_section.pack_propagate(False)
        left_section.pack(side="left")
        left_section.place(y=15)
        
        # Title
        title_frame = ctk.CTkFrame(left_section, fg_color="transparent")
        title_frame.pack(pady=(10, 0), padx=10, anchor="w")
        
        title_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Assets", "productsBG.png"))
        title_image = Image.open(title_image_path).resize((35, 35))
        title_image_tk = ImageTk.PhotoImage(title_image)
        
        title_icon = ctk.CTkLabel(title_frame, image=title_image_tk, text="")
        title_icon.image = title_image_tk
        title_icon.pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(title_frame, text="LISTE DES PRODUITS", 
                    font=("Nunito ExtraBold", 13, "bold"), text_color="#2d2d30").pack(side="left")
        
        ctk.CTkLabel(left_section, text="", height=10).pack()
        
        # Create product cards
        for i, product in enumerate(self.products):
            self.create_product_card(left_section, product, i)
    
    def create_product_card(self, parent, product, index):
        card = ctk.CTkFrame(parent, height=62, width=170, fg_color="#f9f9f9", corner_radius=8)
        card.pack(fill="x", padx=10, pady=5)

        # Change cursor on hover
        def on_enter(e):
            card.configure(cursor="hand2")
        def on_leave(e):
            card.configure(cursor="")
    
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # Click event handler
        card.bind("<Button-1>", lambda e, idx=index: self.on_product_selected(idx))
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e, idx=index: self.on_product_selected(idx))
        
        # Image container
        image_container = ctk.CTkFrame(card, width=39, height=39, corner_radius=8, fg_color="#f9f9f9")
        image_container.place(x=5, rely=0.5, anchor="w")
        
        # Emoji icon based on category
        emoji = "🧱"  # Default
        if product["category"] == "PET": emoji = "🥤"
        elif product["category"] == "HDPE": emoji = "🪣"
        elif product["category"] == "ABS": emoji = "🚗"
        
        ctk.CTkLabel(image_container, text=emoji, font=("Arial", 25), 
                    width=35, height=35, fg_color="#f9f9f9", corner_radius=5).pack(padx=2, pady=2)
        
        # Product name
        ctk.CTkLabel(card, text=product["name"], font=("Nunito ExtraBold", 11, "bold"), 
                    text_color="#2d2d30").place(x=60, y=5)
        
        # Category tag
        ctk.CTkLabel(card, text=f"catégorie : {product['category']}", 
                    font=("Nunito", 10, "bold"), text_color="#ffffff",
                    fg_color=product["color"], corner_radius=3, height=19, padx=2).place(x=60, y=33)
        
        # Stock level bar
        stock_percent = (product["stock"]["current"] / product["stock"]["max"]) * 100
        stock_color = "#fc5730" if stock_percent <= 20 else "#B4D786" if stock_percent >= 60 else "#f9b91c"
        
        canvas = tk.Canvas(card, width=14, height=50, bg="#f9f9f9", highlightthickness=0)
        canvas.place(x=200, y=13)
        canvas.create_rectangle(4, 0, 10, 32, fill="#e0e0e0", width=0)
        canvas.create_rectangle(4, 32 - (stock_percent * 0.32), 10, 32, fill=stock_color, width=0)
        
        stock_text = "Faible" if stock_percent <= 20 else "Élevé" if stock_percent >= 60 else "Moyen"
        ctk.CTkLabel(card, text=stock_text, font=("Nunito", 9), 
                    text_color=stock_color, height=10).place(x=193, y=43)
    
    def create_product_details_section(self, parent):
        right_section = ctk.CTkFrame(parent, width=938-270-40, height=650-30-55-15, 
                                   corner_radius=8, fg_color="#ffffff")
        right_section.pack_propagate(False)
        right_section.pack(side="right", fill="both", expand=True, padx=(290, 0))
        
        right_content = ctk.CTkFrame(right_section, fg_color="transparent")
        right_content.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Top section with category filters
        self.top_section = ctk.CTkFrame(right_content, height=37, fg_color="#ffffff")
        self.top_section.pack_propagate(False)
        self.top_section.pack(fill="x", pady=(0, 20))
        
        # Create category filter buttons
        for i, product in enumerate(self.products):
            self.create_category_button(self.top_section, product, i)
        
        # "Nouveau Produit" button
        button_frame = ctk.CTkFrame(self.top_section, fg_color="#b6d48e", corner_radius=6, 
                                  height=26, border_width=1, border_color="#b6d48e")
        button_frame.pack_propagate(False)
        button_frame.pack(side="left", padx=(16, 0))
        
        ctk.CTkLabel(button_frame, text="➕", font=("Nunito", 11, "bold"), 
                    text_color="white").pack(side="left", padx=(10, 3), pady=2.3)
        ctk.CTkLabel(button_frame, text="Nouveau Produit", font=("Nunito", 14, "bold"), 
                    text_color="white").pack(side="left", padx=(3, 12), pady=0)
        
        # Bottom section for product details
        self.bottom_section = ctk.CTkFrame(right_content, fg_color="#ffffff", 
                                          border_width=1, border_color="#ecf4e2")
        self.bottom_section.pack(fill="both", expand=True)
    
    def create_category_button(self, parent, product, index):
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Assets", product["image"]))
        img = Image.open(image_path).resize((20, 20))
        img_tk = ImageTk.PhotoImage(img)
        
        box = ctk.CTkFrame(parent, width=100, fg_color=product["bg_color"], 
                          border_width=1, corner_radius=8, border_color=product["color"])
        box.pack_propagate(False)
        box.pack(side="left", padx=(12 if index > 0 else 0, 0), pady=5)
        
        inner_frame = ctk.CTkFrame(box, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=5, pady=2)
        
        img_label = ctk.CTkLabel(inner_frame, image=img_tk, text="")
        img_label.image = img_tk
        img_label.pack(side="left")
        
        ctk.CTkLabel(inner_frame, text=product["category"], 
                    text_color=product["color"], font=("Nunito", 14, "bold"), 
                    anchor="w").pack(side="left", fill="both", expand=True, padx=5)
        
        # Bind click event
        box.bind("<Button-1>", lambda e, idx=index: self.on_product_selected(idx))
        for child in box.winfo_children():
            child.bind("<Button-1>", lambda e, idx=index: self.on_product_selected(idx))
    
    def on_product_selected(self, index):
        self.current_product = index
        self.display_product_details(self.products[index])
    
    def display_product_details(self, product):
        # Clear previous details
        for widget in self.bottom_section.winfo_children():
            widget.destroy()
        
        # Product name and price
        ctk.CTkLabel(self.bottom_section, text=product["name"], 
                    font=("Nunito ExtraBold", 18, "bold"), text_color="#333"
                    ).place(x=20, y=20)
        ctk.CTkLabel(self.bottom_section, text=product["price"], 
                    font=("Nunito ExtraBold", 17, "bold"), text_color="#c5c5c5"
                    ).place(x=490, y=17)
        
        # Category box
        category_box = ctk.CTkFrame(self.bottom_section, width=145, fg_color=product["bg_color"], 
                                  border_width=1, corner_radius=4, border_color=product["color"])
        category_box.place(x=20, y=55)
        
        inner_padding_frame = ctk.CTkFrame(category_box, fg_color="transparent")
        inner_padding_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(inner_padding_frame, text=f"Catégorie : {product['category']}", 
                    font=("Nunito ExtraBold", 11, "bold"), text_color=product["color"], 
                    height=8).pack()
        
        # Description frame
        description_frame = ctk.CTkFrame(self.bottom_section, width=200, height=120, 
                                       fg_color="white", border_width=2, 
                                       border_color="#000", corner_radius=8)
        description_frame.place(x=20, y=85)
        
        ctk.CTkLabel(description_frame, text=product["description"], 
                    font=("Nunito", 14, "bold"), justify="left", text_color="#b6b6b6", 
                    padx=10, pady=10).pack(fill="both", expand=True)
        
        # Features section
        features_frame = ctk.CTkFrame(self.bottom_section, fg_color="transparent")
        features_frame.pack(anchor="w", padx=20, pady=(220, 0))
        
        ctk.CTkLabel(features_frame, text="Caractéristiques :", 
                    font=("Nunito", 14, "bold"), text_color="#A2C46E"
                    ).grid(row=0, column=0, sticky="w", columnspan=2, pady=(0, 10))
        
        for index, feature in enumerate(product["features"]):
            f = ctk.CTkFrame(features_frame, fg_color="#f7faf4", corner_radius=20, 
                            width=200, height=30)
            f.grid(row=1 + index // 2, column=index % 2, padx=10, pady=5, sticky="w")
            f.pack_propagate(False)
            f.grid_propagate(False)
            
            inner_frame = tk.Frame(f, bg="#f7faf4")
            inner_frame.pack(fill="both", expand=True, padx=10)
            
            canvas = tk.Canvas(inner_frame, width=25, height=20, bg="#f7faf4", highlightthickness=0)
            canvas.pack(side="left")
            canvas.create_oval(2, 2, 18, 18, width=3, outline=feature["color"])
            
            ctk.CTkLabel(inner_frame, text=feature["name"], 
                        font=("Nunito", 14, "bold"), text_color="#2B2B2B"
                        ).pack(side="left", padx=0)
        
        # Stock level
        # stock_frame = ctk.CTkFrame(features_frame, fg_color="transparent")
        # stock_frame.grid(row=4, column=0, columnspan=2, sticky="w")
        
        # ctk.CTkLabel(stock_frame, text="Niveau de stock :", 
        #             font=("Nunito", 14, "bold"), text_color="#A2C46E"
        #             ).grid(row=0, column=0, sticky="w", columnspan=2, pady=(20, 10))
        
        # stock_canvas = tk.Canvas(stock_frame, width=200, height=10, bg="#E5E5E5", highlightthickness=0)
        # stock_canvas.pack(side="left", padx=(15, 10))
        
        # stock_percentage = product["stock"]["current"] / product["stock"]["max"]
        # stock_canvas.create_rectangle(0, 0, 200 * stock_percentage, 10, fill="#4CAF50", width=0)
        
        # ctk.CTkLabel(stock_frame, text=f"{product['stock']['current']}Kg / {product['stock']['max']}Kg", 
        #             font=("Nunito", 14, "bold"), text_color="#7A7A7A").pack(side="left")

        # In the display_product_details method, replace the stock section with:

        # Stock level
        stock_frame = ctk.CTkFrame(features_frame, fg_color="transparent")
        stock_frame.grid(row=5, column=0, columnspan=2, sticky="w", pady=(20, 0))

        ctk.CTkLabel(stock_frame, text="Niveau de stock :", 
            font=("Nunito", 14, "bold"), text_color="#A2C46E"
            ).grid(row=0, column=0, sticky="w")

        stock_canvas_frame = ctk.CTkFrame(stock_frame, fg_color="transparent")
        stock_canvas_frame.grid(row=0, column=1, padx=(15, 10))

        stock_canvas = tk.Canvas(stock_canvas_frame, width=200, height=10, bg="#E5E5E5", highlightthickness=0)
        stock_canvas.grid(row=0, column=0)

        stock_percentage = product["stock"]["current"] / product["stock"]["max"]
        stock_canvas.create_rectangle(0, 0, 200 * stock_percentage, 10, fill="#4CAF50", width=0)

        ctk.CTkLabel(stock_frame, text=f"{product['stock']['current']}Kg / {product['stock']['max']}Kg", 
                    font=("Nunito", 14, "bold"), text_color="#7A7A7A").grid(row=0, column=2, sticky="w")