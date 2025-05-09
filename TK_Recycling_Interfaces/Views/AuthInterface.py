import sys
import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root)) 

from TK_Recycling_Database.connexion_DB import (
    create_connection
)


# ---------- IMAGE PATHS ----------
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, '../Assets')

bg_image_path = os.path.abspath(os.path.join(ASSETS_DIR, 'LoginBg.png'))
logo_image_path = os.path.abspath(os.path.join(ASSETS_DIR, 'mainLogo.png'))

# ---------- TKINTER WINDOW ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Sign In")
root.geometry("1200x650")
root.configure(bg="white")

# ---------- MAIN CONTAINER ----------
main_container = ctk.CTkFrame(master=root, width=1000, height=600, corner_radius=10,
                              fg_color="#f5f7f2", border_width=1, border_color="#d3d3d3")
main_container.place(relx=0.5, rely=0.5, anchor="center")
main_container.grid_rowconfigure(0, weight=1)
main_container.grid_columnconfigure(0, weight=1)
main_container.grid_columnconfigure(1, weight=1)

# ---------- LEFT SIDE ----------
left_side = ctk.CTkFrame(master=main_container, corner_radius=10,
                         fg_color="transparent", border_width=1, border_color="#d3d3d3")
left_side.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

try:
    bg_image = Image.open(bg_image_path)
    bg_image_resized = bg_image.resize((430, 480), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image_resized)
    bg_label = ctk.CTkLabel(master=left_side, image=bg_image_tk, text="")
    bg_label.pack(expand=True, fill="both")
except Exception as e:
    print("Erreur de chargement d'image :", e)

# ---------- RIGHT SIDE ----------
right_side = ctk.CTkFrame(master=main_container, corner_radius=10, fg_color="transparent")
right_side.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

right_side_wrapper = ctk.CTkFrame(master=right_side, fg_color="transparent")
right_side_wrapper.pack(expand=True, fill="both", pady=20)

logo_frame = ctk.CTkFrame(master=right_side_wrapper, width=60, height=60, fg_color="transparent")
logo_frame.pack()

try:
    logo_image = Image.open(logo_image_path)
    logo_image_resized = logo_image.resize((50, 50), Image.LANCZOS)
    logo_image_tk = ImageTk.PhotoImage(logo_image_resized)
    logo_label = ctk.CTkLabel(master=logo_frame, image=logo_image_tk, text="")
    logo_label.place(relwidth=1, relheight=1)
except Exception as e:
    print("Erreur de chargement d'image :", e)
    logo_label = ctk.CTkLabel(master=logo_frame, text="Logo Not Found", text_color="black", font=("Nunito", 10))
    logo_label.place(relwidth=1, relheight=1)

title_label = ctk.CTkLabel(master=right_side_wrapper, text="Bienvenue !",
                           font=("Nunito", 24, "bold"), text_color="#2e2e30")
title_label.pack(pady=10)

# ---------- FORM ----------
login_form = ctk.CTkFrame(master=right_side_wrapper, fg_color="transparent")
login_form.pack(expand=True, fill="both", pady=10)

email_label = ctk.CTkLabel(master=login_form, text="Email", font=("Nunito", 16, "bold"),
                           text_color="#878686", anchor="w")
email_label.pack(pady=5, anchor="w", padx=20)

email_entry = ctk.CTkEntry(master=login_form, width=300, height=35, corner_radius=10,
                           fg_color="#e8effe", text_color="black", border_width=0)
email_entry.pack(pady=5, anchor="w", padx=20)

password_label = ctk.CTkLabel(master=login_form, text="Mot de passe", font=("Nunito", 16, "bold"),
                              text_color="#878686", anchor="w")
password_label.pack(pady=5, anchor="w", padx=20)

password_entry = ctk.CTkEntry(master=login_form, width=300, height=35, corner_radius=10,
                              fg_color="#e8effe", text_color="black", border_width=0, show="*")
password_entry.pack(pady=5, anchor="w", padx=20)

def base_layout(user_name):
    root.destroy()
    import BaseLayout  
    BaseLayout.base_layout(user_name)


def verify_login():
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not email or not password:
        messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs.")
        return

    db = create_connection()
    if db:
        try:
            cursor = db.cursor()
            query = "SELECT * FROM user WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            result = cursor.fetchone()
            cursor.close()
            db.close()

            if result:
                user_id = result[0]
                user_name = result[1]
                # messagebox.showinfo("Connexion réussie", f"Bienvenue {result[1]}!")
                # Redirect to main layout
                root.destroy()
                import BaseLayout
                BaseLayout.base_layout(user_name)

            else:
                messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite: {e}")
    else:
        messagebox.showerror("Erreur de connexion", "Impossible de se connecter à la base de données.")


login_button = ctk.CTkButton(master=login_form, text="Se connecter", width=200, height=40, fg_color="#98c05d", text_color="white", hover_color="#7da34d", font=("Nunito ExtraBold", 17, "bold") ,corner_radius=10,
                             command=verify_login)
login_button.pack(pady=20, padx=20)

# ---------- MAINLOOP ----------
root.mainloop()
