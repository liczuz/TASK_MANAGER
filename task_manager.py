import mysql.connector
from mysql.connector import Error

def pripojeni_db():
    try:
        spojeni = mysql.connector.connect(
            host="localhost",
            user="root",
            password="K4d1budk487!",
            database="TASK_MANAGER"
        )
        return spojeni
    except Error as e:
        print("Chyba při připojení k databázi:", e)
        return None

def vytvoreni_tabulky():
    spojeni = pripojeni_db()
    if spojeni:
        kurzor = spojeni.cursor()
        kurzor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(100) NOT NULL,
                popis TEXT NOT NULL,
                stav ENUM('nezahájeno', 'probíhá', 'hotovo') DEFAULT 'nezahájeno',
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        spojeni.commit()
        kurzor.close()
        spojeni.close()

def pridat_ukol(nazev, popis):
    if not nazev or not popis:
        return False
    spojeni = pripojeni_db()
    if spojeni:
        kurzor = spojeni.cursor()
        dotaz = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
        kurzor.execute(dotaz, (nazev, popis))
        spojeni.commit()
        kurzor.close()
        spojeni.close()
        return True
    return False

def zobrazit_ukoly():
    spojeni = pripojeni_db()
    if spojeni:
        kurzor = spojeni.cursor(dictionary=True)
        kurzor.execute("SELECT * FROM ukoly WHERE stav IN ('nezahájeno', 'probíhá')")
        vysledky = kurzor.fetchall()
        kurzor.close()
        spojeni.close()
        return vysledky
    return []

def existuje_aktivni_ukol(id_ukolu):
    spojeni = pripojeni_db()
    if spojeni:
        kurzor = spojeni.cursor()
        kurzor.execute(
            "SELECT COUNT(*) FROM ukoly WHERE id = %s AND stav IN ('nezahájeno', 'probíhá')",
            (id_ukolu,))
        vysledek = kurzor.fetchone()
        kurzor.close()
        spojeni.close()
        return vysledek and vysledek[0] > 0
    return False

def aktualizovat_ukol(id_ukolu, novy_stav):
    if novy_stav not in ['probíhá', 'hotovo']:
        return "neplatny_stav"

    if not existuje_aktivni_ukol(id_ukolu):
        return "neexistuje"

    spojeni = pripojeni_db()
    if spojeni:
        kurzor = spojeni.cursor()
        kurzor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
        spojeni.commit()
        kurzor.close()
        spojeni.close()
        return True
    return False

def odstranit_ukol(id_ukolu):
    if not existuje_aktivni_ukol(id_ukolu):
        return False

    spojeni = pripojeni_db()
    if spojeni:
        kurzor = spojeni.cursor()
        dotaz = "DELETE FROM ukoly WHERE id = %s"
        kurzor.execute(dotaz, (id_ukolu,))
        spojeni.commit()
        kurzor.close()
        spojeni.close()
        return True
    return False

def seznam_aktivnich_ukolu():
    return zobrazit_ukoly()

def zpracuj_pridani(nazev, popis):
    return pridat_ukol(nazev, popis)

def zpracuj_aktualizaci(id_ukolu, novy_stav):
    return aktualizovat_ukol(id_ukolu, novy_stav)

def zpracuj_odstraneni(id_ukolu):
    return odstranit_ukol(id_ukolu)

def vyhodnot_volbu(volba, vstupy):
    if volba == "1":
        nazev, popis = vstupy
        return zpracuj_pridani(nazev, popis)

    elif volba == "2":
        return seznam_aktivnich_ukolu()

    elif volba == "3":
        id_ukolu, novy_stav = vstupy
        return zpracuj_aktualizaci(id_ukolu, novy_stav)

    elif volba == "4":
        id_ukolu = vstupy[0]
        return zpracuj_odstraneni(id_ukolu)

    elif volba == "5":
        return "konec"

    return "neplatna"

if __name__ == "__main__":
    vytvoreni_tabulky()
    while True:
        print("\n--- Správce úkolů ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Konec")

        volba = input("Zadej volbu (1-5): ")

        if volba == "1":
            nazev = input("Zadej název úkolu: ")
            popis = input("Zadej popis úkolu: ")
            vysledek = vyhodnot_volbu(volba, (nazev, popis))
            print("Úkol přidán." if vysledek else "Chyba při přidání.")

        elif volba == "2":
            ukoly = vyhodnot_volbu(volba, ())
            if ukoly:
                for u in ukoly:
                    print(f"ID: {u['id']}, Název: {u['nazev']}, Popis: {u['popis']}, Stav: {u['stav']}")
            else:
                print("Žádné aktivní úkoly.")

        elif volba == "3":
            try:
                id_ukolu = int(input("Zadej ID úkolu pro aktualizaci: "))
                if not existuje_aktivni_ukol(id_ukolu):
                    print("Zadané ID nebylo nalezeno mezi aktivními úkoly.")
                    continue

                novy_stav = input("Nový stav (probíhá/hotovo): ")
                vysledek = vyhodnot_volbu(volba, (id_ukolu, novy_stav))
                if vysledek == "neexistuje":
                    print("Zadané ID nebylo nalezeno mezi aktivními úkoly.")
                elif vysledek == "neplatny_stav":
                    print("Zadaný stav není platný.")
                elif vysledek:
                    print("Stav aktualizován.")
                else:
                    print("Aktualizace selhala.")
            except ValueError:
                print("Neplatné ID. Zadej číslo.")

        elif volba == "4":
            try:
                id_ukolu = int(input("Zadej ID úkolu ke smazání: "))
                vysledek = vyhodnot_volbu(volba, (id_ukolu,))
                if vysledek:
                    print("Úkol smazán.")
                else:
                    print("Zadané ID nebylo nalezeno mezi aktivními úkoly.")
            except ValueError:
                print("Neplatné ID. Zadej číslo.")

        elif volba == "5":
            print("Program ukončen.")
            break

        else:
            print("Neplatná volba.")