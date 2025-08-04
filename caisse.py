import tkinter as tk
from tkinter import ttk, messagebox
import json
import hashlib
import datetime
import os

class CaisseNF525:
    def __init__(self, root):
        self.root = root
        self.root.title("Caisse NF525 - Fruits & Légumes")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Configuration des produits
        self.produits = {
            "Courgette": {"prix_ht": 3.00, "tva": 0.055},  # TVA réduite pour fruits/légumes frais
            "Pomme": {"prix_ht": 4.00, "tva": 0.055},
            "Poire": {"prix_ht": 3.30, "tva": 0.055},
            "Orange": {"prix_ht": 2.30, "tva": 0.055}
        }
        
        self.panier = []
        self.quantite_saisie = ""
        self.journal_file = "journal_caisse.json"
        
        # Création de l'interface
        self.create_widgets()
        self.charger_journal()
        
    def create_widgets(self):
        # En-tête
        header = tk.Frame(self.root, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="CAISSE ENREGISTREUSE NF525", 
                font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white').pack(pady=15)
        
        # Conteneur principal
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Zone produits (gauche)
        produits_frame = tk.LabelFrame(main_container, text="Produits", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        produits_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        for produit, info in self.produits.items():
            btn = tk.Button(
                produits_frame, 
                text=f"{produit}\n{info['prix_ht']:.2f}€ HT",
                font=('Arial', 11, 'bold'),
                width=12, height=3,
                bg='#3498db', fg='white',
                command=lambda p=produit: self.ajouter_produit(p)
            )
            btn.pack(pady=5, padx=10)
        
        # Zone panier (centre)
        panier_frame = tk.LabelFrame(main_container, text="Panier", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        panier_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Liste des produits
        self.liste_panier = ttk.Treeview(panier_frame, columns=('qte', 'ht', 'ttc'), show='tree headings', height=10)
        self.liste_panier.heading('#0', text='Produit')
        self.liste_panier.heading('qte', text='Qté')
        self.liste_panier.heading('ht', text='Prix HT')
        self.liste_panier.heading('ttc', text='Prix TTC')
        self.liste_panier.column('#0', width=120)
        self.liste_panier.column('qte', width=50, anchor='center')
        self.liste_panier.column('ht', width=70, anchor='e')
        self.liste_panier.column('ttc', width=70, anchor='e')
        self.liste_panier.pack(padx=10, pady=10)
        
        # Totaux
        self.totaux_frame = tk.Frame(panier_frame, bg='#f0f0f0')
        self.totaux_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.total_ht_label = tk.Label(self.totaux_frame, text="Total HT: 0.00€", font=('Arial', 11), bg='#f0f0f0')
        self.total_ht_label.pack(anchor='e')
        
        self.total_tva_label = tk.Label(self.totaux_frame, text="TVA: 0.00€", font=('Arial', 11), bg='#f0f0f0')
        self.total_tva_label.pack(anchor='e')
        
        self.total_ttc_label = tk.Label(self.totaux_frame, text="Total TTC: 0.00€", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        self.total_ttc_label.pack(anchor='e')
        
        # Zone contrôle (droite)
        controle_frame = tk.Frame(main_container, bg='#f0f0f0')
        controle_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Clavier numérique
        clavier_frame = tk.LabelFrame(controle_frame, text="Clavier Numérique", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        clavier_frame.pack(pady=10)
        
        # Affichage de la quantité
        self.quantite_display = tk.Label(clavier_frame, text="0", font=('Arial', 20), bg='white', width=5, height=1)
        self.quantite_display.grid(row=0, column=0, columnspan=3, pady=5, padx=5)
        
        # Boutons du clavier
        boutons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('C', 4, 0), ('0', 4, 1), ('✓', 4, 2)
        ]
        
        for (text, row, col) in boutons:
            btn = tk.Button(
                clavier_frame, text=text, font=('Arial', 14, 'bold'),
                width=4, height=2,
                bg='#ecf0f1' if text not in ['C', '✓'] else '#e74c3c' if text == 'C' else '#2ecc71',
                command=lambda t=text: self.clavier_action(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
        
        # Boutons de fonction
        fonction_frame = tk.LabelFrame(controle_frame, text="Actions", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        fonction_frame.pack(pady=10, fill=tk.X)
        
        tk.Button(
            fonction_frame, text="Modifier Qté", font=('Arial', 11),
            bg='#f39c12', fg='white', width=15, height=2,
            command=self.modifier_quantite
        ).pack(pady=5)
        
        tk.Button(
            fonction_frame, text="Supprimer", font=('Arial', 11),
            bg='#e74c3c', fg='white', width=15, height=2,
            command=self.supprimer_produit
        ).pack(pady=5)
        
        tk.Button(
            fonction_frame, text="Payer", font=('Arial', 11, 'bold'),
            bg='#27ae60', fg='white', width=15, height=2,
            command=self.payer
        ).pack(pady=5)
        
        tk.Button(
            fonction_frame, text="Annuler", font=('Arial', 11),
            bg='#95a5a6', fg='white', width=15, height=2,
            command=self.annuler_transaction
        ).pack(pady=5)
        
        # Configuration des poids
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
    def ajouter_produit(self, nom_produit):
        produit = self.produits[nom_produit]
        prix_ttc = produit["prix_ht"] * (1 + produit["tva"])
        
        # Vérifier si le produit existe déjà dans le panier
        for item in self.panier:
            if item["nom"] == nom_produit:
                item["quantite"] += 1
                self.maj_affichage()
                return
        
        # Ajouter nouveau produit
        self.panier.append({
            "nom": nom_produit,
            "quantite": 1,
            "prix_ht": produit["prix_ht"],
            "prix_ttc": prix_ttc,
            "tva": produit["tva"]
        })
        
        self.maj_affichage()
    
    def clavier_action(self, touche):
        if touche == 'C':
            self.quantite_saisie = ""
        elif touche == '✓':
            self.valider_quantite()
        else:
            self.quantite_saisie += touche
        
        self.quantite_display.config(text=self.quantite_saisie if self.quantite_saisie else "0")
    
    def valider_quantite(self):
        if not self.quantite_saisie:
            return
        
        try:
            quantite = int(self.quantite_saisie)
            if quantite <= 0:
                raise ValueError
            
            # Appliquer la quantité au produit sélectionné
            selection = self.liste_panier.selection()
            if selection:
                index = self.liste_panier.index(selection[0])
                self.panier[index]["quantite"] = quantite
                self.maj_affichage()
            
            self.quantite_saisie = ""
            self.quantite_display.config(text="0")
        except ValueError:
            messagebox.showerror("Erreur", "Quantité invalide")
            self.quantite_saisie = ""
            self.quantite_display.config(text="0")
    
    def modifier_quantite(self):
        selection = self.liste_panier.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Sélectionnez un produit")
            return
        
        # Focus sur le clavier
        self.quantite_saisie = ""
        self.quantite_display.config(text="0")
    
    def supprimer_produit(self):
        selection = self.liste_panier.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Sélectionnez un produit")
            return
        
        index = self.liste_panier.index(selection[0])
        del self.panier[index]
        self.maj_affichage()
    
    def maj_affichage(self):
        # Vider la liste
        for item in self.liste_panier.get_children():
            self.liste_panier.delete(item)
        
        # Remplir avec les produits du panier
        total_ht = 0.0
        total_tva = 0.0
        total_ttc = 0.0
        
        for produit in self.panier:
            total_ht += produit["prix_ht"] * produit["quantite"]
            total_tva += produit["prix_ht"] * produit["tva"] * produit["quantite"]
            total_ttc += produit["prix_ttc"] * produit["quantite"]
            
            self.liste_panier.insert(
                '', 'end', text=produit["nom"],
                values=(produit["quantite"], 
                       f"{produit['prix_ht']:.2f}€", 
                       f"{produit['prix_ttc']:.2f}€")
            )
        
        # Mettre à jour les totaux
        self.total_ht_label.config(text=f"Total HT: {total_ht:.2f}€")
        self.total_tva_label.config(text=f"TVA: {total_tva:.2f}€")
        self.total_ttc_label.config(text=f"Total TTC: {total_ttc:.2f}€")
    
    def payer(self):
        if not self.panier:
            messagebox.showwarning("Avertissement", "Le panier est vide")
            return
        
        # Calcul des totaux
        total_ht = sum(p["prix_ht"] * p["quantite"] for p in self.panier)
        total_tva = sum(p["prix_ht"] * p["tva"] * p["quantite"] for p in self.panier)
        total_ttc = sum(p["prix_ttc"] * p["quantite"] for p in self.panier)
        
        # Création du ticket
        ticket = {
            "timestamp": datetime.datetime.now().isoformat(),
            "produits": self.panier.copy(),
            "total_ht": total_ht,
            "total_tva": total_tva,
            "total_ttc": total_ttc,
            "hash": self.generate_hash(total_ht, total_ttc)
        }
        
        # Enregistrement dans le journal
        self.enregistrer_journal(ticket)
        
        # Afficher le récapitulatif
        recap = f"=== TICKET DE CAISSE ===\n"
        recap += f"Date: {ticket['timestamp'][:19]}\n"
        recap += f"Hash: {ticket['hash'][:16]}...\n\n"
        
        for p in self.panier:
            recap += f"{p['nom']} x{p['quantite']} - {p['prix_ttc']:.2f}€\n"
        
        recap += f"\nTotal HT: {total_ht:.2f}€\n"
        recap += f"TVA: {total_tva:.2f}€\n"
        recap += f"Total TTC: {total_ttc:.2f}€\n"
        recap += "\n=== PAIEMENT ACCEPTÉ ==="
        
        messagebox.showinfo("Paiement", recap)
        
        # Réinitialiser le panier
        self.panier = []
        self.maj_affichage()
    
    def generate_hash(self, total_ht, total_ttc):
        data = f"{total_ht}{total_ttc}{datetime.datetime.now()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def enregistrer_journal(self, ticket):
        journal = []
        if os.path.exists(self.journal_file):
            with open(self.journal_file, 'r') as f:
                journal = json.load(f)
        
        journal.append(ticket)
        
        with open(self.journal_file, 'w') as f:
            json.dump(journal, f, indent=2)
    
    def annuler_transaction(self):
        if not self.panier:
            return
        
        if messagebox.askyesno("Confirmation", "Annuler la transaction en cours?"):
            self.panier = []
            self.maj_affichage()
            self.quantite_saisie = ""
            self.quantite_display.config(text="0")
    
    def charger_journal(self):
        if not os.path.exists(self.journal_file):
            with open(self.journal_file, 'w') as f:
                json.dump([], f)

# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = CaisseNF525(root)
    root.mainloop()