import tkinter as tk
from tkinter import messagebox
import json
import hashlib
import datetime
import os

class CaisseNF525:
    def __init__(self, root):
        self.root = root
        self.root.title("Caisse NF525 - Sécurisée")
        self.produits = []
        self.total_ht = 0.0
        self.total_ttc = 0.0
        self.tva_rate = 0.20
        self.journal_file = "journal_caisse.json"
        
        # Création de l'interface
        self.create_widgets()
        self.charger_journal()

    def create_widgets(self):
        # Zone d'affichage
        self.display = tk.Text(self.root, height=10, width=40, state='disabled')
        self.display.pack(pady=10)
        
        # Champs de saisie
        tk.Label(self.root, text="Produit:").pack()
        self.entry_produit = tk.Entry(self.root)
        self.entry_produit.pack()
        
        tk.Label(self.root, text="Quantité:").pack()
        self.entry_qte = tk.Entry(self.root)
        self.entry_qte.pack()
        
        tk.Label(self.root, text="Prix HT:").pack()
        self.entry_prix = tk.Entry(self.root)
        self.entry_prix.pack()
        
        # Boutons
        tk.Button(self.root, text="Ajouter", command=self.ajouter_produit).pack(pady=5)
        tk.Button(self.root, text="Payer", command=self.payer).pack(pady=5)
        tk.Button(self.root, text="Voir Journal", command=self.voir_journal).pack(pady=5)

    def ajouter_produit(self):
        try:
            produit = self.entry_produit.get()
            qte = int(self.entry_qte.get())
            prix_ht = float(self.entry_prix.get())
            
            # Calcul TTC
            prix_ttc = prix_ht * (1 + self.tva_rate)
            self.produits.append({
                "produit": produit,
                "qte": qte,
                "prix_ht": prix_ht,
                "prix_ttc": prix_ttc
            })
            
            self.total_ht += prix_ht * qte
            self.total_ttc += prix_ttc * qte
            
            self.maj_affichage()
            self.clear_entries()
            
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs invalides")

    def payer(self):
        if not self.produits:
            messagebox.showwarning("Avertissement", "Aucun produit enregistré")
            return
            
        # Génération d'un ticket sécurisé
        ticket = {
            "timestamp": datetime.datetime.now().isoformat(),
            "produits": self.produits,
            "total_ht": self.total_ht,
            "total_ttc": self.total_ttc,
            "tva": self.total_ttc - self.total_ht,
            "hash": self.generate_hash()
        }
        
        # Enregistrement dans le journal (NF525)
        self.enregistrer_journal(ticket)
        
        # Affichage du ticket
        self.afficher_ticket(ticket)
        
        # Réinitialisation
        self.reset_caisse()

    def generate_hash(self):
        data = f"{self.total_ht}{self.total_ttc}{datetime.datetime.now()}"
        return hashlib.sha256(data.encode()).hexdigest()

    def enregistrer_journal(self, ticket):
        journal = []
        if os.path.exists(self.journal_file):
            with open(self.journal_file, 'r') as f:
                journal = json.load(f)
        
        journal.append(ticket)
        
        with open(self.journal_file, 'w') as f:
            json.dump(journal, f, indent=2)

    def afficher_ticket(self, ticket):
        self.display.config(state='normal')
        self.display.delete(1.0, tk.END)
        
        self.display.insert(tk.END, f"=== TICKET NF525 ===\n")
        self.display.insert(tk.END, f"Date: {ticket['timestamp']}\n")
        self.display.insert(tk.END, f"Hash: {ticket['hash'][:16]}...\n\n")
        
        for produit in ticket["produits"]:
            self.display.insert(tk.END, 
                f"{produit['produit']} x{produit['qte']} - "
                f"€{produit['prix_ttc']:.2f}\n"
            )
        
        self.display.insert(tk.END, "\n-----------------\n")
        self.display.insert(tk.END, f"Total HT: €{ticket['total_ht']:.2f}\n")
        self.display.insert(tk.END, f"TVA (20%): €{ticket['tva']:.2f}\n")
        self.display.insert(tk.END, f"Total TTC: €{ticket['total_ttc']:.2f}\n")
        self.display.insert(tk.END, "\n=== FIN TICKET ===")
        
        self.display.config(state='disabled')

    def voir_journal(self):
        if not os.path.exists(self.journal_file):
            messagebox.showinfo("Journal", "Aucune transaction enregistrée")
            return
            
        with open(self.journal_file, 'r') as f:
            journal = json.load(f)
        
        self.display.config(state='normal')
        self.display.delete(1.0, tk.END)
        
        for ticket in journal:
            self.display.insert(tk.END, 
                f"{ticket['timestamp']} - "
                f"€{ticket['total_ttc']:.2f} - "
                f"{ticket['hash'][:8]}...\n"
            )
        
        self.display.config(state='disabled')

    def maj_affichage(self):
        self.display.config(state='normal')
        self.display.delete(1.0, tk.END)
        
        for produit in self.produits:
            self.display.insert(tk.END, 
                f"{produit['produit']} x{produit['qte']} - "
                f"€{produit['prix_ttc']:.2f}\n"
            )
        
        self.display.insert(tk.END, "\n-----------------\n")
        self.display.insert(tk.END, f"Total HT: €{self.total_ht:.2f}\n")
        self.display.insert(tk.END, f"Total TTC: €{self.total_ttc:.2f}\n")
        
        self.display.config(state='disabled')

    def clear_entries(self):
        self.entry_produit.delete(0, tk.END)
        self.entry_qte.delete(0, tk.END)
        self.entry_prix.delete(0, tk.END)

    def reset_caisse(self):
        self.produits = []
        self.total_ht = 0.0
        self.total_ttc = 0.0
        self.maj_affichage()

    def charger_journal(self):
        if not os.path.exists(self.journal_file):
            with open(self.journal_file, 'w') as f:
                json.dump([], f)

# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = CaisseNF525(root)
    root.mainloop()