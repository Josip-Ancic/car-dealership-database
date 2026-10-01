-- Car dealership management system — database schema (PostgreSQL)
-- Sustav za upravljanje vozilima, najmom i kupnjom u autokući — shema baze

CREATE SCHEMA IF NOT EXISTS bp2_projekt;
SET search_path TO bp2_projekt;

CREATE TABLE drzava
(
    id_drzava SERIAL PRIMARY KEY,
    naziv     VARCHAR(100) NOT NULL,
    oznaka    VARCHAR(10)  NOT NULL
);

CREATE TABLE vrsta_usluge
(
    id_vrsta_usluge SERIAL PRIMARY KEY,
    naziv           VARCHAR(50) NOT NULL
);

CREATE TABLE kupac
(
    id_kupac SERIAL PRIMARY KEY,
    ime      VARCHAR(50)  NOT NULL,
    prezime  VARCHAR(50)  NOT NULL,
    email    VARCHAR(100) NOT NULL,
    telefon  VARCHAR(30)
);

CREATE TABLE autokuca
(
    id_autokuca SERIAL PRIMARY KEY,
    naziv       VARCHAR(100) NOT NULL,
    adresa      VARCHAR(150) NOT NULL,
    id_drzava   INTEGER      NOT NULL
        CONSTRAINT fk_autokuca_drzava
            REFERENCES drzava
            ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE vozilo
(
    id_vozilo          SERIAL PRIMARY KEY,
    marka              VARCHAR(50)    NOT NULL,
    model              VARCHAR(50)    NOT NULL,
    godina_proizvodnje INTEGER        NOT NULL,
    kilometraza        INTEGER        NOT NULL,
    cijena             NUMERIC(10, 2) NOT NULL,
    status_vozila      VARCHAR(30)    NOT NULL,
    id_autokuca        INTEGER        NOT NULL
        CONSTRAINT fk_vozilo_autokuca
            REFERENCES autokuca
            ON UPDATE CASCADE ON DELETE CASCADE
);

-- Central entity: every interaction between a customer and a vehicle
CREATE TABLE usluga
(
    id_usluga       SERIAL PRIMARY KEY,
    datum_pocetka   TIMESTAMP   NOT NULL,
    datum_zavrsetka TIMESTAMP,
    status_usluge   VARCHAR(30) NOT NULL,
    id_vrsta_usluge INTEGER     NOT NULL
        CONSTRAINT fk_usluga_vrsta
            REFERENCES vrsta_usluge
            ON UPDATE CASCADE ON DELETE CASCADE,
    id_vozilo       INTEGER     NOT NULL
        CONSTRAINT fk_usluga_vozilo
            REFERENCES vozilo
            ON UPDATE CASCADE ON DELETE CASCADE,
    id_kupac        INTEGER     NOT NULL
        CONSTRAINT fk_usluga_kupac
            REFERENCES kupac
            ON UPDATE CASCADE ON DELETE CASCADE
);

-- 1:1 specialisations of usluga
CREATE TABLE probna_voznja
(
    id_probna_voznja SERIAL PRIMARY KEY,
    termin           TIMESTAMP NOT NULL,
    trajanje_min     INTEGER   NOT NULL,
    id_usluga        INTEGER   NOT NULL UNIQUE
        CONSTRAINT fk_probna_usluga
            REFERENCES usluga
            ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE najam
(
    id_najam       SERIAL PRIMARY KEY,
    cijena_po_danu NUMERIC(10, 2) NOT NULL,
    ukupan_iznos   NUMERIC(10, 2) NOT NULL,
    id_usluga      INTEGER        NOT NULL UNIQUE
        CONSTRAINT fk_najam_usluga
            REFERENCES usluga
            ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE kupnja
(
    id_kupnja      SERIAL PRIMARY KEY,
    datum_kupnje   DATE           NOT NULL,
    nacin_placanja VARCHAR(50)    NOT NULL,
    ukupna_cijena  NUMERIC(10, 2) NOT NULL,
    id_usluga      INTEGER        NOT NULL UNIQUE
        CONSTRAINT fk_kupnja_usluga
            REFERENCES usluga
            ON UPDATE CASCADE ON DELETE CASCADE
);

-- 1:N — one service can have several payments (instalments, leasing)
CREATE TABLE placanje
(
    id_placanje     SERIAL PRIMARY KEY,
    iznos           NUMERIC(10, 2) NOT NULL,
    datum           DATE           NOT NULL,
    status_placanja VARCHAR(30)    NOT NULL,
    id_usluga       INTEGER        NOT NULL
        CONSTRAINT fk_placanje_usluga
            REFERENCES usluga
            ON UPDATE CASCADE ON DELETE CASCADE
);
