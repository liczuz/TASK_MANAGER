import mysql.connector
import pytest
from datetime import datetime

def pripojeni_test_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="K4d1budk487!",
        database="task_manager_test"
    )

def smaz_testovaci_ukol(nazev):
    spojeni = pripojeni_test_db()
    kurzor = spojeni.cursor()
    kurzor.execute("DELETE FROM ukoly WHERE nazev = %s", (nazev,))
    spojeni.commit()
    kurzor.close()
    spojeni.close()

def test_pridani_ukolu_pozitivni():
    spojeni = pripojeni_test_db()
    kurzor = spojeni.cursor()

    nazev = "Testovací úkol"
    popis = "Testovací popis úkolu."

    kurzor.execute(
        "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)",
        (nazev, popis)
    )
    spojeni.commit()

    kurzor.execute("SELECT * FROM ukoly WHERE nazev = %s", (nazev,))
    vysledek = kurzor.fetchone()

    assert vysledek is not None
    assert vysledek[1] == nazev
    assert vysledek[2] == popis

    kurzor.close()
    spojeni.close()
    smaz_testovaci_ukol(nazev)

def test_pridani_ukolu_negativni():
    spojeni = pripojeni_test_db()
    kurzor = spojeni.cursor()

    nazev = "TEST" * 999
    popis = "Test s překročením počtu povolených znaků."

    with pytest.raises(mysql.connector.Error):
        kurzor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
        spojeni.commit()

    kurzor.close()
    spojeni.close()

def test_aktualizace_ukolu_pozitivni():
    spojeni = pripojeni_test_db()
    kurzor = spojeni.cursor()

    nazev = "Aktualizace úkolu"
    popis = "Před aktualizací"

    kurzor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
    spojeni.commit()

    kurzor.execute("SELECT id FROM ukoly WHERE nazev = %s", (nazev,))
    ukol_id = kurzor.fetchone()[0]

    kurzor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", ("hotovo", ukol_id))
    spojeni.commit()

    kurzor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
    stav = kurzor.fetchone()[0]
    assert stav == "hotovo"

    kurzor.close()
    spojeni.close()
    smaz_testovaci_ukol(nazev)

def test_aktualizace_ukolu_negativni():
    spojeni = pripojeni_test_db()
    kurzor = spojeni.cursor()

    neexistujici_id = 999999
    kurzor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", ("hotovo", neexistujici_id))
    spojeni.commit()

    assert kurzor.rowcount == 0

    kurzor.close()
    spojeni.close()

def test_odstraneni_ukolu_pozitivni():
    spojeni = pripojeni_test_db()
    kurzor = spojeni.cursor()

    nazev = "Úkol ke smazání"
    popis = "Testovací úkol pro smazání."

    kurzor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
    spojeni.commit()

    kurzor.execute("SELECT id FROM ukoly WHERE nazev = %s", (nazev,))
    ukol_id = kurzor.fetchone()[0]

    kurzor.execute("DELETE FROM ukoly WHERE id = %s", (ukol_id,))
    spojeni.commit()

    kurzor.execute("SELECT * FROM ukoly WHERE id = %s", (ukol_id,))
    assert kurzor.fetchone() is None

    kurzor.close()
    spojeni.close()

def test_odstraneni_ukolu_negativni():
    spojeni = pripojeni_test_db()
    kurzor = spojeni.cursor()

    neexistujici_id = 999999
    kurzor.execute("DELETE FROM ukoly WHERE id = %s", (neexistujici_id,))
    spojeni.commit()

    assert kurzor.rowcount == 0

    kurzor.close()
    spojeni.close()