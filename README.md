🧾 Caisse Enregistreuse NF525
Une interface web de caisse enregistreuse moderne, intuitive et conforme à la norme NF525. Elle permet de gérer les produits, le panier, les paiements et l'affichage d'un reçu.

📸 Aperçu
Interface principale :

Clavier numérique :

Panier en cours :


🚀 Fonctionnalités

🛒 Ajout de produits au panier avec un seul clic
➕ / ➖ Modification des quantités
💰 Calcul automatique du total HT, TVA et TTC
🔢 Clavier numérique interactif
🧾 Génération d’un reçu (affichage en mode debug)
🔐 Intégration possible d'une signature cryptée (via CryptoJS)


🗂 Structure du projet
CaisseEnregistreuse/├── index.html # Fichier principal├── img/│ ├── interface.png # Capture d'écran de l'interface│ ├── keypad.png # Capture du clavier│ └── panier.png # Capture du panier└── README.md # Ce fichier

💡 Utilisation

Téléchargez ou clonez ce dépôt :git clone https://github.com/VictorBongard/CaisseEnregistreuse.git


Ouvrez le fichier index.html dans votre navigateur préféré.
Cliquez sur les boutons produit pour simuler l’ajout au panier.


🛠 Dépendances

CryptoJS — pour le hachage ou la signature éventuelle des tickets.


📋 Conformité NF525
Ce projet est conçu pour servir de prototype d’interface de caisse respectant certains principes de la norme NF525, notamment :

L'inaltérabilité des données (via hachage)
La lisibilité du ticket client
Le détail des montants HT, TVA, et TTC

⚠️ Attention : ce prototype n'est pas certifié. Il est à compléter avec une gestion sécurisée des données, des signatures électroniques inviolables, et un système d'archivage certifié.

🧑‍💻 Auteur
Développé par Victor Bongard📧 Contact : victor.bongard@domaine.com

📄 Licence
Ce projet est distribué sous licence MIT. Voir le fichier LICENSE pour plus d’informations.
