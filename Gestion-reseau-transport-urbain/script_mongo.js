// 1. Afficher tous les voyages effectués le 01-01-2025
db.voyages.find({
  date: new Date("2025-01-01"),
});

// 2. Collection BON-Voyage : voyages sans problème
db.voyages.aggregate([
  {
    $match: {
      observation: { $in: [null, "", "RAS"] },
    },
  },
  {
    $project: {
      _id: 0,
      numero: 1,
      numLigne: 1,
      date: 1,
      heure: 1,
      sens: 1,
      moyenTransport: 1,
      numNavette: 1,
    },
  },
  {
    $out: "BON-Voyage",
  },
]);

// 3. Collection Ligne-Voyages : nombre de voyages par ligne
db.voyages.aggregate([
  {
    $group: {
      _id: "$numLigne",
      totalVoyages: { $sum: 1 },
    },
  },
  {
    $sort: { totalVoyages: -1 },
  },
  {
    $project: {
      _id: 0,
      numLigne: "$_id",
      totalVoyages: 1,
    },
  },
  {
    $out: "Ligne-Voyages",
  },
]);

// 4. Augmenter de 100 le nombre de voyageurs pour les voyages par métro avant le 15-01-2025
db.voyages.updateMany(
  {
    moyenTransport: "métro",
    date: { $lt: new Date("2025-01-15") },
  },
  {
    $inc: { nbVoyageurs: 100 },
  }
);

// 5. Ligne-Voyages avec MapReduce
db.voyages.mapReduce(
  function () {
    emit(this.numLigne, 1);
  },
  function (key, values) {
    return Array.sum(values);
  },
  {
    out: "Ligne-Voyages-MapReduce",
  }
);

// 6a. Navettes ayant effectué le nombre max de voyages
// Étape 1 : calcul du nombre de voyages par navette
db.voyages.aggregate([
  {
    $group: {
      _id: { navette: "$numNavette", moyen: "$moyenTransport" },
      total: { $sum: 1 },
    },
  },
  {
    $sort: { total: -1 },
  },
  {
    $limit: 1,
  },
]);

// 6b. Moyens de transport dont le nombre de voyageurs dépasse toujours un seuil S par jour
// Exemple : S = 10000
db.voyages.aggregate([
  {
    $group: {
      _id: { date: "$date", moyen: "$moyenTransport" },
      totalVoyageurs: { $sum: "$nbVoyageurs" },
    },
  },
  {
    $match: { totalVoyageurs: { $lt: 10000 } },
  },
  {
    $group: {
      _id: "$_id.moyen",
    },
  },
]);

// Insertion dans BON-Voyage

db["BON-Voyage"].insertMany([
  {
    numero: "V0001",
    numLigne: "M001",
    date: new Date("2025-01-01"),
    heure: "08:00",
    sens: "aller",
    moyenTransport: "métro",
    numNavette: "N001",
  },
  {
    numero: "V0003",
    numLigne: "M001",
    date: new Date("2025-01-10"),
    heure: "10:00",
    sens: "aller",
    moyenTransport: "métro",
    numNavette: "N001",
  },
  {
    numero: "V0005",
    numLigne: "TR001",
    date: new Date("2025-01-15"),
    heure: "07:00",
    sens: "aller",
    moyenTransport: "tramway",
    numNavette: "N004",
  },
]);

// Insertion dans Ligne-Voyage

db["Ligne-Voyages"].insertMany([
  { numLigne: "M001", totalVoyages: 3 },
  { numLigne: "B001", totalVoyages: 1 },
  { numLigne: "TR001", totalVoyages: 1 },
]);

// Ligne-Voyages-MapReduce

db["Ligne-Voyages-MapReduce"].insertMany([
  { _id: "M001", value: 3 },
  { _id: "B001", value: 1 },
  { _id: "TR001", value: 1 },
]);

// Insertion dans Voyages

db.voyages.insertMany([
  {
    numero: "V0001",
    numLigne: "M001",
    date: new Date("2025-01-01"),
    heure: "08:00",
    sens: "aller",
    nbVoyageurs: 120,
    observation: "RAS",
    moyenTransport: "métro",
    numNavette: "N001",
    ligne: {
      code: "M001",
      stationDepart: "S001",
      stationArrivee: "S005",
    },
    navette: {
      numero: "N001",
      marque: "Alstom",
      annee: 2020,
    },
  },
  {
    numero: "V0002",
    numLigne: "B001",
    date: new Date("2025-01-01"),
    heure: "09:00",
    sens: "retour",
    nbVoyageurs: 95,
    observation: "Retard",
    moyenTransport: "bus",
    numNavette: "N002",
    ligne: {
      code: "B001",
      stationDepart: "S002",
      stationArrivee: "S004",
    },
    navette: {
      numero: "N002",
      marque: "Mercedes",
      annee: 2022,
    },
  },
  {
    numero: "V0003",
    numLigne: "M001",
    date: new Date("2025-01-10"),
    heure: "10:00",
    sens: "aller",
    nbVoyageurs: 150,
    observation: "RAS",
    moyenTransport: "métro",
    numNavette: "N001",
  },
  {
    numero: "V0004",
    numLigne: "M001",
    date: new Date("2025-01-14"),
    heure: "14:00",
    sens: "retour",
    nbVoyageurs: 130,
    observation: "Panne",
    moyenTransport: "métro",
    numNavette: "N003",
  },
  {
    numero: "V0005",
    numLigne: "TR001",
    date: new Date("2025-01-15"),
    heure: "07:00",
    sens: "aller",
    nbVoyageurs: 180,
    observation: "RAS",
    moyenTransport: "tramway",
    numNavette: "N004",
  },
]);
