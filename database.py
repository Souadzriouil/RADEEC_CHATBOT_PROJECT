import sqlite3
import os
from datetime import datetime
import random

# Supprimer l'ancienne base si elle existe
if os.path.exists('radeec.db'):
    os.remove('radeec.db')
    print("🗑️  Ancienne base supprimée\n")

# Créer la connexion
conn = sqlite3.connect('radeec.db')
cursor = conn.cursor()

print("="*80)
print("💧 CRÉATION BASE DE DONNÉES RADEEC - VERSION CORRIGÉE")
print("="*80)

# ========== TABLE 1: CLIENTS ==========
print("\n📋 Création table CLIENTS...")
cursor.execute('''
    CREATE TABLE clients (
        numero_compte TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        cin TEXT,
        adresse TEXT,
        telephone TEXT,
        email TEXT
    )
''')

clients = [
    ('123456', 'Benali', 'Ahmed', 'AB123456', 'Rue Mohammed V, Settat', '0612345678', 'ahmed@email.com'),
    ('654321', 'Alaoui', 'Fatima', 'FA654321', 'Avenue Hassan II, Settat', '0698765432', 'fatima@email.com'),
    ('789012', 'Idrissi', 'Youssef', 'YI789012', 'Boulevard Bir Anzarane, Settat', '0623456789', 'youssef@email.com')
]

cursor.executemany('INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?)', clients)
print("✅ 3 clients créés")

# ========== TABLE 2: FACTURES (PLUSIEURS MOIS) ==========
print("\n💰 Création table FACTURES...")
cursor.execute('''
    CREATE TABLE factures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_compte TEXT NOT NULL,
        numero_facture TEXT,
        montant REAL NOT NULL,
        date_facture DATE,
        etat TEXT,
        FOREIGN KEY (numero_compte) REFERENCES clients(numero_compte)
    )
''')

# Générer des factures pour les 6 derniers mois
factures = []
facture_counter = 1

for mois_num in range(6, 12):  # Juin (6) à Novembre (11)
    date = datetime(2024, mois_num, 1).strftime('%Y-%m-%d')
    
    for compte in ['123456', '654321', '789012']:
        montant = round(random.uniform(150, 350), 2)
        
        # Anciens mois payés, derniers mois mixtes
        if mois_num < 10:
            etat = 'Payée'
        else:
            etat = random.choice(['Payée', 'Non payée'])
        
        numero_facture = f'FAC-2024-{facture_counter:03d}'
        factures.append((compte, numero_facture, montant, date, etat))
        facture_counter += 1

cursor.executemany('INSERT INTO factures (numero_compte, numero_facture, montant, date_facture, etat) VALUES (?, ?, ?, ?, ?)', factures)
print(f"✅ {len(factures)} factures créées (6 mois)")

# ========== TABLE 3: CONSOMMATIONS (PLUSIEURS MOIS) ==========
print("\n💧 Création table CONSOMMATIONS...")
cursor.execute('''
    CREATE TABLE consommations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_compte TEXT NOT NULL,
        consommation_m3 REAL NOT NULL,
        date_releve DATE,
        mois TEXT,
        FOREIGN KEY (numero_compte) REFERENCES clients(numero_compte)
    )
''')

# Noms de mois EXACTEMENT comme ils seront recherchés
mois_noms = ['Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre']
consommations = []

for i, mois_nom in enumerate(mois_noms):
    # Date de relevé (5ème jour du mois)
    mois_num = 6 + i  # Juin = 6, Juillet = 7, etc.
    date = datetime(2024, mois_num, 5).strftime('%Y-%m-%d')
    
    for compte in ['123456', '654321', '789012']:
        # Consommations variables mais réalistes
        consommation = round(random.uniform(10, 25), 1)
        
        consommations.append((compte, consommation, date, mois_nom))

cursor.executemany('INSERT INTO consommations (numero_compte, consommation_m3, date_releve, mois) VALUES (?, ?, ?, ?)', consommations)
print(f"✅ {len(consommations)} consommations créées (6 mois)")

# Sauvegarder
conn.commit()

print("\n" + "="*80)
print("📊 VÉRIFICATION DES DONNÉES")
print("="*80)

# Vérifier les consommations avec détails
print("\n💧 VÉRIFICATION TABLE CONSOMMATIONS:")
print("-"*80)
cursor.execute("SELECT * FROM consommations ORDER BY date_releve")
all_consommations = cursor.fetchall()
print(f"Total enregistrements: {len(all_consommations)}")
print("\nPremiers enregistrements:")
for row in all_consommations[:6]:
    print(f"  ID: {row[0]} | Compte: {row[1]} | Conso: {row[2]} m³ | Date: {row[3]} | Mois: '{row[4]}'")

# Afficher les mois distincts pour vérifier
print("\n📅 MOIS DISTINCTS DANS LA BASE:")
cursor.execute("SELECT DISTINCT mois FROM consommations ORDER BY date_releve")
mois_distincts = cursor.fetchall()
for mois in mois_distincts:
    print(f"  • '{mois[0]}'")

# Test de requête
print("\n🔍 TEST DE RECHERCHE:")
print("-"*80)
test_compte = '123456'
test_mois = 'novembre'
print(f"Recherche: Compte {test_compte}, Mois '{test_mois}'")

cursor.execute("""
    SELECT consommation_m3, date_releve, mois 
    FROM consommations 
    WHERE numero_compte=? AND LOWER(mois)=?
    ORDER BY date_releve DESC
    LIMIT 1
""", (test_compte, test_mois.lower()))

result = cursor.fetchone()
if result:
    print(f"✅ Trouvé: {result[0]} m³ pour {result[2]} (date: {result[1]})")
else:
    print("❌ Non trouvé")

# Afficher aperçu des factures
print("\n💰 APERÇU FACTURES PAR COMPTE:")
print("-"*80)
for compte in ['123456', '654321', '789012']:
    cursor.execute("""
        SELECT COUNT(*), SUM(montant) 
        FROM factures 
        WHERE numero_compte=?
    """, (compte,))
    count, total = cursor.fetchone()
    print(f"  Compte {compte}: {count} factures, Total: {total:.2f} MAD")

# Statistiques finales
print("\n" + "="*80)
print("📈 STATISTIQUES FINALES")
print("="*80)

cursor.execute("SELECT COUNT(*) FROM clients")
print(f"  • Clients: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM factures")
print(f"  • Factures: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM consommations")
print(f"  • Consommations: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM factures WHERE etat='Non payée'")
print(f"  • Factures impayées: {cursor.fetchone()[0]}")

cursor.execute("SELECT AVG(montant) FROM factures")
print(f"  • Montant moyen facture: {cursor.fetchone()[0]:.2f} MAD")

cursor.execute("SELECT AVG(consommation_m3) FROM consommations")
print(f"  • Consommation moyenne: {cursor.fetchone()[0]:.2f} m³")

conn.close()

print("\n" + "="*80)
print("✅ BASE DE DONNÉES CRÉÉE ET VÉRIFIÉE AVEC SUCCÈS!")
print("📁 Fichier: radeec.db")
print("="*80)

print("\n💡 INFORMATIONS IMPORTANTES:")
print("  • Comptes de test: 123456, 654321, 789012")
print("  • Période: Juin à Novembre 2024")
print("  • Mois disponibles: Juin, Juillet, Août, Septembre, Octobre, Novembre")
print("  • Format des mois: Première lettre en majuscule")
print("="*80)