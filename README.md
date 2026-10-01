# Car Dealership Management System (PostgreSQL)

Relational database for a used-car dealership that handles the vehicle inventory, test drives, rentals, purchases and payments. The domain is based on a real dealership in Varaždin, Croatia.

> Course project: **Databases 2** (Baze podataka 2), Faculty of Organization and Informatics (FOI), University of Zagreb, January 2026

## Highlights

- **10-table ERA model** built around a central `usluga` (service) entity. Each test drive, rental or purchase is one service, linked 1:1 to its own detail table.
- **Payments in instalments**: one service can have many payments, which covers cash, credit and leasing.
- **Two PL/pgSQL triggers**:
  - block deleting a service that is still `aktivna` / `u tijeku`  
  - automatically close a service when a payment is recorded as `plaćeno`
- **Simple and complex SQL queries** with joins, aggregation and grouping.
- **Python Tkinter GUI** (`app/`): a form for adding vehicles, and a table view for updating and deleting services. The delete trigger shows up here as an error message.

## Tech stack

PostgreSQL · PL/pgSQL · DataGrip · draw.io · Python (Tkinter)

## Repository structure

```
app/
  dodaj.py           # Tkinter form: add a vehicle
  upd_del.py         # Tkinter: list, update and delete services
sql/
  01_schema.sql      # schema bp2_projekt + all tables and constraints
  02_seed_data.sql   # sample data (fictional customers)
  03_triggers.sql    # both triggers
  04_queries.sql     # example queries
docs/
  Sustav_za_upravljanje_vozilima.pdf   # full project documentation (Croatian)
```

## Run it

```bash
createdb dealership
psql -d dealership -f sql/01_schema.sql
psql -d dealership -f sql/02_seed_data.sql
psql -d dealership -f sql/03_triggers.sql
psql -d dealership -f sql/04_queries.sql
```

Try the triggers:

```sql
SET search_path TO bp2_projekt;
DELETE FROM usluga WHERE id_usluga = 2;          -- blocked: service is active
INSERT INTO placanje (iznos, datum, status_placanja, id_usluga)
VALUES (180, '2025-05-05', 'plaćeno', 2);         -- service 2 becomes 'završena'
```

Run the GUI (the database connection is read from environment variables):

```bash
pip install psycopg2-binary
export DB_NAME=dealership DB_USER=postgres DB_PASSWORD=your_password
python app/dodaj.py
python app/upd_del.py
```

## Data model

`drzava` 1─N `autokuca` 1─N `vozilo` 1─N `usluga` N─1 `kupac`  
`usluga` N─1 `vrsta_usluge` · `usluga` 1─1 `probna_voznja` / `najam` / `kupnja` · `usluga` 1─N `placanje`

---

## Hrvatski

# Sustav za upravljanje vozilima, najmom i kupnjom u autokući

Relacijska baza podataka za autokuću rabljenih vozila. Pokriva evidenciju vozila, probne vožnje, najam, kupnju i plaćanja. Domena je inspirirana stvarnom autokućom iz Varaždina.

> Projektni zadatak iz kolegija **Baze podataka 2**, Fakultet organizacije i informatike (FOI), Sveučilište u Zagrebu, siječanj 2026.

### Ključno

- **ERA model s 10 tablica** sa središnjim entitetom `usluga`. Svaka probna vožnja, najam ili kupnja jedna je usluga, povezana 1:1 sa svojom tablicom detalja.
- **Plaćanje na rate**: jedna usluga može imati više plaćanja, pa su pokriveni gotovina, kredit i leasing.
- **Dva PL/pgSQL okidača**:
  - zabrana brisanja usluga koje su `aktivna` / `u tijeku`  
  - automatsko zatvaranje usluge kad se plaćanje evidentira kao `plaćeno`
- **Jednostavni i složeni SQL upiti** sa spajanjem tablica, agregacijom i grupiranjem.
- **Python Tkinter sučelje** (`app/`): forma za unos vozila te tablica za ažuriranje i brisanje usluga.

### Tehnologije

PostgreSQL · PL/pgSQL · DataGrip · draw.io · Python (Tkinter)

### Pokretanje

Skripte iz mape `sql/` pokreni redom od 01 do 04. Za sučelje postavi varijable okruženja `DB_NAME`, `DB_USER` i `DB_PASSWORD` pa pokreni `app/dodaj.py` ili `app/upd_del.py` (naredbe su iznad). Cjelovita dokumentacija nalazi se u `docs/`.
