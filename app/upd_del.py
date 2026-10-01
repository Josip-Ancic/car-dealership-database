import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import psycopg2


# --- POSTAVKE BAZE (po potrebi promijeni) ---
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}


def dohvati_vezu():
    """Otvara vezu prema bazi i postavlja search_path (dodatna sigurnost)."""
    conn = psycopg2.connect(**DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute("SET search_path TO bp2_projekt, public;")
    conn.commit()
    return conn


def parsiraj_datetime(tekst):
    """
    Prima:
      - 'YYYY-MM-DD HH:MM'
      - 'YYYY-MM-DD HH:MM:SS'
    Vraća datetime ili baca ValueError.
    """
    tekst = tekst.strip()
    if len(tekst) == 16:
        return datetime.strptime(tekst, "%Y-%m-%d %H:%M")
    return datetime.strptime(tekst, "%Y-%m-%d %H:%M:%S")


class UslugaUpdDelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ažuriraj / izbriši uslugu")

        # Mape za combobox (prikaz -> id)
        self.mapa_vrsta = {}
        self.mapa_vozilo = {}
        self.mapa_kupac = {}

        # Gornji dio: tablica usluga
        okvir_tablica = ttk.Frame(root, padding=10)
        okvir_tablica.pack(fill="both", expand=True)

        stupci = ("id_usluga", "datum_pocetka", "datum_zavrsetka", "status_usluge", "vrsta", "vozilo", "kupac")
        self.tree = ttk.Treeview(okvir_tablica, columns=stupci, show="headings", height=8)
        self.tree.pack(side="left", fill="both", expand=True)

        for col, txt, w in [
            ("id_usluga", "ID", 70),
            ("datum_pocetka", "Početak", 160),
            ("datum_zavrsetka", "Završetak", 160),
            ("status_usluge", "Status", 120),
            ("vrsta", "Vrsta", 140),
            ("vozilo", "Vozilo", 200),
            ("kupac", "Kupac", 200),
        ]:
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=w)

        scroll = ttk.Scrollbar(okvir_tablica, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.bind("<<TreeviewSelect>>", self.na_odabir_reda)

        # Donji dio: forma za update/delete
        okvir_forma = ttk.LabelFrame(root, text="Uredi odabranu uslugu", padding=12)
        okvir_forma.pack(fill="x", padx=10, pady=10)

        ttk.Label(okvir_forma, text="ID usluge:").grid(row=0, column=0, sticky="w", pady=4)
        self.id_usluga_var = tk.StringVar()
        self.unos_id = ttk.Entry(okvir_forma, textvariable=self.id_usluga_var, width=25, state="readonly")
        self.unos_id.grid(row=0, column=1, pady=4, sticky="w")

        ttk.Label(okvir_forma, text="Datum početka (YYYY-MM-DD HH:MM):").grid(row=1, column=0, sticky="w", pady=4)
        self.datum_poc_var = tk.StringVar()
        self.unos_poc = ttk.Entry(okvir_forma, textvariable=self.datum_poc_var, width=25)
        self.unos_poc.grid(row=1, column=1, pady=4, sticky="w")

        ttk.Label(okvir_forma, text="Datum završetka (prazno ili YYYY-MM-DD HH:MM):").grid(row=2, column=0, sticky="w", pady=4)
        self.datum_zav_var = tk.StringVar()
        self.unos_zav = ttk.Entry(okvir_forma, textvariable=self.datum_zav_var, width=25)
        self.unos_zav.grid(row=2, column=1, pady=4, sticky="w")

        ttk.Label(okvir_forma, text="Status usluge:").grid(row=3, column=0, sticky="w", pady=4)
        self.status_var = tk.StringVar()
        self.combo_status = ttk.Combobox(okvir_forma, textvariable=self.status_var, width=23, state="readonly")
        self.combo_status["values"] = ("aktivna", "u tijeku", "završena", "otkazana")
        self.combo_status.current(0)
        self.combo_status.grid(row=3, column=1, pady=4, sticky="w")

        ttk.Label(okvir_forma, text="Vrsta usluge:").grid(row=4, column=0, sticky="w", pady=4)
        self.vrsta_var = tk.StringVar()
        self.combo_vrsta = ttk.Combobox(okvir_forma, textvariable=self.vrsta_var, width=23, state="readonly")
        self.combo_vrsta.grid(row=4, column=1, pady=4, sticky="w")

        ttk.Label(okvir_forma, text="Vozilo:").grid(row=5, column=0, sticky="w", pady=4)
        self.vozilo_var = tk.StringVar()
        self.combo_vozilo = ttk.Combobox(okvir_forma, textvariable=self.vozilo_var, width=23, state="readonly")
        self.combo_vozilo.grid(row=5, column=1, pady=4, sticky="w")

        ttk.Label(okvir_forma, text="Kupac:").grid(row=6, column=0, sticky="w", pady=4)
        self.kupac_var = tk.StringVar()
        self.combo_kupac = ttk.Combobox(okvir_forma, textvariable=self.kupac_var, width=23, state="readonly")
        self.combo_kupac.grid(row=6, column=1, pady=4, sticky="w")

        okvir_gumbi = ttk.Frame(okvir_forma)
        okvir_gumbi.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Button(okvir_gumbi, text="Osvježi listu", command=self.ucitaj_sve).pack(side="left")
        ttk.Button(okvir_gumbi, text="Ažuriraj", command=self.azuriraj_uslugu).pack(side="left", padx=8)
        ttk.Button(okvir_gumbi, text="Izbriši", command=self.izbrisi_uslugu).pack(side="left", padx=8)
        ttk.Button(okvir_gumbi, text="Zatvori", command=root.destroy).pack(side="right")

        self.ucitaj_sve()

    def ucitaj_dropdownove(self):
        """Učitaj vrsta_usluge, vozilo i kupac za combobox."""
        conn = dohvati_vezu()
        cur = conn.cursor()

        # Vrste usluga
        cur.execute("SELECT id_vrsta_usluge, naziv FROM bp2_projekt.vrsta_usluge ORDER BY naziv;")
        self.mapa_vrsta = {naziv: idv for idv, naziv in cur.fetchall()}
        self.combo_vrsta["values"] = list(self.mapa_vrsta.keys())

        # Vozila
        cur.execute("""
            SELECT id_vozilo, (marka || ' ' || model || ' (ID:' || id_vozilo || ')') AS prikaz
            FROM bp2_projekt.vozilo
            ORDER BY marka, model;
        """)
        self.mapa_vozilo = {prikaz: idv for idv, prikaz in cur.fetchall()}
        self.combo_vozilo["values"] = list(self.mapa_vozilo.keys())

        # Kupci
        cur.execute("""
            SELECT id_kupac, (ime || ' ' || prezime || ' (ID:' || id_kupac || ')') AS prikaz
            FROM bp2_projekt.kupac
            ORDER BY ime, prezime;
        """)
        self.mapa_kupac = {prikaz: idk for idk, prikaz in cur.fetchall()}
        self.combo_kupac["values"] = list(self.mapa_kupac.keys())

        cur.close()
        conn.close()

        # Postavi default ako postoje vrijednosti
        if self.combo_vrsta["values"]:
            self.combo_vrsta.current(0)
        if self.combo_vozilo["values"]:
            self.combo_vozilo.current(0)
        if self.combo_kupac["values"]:
            self.combo_kupac.current(0)

    def ucitaj_usluge(self):
        """Učitaj usluge u tablicu."""
        conn = dohvati_vezu()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                u.id_usluga,
                u.datum_pocetka,
                u.datum_zavrsetka,
                u.status_usluge,
                vu.naziv AS vrsta,
                (v.marka || ' ' || v.model || ' (ID:' || v.id_vozilo || ')') AS vozilo,
                (k.ime || ' ' || k.prezime || ' (ID:' || k.id_kupac || ')') AS kupac
            FROM bp2_projekt.usluga u
            JOIN bp2_projekt.vrsta_usluge vu ON vu.id_vrsta_usluge = u.id_vrsta_usluge
            JOIN bp2_projekt.vozilo v ON v.id_vozilo = u.id_vozilo
            JOIN bp2_projekt.kupac k ON k.id_kupac = u.id_kupac
            ORDER BY u.id_usluga DESC;
        """)
        redci = cur.fetchall()

        cur.close()
        conn.close()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in redci:
            self.tree.insert("", "end", values=r)

    def ucitaj_sve(self):
        try:
            self.ucitaj_dropdownove()
            self.ucitaj_usluge()
        except Exception as e:
            messagebox.showerror("Greška", f"Ne mogu učitati podatke.\n\nDetalji:\n{e}")

    def na_odabir_reda(self, event):
        """Kad korisnik klikne red u tablici, popuni formu."""
        odabrano = self.tree.selection()
        if not odabrano:
            return

        vrijednosti = self.tree.item(odabrano[0], "values")
        if not vrijednosti:
            return

        id_usluga, dat_poc, dat_zav, status, vrsta, vozilo, kupac = vrijednosti

        self.id_usluga_var.set(str(id_usluga))

        # Datumi: pretvori u 'YYYY-MM-DD HH:MM' format (ako je None, prikaži prazno)
        self.datum_poc_var.set(str(dat_poc)[:16] if dat_poc else "")
        self.datum_zav_var.set(str(dat_zav)[:16] if dat_zav else "")

        # Status
        if status in self.combo_status["values"]:
            self.status_var.set(status)
        else:
            self.status_var.set(self.combo_status["values"][0])

        # Vrsta/vozilo/kupac (prikaz u tablici je isti format kao u dropdownu)
        if vrsta in self.mapa_vrsta:
            self.vrsta_var.set(vrsta)
        if vozilo in self.mapa_vozilo:
            self.vozilo_var.set(vozilo)
        if kupac in self.mapa_kupac:
            self.kupac_var.set(kupac)

    def azuriraj_uslugu(self):
        """UPDATE nad uslugom prema vrijednostima iz forme."""
        try:
            id_txt = self.id_usluga_var.get().strip()
            if not id_txt:
                messagebox.showwarning("Upozorenje", "Prvo odaberi uslugu iz tablice.")
                return

            id_usluga = int(id_txt)

            datum_poc = parsiraj_datetime(self.datum_poc_var.get())
            datum_zav_txt = self.datum_zav_var.get().strip()
            datum_zav = None if datum_zav_txt == "" else parsiraj_datetime(datum_zav_txt)

            status = self.status_var.get().strip()

            vrsta_prikaz = self.vrsta_var.get().strip()
            vozilo_prikaz = self.vozilo_var.get().strip()
            kupac_prikaz = self.kupac_var.get().strip()

            id_vrsta = self.mapa_vrsta.get(vrsta_prikaz)
            id_vozilo = self.mapa_vozilo.get(vozilo_prikaz)
            id_kupac = self.mapa_kupac.get(kupac_prikaz)

            if not (id_vrsta and id_vozilo and id_kupac):
                messagebox.showwarning("Upozorenje", "Odaberi valjanu vrstu usluge, vozilo i kupca.")
                return

            conn = dohvati_vezu()
            cur = conn.cursor()

            cur.execute("""
                UPDATE bp2_projekt.usluga
                SET datum_pocetka = %s,
                    datum_zavrsetka = %s,
                    status_usluge = %s,
                    id_vrsta_usluge = %s,
                    id_vozilo = %s,
                    id_kupac = %s
                WHERE id_usluga = %s;
            """, (datum_poc, datum_zav, status, id_vrsta, id_vozilo, id_kupac, id_usluga))

            if cur.rowcount == 0:
                conn.rollback()
                cur.close()
                conn.close()
                messagebox.showwarning("Upozorenje", "Usluga s tim ID-om ne postoji.")
                return

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("Uspjeh", "Usluga je ažurirana.")
            self.ucitaj_usluge()

        except ValueError:
            messagebox.showerror("Greška", "Provjeri format datuma: YYYY-MM-DD HH:MM (ili HH:MM:SS).")
        except Exception as e:
            messagebox.showerror("Greška", f"Ne mogu ažurirati uslugu.\n\nDetalji:\n{e}")

    def izbrisi_uslugu(self):
        """DELETE usluge. Može pasti ako postoje povezani zapisi (npr. placanje/kupnja/najam)."""
        try:
            id_txt = self.id_usluga_var.get().strip()
            if not id_txt:
                messagebox.showwarning("Upozorenje", "Prvo odaberi uslugu iz tablice.")
                return

            id_usluga = int(id_txt)

            if not messagebox.askyesno("Potvrda", f"Sigurno želiš izbrisati uslugu ID {id_usluga}?"):
                return

            conn = dohvati_vezu()
            cur = conn.cursor()

            cur.execute("DELETE FROM bp2_projekt.usluga WHERE id_usluga = %s;", (id_usluga,))

            if cur.rowcount == 0:
                conn.rollback()
                cur.close()
                conn.close()
                messagebox.showwarning("Upozorenje", "Usluga s tim ID-om ne postoji.")
                return

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("Uspjeh", "Usluga je obrisana.")
            self.id_usluga_var.set("")
            self.datum_poc_var.set("")
            self.datum_zav_var.set("")
            self.ucitaj_usluge()

        except Exception as e:
            messagebox.showerror(
                "Greška",
                "Ne mogu izbrisati uslugu.\n"
                "Ako postoje povezani zapisi (npr. placanje/kupnja/najam/probna_voznja), brisanje će biti blokirano.\n\n"
                f"Detalji:\n{e}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = UslugaUpdDelApp(root)
    root.mainloop()
