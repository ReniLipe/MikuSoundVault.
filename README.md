# 🎵 MikuSoundVault - Music Store & Management System

MikuSoundVault è una piattaforma e-commerce e gestionale dedicata alla vendita di strumenti musicali e accessori. Il progetto combina un'estetica moderna ispirata a Hatsune Miku con una logica di gestione magazzino e ordini professionale.

## 🚀 Obiettivi del Progetto
- Fornire un'interfaccia intuitiva per l'acquisto di strumenti musicali.
- Implementare un sistema di gestione ordini (gestionale) per l'amministratore.
- Gestire in tempo reale lo stock del magazzino.

## ✨ Caratteristiche Principali
- **Catalogo Dinamico**: Suddivisione in categorie (Chitarre, Tastiere, ecc.) con filtri.
- **Sistema Carrello**: Aggiunta, rimozione e riepilogo costi.
- **Gestionale Admin**: Visualizzazione ordini, dettaglio articoli e aggiornamento stato.
- **Inventario Magazzino**: Monitoraggio in tempo reale delle scorte con avvisi visivi per stock basso.
- **Auto-Stock**: Riduzione automatica delle quantità in magazzino al momento del checkout.
- **Design Responsive**: Ottimizzato per desktop e mobile con Bootstrap 5.

## 🛠 Installazione e Esecuzione Locale

### 1. Clonazione e Setup Ambiente
```bash
git clone <tuo-link-github>
cd PyCharmMiscProject
python -m venv .venv
source .venv/Scripts/activate  # Su Windows: .venv\Scripts\activate
```

### 2. Installazione Dipendenze
```bash
pip install -r requirements.txt
```

### 3. Database e Dati Iniziali
Il progetto include già un file `db.sqlite3` con dati precaricati. Se vuoi resettarlo:
```bash
python manage.py migrate
python manage.py populate_store
```

### 4. Esecuzione
```bash
python manage.py runserver
```
Il sito sarà disponibile su `http://127.0.0.1:8000`.

## 👥 Ruoli Utente e Account Demo
- **Admin (Gestionale)**:
  - Username: `admin`
  - Password: `password123` (o quella impostata)
  - Permessi: Accesso a `/admin-orders/` e gestione magazzino.
- **Cliente (Store)**:
  - Può registrarsi, navigare e acquistare.

## 🌐 Deployment
Il sito è raggiungibile online al seguente indirizzo:
**[LINK-AL-TUO-DEPLOYMENT]** (es. su PythonAnywhere o Render)

## 🧪 Testing Workflow
È possibile testare le funzionalità principali tramite lo script di test incluso:
```bash
python test_workflow.py
```
Oppure manualmente:
1. Navigare su `/store/`.
2. Aggiungere un prodotto al carrello.
3. Effettuare il checkout (verificare la riduzione dello stock in `/product/<slug>/`).

## 📂 Struttura del Codice
- `store/`: Gestione catalogo, carrello e ordini.
- `users/`: Gestione profili e autenticazione.
- `musicstore/`: Configurazioni di sistema e settings.
- `templates/`: File HTML globali e componenti UI.
