import os
import tkinter as tk
from tkinter import ttk, messagebox
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


class DodajVoziloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dodaj novo vozilo")

        self.mapa_autokuca = {}  # naziv -> id_autokuca

        okvir = ttk.Frame(root, padding=12)
        okvir.pack(fill="both", expand=True)

        # Polja
        ttk.Label(okvir, text="Marka:").grid(row=0, column=0, sticky="w", pady=4)
        self.unos_marka = ttk.Entry(okvir, width=35)
        self.unos_marka.grid(row=0, column=1, pady=4)

        ttk.Label(okvir, text="Model:").grid(row=1, column=0, sticky="w", pady=4)
        self.unos_model = ttk.Entry(okvir, width=35)
        self.unos_model.grid(row=1, column=1, pady=4)

        ttk.Label(okvir, text="Godina proizvodnje:").grid(row=2, column=0, sticky="w", pady=4)
        self.unos_godina = ttk.Entry(okvir, width=35)
        self.unos_godina.grid(row=2, column=1, pady=4)

        ttk.Label(okvir, text="Kilometraža:").grid(row=3, column=0, sticky="w", pady=4)
        self.unos_km = ttk.Entry(okvir, width=35)
        self.unos_km.grid(row=3, column=1, pady=4)

        ttk.Label(okvir, text="Cijena (npr. 12000.50):").grid(row=4, column=0, sticky="w", pady=4)
        self.unos_cijena = ttk.Entry(okvir, width=35)
        self.unos_cijena.grid(row=4, column=1, pady=4)

        ttk.Label(okvir, text="Status vozila:").grid(row=5, column=0, sticky="w", pady=4)
        self.status_var = tk.StringVar()
        self.combo_status = ttk.Combobox(okvir, textvariable=self.status_var, width=33, state="readonly")
        self.combo_status["values"] = ("dostupno", "zauzeto", "rezervirano", "servis")
        self.combo_status.current(0)
        self.combo_status.grid(row=5, column=1, pady=4, sticky="w")

        ttk.Label(okvir, text="Autokuća:").grid(row=6, column=0, sticky="w", pady=4)
        self.autokuca_var = tk.StringVar()
        self.combo_autokuca = ttk.Combobox(okvir, textvariable=self.autokuca_var, width=33, state="readonly")
        self.combo_autokuca.grid(row=6, column=1, pady=4, sticky="w")

        # Gumbi
        okvir_gumbi = ttk.Frame(okvir)
        okvir_gumbi.grid(row=7, column=0, columnspan=2, pady=12, sticky="ew")

        ttk.Button(okvir_gumbi, text="Spremi", command=self.spremi_vozilo).pack(side="left")
        ttk.Button(okvir_gumbi, text="Očisti", command=self.ocisti).pack(side="left", padx=8)
        ttk.Button(okvir_gumbi, text="Zatvori", command=root.destroy).pack(side="right")

        self.ucitaj_autokuce()

    def ucitaj_autokuce(self):
        """Učitaj autokuće za dropdown."""
        try:
            conn = dohvati_vezu()
            cur = conn.cursor()

            cur.execute("""
                SELECT a.id_autokuca, a.naziv
                FROM bp2_projekt.autokuca a
                ORDER BY a.naziv;
            """)
            podaci = cur.fetchall()

            cur.close()
            conn.close()

            self.mapa_autokuca.clear()
            nazivi = []
            for id_a, naziv in podaci:
                self.mapa_autokuca[naziv] = id_a
                nazivi.append(naziv)

            self.combo_autokuca["values"] = nazivi
            if nazivi:
                self.combo_autokuca.current(0)

        except Exception as e:
            messagebox.showerror("Greška", f"Ne mogu učitati autokuće.\n\nDetalji:\n{e}")

    def ocisti(self):
        self.unos_marka.delete(0, tk.END)
        self.unos_model.delete(0, tk.END)
        self.unos_godina.delete(0, tk.END)
        self.unos_km.delete(0, tk.END)
        self.unos_cijena.delete(0, tk.END)
        self.combo_status.current(0)
        if self.combo_autokuca["values"]:
            self.combo_autokuca.current(0)

    def spremi_vozilo(self):
        """Validacija + INSERT u vozilo (id_vozilo je serial pa ga NE upisujemo)."""
        try:
            marka = self.unos_marka.get().strip()
            model = self.unos_model.get().strip()
            godina_txt = self.unos_godina.get().strip()
            km_txt = self.unos_km.get().strip()
            cijena_txt = self.unos_cijena.get().strip()
            status = self.status_var.get().strip()
            autokuca_naziv = self.autokuca_var.get().strip()

            if not marka or not model or not godina_txt or not km_txt or not cijena_txt or not autokuca_naziv:
                messagebox.showwarning("Upozorenje", "Sva polja moraju biti popunjena.")
                return

            godina = int(godina_txt)
            km = int(km_txt)
            cijena = float(cijena_txt)

            id_autokuca = self.mapa_autokuca.get(autokuca_naziv)
            if not id_autokuca:
                messagebox.showwarning("Upozorenje", "Odaberi valjanu autokuću.")
                return

            conn = dohvati_vezu()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO bp2_projekt.vozilo
                    (marka, model, godina_proizvodnje, kilometraza, cijena, status_vozila, id_autokuca)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_vozilo;
            """, (marka, model, godina, km, cijena, status, id_autokuca))

            novi_id = cur.fetchone()[0]
            conn.commit()

            cur.close()
            conn.close()

            messagebox.showinfo("Uspjeh", f"Vozilo je dodano. Novi ID: {novi_id}")
            self.ocisti()

        except ValueError:
            messagebox.showerror("Greška", "Godina, kilometraža i cijena moraju biti brojevi (cijena može biti decimalna).")
        except Exception as e:
            messagebox.showerror("Greška", f"Ne mogu spremiti vozilo.\n\nDetalji:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DodajVoziloApp(root)
    root.mainloop()
