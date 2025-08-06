SET LINESIZE 150
SET WRAP OFF

-- Supprimer les corps des types
DROP TYPE BODY t_voyage;
DROP TYPE BODY t_troncon;
DROP TYPE BODY t_moyenTransport;
DROP TYPE BODY t_ligne;
DROP TYPE BODY t_station;
DROP TYPE BODY t_navette;

-- Supprimer les tables
DROP TABLE Voyage CASCADE CONSTRAINTS;
DROP TABLE Troncon CASCADE CONSTRAINTS;
DROP TABLE Ligne CASCADE CONSTRAINTS;
DROP TABLE Navette CASCADE CONSTRAINTS;
DROP TABLE Station CASCADE CONSTRAINTS;
DROP TABLE MoyenTransport CASCADE CONSTRAINTS;

-- Supprimer les Nested Tables
DROP TYPE tset_ref_voyage FORCE;
DROP TYPE tset_ref_troncon FORCE;
DROP TYPE tset_ref_moyenTransport FORCE;
DROP TYPE tset_ref_ligne FORCE;
DROP TYPE tset_ref_station FORCE;
DROP TYPE tset_ref_navette FORCE;

-- Supprimer les types
DROP TYPE t_voyage FORCE;
DROP TYPE t_troncon FORCE;
DROP TYPE t_moyenTransport FORCE;
DROP TYPE t_ligne FORCE;
DROP TYPE t_station FORCE;
DROP TYPE t_navette FORCE;

-- Supprimer les tuples
DELETE FROM Voyage;
DELETE FROM Troncon;
DELETE FROM Ligne;
DELETE FROM Navette;
DELETE FROM Station;
DELETE FROM MoyenTransport;

-- --------------------------------------- Définition des Types d'Objets ---------------------------------------

CREATE TYPE t_moyenTransport ;
/
CREATE TYPE tset_ref_moyenTransport AS TABLE OF REF t_moyenTransport ;
/

CREATE TYPE t_station ;
/
CREATE TYPE tset_ref_station AS TABLE OF REF t_station ;
/

CREATE TYPE t_troncon ;
/
CREATE TYPE tset_ref_troncon AS TABLE OF REF t_troncon ;
/

CREATE TYPE t_navette ;
/
CREATE TYPE tset_ref_navette AS TABLE OF REF t_navette ;
/

CREATE TYPE t_ligne ;
/
CREATE TYPE tset_ref_ligne AS TABLE OF REF t_ligne ;
/

CREATE TYPE t_voyage ;
/
CREATE TYPE tset_ref_voyage AS TABLE OF REF t_voyage ;
/

-- Type MoyenTransport
CREATE OR REPLACE TYPE t_moyenTransport AS OBJECT (
    codeMT VARCHAR2(20), -- "MET", "TRA", "BUS", "TRN"
    ouverture TIMESTAMP,
    fermeture TIMESTAMP,
    nbVoyageurMoy NUMBER,
    lignes tset_ref_ligne,
    stations tset_ref_station,
    MEMBER FUNCTION getNbVoyagesTransport(dateVoyage DATE) RETURN NUMBER,
    MEMBER FUNCTION getNbVoyageursTransport(dateVoyage DATE) RETURN NUMBER
);
/

-- Type Station
CREATE OR REPLACE TYPE t_station AS OBJECT (
    codeStat VARCHAR2(15),
    nomStat VARCHAR2(30),
    longitude FLOAT,
    latitude FLOAT,
    type VARCHAR2(10), -- "principale" ou "secondaire"
    ligneDepart REF t_ligne,
    ligneArrivee REF t_ligne,
    moyenTransports tset_ref_moyenTransport,
    tronconDebut tset_ref_troncon,
    tronconFin tset_ref_troncon,
    MEMBER PROCEDURE changerNom(ancienNom VARCHAR2, nouveauNom VARCHAR2),
    MEMBER FUNCTION estPrincipale RETURN BOOLEAN
);
/

-- Type Ligne
CREATE OR REPLACE TYPE t_ligne AS OBJECT (
    codeLigne VARCHAR2(5),
    stationDepart REF t_station,
    stationArrivee REF t_station,
    moyenTransport REF t_moyenTransport,
    troncons tset_ref_troncon,
    voyages tset_ref_voyage,
    MEMBER FUNCTION getNavettes RETURN tset_ref_navette,
    MEMBER FUNCTION getNbVoyages(dateDebut DATE, dateFin DATE) RETURN NUMBER
);
/

-- Type Troncon
CREATE OR REPLACE TYPE t_troncon AS OBJECT (
    numT VARCHAR2(8),
    ligne REF t_ligne,
    stationDepart REF t_station,
    stationArrivee REF t_station,
    longueur FLOAT,
    MEMBER FUNCTION calculerDuree RETURN FLOAT
);
/

-- Type Navette
CREATE OR REPLACE TYPE t_navette AS OBJECT (
    numN VARCHAR2(8),
    marque VARCHAR2(15),
    annee NUMBER,
    voyages tset_ref_voyage,
    MEMBER FUNCTION getVoyages RETURN INTEGER
);
/

-- Type Voyage
CREATE OR REPLACE TYPE t_voyage AS OBJECT (
    numV VARCHAR2(6),
    duree FLOAT,
    dateV DATE,
    heureDebut TIMESTAMP,
    sens VARCHAR(6), -- "Aller" ou "Retour"
    nbVoyageurs NUMBER,
    observation VARCHAR2(11), -- "RAS" ou "Panne" ou "Retard"
    navette REF t_navette,
    ligne REF t_ligne,
    MEMBER FUNCTION estSansProbleme RETURN BOOLEAN
);
/

-- --------------------------------------- Création des Tables d'Objet ---------------------------------------

-- Table d'objets pour MoyenTransport
CREATE TABLE MoyenTransport OF t_moyenTransport (
    PRIMARY KEY (codeMT),
    CONSTRAINT chk_codeMT CHECK (codeMT IN ('MET', 'TRA', 'BUS', 'TRN')),
    CONSTRAINT chk_horaires CHECK (ouverture < fermeture))
    NESTED TABLE lignes STORE AS table_lignes_MT,
    NESTED TABLE stations STORE AS table_stations_MT;

-- Table d'objets pour Station
CREATE TABLE Station OF t_station (
    PRIMARY KEY (codeStat),
    CONSTRAINT chk_type CHECK (type IN ('principale', 'secondaire')))
    NESTED TABLE moyenTransports STORE AS table_station_MT,
    NESTED TABLE tronconDebut STORE AS table_stations_tronconDebut,
    NESTED TABLE tronconFin STORE AS table_stations_tronconFin;

-- Table d'objets pour Ligne
CREATE TABLE Ligne OF t_ligne (
    PRIMARY KEY (codeLigne),
    FOREIGN KEY (stationDepart) REFERENCES Station,
    FOREIGN KEY (stationArrivee) REFERENCES Station,
    FOREIGN KEY (moyenTransport) REFERENCES MoyenTransport,
    CONSTRAINT chk_stations2 CHECK (stationDepart != stationArrivee))
    NESTED TABLE troncons STORE AS table_ligne_troncons,
    NESTED TABLE voyages STORE AS table_ligne_voyages;

-- Table d'objets pour Troncon
CREATE TABLE Troncon OF t_troncon (
    PRIMARY KEY (numT),
    FOREIGN KEY (stationDepart) REFERENCES Station,
    FOREIGN KEY (stationArrivee) REFERENCES Station,
    CONSTRAINT chk_stations1 CHECK (stationDepart != stationArrivee),
    CONSTRAINT chk_longueur CHECK (longueur > 0)
);

-- Table d'objets pour Navette
CREATE TABLE Navette OF t_navette (PRIMARY KEY (numN))
NESTED TABLE voyages STORE AS table_navette_voyages;

-- Table d'objets pour Voyage
CREATE TABLE Voyage OF t_voyage (
    PRIMARY KEY (numV),
    FOREIGN KEY (navette) REFERENCES Navette,
    FOREIGN KEY (ligne) REFERENCES Ligne,
    CONSTRAINT chk_sens CHECK (sens IN ('Aller', 'Retour')),
    CONSTRAINT chk_observation CHECK (observation IN ('RAS', 'Panne', 'Retard', 'Accident'))
);

-- --------------------------------------- Implémentation des Méthodes ---------------------------------------

-- Méthode getVoyages() de t_navette
CREATE OR REPLACE TYPE BODY t_navette AS
  MEMBER FUNCTION getVoyages RETURN INTEGER IS
  BEGIN
    RETURN CARDINALITY(self.voyages);
  END;
END;
/

-- Méthodes de t_ligne

    -- Méthode getNavettes()
    CREATE OR REPLACE TYPE BODY t_ligne AS
    MEMBER FUNCTION getNavettes RETURN tset_ref_navette IS
        listeNavettes tset_ref_navette := tset_ref_navette();
    BEGIN
        SELECT CAST(COLLECT(DISTINCT v.navette) AS tset_ref_navette)
        INTO listeNavettes
        FROM Voyage v
        WHERE DEREF(v.ligne) = REF(self);

        RETURN listeNavettes;
    END;

    -- Méthode getNbVoyages()
    MEMBER FUNCTION getNbVoyages(dateDebut DATE, dateFin DATE) RETURN NUMBER IS
        nb NUMBER;
    BEGIN
        SELECT COUNT(*)
        INTO nb
        FROM Voyage v
        WHERE DEREF(v.ligne) = REF(self)
        AND v.dateV BETWEEN dateDebut AND dateFin;

        RETURN nb;
    END;
END;
/

-- Méthodes de t_station
CREATE OR REPLACE TYPE BODY t_station AS

    -- Méthode changerNom()
    MEMBER PROCEDURE changerNom(ancienNom VARCHAR2, nouveauNom VARCHAR2) IS
    BEGIN
        -- Si le nom courant correspond à l'ancien nom demandé
        IF self.nomStat = ancienNom THEN
        self.nomStat := nouveauNom;
        END IF;

        -- Met à jour aussi les noms dans les lignes où la station est pointée
        UPDATE Ligne l
        SET l.stationDepart.nomStat = nouveauNom
        WHERE DEREF(l.stationDepart).codeStat = self.codeStat
        AND DEREF(l.stationDepart).nomStat = ancienNom;

        UPDATE Ligne l
        SET l.stationArrivee.nomStat = nouveauNom
        WHERE DEREF(l.stationArrivee).codeStat = self.codeStat
        AND DEREF(l.stationArrivee).nomStat = ancienNom;

        -- Met à jour les tronçons
        UPDATE Troncon t
        SET t.stationDepart.nomStat = nouveauNom
        WHERE DEREF(t.stationDepart).codeStat = self.codeStat
        AND DEREF(t.stationDepart).nomStat = ancienNom;

        UPDATE Troncon t
        SET t.stationArrivee.nomStat = nouveauNom
        WHERE DEREF(t.stationArrivee).codeStat = self.codeStat
        AND DEREF(t.stationArrivee).nomStat = ancienNom;
    END;

    -- Méthode estPrincipale()
    MEMBER FUNCTION estPrincipale RETURN BOOLEAN IS
    BEGIN
        RETURN (type = 'principale');
    END;
END;
/

-- Méthodes de t_moyenTransport
CREATE OR REPLACE TYPE BODY t_moyenTransport AS

    -- Méthode getNbVoyagesTransport()
    MEMBER FUNCTION getNbVoyagesTransport(dateVoyage DATE) RETURN NUMBER IS
        nb NUMBER;
    BEGIN
        SELECT COUNT(*)
        INTO nb
        FROM Voyage v
        WHERE v.dateV = dateVoyage
        AND DEREF(v.ligne.moyenTransport) = REF(self);

        RETURN nb;
    END;

    -- Méthode getNbVoyageursTransport()
    MEMBER FUNCTION getNbVoyageursTransport(dateVoyage DATE) RETURN NUMBER IS
        total NUMBER;
    BEGIN
        SELECT SUM(v.nbVoyageurs)
        INTO total
        FROM Voyage v
        WHERE v.dateV = dateVoyage
        AND DEREF(v.ligne.moyenTransport) = REF(self);

        RETURN NVL(total, 0);
    END;
END;
/

-- Méthode calculerDuree() de t_troncon
CREATE OR REPLACE TYPE BODY t_troncon AS

    MEMBER FUNCTION calculerDuree RETURN FLOAT IS
        vitesse FLOAT := 40;
        code VARCHAR2(20);
    BEGIN
        SELECT mt.codeMT
        INTO code
        FROM Ligne l, MoyenTransport mt
        WHERE REF(l) = self.ligne
        AND l.moyenTransport = REF(mt);

        -- Ajuster la vitesse selon le type
        IF    code = 'MET' THEN vitesse := 60;
        ELSIF code = 'TRN' THEN vitesse := 50;
        ELSIF code = 'TRA' THEN vitesse := 80;
        ELSIF code = 'BUS' THEN vitesse := 30;
        END IF;

        RETURN self.longueur / vitesse;
    END;

END;
/

-- Méthode estSansProbleme()
CREATE OR REPLACE TYPE BODY t_voyage AS
    MEMBER FUNCTION estSansProbleme RETURN BOOLEAN IS
    BEGIN
        RETURN (observation IS NULL OR observation = 'RAS');
    END;
END;
/

-- --------------------------------------- Remplissage des tables ---------------------------------------

-- Insértion des données dans la table MoyenTransport
INSERT INTO MoyenTransport VALUES ('MET', TO_TIMESTAMP('06:00', 'HH24:MI'), TO_TIMESTAMP('23:00', 'HH24:MI'), 5000, NULL, NULL);
INSERT INTO MoyenTransport VALUES ('TRN', TO_TIMESTAMP('07:00', 'HH24:MI'), TO_TIMESTAMP('21:00', 'HH24:MI'), 4000, NULL, NULL);
INSERT INTO MoyenTransport VALUES ('BUS', TO_TIMESTAMP('05:00', 'HH24:MI'), TO_TIMESTAMP('22:00', 'HH24:MI'), 3000, NULL, NULL);
INSERT INTO MoyenTransport VALUES ('TRA', TO_TIMESTAMP('06:30', 'HH24:MI'), TO_TIMESTAMP('22:30', 'HH24:MI'), 2500, NULL, NULL);

-- Insérer des données dans la table Station
INSERT INTO Station VALUES ('S001', 'Gare de Bab Ezzouar', 36.7529, 3.1596, 'principale', NULL, NULL, NULL, NULL, NULL);
INSERT INTO Station VALUES ('S002', 'Station de Ruisseaux', 36.7318, 3.2197, 'principale', NULL, NULL, NULL, NULL, NULL);
INSERT INTO Station VALUES ('S003', 'Station de Mohammadia', 36.7103, 3.2500, 'secondaire', NULL, NULL, NULL, NULL, NULL);
INSERT INTO Station VALUES ('S004', 'Station de Bordj El Kiffan', 36.7000, 3.2800, 'secondaire', NULL, NULL, NULL, NULL, NULL);
INSERT INTO Station VALUES ('S005', 'Gare Alger Centre', 36.7529, 3.0586, 'principale', NULL, NULL, NULL, NULL, NULL);
INSERT INTO Station VALUES ('S006', 'Station de Hussein Dey', 36.7667, 3.0833, 'secondaire', NULL, NULL, NULL, NULL, NULL);
INSERT INTO Station VALUES ('S007', 'Station de Kouba', 36.7417, 3.0333, 'secondaire', NULL, NULL, NULL, NULL, NULL);

-- Insértion des Données dans la Table Ligne

-- Lignes pour le Bus
INSERT INTO Ligne VALUES ('B001', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S001'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S002'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'BUS'), NULL, NULL);
INSERT INTO Ligne VALUES ('B002', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S002'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S003'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'BUS'), NULL, NULL);
INSERT INTO Ligne VALUES ('B003', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S003'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S004'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'BUS'), NULL, NULL);

-- Lignes pour le Métro
INSERT INTO Ligne VALUES ('M001', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S001'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S005'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'MET'), NULL, NULL);
INSERT INTO Ligne VALUES ('M002', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S005'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S006'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'MET'), NULL, NULL);
INSERT INTO Ligne VALUES ('M003', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S006'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S007'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'MET'), NULL, NULL);

-- Lignes pour le Tramway
INSERT INTO Ligne VALUES ('TR001', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S002'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S003'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'TRN'), NULL, NULL);
INSERT INTO Ligne VALUES ('TR002', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S003'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S004'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'TRN'), NULL, NULL);
INSERT INTO Ligne VALUES ('TR003', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S004'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S005'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'TRN'), NULL, NULL);

-- Lignes pour le Train
INSERT INTO Ligne VALUES ('TN001', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S001'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S006'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'TRA'), NULL, NULL);
INSERT INTO Ligne VALUES ('TN002', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S006'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S007'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'TRA'), NULL, NULL);
INSERT INTO Ligne VALUES ('TN003', (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S007'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S005'), (SELECT REF(m) FROM MoyenTransport m WHERE m.codeMT = 'TRA'), NULL, NULL);

-- Insértion des données dans la table Troncon
INSERT INTO Troncon VALUES ('T001', (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'B001'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S001'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S002'), 10.5);
INSERT INTO Troncon VALUES ('T002', (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'B002'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S002'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S003'), 15.0);
INSERT INTO Troncon VALUES ('T003', (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'B003'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S003'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S004'), 20.0);
INSERT INTO Troncon VALUES ('T004', (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'M001'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S004'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S005'), 25.0);
INSERT INTO Troncon VALUES ('T005', (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'M002'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S005'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S006'), 30.0);
INSERT INTO Troncon VALUES ('T006', (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TR001'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S006'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S007'), 35.0);
INSERT INTO Troncon VALUES ('T007', (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TR002'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S007'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S001'), 40.0);
INSERT INTO Troncon VALUES ('T008', (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TN001'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S001'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S005'), 45.0);
INSERT INTO Troncon VALUES ('T009', (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TN002'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S005'), (SELECT REF(s) FROM Station s WHERE s.codeStat = 'S006'), 50.0);

-- Insértion des données dans la table Navette
INSERT INTO Navette VALUES ('N001', 'Siemens', 2024, null);
INSERT INTO Navette VALUES ('N002', 'Bombardier', 2023, null);
INSERT INTO Navette VALUES ('N003', 'Mercedes-Benz', 2025, null);
INSERT INTO Navette VALUES ('N004', 'Yutong', 2023, null);
INSERT INTO Navette VALUES ('N005', 'Siemens', 2022, null);
INSERT INTO Navette VALUES ('N006', 'Hitachi', 2021, null);
INSERT INTO Navette VALUES ('N007', 'Alstom', 2019, null);
INSERT INTO Navette VALUES ('N008', 'Bombardier', 2020, null);

-- Insértion des données dans la table Voyage pour la période du 01-01-2025 au 01-03-2025
INSERT INTO Voyage VALUES ('V0001', 0.5, TO_DATE('2025-01-01', 'YYYY-MM-DD'), TO_TIMESTAMP('08:00', 'HH24:MI'), 'Aller',  50,   'RAS',      (SELECT REF(n) FROM Navette n WHERE n.numN = 'N003'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'B001'));
INSERT INTO Voyage VALUES ('V0002', 1.5, TO_DATE('2025-03-04', 'YYYY-MM-DD'), TO_TIMESTAMP('09:00', 'HH24:MI'), 'Retour', 800,  'Accident', (SELECT REF(n) FROM Navette n WHERE n.numN = 'N002'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'M001'));
INSERT INTO Voyage VALUES ('V0003', 1.5, TO_DATE('2025-01-02', 'YYYY-MM-DD'), TO_TIMESTAMP('10:00', 'HH24:MI'), 'Aller',  150,  'RAS',      (SELECT REF(n) FROM Navette n WHERE n.numN = 'N007'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TR001'));
INSERT INTO Voyage VALUES ('V0004', 1.0, TO_DATE('2025-01-12', 'YYYY-MM-DD'), TO_TIMESTAMP('11:00', 'HH24:MI'), 'Retour', 600,  'RAS',      (SELECT REF(n) FROM Navette n WHERE n.numN = 'N005'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TN001'));
INSERT INTO Voyage VALUES ('V0005', 2.0, TO_DATE('2025-01-03', 'YYYY-MM-DD'), TO_TIMESTAMP('12:00', 'HH24:MI'), 'Aller',  85,   'Panne',    (SELECT REF(n) FROM Navette n WHERE n.numN = 'N004'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'B002'));
INSERT INTO Voyage VALUES ('V0006', 0.5, TO_DATE('2025-02-17', 'YYYY-MM-DD'), TO_TIMESTAMP('13:00', 'HH24:MI'), 'Retour', 920,  'RAS',      (SELECT REF(n) FROM Navette n WHERE n.numN = 'N001'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'M002'));
INSERT INTO Voyage VALUES ('V0007', 1.5, TO_DATE('2025-01-14', 'YYYY-MM-DD'), TO_TIMESTAMP('14:00', 'HH24:MI'), 'Aller',  230,  'Retard',   (SELECT REF(n) FROM Navette n WHERE n.numN = 'N008'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TR002'));
INSERT INTO Voyage VALUES ('V0008', 0.7, TO_DATE('2025-03-04', 'YYYY-MM-DD'), TO_TIMESTAMP('15:00', 'HH24:MI'), 'Retour', 850,  'RAS',      (SELECT REF(n) FROM Navette n WHERE n.numN = 'N006'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TN002'));
INSERT INTO Voyage VALUES ('V0009', 2.5, TO_DATE('2025-01-25', 'YYYY-MM-DD'), TO_TIMESTAMP('16:00', 'HH24:MI'), 'Aller',  70,   'Panne',    (SELECT REF(n) FROM Navette n WHERE n.numN = 'N004'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'B003'));
INSERT INTO Voyage VALUES ('V0010', 1.0, TO_DATE('2025-03-05', 'YYYY-MM-DD'), TO_TIMESTAMP('17:00', 'HH24:MI'), 'Retour', 1050, 'RAS',      (SELECT REF(n) FROM Navette n WHERE n.numN = 'N001'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'M003'));
INSERT INTO Voyage VALUES ('V0011', 3.0, TO_DATE('2025-01-06', 'YYYY-MM-DD'), TO_TIMESTAMP('18:00', 'HH24:MI'), 'Aller',  180,  'Accident', (SELECT REF(n) FROM Navette n WHERE n.numN = 'N007'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TR003'));
INSERT INTO Voyage VALUES ('V0012', 1.5, TO_DATE('2025-01-06', 'YYYY-MM-DD'), TO_TIMESTAMP('19:00', 'HH24:MI'), 'Retour', 1000, 'Retard',   (SELECT REF(n) FROM Navette n WHERE n.numN = 'N005'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TN003'));
INSERT INTO Voyage VALUES ('V0013', 2.0, TO_DATE('2025-02-27', 'YYYY-MM-DD'), TO_TIMESTAMP('08:30', 'HH24:MI'), 'Aller',  90,   'RAS',      (SELECT REF(n) FROM Navette n WHERE n.numN = 'N002'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'B001'));
INSERT INTO Voyage VALUES ('V0014', 1.5, TO_DATE('2025-01-07', 'YYYY-MM-DD'), TO_TIMESTAMP('09:30', 'HH24:MI'), 'Retour', 250,  'Retard',   (SELECT REF(n) FROM Navette n WHERE n.numN = 'N003'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'M001'));
INSERT INTO Voyage VALUES ('V0015', 2.5, TO_DATE('2025-02-28', 'YYYY-MM-DD'), TO_TIMESTAMP('10:30', 'HH24:MI'), 'Aller',  300,  'RAS',      (SELECT REF(n) FROM Navette n WHERE n.numN = 'N004'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TR001'));
INSERT INTO Voyage VALUES ('V0016', 1.0, TO_DATE('2025-01-18', 'YYYY-MM-DD'), TO_TIMESTAMP('11:30', 'HH24:MI'), 'Retour', 350,  'Panne',    (SELECT REF(n) FROM Navette n WHERE n.numN = 'N005'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TN001'));
INSERT INTO Voyage VALUES ('V0017', 3.0, TO_DATE('2025-02-09', 'YYYY-MM-DD'), TO_TIMESTAMP('12:30', 'HH24:MI'), 'Aller',  40,   'RAS',      (SELECT REF(n) FROM Navette n WHERE n.numN = 'N006'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'B002'));
INSERT INTO Voyage VALUES ('V0018', 1.5, TO_DATE('2025-01-19', 'YYYY-MM-DD'), TO_TIMESTAMP('13:30', 'HH24:MI'), 'Retour', 850,  'Accident', (SELECT REF(n) FROM Navette n WHERE n.numN = 'N007'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'M002'));
INSERT INTO Voyage VALUES ('V0019', 2.0, TO_DATE('2025-01-10', 'YYYY-MM-DD'), TO_TIMESTAMP('14:30', 'HH24:MI'), 'Aller',  500,  'RAS',      (SELECT REF(n) FROM Navette n WHERE n.numN = 'N008'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TR002'));
INSERT INTO Voyage VALUES ('V0020', 1.0, TO_DATE('2025-03-08', 'YYYY-MM-DD'), TO_TIMESTAMP('15:30', 'HH24:MI'), 'Retour', 550,  'Retard',   (SELECT REF(n) FROM Navette n WHERE n.numN = 'N001'), (SELECT REF(l) FROM Ligne l WHERE l.codeLigne = 'TN002'));

-- Moyens de Transport → lignes et stations

UPDATE MoyenTransport m SET m.lignes = (SELECT CAST(COLLECT(REF(l)) AS tset_ref_ligne) FROM Ligne l WHERE l.moyenTransport = REF(m)) WHERE m.codeMT = 'MET';
UPDATE MoyenTransport m
SET m.stations = (
  SELECT CAST(COLLECT(DISTINCT s_ref) AS tset_ref_station)
  FROM (
    SELECT l.stationDepart AS s_ref FROM Ligne l WHERE l.moyenTransport = REF(m)
    UNION
    SELECT l.stationArrivee FROM Ligne l WHERE l.moyenTransport = REF(m)
  )
)
WHERE m.codeMT = 'MET';

UPDATE MoyenTransport m SET m.lignes = (SELECT CAST(COLLECT(REF(l)) AS tset_ref_ligne) FROM Ligne l WHERE l.moyenTransport = REF(m)) WHERE m.codeMT = 'TRN';
UPDATE MoyenTransport m
SET m.stations = (
  SELECT CAST(COLLECT(DISTINCT s_ref) AS tset_ref_station)
  FROM (
    SELECT l.stationDepart AS s_ref FROM Ligne l WHERE l.moyenTransport = REF(m)
    UNION
    SELECT l.stationArrivee FROM Ligne l WHERE l.moyenTransport = REF(m)
  )
)
WHERE m.codeMT = 'TRN';

UPDATE MoyenTransport m SET m.lignes = (SELECT CAST(COLLECT(REF(l)) AS tset_ref_ligne) FROM Ligne l WHERE l.moyenTransport = REF(m)) WHERE m.codeMT = 'BUS';
UPDATE MoyenTransport m
SET m.stations = (
  SELECT CAST(COLLECT(DISTINCT s_ref) AS tset_ref_station)
  FROM (
    SELECT l.stationDepart AS s_ref FROM Ligne l WHERE l.moyenTransport = REF(m)
    UNION
    SELECT l.stationArrivee FROM Ligne l WHERE l.moyenTransport = REF(m)
  )
)
WHERE m.codeMT = 'BUS';

UPDATE MoyenTransport m SET m.lignes = (SELECT CAST(COLLECT(REF(l)) AS tset_ref_ligne) FROM Ligne l WHERE l.moyenTransport = REF(m)) WHERE m.codeMT = 'TRA';
UPDATE MoyenTransport m
SET m.stations = (
  SELECT CAST(COLLECT(DISTINCT s_ref) AS tset_ref_station)
  FROM (
    SELECT l.stationDepart AS s_ref FROM Ligne l WHERE l.moyenTransport = REF(m)
    UNION
    SELECT l.stationArrivee FROM Ligne l WHERE l.moyenTransport = REF(m)
  )
)
WHERE m.codeMT = 'TRA';

-- Stations → tronçons (tronconDebut et tronconFin)

UPDATE Station s SET s.tronconDebut = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationDepart = REF(s))  WHERE s.codeStat = 'S001';
UPDATE Station s SET s.tronconFin   = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationArrivee = REF(s)) WHERE s.codeStat = 'S001';

UPDATE Station s SET s.tronconDebut = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationDepart = REF(s))  WHERE s.codeStat = 'S002';
UPDATE Station s SET s.tronconFin   = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationArrivee = REF(s)) WHERE s.codeStat = 'S002';

UPDATE Station s SET s.tronconDebut = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationDepart = REF(s))  WHERE s.codeStat = 'S003';
UPDATE Station s SET s.tronconFin   = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationArrivee = REF(s)) WHERE s.codeStat = 'S003';

UPDATE Station s SET s.tronconDebut = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationDepart = REF(s))  WHERE s.codeStat = 'S004';
UPDATE Station s SET s.tronconFin   = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationArrivee = REF(s)) WHERE s.codeStat = 'S004';

UPDATE Station s SET s.tronconDebut = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationDepart = REF(s))  WHERE s.codeStat = 'S005';
UPDATE Station s SET s.tronconFin   = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationArrivee = REF(s)) WHERE s.codeStat = 'S005';

UPDATE Station s SET s.tronconDebut = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationDepart = REF(s))  WHERE s.codeStat = 'S006';
UPDATE Station s SET s.tronconFin   = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationArrivee = REF(s)) WHERE s.codeStat = 'S006';

UPDATE Station s SET s.tronconDebut = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationDepart = REF(s))  WHERE s.codeStat = 'S007';
UPDATE Station s SET s.tronconFin   = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.stationArrivee = REF(s)) WHERE s.codeStat = 'S007';

-- Lignes → tronçons & voyages

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'B001';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'B001';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'B002';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'B002';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'B003';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'B003';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'M001';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'M001';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'M002';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'M002';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'M003';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'M003';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'TR001';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'TR001';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'TR002';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'TR002';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'TR003';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'TR003';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'TN001';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'TN001';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'TN002';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'TN002';

UPDATE Ligne l SET l.voyages  = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage)  FROM Voyage v  WHERE v.ligne = REF(l))  WHERE l.codeLigne = 'TN003';
UPDATE Ligne l SET l.troncons = (SELECT CAST(COLLECT(REF(t)) AS tset_ref_troncon) FROM Troncon t WHERE t.ligne = REF(l) ) WHERE l.codeLigne = 'TN003';

-- Navette → voyages
UPDATE Navette n SET n.voyages = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage) FROM Voyage v WHERE v.navette = REF(n) ) WHERE n.numN = 'N001'; 
UPDATE Navette n SET n.voyages = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage) FROM Voyage v WHERE v.navette = REF(n) ) WHERE n.numN = 'N002'; 
UPDATE Navette n SET n.voyages = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage) FROM Voyage v WHERE v.navette = REF(n) ) WHERE n.numN = 'N003'; 
UPDATE Navette n SET n.voyages = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage) FROM Voyage v WHERE v.navette = REF(n) ) WHERE n.numN = 'N004'; 
UPDATE Navette n SET n.voyages = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage) FROM Voyage v WHERE v.navette = REF(n) ) WHERE n.numN = 'N005'; 
UPDATE Navette n SET n.voyages = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage) FROM Voyage v WHERE v.navette = REF(n) ) WHERE n.numN = 'N006'; 
UPDATE Navette n SET n.voyages = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage) FROM Voyage v WHERE v.navette = REF(n) ) WHERE n.numN = 'N007'; 
UPDATE Navette n SET n.voyages = (SELECT CAST(COLLECT(REF(v)) AS tset_ref_voyage) FROM Voyage v WHERE v.navette = REF(n) ) WHERE n.numN = 'N008';

-- 10. Lister tous les voyages ayant enregistré un quelconque problème (panne, retard, accident, …) 
SELECT
    v.numV AS "Numéro de Voyage",
    v.dateV AS "Date",
    DEREF(DEREF(v.ligne).moyenTransport).codeMT AS "Moyen de Transport",
    DEREF(v.navette).numN AS "Navette"
FROM
    Voyage v
WHERE
    v.observation != 'RAS';

-- 11. Lister toutes les lignes (numéro, début et fin) comportant une station principale 
SELECT
    l.codeLigne AS "Ligne",
    DEREF(l.stationDepart).codeStat AS "Station Départ",
    DEREF(l.stationArrivee).codeStat AS "Station Fin"
FROM
    Ligne l
WHERE
    DEREF(l.stationDepart).type = 'principale'
    OR DEREF(l.stationArrivee).type = 'principale';

-- 12. Quelles sont les navettes ayant effectué le maximum de voyages durant le mois de janvier 2025 ? Préciser le nombre de voyages. 
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
    );

-- 13. Quelles sont les stations offrant au moins 2 moyens de transport ? (préciser la station et les moyens de transport offerts)
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
    COUNT(DISTINCT DEREF(L.MoyenTransport).codeMT) >= 2;  

commit;
/
