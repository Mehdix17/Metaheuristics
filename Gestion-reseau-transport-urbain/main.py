import oracledb
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["smartcity"]

USERNAME = "SYSTEM"
PASSWORD = "1953"
DSN = "localhost/XEPDB1"

MENU = """                  
                             ____________________________________________________________________________________________
                            |                                                                                            |
                            |                               Partie I : Relationnel-Objet                                 |
                            | ___________________________________________________________________________________________|
                            |                                                                                            |
                            | 1) Lister tous les voyages ayant enregistré un quelconque problème                         |
                            |                                                                                            |
                            | 2) Lister toutes les lignes comportant une station principale                              |
                            |                                                                                            |
                            | 3) Lister les navettes ayant effectué le maximum de voyages durant le mois de janvier 2025 |
                            |                                                                                            |
                            | 4) Lister les stations offrant au moins 2 moyens de transport                              |
                            |____________________________________________________________________________________________|
                             ____________________________________________________________________________________________
                            |                                                                                            |
                            |                    Partie II :  NoSQL - Modèle orienté « documents »                       |
                            | ___________________________________________________________________________________________|
                            |                                                                                            |
                            | 5) Afficher tous les voyages effectués en date du 01-01-2025                               |
                            |                                                                                            |
                            | 6) Récupérer tous les voyages n'ayant enregistré aucun problème                            |
                            |                                                                                            |
                            | 7) Récupérer  les numéros de lignes et le nombre total de voyages effectués                |
                            |                                                                                            |
                            | 8) Augmenter de 100, le nombre de voyageurs sur tous les voyages effectués par métro       |
                            |    avant la date du 15 janvier 2025                                                        |  
                            |                                                                                            |
                            | 9) Récupérer les numéros de lignes et le nombre total de voyages effectués avec Map-Reduce |
                            |                                                                                            |
                            | 10) Quitter                                                                                |
                            |____________________________________________________________________________________________|
"""

REQUESTS = {

    "1": """
            SELECT
                v.numV AS "Numéro de Voyage",
                v.dateV AS "Date",
                DEREF(DEREF(v.ligne).moyenTransport).codeMT AS "Moyen de Transport",
                DEREF(v.navette).numN AS "Navette"
            FROM
                Voyage v
            WHERE
                v.observation != 'RAS'
        """,
    "2": """
            SELECT
                l.codeLigne AS "Ligne",
                DEREF(l.stationDepart).codeStat AS "Station Départ",
                DEREF(l.stationArrivee).codeStat AS "Station Fin"
            FROM
                Ligne l
            WHERE
                DEREF(l.stationDepart).type = 'principale'
                OR DEREF(l.stationArrivee).type = 'principale'
        """,

    "3":  """
            SELECT
                DEREF(v.navette).numN AS "Navette",
                DEREF(DEREF(v.ligne).moyenTransport).codeMT AS "Type Transport",
                DEREF(v.navette).annee AS "Année Mise en Service",
                COUNT(v.numV) AS "Nombre de Voyages"
            FROM
                Voyage v
            WHERE
                v.dateV BETWEEN TO_DATE('2025-01-01', 'YYYY-MM-DD') AND TO_DATE('2025-01-31', 'YYYY-MM-DD')
            GROUP BY
                DEREF(v.navette).numN, DEREF(DEREF(v.ligne).moyenTransport).codeMT, DEREF(v.navette).annee
            HAVING
                COUNT(v.numV) = (
                    SELECT MAX(cnt)
                    FROM (
                        SELECT COUNT(*) AS cnt
                        FROM Voyage v2
                        WHERE v2.dateV BETWEEN TO_DATE('2025-01-01', 'YYYY-MM-DD') AND TO_DATE('2025-01-31', 'YYYY-MM-DD')
                        GROUP BY v2.navette
                        )
                )
        """,
    
    "4":  """
        SELECT  
            S.codeStat AS "Station",  
            S.NomStat AS "Nom Station",  
            LISTAGG(DEREF(L.MoyenTransport).codeMT, ', ') WITHIN GROUP (ORDER BY DEREF(L.MoyenTransport).codeMT) AS "Moyens de Transport"  
        FROM  
            Ligne L  
            JOIN Station S ON DEREF(L.StationDepart).codeStat = S.codeStat  
                        OR DEREF(L.StationArrivee).codeStat = S.codeStat  
        GROUP BY  
            S.codeStat, S.NomStat  
        HAVING  
            COUNT(DISTINCT DEREF(L.MoyenTransport).codeMT) >= 2
        """
}

# Fonction pour exécuter une requête
def execute_sql_querry(cursor, request):
    try:
        cursor.execute(request)
        colonnes = [col[0] for col in cursor.description]
        lignes = cursor.fetchall()

        if not lignes:
            print("\nAucun résultat trouvé.")
            return

        # Calcul de la largeur maximale pour chaque colonne
        col_widths = []
        for i, col in enumerate(colonnes):
            max_len = len(col)
            for row in lignes:
                max_len = max(max_len, len(str(row[i])))
            col_widths.append(max_len + 2)

        # Affichage des entêtes
        print("\nRésultats :")
        print("-" * sum(col_widths))
        for i, col in enumerate(colonnes):
            print(col.ljust(col_widths[i]), end="")
        print()
        print("-" * sum(col_widths))

        # Affichage des lignes
        for row in lignes:
            for i, val in enumerate(row):
                print(str(val).ljust(col_widths[i]), end="")
            print()
        print("-" * sum(col_widths))

    except oracledb.DatabaseError as e:
        err, = e.args
        print(f"\nErreur lors de l'exécution de la requête : {err.message}")

def execute_mongo_querry(choix):

    if choix == "5":
        results = db.voyages.find({"date": datetime(2025, 1, 1)})
        print_results(results)

    elif choix == "6":
        pipeline = [
            {"$match": {"observation": {"$in": [None, "", "RAS"]}}},
            {"$project": {
                "_id": 0,
                "numero": 1,
                "numLigne": 1,
                "date": 1,
                "heure": 1,
                "sens": 1,
                "moyenTransport": 1,
                "numNavette": 1
            }},
            {"$out": "BON-Voyage"}
        ]
        db.voyages.aggregate(pipeline)
        print("\n✅ Collection BON-Voyage créée avec succès.")

    elif choix == "7":
        pipeline = [
            {"$group": {"_id": "$numLigne", "totalVoyages": {"$sum": 1}}},
            {"$sort": {"totalVoyages": -1}},
            {"$project": {"_id": 0, "numLigne": "$_id", "totalVoyages": 1}},
            {"$out": "Ligne-Voyages"}
        ]
        db.voyages.aggregate(pipeline)
        print("\n✅ Collection Ligne-Voyages créée avec succès.")

    elif choix == "8":
        result = db.voyages.update_many(
            {"moyenTransport": "métro", "date": {"$lt": datetime(2025, 1, 15)}},
            {"$inc": {"nbVoyageurs": 100}}
        )
        print(f"\n✅ {result.modified_count} documents mis à jour.")

    elif choix == "9":
        pipeline = [
            {
                "$group": {
                    "_id": "$numLigne",
                    "totalVoyages": { "$sum": 1 }
                }
            },
            {
                "$out": "Ligne-Voyages-MapReduce"
            }
        ]
        db.voyages.aggregate(pipeline)
        print("✅ Ligne-Voyages-MapReduce créée via aggregate.")

def print_results(cursor):
    results = list(cursor)
    if not results:
        print("\nAucun résultat trouvé.")
        return
    for doc in results:
        print(dumps(doc, indent=2, ensure_ascii=False))

# Fonction pour afficher le menu
def menu():
    conn = oracledb.connect(user=USERNAME, password=PASSWORD, dsn=DSN)
    cursor = conn.cursor()

    while True:
        print(MENU)
        choix = input("\nEntrer le numéro de la requête : ").strip()
        if choix == "10":
            print("Fin du programme.")
            break
        if choix in ("1", "2", "3", "4"): # SQL Request
            execute_sql_querry(cursor, REQUESTS[choix])
        elif choix in ("5", "6", "7", "8", "9"): # MongoDB Request
            execute_mongo_querry(choix)
        else:
            print("\nOption invalide ❌")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    menu()
