import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# Chemins des fichiers et liste des catégories de produits
icone_path = 'C:/Users/Admin/Pictures/Nouveau dossier/icon.ico'
fichier_stock = 'C:/Users/ASUS/Desktop/test/stock.csv'
fichier_fournisseurs = 'C:/Users/ASUS/Desktop/test/fournisseurs.csv'
fichier_categories = 'C:/Users/ASUS/Desktop/test/categorie.csv'
categories_produits = [
    "SEO", "Marketing par email", "Publicité payante", "Marketing des médias sociaux",
    "Analyse de données", "Stratégie de contenu", "E-commerce", "Design graphique", "Développement web"
]

# Classe Produit pour représenter les produits
class Produit:
    def __init__(self, id, nom, quantite, prix, categorie):
        self.id = id
        self.nom = nom
        self.quantite = int(quantite)
        self.prix = float(prix)
        self.categorie = categorie

# Classe principale de l'application
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion de stock")
        self.configure(background='#a961b8')

        # Initialiser les fournisseurs depuis le fichier CSV
        self.fournisseurs = self.load_fournisseurs(fichier_fournisseurs)

        self.init_login_interface()

    def init_login_interface(self):
        self.clear_widgets()
        tk.Label(self, text="Login", font=("Courier", 18, "bold"), bg="#a961b8", fg="white").grid(row=0, column=1, pady=(10, 15), columnspan=2)
        tk.Label(self, text="Nom d'utilisateur", font=("Courier", 12, "bold"), bg='#a961b8', fg='white').grid(row=1, column=0, pady=(10, 0))
        self.username_entry = ttk.Entry(self, font=("Helvetica", 10))
        self.username_entry.grid(row=1, column=1)
        tk.Label(self, text="Mot de passe", font=("Courier", 12, "bold"), bg='#a961b8', fg='white').grid(row=2, column=0, pady=(10, 0))
        self.password_entry = ttk.Entry(self, show="*", font=("Helvetica", 10))
        self.password_entry.grid(row=2, column=1)
        tk.Button(self, text="Connexion", command=self.verifier_login, font=("Helvetica", 11)).grid(row=3, column=1, columnspan=2, pady=(20, 0))

    def verifier_login(self):
        # Vérification factice pour l'exemple
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Vérifiez les informations d'identification (exemple factice)
        if username == "admin" and password == "password":
            self.afficher_menu_principal()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def afficher_menu_principal(self):
        self.clear_widgets()

        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = tk.Label(frame, text="Menu Principal", font=("Helvetica", 16, "bold"), fg="purple", bg="#a961b8")
        title_label.grid(row=0, column=0, pady=(10, 20), columnspan=2)
        
        # Boutons pour les opérations principales
        gerer_produit_btn = ttk.Button(frame, text="Gérer les Produits", command=self.create_widgets)
        gerer_produit_btn.grid(row=1, column=0, columnspan=2, pady=10)

        gerer_categories_btn = ttk.Button(frame, text="Gérer les Catégories", command=self.gerer_categories_window)
        gerer_categories_btn.grid(row=2, column=0, columnspan=2, pady=10)

        gerer_fournisseurs_btn = ttk.Button(frame, text="Gérer les Fournisseurs", command=self.gerer_fournisseurs_window)
        gerer_fournisseurs_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def create_widgets(self):
        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = tk.Label(frame, text="Gestion de stock", font=("Helvetica", 16, "bold"), fg="purple", bg="#a961b8")
        title_label.grid(row=0, column=0, pady=(10, 20), columnspan=2)

        # Boutons pour les opérations sur les produits
        retour_btn = ttk.Button(frame, text="Retour au Menu Principal", command=self.afficher_menu_principal)
        retour_btn.grid(row=0, column=0, sticky=tk.W, pady=10)

        ajouter_produit_btn = ttk.Button(frame, text="Ajouter produit", command=self.ajouter_produit_window)
        ajouter_produit_btn.grid(row=1, column=0, columnspan=2, pady=10)

        supprimer_produit_btn = ttk.Button(frame, text="Supprimer produit", command=self.supprimer_produit_window)
        supprimer_produit_btn.grid(row=2, column=0, columnspan=2, pady=10)

        rechercher_produit_btn = ttk.Button(frame, text="Rechercher produit", command=self.rechercher_produit_window)
        rechercher_produit_btn.grid(row=3, column=0, columnspan=2, pady=10)

        modifier_produit_btn = ttk.Button(frame, text="Modifier produit", command=self.modifier_produit)
        modifier_produit_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Tableau pour afficher les produits
        self.tree = ttk.Treeview(frame, columns=("ID", "Nom", "Quantité", "Prix", "Catégorie"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Quantité", text="Quantité")
        self.tree.heading("Prix", text="Prix")
        self.tree.heading("Catégorie", text="Catégorie")
        self.tree.grid(row=5, column=0, columnspan=2, pady=10)

        # Mettre à jour le tableau initial
        self.mise_a_jour_table()

    def ajouter_produit_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Ajouter un produit")

        ttk.Label(add_window, text="ID").grid(row=0, column=0)
        id_entry = ttk.Entry(add_window)
        id_entry.grid(row=0, column=1)

        ttk.Label(add_window, text="Nom").grid(row=1, column=0)
        nom_entry = ttk.Entry(add_window)
        nom_entry.grid(row=1, column=1)

        ttk.Label(add_window, text="Quantité").grid(row=2, column=0)
        quantite_entry = ttk.Entry(add_window)
        quantite_entry.grid(row=2, column=1)

        ttk.Label(add_window, text="Prix").grid(row=3, column=0)
        prix_entry = ttk.Entry(add_window)
        prix_entry.grid(row=3, column=1)

        ttk.Label(add_window, text="Catégorie").grid(row=4, column=0)
        categorie_var = tk.StringVar(self)
        categorie_dropdown = ttk.Combobox(add_window, textvariable=categorie_var, values=categories_produits)
        categorie_dropdown.grid(row=4, column=1)

        def add_product():
            produit = Produit(id_entry.get(), nom_entry.get(), quantite_entry.get(), prix_entry.get(), categorie_dropdown.get())
            self.ajouter_produit(fichier_stock, produit)
            add_window.destroy()

        ttk.Button(add_window, text="Ajouter produit", command=add_product).grid(row=5, column=0, columnspan=2, pady=10)

    def supprimer_produit_window(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à supprimer.")
            return
        produit_id = self.tree.item(selection[0], 'values')[0]
        self.supprimer_produit(fichier_stock, produit_id)

    def rechercher_produit_window(self):
        recherche_window = tk.Toplevel(self)
        recherche_window.title("Recherche de produit")

        ttk.Label(recherche_window, text="ID du produit").grid(row=0, column=0)
        recherche_entry = ttk.Entry(recherche_window)
        recherche_entry.grid(row=0, column=1)

        def effectuer_recherche():
            recherche_id = recherche_entry.get()
            if not recherche_id:
                messagebox.showwarning("Avertissement", "Veuillez saisir un ID de produit.")
                return
            
            produits = self.afficher_stock(fichier_stock)
            found = False
            for produit in produits:
                if produit.id == recherche_id:
                    messagebox.showinfo("Résultat de la recherche", f"Nom: {produit.nom}\nQuantité: {produit.quantite}\nPrix: {produit.prix}\nCatégorie: {produit.categorie}")
                    found = True
                    break

            if not found:
                messagebox.showwarning("Avertissement", "Aucun produit trouvé avec cet ID.")

        ttk.Button(recherche_window, text="Rechercher", command=effectuer_recherche).grid(row=1, column=0, columnspan=2, pady=10)

    def modifier_produit(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à modifier.")
            return
        
        produit_id = self.tree.item(selection[0], 'values')[0]
        self.modifier_produit_window(produit_id)

    def modifier_produit_window(self, produit_id):
        produits = self.afficher_stock(fichier_stock)
        produit_a_modifier = None
        for produit in produits:
            if produit.id == produit_id:
                produit_a_modifier = produit
                break
        
        if produit_a_modifier is None:
            messagebox.showwarning("Avertissement", "Produit non trouvé.")
            return

        modify_window = tk.Toplevel(self)
        modify_window.title("Modifier produit")

        ttk.Label(modify_window, text="ID").grid(row=0, column=0)
        id_label = ttk.Label(modify_window, text=produit_a_modifier.id)
        id_label.grid(row=0, column=1)

        ttk.Label(modify_window, text="Nom").grid(row=1, column=0)
        nom_entry = ttk.Entry(modify_window)
        nom_entry.insert(0, produit_a_modifier.nom)
        nom_entry.grid(row=1, column=1)

        ttk.Label(modify_window, text="Quantité").grid(row=2, column=0)
        quantite_entry = ttk.Entry(modify_window)
        quantite_entry.insert(0, produit_a_modifier.quantite)
        quantite_entry.grid(row=2, column=1)

        ttk.Label(modify_window, text="Prix").grid(row=3, column=0)
        prix_entry = ttk.Entry(modify_window)
        prix_entry.insert(0, produit_a_modifier.prix)
        prix_entry.grid(row=3, column=1)

        ttk.Label(modify_window, text="Catégorie").grid(row=4, column=0)
        categorie_var = tk.StringVar(self)
        categorie_dropdown = ttk.Combobox(modify_window, textvariable=categorie_var, values=categories_produits)
        categorie_dropdown.set(produit_a_modifier.categorie)
        categorie_dropdown.grid(row=4, column=1)

        def save_changes():
            produit_a_modifier.nom = nom_entry.get()
            produit_a_modifier.quantite = quantite_entry.get()
            produit_a_modifier.prix = prix_entry.get()
            produit_a_modifier.categorie = categorie_dropdown.get()

            self.sauvegarder_stock(fichier_stock, produits)
            modify_window.destroy()
            self.mise_a_jour_table()

        ttk.Button(modify_window, text="Enregistrer", command=save_changes).grid(row=5, column=0, columnspan=2, pady=10)

    def gerer_categories_window(self):
        categories_window = tk.Toplevel(self)
        categories_window.title("Gérer les Catégories")

        ttk.Label(categories_window, text="Liste des Catégories", font=("Helvetica", 14, "bold")).grid(row=0, column=0, pady=(10, 20))

        self.categories_listbox = tk.Listbox(categories_window, height=10, width=50, font=("Helvetica", 12))
        self.categories_listbox.grid(row=1, column=0, padx=20, pady=(0, 10))

        for category in categories_produits:
            self.categories_listbox.insert(tk.END, category)

        ttk.Button(categories_window, text="Ajouter Catégorie", command=self.ajouter_categorie).grid(row=2, column=0, pady=10)
        ttk.Button(categories_window, text="Supprimer Catégorie", command=self.supprimer_categorie).grid(row=3, column=0, pady=10)

    def ajouter_categorie(self):
        add_cat_window = tk.Toplevel(self)
        add_cat_window.title("Ajouter Catégorie")

        ttk.Label(add_cat_window, text="Nouvelle Catégorie", font=("Helvetica", 14, "bold")).grid(row=0, column=0, pady=(10, 20))
        new_cat_entry = ttk.Entry(add_cat_window, font=("Helvetica", 12))
        new_cat_entry.grid(row=1, column=0, padx=20, pady=10)

        def save_category():
            new_category = new_cat_entry.get()
            if new_category:
                categories_produits.append(new_category)
                self.categories_listbox.insert(tk.END, new_category)
                self.sauvegarder_categories(fichier_categories, categories_produits)
                add_cat_window.destroy()
            else:
                messagebox.showwarning("Avertissement", "Veuillez entrer une nouvelle catégorie.")

        ttk.Button(add_cat_window, text="Enregistrer", command=save_category).grid(row=2, column=0, pady=10)

    def supprimer_categorie(self):
        selection = self.categories_listbox.curselection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une catégorie à supprimer.")
            return

        selected_category = self.categories_listbox.get(selection[0])
        if selected_category in categories_produits:
            categories_produits.remove(selected_category)
            self.categories_listbox.delete(selection[0])
            self.sauvegarder_categories(fichier_categories, categories_produits)

    def gerer_fournisseurs_window(self):
        fournisseurs_window = tk.Toplevel(self)
        fournisseurs_window.title("Gérer les Fournisseurs")

        ttk.Label(fournisseurs_window, text="Liste des Fournisseurs", font=("Helvetica", 14, "bold")).grid(row=0, column=0, pady=(10, 20))

        self.fournisseurs_listbox = tk.Listbox(fournisseurs_window, height=10, width=50, font=("Helvetica", 12))
        self.fournisseurs_listbox.grid(row=1, column=0, padx=20, pady=(0, 10))

        for fournisseur in self.fournisseurs:
            self.fournisseurs_listbox.insert(tk.END, fournisseur)

        ttk.Button(fournisseurs_window, text="Ajouter Fournisseur", command=self.ajouter_fournisseur).grid(row=2, column=0, pady=10)
        ttk.Button(fournisseurs_window, text="Supprimer Fournisseur", command=self.supprimer_fournisseur).grid(row=3, column=0, pady=10)

    def ajouter_fournisseur(self):
        add_fournisseur_window = tk.Toplevel(self)
        add_fournisseur_window.title("Ajouter Fournisseur")

        ttk.Label(add_fournisseur_window, text="Nouveau Fournisseur", font=("Helvetica", 14, "bold")).grid(row=0, column=0, pady=(10, 20))
        new_fournisseur_entry = ttk.Entry(add_fournisseur_window, font=("Helvetica", 12))
        new_fournisseur_entry.grid(row=1, column=0, padx=20, pady=10)

        def save_supplier():
            new_supplier = new_fournisseur_entry.get()
            if new_supplier:
                self.fournisseurs.append(new_supplier)
                self.fournisseurs_listbox.insert(tk.END, new_supplier)
                self.sauvegarder_fournisseurs(fichier_fournisseurs, self.fournisseurs)
                add_fournisseur_window.destroy()
            else:
                messagebox.showwarning("Avertissement", "Veuillez entrer un nouveau fournisseur.")

        ttk.Button(add_fournisseur_window, text="Enregistrer", command=save_supplier).grid(row=2, column=0, pady=10)

    def supprimer_fournisseur(self):
        selection = self.fournisseurs_listbox.curselection()
        if not selection:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un fournisseur à supprimer.")
            return

        selected_supplier = self.fournisseurs_listbox.get(selection[0])
        if selected_supplier in self.fournisseurs:
            self.fournisseurs.remove(selected_supplier)
            self.fournisseurs_listbox.delete(selection[0])
            self.sauvegarder_fournisseurs(fichier_fournisseurs, self.fournisseurs)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def load_fournisseurs(self, fichier):
        if os.path.exists(fichier):
            with open(fichier, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                return [row[0] for row in reader]
        return []

    def sauvegarder_fournisseurs(self, fichier, fournisseurs):
        with open(fichier, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for fournisseur in fournisseurs:
                writer.writerow([fournisseur])

    def afficher_stock(self, fichier):
        produits = []
        if os.path.exists(fichier):
            with open(fichier, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    produits.append(Produit(row[0], row[1], row[2], row[3], row[4]))
        return produits

    def ajouter_produit(self, fichier, produit):
        with open(fichier, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([produit.id, produit.nom, produit.quantite, produit.prix, produit.categorie])
        self.mise_a_jour_table()

    def supprimer_produit(self, fichier, produit_id):
        produits = self.afficher_stock(fichier)
        produits = [p for p in produits if p.id != produit_id]
        self.sauvegarder_stock(fichier, produits)
        self.mise_a_jour_table()

    def sauvegarder_stock(self, fichier, produits):
        with open(fichier, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Nom", "Quantité", "Prix", "Catégorie"])
            for produit in produits:
                writer.writerow([produit.id, produit.nom, produit.quantite, produit.prix, produit.categorie])

    def mise_a_jour_table(self):
        self.tree.delete(*self.tree.get_children())
        produits = self.afficher_stock(fichier_stock)
        for produit in produits:
            self.tree.insert("", tk.END, values=(produit.id, produit.nom, produit.quantite, produit.prix, produit.categorie))

    def sauvegarder_categories(self, fichier, categories):
        with open(fichier, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for category in categories:
                writer.writerow([category])

if __name__ == "__main__":
    app = Application()
    app.mainloop()
