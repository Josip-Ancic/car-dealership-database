-- Example queries / Primjeri upita
SET search_path TO bp2_projekt;

-- ---------- Simple / Jednostavni ----------

-- All vehicles
SELECT * FROM vozilo;

-- Available vehicles with price
SELECT marka, model, cijena
FROM vozilo
WHERE status_vozila = 'dostupno';

-- Customer contact list
SELECT ime, prezime, email FROM kupac;

-- Finished services
SELECT * FROM usluga
WHERE status_usluge = 'završena';

-- ---------- Complex / Složeni ----------

-- Services with customer and vehicle details
SELECT k.ime, k.prezime, v.marka, v.model, u.status_usluge
FROM usluga u
JOIN kupac k ON u.id_kupac = k.id_kupac
JOIN vozilo v ON u.id_vozilo = v.id_vozilo;

-- Rentals with total amount
SELECT k.ime, k.prezime, n.ukupan_iznos
FROM najam n
JOIN usluga u ON n.id_usluga = u.id_usluga
JOIN kupac k ON u.id_kupac = k.id_kupac;

-- Number of services per service type
SELECT vu.naziv, COUNT(*) AS broj_usluga
FROM usluga u
JOIN vrsta_usluge vu ON u.id_vrsta_usluge = vu.id_vrsta_usluge
GROUP BY vu.naziv;

-- Total paid per service (useful for instalments)
SELECT u.id_usluga, SUM(p.iznos) AS ukupno_placeno
FROM placanje p
JOIN usluga u ON p.id_usluga = u.id_usluga
GROUP BY u.id_usluga;

-- Sold vehicles with sale price
SELECT v.marka, v.model, ku.ukupna_cijena
FROM kupnja ku
JOIN usluga u ON ku.id_usluga = u.id_usluga
JOIN vozilo v ON u.id_vozilo = v.id_vozilo;
