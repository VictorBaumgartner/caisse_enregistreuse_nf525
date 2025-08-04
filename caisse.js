<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Caisse Enregistreuse NF525</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
    <style>
        * {
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 28px;
        }
        
        .content {
            display: flex;
            flex-wrap: wrap;
            padding: 20px;
        }
        
        .products-section {
            flex: 1;
            min-width: 300px;
            margin-right: 20px;
        }
        
        .cart-section {
            flex: 2;
            min-width: 400px;
        }
        
        .section-title {
            font-size: 20px;
            margin-bottom: 15px;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }
        
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
        }
        
        .product-btn {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .product-btn:hover {
            background-color: #2980b9;
            transform: translateY(-3px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }
        
        .product-name {
            font-size: 18px;
            margin-bottom: 5px;
        }
        
        .product-price {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .cart-container {
            background-color: #f9f9f9;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .cart-items {
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 15px;
        }
        
        .cart-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        
        .cart-item:last-child {
            border-bottom: none;
        }
        
        .cart-item-info {
            flex: 1;
        }
        
        .cart-item-name {
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .cart-item-price {
            color: #7f8c8d;
            font-size: 14px;
        }
        
        .cart-item-actions {
            display: flex;
            align-items: center;
        }
        
        .quantity-btn {
            background-color: #3498db;
            color: white;
            border: none;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            font-weight: bold;
            margin: 0 5px;
        }
        
        .quantity-btn:hover {
            background-color: #2980b9;
        }
        
        .quantity-display {
            min-width: 30px;
            text-align: center;
            font-weight: bold;
        }
        
        .cart-totals {
            border-top: 2px solid #3498db;
            padding-top: 15px;
        }
        
        .total-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .total-row.final {
            font-weight: bold;
            font-size: 18px;
            color: #2c3e50;
            margin-top: 10px;
        }
        
        .keypad-section {
            margin-top: 20px;
        }
        
        .keypad {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            max-width: 300px;
            margin: 0 auto;
        }
        
        .keypad-btn {
            background-color: #ecf0f1;
            border: none;
            border-radius: 8px;
            padding: 20px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .keypad-btn:hover {
            background-color: #bdc3c7;
        }
        
        .keypad-btn.action {
            background-color: #2ecc71;
            color: white;
        }
        
        .keypad-btn.action:hover {
            background-color: #27ae60;
        }
        
        .keypad-btn.clear {
            background-color: #e74c3c;
            color: white;
        }
        
        .keypad-btn.clear:hover {
            background-color: #c0392b;
        }
        
        .keypad-display {
            background-color: #2c3e50;
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            border-radius: 8px;
        }
        
        .actions {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }
        
        .action-btn {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 16px;
        }
        
        .pay-btn {
            background-color: #2ecc71;
            color: white;
        }
        
        .pay-btn:hover {
            background-color: #27ae60;
        }
        
        .cancel-btn {
            background-color: #e74c3c;
            color: white;
        }
        
        .cancel-btn:hover {
            background-color: #c0392b;
        }
        
        .receipt {
            background-color: #f9f9f9;
            border: 1px dashed #ccc;
            padding: 15px;
            margin-top: 20px;
            border-radius: 8px;
            font-family: monospace;
            white-space: pre-line;
            display: none;
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: #2ecc71;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            display: none;
            z-index: 1000;
        }
        
        @media (max-width: 768px) {
            .content {
                flex-direction: column;
            }
            
            .products-section {
                margin-right: 0;
                margin-bottom: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Caisse Enregistreuse NF525</h1>
        </div>
        
        <div class="content">
            <div class="products-section">
                <h2 class="section-title">Produits</h2>
                <div class="products-grid">
                    <button class="product-btn" data-product="Courgette" data-price="3.00">
                        <div class="product-name">Courgette</div>
                        <div class="product-price">3.00€ HT</div>
                    </button>
                    <button class="product-btn" data-product="Pomme" data-price="4.00">
                        <div class="product-name">Pomme</div>
                        <div class="product-price">4.00€ HT</div>
                    </button>
                    <button class="product-btn" data-product="Poire" data-price="3.30">
                        <div class="product-name">Poire</div>
                        <div class="product-price">3.30€ HT</div>
                    </button>
                    <button class="product-btn" data-product="Orange" data-price="2.30">
                        <div class="product-name">Orange</div>
                        <div class="product-price">2.30€ HT</div>
                    </button>
                </div>
            </div>
            
            <div class="cart-section">
                <h2 class="section-title">Panier</h2>
                <div class="cart-container">
                    <div class="cart-items" id="cart-items">
                        <!-- Les articles du panier seront ajoutés ici -->
                    </div>
                    <div class="cart-totals">
                        <div class="total-row">
                            <span>Total HT:</span>
                            <span id="total-ht">0.00€</span>
                        </div>
                        <div class="total-row">
                            <span>TVA (5.5%):</span>
                            <span id="total-tva">0.00€</span>
                        </div>
                        <div class="total-row final">
                            <span>Total TTC:</span>
                            <span id="total-ttc">0.00€</span>
                        </div>
                    </div>
                </div>
                
                <div class="keypad-section">
                    <h2 class="section-title">Clavier Numérique</h2>
                    <div class="keypad-display" id="keypad-display">0</div>
                    <div class="keypad">
                        <button class="keypad-btn" data-key="7">7</button>
                        <button class="keypad-btn" data-key="8">8</button>
                        <button class="keypad-btn" data-key="9">9</button>
                        <button class="keypad-btn" data-key="4">4</button>
                        <button class="keypad-btn" data-key="5">5</button>
                        <button class="keypad-btn" data-key="6">6</button>
                        <button class="keypad-btn" data-key="1">1</button>
                        <button class="keypad-btn" data-key="2">2</button>
                        <button class="keypad-btn" data-key="3">3</button>
                        <button class="keypad-btn clear" data-key="C">C</button>
                        <button class="keypad-btn" data-key="0">0</button>
                        <button class="keypad-btn action" data-key="OK">OK</button>
                    </div>
                </div>
                
                <div class="actions">
                    <button class="action-btn pay-btn" id="pay-btn">Payer</button>
                    <button class="action-btn cancel-btn" id="cancel-btn">Annuler</button>
                </div>
                
                <div class="receipt" id="receipt"></div>
            </div>
        </div>
    </div>
    
    <div class="notification" id="notification"></div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Configuration des produits
            const products = {
                "Courgette": { price: 3.00, tva: 0.055 },
                "Pomme": { price: 4.00, tva: 0.055 },
                "Poire": { price: 3.30, tva: 0.055 },
                "Orange": { price: 2.30, tva: 0.055 }
            };
            
            // État de l'application
            let cart = [];
            let keypadInput = "0";
            let selectedProductIndex = null;
            
            // Éléments du DOM
            const cartItemsContainer = document.getElementById('cart-items');
            const totalHtElement = document.getElementById('total-ht');
            const totalTvaElement = document.getElementById('total-tva');
            const totalTtcElement = document.getElementById('total-ttc');
            const keypadDisplay = document.getElementById('keypad-display');
            const receiptElement = document.getElementById('receipt');
            const notificationElement = document.getElementById('notification');
            
            // Initialisation
            updateCartDisplay();
            
            // Gestion des clics sur les produits
            document.querySelectorAll('.product-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const productName = this.getAttribute('data-product');
                    const productPrice = parseFloat(this.getAttribute('data-price'));
                    
                    // Vérifier si le produit est déjà dans le panier
                    const existingProductIndex = cart.findIndex(item => item.name === productName);
                    
                    if (existingProductIndex !== -1) {
                        // Incrémenter la quantité
                        cart[existingProductIndex].quantity += 1;
                    } else {
                        // Ajouter un nouveau produit
                        cart.push({
                            name: productName,
                            price: productPrice,
                            tva: products[productName].tva,
                            quantity: 1
                        });
                    }
                    
                    updateCartDisplay();
                    showNotification(`${productName} ajouté au panier`);
                });
            });
            
            // Gestion du clavier numérique
            document.querySelectorAll('.keypad-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const key = this.getAttribute('data-key');
                    
                    if (key === 'C') {
                        keypadInput = "0";
                    } else if (key === 'OK') {
                        if (selectedProductIndex !== null) {
                            const quantity = parseInt(keypadInput);
                            if (quantity > 0) {
                                cart[selectedProductIndex].quantity = quantity;
                                updateCartDisplay();
                                showNotification(`Quantité mise à jour: ${quantity}`);
                            }
                            keypadInput = "0";
                            selectedProductIndex = null;
                        }
                    } else {
                        if (keypadInput === "0") {
                            keypadInput = key;
                        } else {
                            keypadInput += key;
                        }
                    }
                    
                    keypadDisplay.textContent = keypadInput;
                });
            });
            
            // Gestion des boutons d'action
            document.getElementById('pay-btn').addEventListener('click', processPayment);
            document.getElementById('cancel-btn').addEventListener('click', cancelTransaction);
            
            // Fonction pour mettre à jour l'affichage du panier
            function updateCartDisplay() {
                // Vider le conteneur du panier
                cartItemsContainer.innerHTML = '';
                
                let totalHt = 0;
                let totalTva = 0;
                
                // Ajouter chaque produit au panier
                cart.forEach((item, index) => {
                    const itemPriceHt = item.price * item.quantity;
                    const itemTva = itemPriceHt * item.tva;
                    const itemPriceTtc = itemPriceHt + itemTva;
                    
                    totalHt += itemPriceHt;
                    totalTva += itemTva;
                    
                    const cartItemElement = document.createElement('div');
                    cartItemElement.className = 'cart-item';
                    cartItemElement.innerHTML = `
                        <div class="cart-item-info">
                            <div class="cart-item-name">${item.name}</div>
                            <div class="cart-item-price">${item.price.toFixed(2)}€ HT × ${item.quantity} = ${itemPriceTtc.toFixed(2)}€ TTC</div>
                        </div>
                        <div class="cart-item-actions">
                            <button class="quantity-btn" data-index="${index}" data-action="decrease">-</button>
                            <div class="quantity-display">${item.quantity}</div>
                            <button class="quantity-btn" data-index="${index}" data-action="increase">+</button>
                            <button class="quantity-btn" data-index="${index}" data-action="select" style="background-color: #9b59b6;">✓</button>
                        </div>
                    `;
                    
                    cartItemsContainer.appendChild(cartItemElement);
                });
                
                // Mettre à jour les totaux
                const totalTtc = totalHt + totalTva;
                totalHtElement.textContent = `${totalHt.toFixed(2)}€`;
                totalTvaElement.textContent = `${totalTva.toFixed(2)}€`;
                totalTtcElement.textContent = `${totalTtc.toFixed(2)}€`;
                
                // Ajouter les écouteurs d'événements pour les boutons de quantité
                document.querySelectorAll('.quantity-btn').forEach(button => {
                    button.addEventListener('click', function() {
                        const index = parseInt(this.getAttribute('data-index'));
                        const action = this.getAttribute('data-action');
                        
                        if (action === 'increase') {
                            cart[index].quantity += 1;
                            updateCartDisplay();
                        } else if (action === 'decrease') {
                            if (cart[index].quantity > 1) {
                                cart[index].quantity -= 1;
                                updateCartDisplay();
                            } else {
                                cart.splice(index, 1);
                                updateCartDisplay();
                            }
                        } else if (action === 'select') {
                            selectedProductIndex = index;
                            keypadInput = cart[index].quantity.toString();
                            keypadDisplay.textContent = keypadInput;
                            showNotification(`Produit sélectionné: ${cart[index].name}`);
                        }
                    });
                });
            }
            
            // Fonction pour traiter le paiement
            function processPayment() {
                if (cart.length === 0) {
                    showNotification("Le panier est vide", "error");
                    return;
                }
                
                // Calculer les totaux
                let totalHt = 0;
                let totalTva = 0;
                
                cart.forEach(item => {
                    const itemPriceHt = item.price * item.quantity;
                    const itemTva = itemPriceHt * item.tva;
                    
                    totalHt += itemPriceHt;
                    totalTva += itemTva;
                });
                
                const totalTtc = totalHt + totalTva;
                
                // Créer un ticket
                const timestamp = new Date().toISOString();
                const hash = CryptoJS.SHA256(`${totalHt}${totalTtc}${timestamp}`).toString();
                
                const receipt = {
                    timestamp: timestamp,
                    products: [...cart],
                    totalHt: totalHt,
                    totalTva: totalTva,
                    totalTtc: totalTtc,
                    hash: hash
                };
                
                // Enregistrer dans le journal (localStorage)
                let journal = JSON.parse(localStorage.getItem('caisse_journal') || '[]');
                journal.push(receipt);
                localStorage.setItem('caisse_journal', JSON.stringify(journal));
                
                // Afficher le ticket
                let receiptText = `=== TICKET DE CAISSE NF525 ===\n`;
                receiptText += `Date: ${new Date(timestamp).toLocaleString()}\n`;
                receiptText += `Hash: ${hash.substring(0, 16)}...\n\n`;
                
                cart.forEach(item => {
                    const itemPriceHt = item.price * item.quantity;
                    const itemTva = itemPriceHt * item.tva;
                    const itemPriceTtc = itemPriceHt + itemTva;
                    
                    receiptText += `${item.name} x${item.quantity} - ${itemPriceTtc.toFixed(2)}€ TTC\n`;
                });
                
                receiptText += `\nTotal HT: ${totalHt.toFixed(2)}€\n`;
                receiptText += `TVA (5.5%): ${totalTva.toFixed(2)}€\n`;
                receiptText += `Total TTC: ${totalTtc.toFixed(2)}€\n`;
                receiptText += `\n=== PAIEMENT ACCEPTÉ ===`;
                
                receiptElement.textContent = receiptText;
                receiptElement.style.display = 'block';
                
                // Réinitialiser le panier
                cart = [];
                updateCartDisplay();
                
                showNotification("Paiement effectué avec succès");
            }
            
            // Fonction pour annuler la transaction
            function cancelTransaction() {
                if (cart.length === 0) {
                    showNotification("Aucune transaction en cours", "warning");
                    return;
                }
                
                if (confirm("Voulez-vous annuler la transaction en cours ?")) {
                    cart = [];
                    updateCartDisplay();
                    receiptElement.style.display = 'none';
                    showNotification("Transaction annulée", "warning");
                }
            }
            
            // Fonction pour afficher une notification
            function showNotification(message, type = "success") {
                notificationElement.textContent = message;
                notificationElement.style.backgroundColor = type === "error" ? "#e74c3c" : 
                                                          type === "warning" ? "#f39c12" : "#2ecc71";
                notificationElement.style.display = 'block';
                
                setTimeout(() => {
                    notificationElement.style.display = 'none';
                }, 3000);
            }
        });
    </script>
</body>
</html>