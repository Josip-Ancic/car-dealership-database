-- Triggers / Okidači
SET search_path TO bp2_projekt;

-- 1) Block deleting services that are still active or in progress
--    Zabrana brisanja usluga koje su aktivne ili u tijeku
CREATE OR REPLACE FUNCTION sprijeci_brisanje_aktivne_usluge()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.status_usluge IN ('aktivna', 'u tijeku') THEN
        RAISE EXCEPTION
            'Brisanje nije dopušteno: usluga (ID=%) je "%". Prvo promijeni status (npr. završena/otkazana).',
            OLD.id_usluga, OLD.status_usluge
            USING ERRCODE = '45000';
    END IF;
    RETURN OLD;
END;
$$;

DROP TRIGGER IF EXISTS trg_sprijeci_brisanje_aktivne_usluge ON usluga;
CREATE TRIGGER trg_sprijeci_brisanje_aktivne_usluge
BEFORE DELETE ON usluga
FOR EACH ROW
EXECUTE FUNCTION sprijeci_brisanje_aktivne_usluge();

-- 2) Mark the service as finished once a payment is recorded as paid
--    Automatsko zatvaranje usluge nakon izvršenog plaćanja
CREATE OR REPLACE FUNCTION zatvori_uslugu_nakon_placanja()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.status_placanja = 'plaćeno' THEN
        UPDATE usluga
        SET status_usluge = 'završena'
        WHERE id_usluga = NEW.id_usluga;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_zavrsetak_usluge ON placanje;
CREATE TRIGGER trg_zavrsetak_usluge
AFTER INSERT ON placanje
FOR EACH ROW
EXECUTE FUNCTION zatvori_uslugu_nakon_placanja();
