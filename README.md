Projekt "Spravce ukolu" se sklada ze dvou casti:
1. Aplikace "task_manager.py" slouzi ke sprave ukolu s ulozenim do databaze MySQL "ukoly".
2. Testy "task_manager_test" nad databazovou tabulkou v MySQL "ukoly" s vyuzitim pytestu.

V obou souborech je pouzito pripojeni:
- user: "root"
- password: "K4d1budk487!"
- host: "localhost"

Tabulka "ukoly" se vytvori pri prvnim spusteni aplikace "task_manager.py" i pri behu testu pomoci pytestu. Obe casti projektu vyuzivaji prikaz "CREATE TABLE IF NOT EXISTS", cimz se zabrani opakovanemu vytvareni tabulky.

Aplikace pouziva databazi "task_manager", testy "task_manager_test".

= = = = =

Aplikace "task_manager.py"
Textove menu aplikace umoznuje:
- Pridani noveho ukolu
- Zobrazeni aktivnich ukolu
- Aktualizaci stavu ukolu
- Odstraneni ukolu
- Ukonceni programu

- Oddelena logika od vstupu/vystupu ("input()" a "print()" jsou pouzite pouze v hlavnim menu).
- Osetreni chybnych ID a neplatnych stavu (mj. nezobrazi jiz splnene ukoly ve stavu "hotovo").
- Funkce jsou testovatelne samostatne.

Spusteni aplikace probiha pres terminal prikazem "python task_manager.py" nebo tlacitkem "Run Python File".

= = = = =

Testy "task_manager_test" zahrnuji:
- Pouziti funkce "@pytest.fixture" pro automaticke pripojeni a vytvoreni tabulky.
- Automaticke cisteni dat po testech.
- Praci s realnym pripojenim k testovaci databazi.

Struktura kodu obsahuje testy jednotlivych funkcionalit tabulky "ukoly":
- Test pridani ukolu (pozitivni i negativni).
- Test aktualizace stavu ukolu (pozitivni i negativni).
- Test odstraneni ukolu (pozitivni i negativni).

Spusteni testu je doporuceno pres terminal rozsirenym prikazem "pytest task_manager_test.py -v". Priznak/prepinac "-v" (verbose) v prikazu zobrazi podrobnejsi vystup, tj. nazev kazdeho testu a jeho vysledek (passed, failed, atd.), misto pouze strucneho shrnuti za pouziti zakladniho prikazu "pytest task_manager_test.py".

Vysledna data se po kazdem behu testu smazou (doporuceno dle zadani projektu).

= = = = =

Poznamky:
- Opakujici se casti kodu v predchozi odevzdane verzi projektu byly nahrazeny pomocnymi funkcemi, tj. byl proveden refaktor kodu.
- Pro pripojeni do databaze pouzita funce "@pytest.fixture".
- Pouziti "dictionary=True" pro lepsi citelnost vysledku.
- Osetreni pozitivnich i negativnich pripadu.
- Pouziti "fixture" a "yield" pro pripojeni a uklid testovaci databaze.
