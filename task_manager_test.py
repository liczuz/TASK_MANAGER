import mysql.connector
import pytest
from datetime import datetime

@pytest.fixture(scope="module")
def test_db():
    spojeni = mysql.connector.connect(
        host="localhost",
        user="root",
        password="K4d1budk487!",
        database="task_manager_test"
    )
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
    yield spojeni
    kurzor.execute("DELETE FROM ukoly")
    spojeni.commit()
    kurzor.close()
    spojeni.close()

@pytest.fixture
def vloz_ukol(test_db):
    def _vloz(nazev, popis):
        kurzor = test_db.cursor()
        kurzor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
        test_db.commit()
        kurzor.execute("SELECT id FROM ukoly WHERE nazev = %s", (nazev,))
        return kurzor.fetchone()[0]
    return _vloz

def test_pridani_ukolu_pozitivni(test_db):
    nazev = "Testovací úkol"
    popis = "Testovací popis"
    kurzor = test_db.cursor(dictionary=True)

    kurzor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
    test_db.commit()

    kurzor.execute("SELECT * FROM ukoly WHERE nazev = %s", (nazev,))
    vysledek = kurzor.fetchone()
    assert vysledek is not None
    assert vysledek["nazev"] == nazev
    assert vysledek["popis"] == popis

def test_pridani_ukolu_negativni(test_db):
    nazev = "X" * 999
    popis = "Příliš dlouhý název"
    kurzor = test_db.cursor()
    with pytest.raises(mysql.connector.Error):
        kurzor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
        test_db.commit()

def test_aktualizace_ukolu_pozitivni(test_db, vloz_ukol):
    ukol_id = vloz_ukol("Aktualizace", "Test")
    kurzor = test_db.cursor()
    kurzor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", ("hotovo", ukol_id))
    test_db.commit()

    kurzor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
    stav = kurzor.fetchone()[0]
    assert stav == "hotovo"

def test_aktualizace_ukolu_negativni(test_db):
    kurzor = test_db.cursor()
    kurzor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", ("hotovo", 123456))
    test_db.commit()
    assert kurzor.rowcount == 0

def test_odstraneni_ukolu_pozitivni(test_db, vloz_ukol):
    ukol_id = vloz_ukol("Smazat", "Test")
    kurzor = test_db.cursor()
    kurzor.execute("DELETE FROM ukoly WHERE id = %s", (ukol_id,))
    test_db.commit()

    kurzor.execute("SELECT * FROM ukoly WHERE id = %s", (ukol_id,))
    vysledek = kurzor.fetchone()
    assert vysledek is None

def test_odstraneni_ukolu_negativni(test_db):
    kurzor = test_db.cursor()
    kurzor.execute("DELETE FROM ukoly WHERE id = %s", (123456,))
    test_db.commit()
    assert kurzor.rowcount == 0