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
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav ENUM('nezahájeno', 'probíhá', 'hotovo') DEFAULT 'nezahájeno',
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        spojeni.commit()
        kurzor.close()
        spojeni.close()

def hlavni_menu():
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
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            aktualizovat_ukol()
        elif volba == "4":
            odstranit_ukol()
        elif volba == "5":
            print("Program ukončen.")
            break
        else:
            print("Neplatná volba.")

def pridat_ukol():
    nazev = input("Zadej název úkolu: ")
    popis = input("Zadej popis úkolu: ")

    if not nazev or not popis:
        print("Název ani popis nesmí být prázdné!")
        return

    spojeni = pripojeni_db()
    if spojeni:
        kurzor = spojeni.cursor()
        dotaz = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
        kurzor.execute(dotaz, (nazev, popis))
        spojeni.commit()
        print("Úkol byl úspěšně přidán.")
        kurzor.close()
        spojeni.close() 

def zobrazit_ukoly():
    spojeni = pripojeni_db()
    if spojeni:
        kurzor = spojeni.cursor()
        dotaz = "SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN ('nezahájeno', 'probíhá')"
        kurzor.execute(dotaz)
        vysledky = kurzor.fetchall()

        if vysledky:
            print("\nÚkoly:")
            for radek in vysledky:
                print(f"ID: {radek[0]}, Název: {radek[1]}, Popis: {radek[2]}, Stav: {radek[3]}")
        else:
            print("Žádné aktivní úkoly nebyly nalezeny.")

        kurzor.close()
        spojeni.close()

def aktualizovat_ukol():
    zobrazit_ukoly()
    id_ukolu = input("Zadej ID úkolu, který chceš aktualizovat: ")
    novy_stav = input("Zadej nový stav (probíhá/hotovo): ")

    if novy_stav not in ['probíhá', 'hotovo']:
        print("Neplatný stav.")
        return

    spojeni = pripojeni_db()
    if spojeni:
        kurzor = spojeni.cursor()
        dotaz = "UPDATE ukoly SET stav = %s WHERE id = %s"
        kurzor.execute(dotaz, (novy_stav, id_ukolu))
        if kurzor.rowcount == 0:
            print("Úkol s tímto ID neexistuje.")
        else:
            spojeni.commit()
            print("Stav úkolu byl aktualizován.")
        kurzor.close()
        spojeni.close()

def odstranit_ukol():
    zobrazit_ukoly()
    id_ukolu = input("Zadej ID úkolu ke smazání: ")

    spojeni = pripojeni_db()
    if spojeni:
        kurzor = spojeni.cursor()
        dotaz = "DELETE FROM ukoly WHERE id = %s"
        kurzor.execute(dotaz, (id_ukolu,))
        if kurzor.rowcount == 0:
            print("Úkol s tímto ID neexistuje.")
        else:
            spojeni.commit()
            print("Úkol byl odstraněn.")
        kurzor.close()
        spojeni.close()

if __name__ == "__main__":
    hlavni_menu()