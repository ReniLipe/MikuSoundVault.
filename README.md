# 🎵 MikuSoundVault - Music Store & Management System

**Studente:** [RENATO LIPEROTI]  
**Matricola:** [1734900]  
**Tipologia di Progetto:** Full-Stack Web Application  
**Framework used:** Django

MikuSoundVault è una piattaforma e-commerce e gestionale dedicata alla vendita di strumenti musicali e accessori. Il progetto combina un'estetica moderna ispirata a Hatsune Miku con una logica di gestione magazzino e ordini professionale, rispettando tutti i requisiti ministeriali richiesti (database relazionale SQLite incluso, Class-Based Views, ruoli utente e Access Control).

## 🚀 Obiettivi del Progetto
- Fornire un'interfaccia intuitiva per l'acquisto di strumenti musicali.
- Implementare un sistema di gestione ordini (gestionale) per l'amministratore.
- Gestire in tempo reale lo stock del magazzino.

## 🌍 Link al Deployment
Il progetto è live e completamente testabile al seguente indirizzo:
👉 **[SOSTITUISCI-QUESTO-TESTO-CON-IL-TUO-LINK-DI-PYTHONANYWHERE]**

---

## 🔐 Ruoli Utente e Credenziali (Demo per Valutazione)
Il database (`db.sqlite3`) pre-popolato è incluso nel repository per facilitare la correzione. Sono pronti all'uso due account di test con ruoli differenti:

### 1. Account Store Manager (Admin / Gestionale)
Permette l'accesso esclusivo al gestionale (Access Control tramite `ManagerRequiredMixin`) per il CRUD dell'inventario e l'aggiornamento dello stato delle spedizioni.
- **Username:** `admin_demo`
- **Password:** `admin12345`

### 2. Account Cliente (Store)
Permette la navigazione, l'aggiunta al carrello, il checkout e la visualizzazione in sola lettura del proprio storico ordini.
- **Username:** `user_demo`
- **Password:** `user12345`

---

## ✨ Caratteristiche Tecniche e Principali
- **Catalogo Dinamico**: Suddivisione in categorie con filtri e design responsive ottimizzato (Bootstrap 5).
- **Gestione Ruoli (Access Control):** Sistema di permessi che blinda le viste CRUD lato backend e modifica dinamicamente la navbar lato frontend a seconda del ruolo (`manager` o `customer`).
- **Class-Based Views (CBVs):** Utilizzate estensivamente per le operazioni CRUD dell'inventario e per l'aggiornamento del profilo utente.
- **Transazioni Sicure e Auto-Stock:** Checkout protetto da `@transaction.atomic` che verifica la disponibilità in magazzino e riduce automaticamente le quantità al momento dell'acquisto.
- **UI/UX Differenziata:** Il manager interagisce con form e badge operativi per cambiare lo stato degli ordini, mentre il cliente visualizza un log storico.

---

## 🛠 Installazione e Esecuzione Locale

### 1. Clonazione e Setup Ambiente
``` bash 
git clone <tuo-link-github>
cd <nome-cartella-progetto>
python -m venv venv
```


### 2. Attivazione Ambiente Virtuale
Su Windows: `venv\Scripts\activate`

Su macOS / Linux: `source venv/bin/activate`

### 3. Installazione Dipendenze
``` bash 
pip install -r requirements.txt
```

### 4. Database e Dati Iniziali
Il progetto include già un file db.sqlite3 con dati precaricati. Se si desidera resettarlo completamente e ripopolarlo da zero:
``` bash 
python manage.py migrate
python manage.py populate_store
```

### 5. Esecuzione
``` bash 
python manage.py runserver
```
Il sito sarà disponibile su http://127.0.0.1:8000.

---

## 🧪 Testing Workflow
È possibile testare le funzionalità principali tramite lo script di test incluso:
``` bash 
python test_workflow.py
```
Oppure manualmente seguendo questo flusso operativo:

1 Effettuare il login come user_demo (Cliente).

2 Navigare nel catalogo `(/store/)` e aggiungere un prodotto al carrello.

3 Effettuare il checkout e verificare l'ordine in "I Miei Ordini" (verificare la riduzione dello stock in `/product/<slug>/`).

4 Fare il logout ed effettuare l'accesso come `admin_demo` (Manager).

5 Aprire il "Gestionale Ordini" (`/admin-orders/`) e aggiornare lo stato dell'ordine.

--- 

## 📂 Struttura del Codice
`store/`: Gestione catalogo, carrello, logica degli ordini e CRUD magazzino.

`users/`: Gestione profili personalizzati e autenticazione.

`musicstore/`: Configurazioni di sistema centrali e settings.

`templates/`: File HTML globali e componenti UI.