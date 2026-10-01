-- Sample data (fictional customers) / Testni podaci (izmišljeni kupci)
SET search_path TO bp2_projekt;

INSERT INTO drzava (id_drzava, naziv, oznaka) VALUES
(1, 'Hrvatska', 'HR'),
(2, 'Njemačka', 'DE'),
(3, 'Austrija', 'AT'),
(4, 'Slovenija', 'SI'),
(5, 'Italija', 'IT'),
(6, 'Francuska', 'FR'),
(7, 'Španjolska', 'ES'),
(8, 'Poljska', 'PL'),
(9, 'Mađarska', 'HU'),
(10, 'Češka', 'CZ');
SELECT setval(pg_get_serial_sequence('drzava', 'id_drzava'), 10);

INSERT INTO autokuca (naziv, adresa, id_drzava) VALUES
('Superauto', 'Ulica bana Jelačića 15, Varaždin', 1),
('AutoCentar Plus', 'Industrijska 4, Zagreb', 1),
('Premium Cars', 'Hauptstrasse 12, München', 2),
('Auto Wien', 'Ringstrasse 8, Beč', 3),
('Ljubljana Auto', 'Trg republike 3, Ljubljana', 4),
('Milano Cars', 'Via Roma 22, Milano', 5),
('Paris Auto', 'Rue de Lyon 10, Paris', 6),
('Madrid Motors', 'Calle Mayor 5, Madrid', 7),
('Budapest Auto', 'Andrassy ut 14, Budimpešta', 9),
('Prague Cars', 'Vaclavske namesti 9, Prag', 10);

INSERT INTO vozilo (marka, model, godina_proizvodnje, kilometraza, cijena, status_vozila, id_autokuca) VALUES
('Volkswagen', 'Golf', 2019, 45000, 15000.00, 'dostupno', 1),
('Audi', 'A4', 2020, 38000, 22000.00, 'dostupno', 1),
('BMW', '320d', 2018, 60000, 21000.00, 'dostupno', 2),
('Mercedes', 'C220', 2019, 50000, 24000.00, 'dostupno', 3),
('Škoda', 'Octavia', 2021, 30000, 18000.00, 'dostupno', 1),
('Toyota', 'Corolla', 2020, 42000, 17000.00, 'dostupno', 4),
('Peugeot', '308', 2017, 70000, 13000.00, 'dostupno', 6),
('Renault', 'Megane', 2018, 65000, 14000.00, 'dostupno', 7),
('Mazda', '3', 2019, 48000, 16500.00, 'dostupno', 8),
('Opel', 'Astra', 2020, 35000, 15500.00, 'dostupno', 9);

INSERT INTO kupac (ime, prezime, email, telefon) VALUES
('Ivan', 'Horvat', 'ivan.horvat@example.com', '0911111111'),
('Marko', 'Marić', 'marko.maric@example.com', '0912222222'),
('Ana', 'Kovač', 'ana.kovac@example.com', '0913333333'),
('Petra', 'Novak', 'petra.novak@example.com', '0914444444'),
('Luka', 'Babić', 'luka.babic@example.com', '0915555555'),
('Maja', 'Radić', 'maja.radic@example.com', '0916666666'),
('Filip', 'Jurić', 'filip.juric@example.com', '0917777777'),
('Iva', 'Božić', 'iva.bozic@example.com', '0918888888'),
('Tomislav', 'Perić', 'tomislav.peric@example.com', '0919999999'),
('Nikola', 'Pavić', 'nikola.pavic@example.com', '0920000000');

INSERT INTO vrsta_usluge (naziv) VALUES
('Probna vožnja'),
('Najam'),
('Kupnja');

INSERT INTO usluga (datum_pocetka, datum_zavrsetka, status_usluge, id_vrsta_usluge, id_vozilo, id_kupac) VALUES
('2025-05-01 10:00', '2025-05-01 10:30', 'završena', 1, 1, 1),
('2025-05-02 09:00', '2025-05-05 09:00', 'aktivna', 2, 2, 2),
('2025-05-03 12:00', NULL, 'završena', 3, 3, 3),
('2025-05-04 11:00', '2025-05-04 11:30', 'završena', 1, 4, 4),
('2025-05-06 08:00', '2025-05-10 08:00', 'aktivna', 2, 5, 5),
('2025-05-07 13:00', NULL, 'završena', 3, 6, 6),
('2025-05-08 14:00', '2025-05-08 14:30', 'završena', 1, 7, 7),
('2025-05-09 09:00', '2025-05-12 09:00', 'aktivna', 2, 8, 8),
('2025-05-10 15:00', NULL, 'završena', 3, 9, 9),
('2025-05-11 10:00', '2025-05-11 10:30', 'završena', 1, 10, 10);

INSERT INTO probna_voznja (termin, trajanje_min, id_usluga) VALUES
('2025-05-01 10:00', 30, 1),
('2025-05-04 11:00', 30, 4),
('2025-05-08 14:00', 30, 7),
('2025-05-11 10:00', 30, 10);

INSERT INTO najam (cijena_po_danu, ukupan_iznos, id_usluga) VALUES
(45.00, 180.00, 2),
(50.00, 250.00, 5),
(55.00, 165.00, 8);

INSERT INTO kupnja (datum_kupnje, nacin_placanja, ukupna_cijena, id_usluga) VALUES
('2025-05-03', 'gotovina', 21000.00, 3),
('2025-05-07', 'kredit', 17000.00, 6),
('2025-05-10', 'leasing', 16500.00, 9);

INSERT INTO placanje (iznos, datum, status_placanja, id_usluga) VALUES
(21000.00, '2025-05-03', 'plaćeno', 3),
(5000.00, '2025-05-07', 'plaćeno', 6),
(12000.00, '2025-05-07', 'na rate', 6),
(6000.00, '2025-05-10', 'plaćeno', 9),
(10500.00, '2025-05-10', 'na rate', 9);
