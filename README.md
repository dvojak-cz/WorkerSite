# Worker Site
Worker Site je webová aplikace pro správu pracovních výkazů

## Spuštění
### Prostedí
Aby byla aplikace funkční, jen úptřeba nastavit virtuální prostředí.
Virtuální prostředí nasatvíte spuštěním následujících příkazů:
```shell
python3 -m venv __venv__
source __venv__/bin/activate
pip3 install -r requirements.txt
```
### Rozběhnutí aplikace
Pro nastartování aplikace použijte následující příkazy:
```shell
python3 manage.py runserver
```
### Testy
Pro spuštění testu zadejte následující příkaz do příkazové řádky
```shell
python3 manage.py test
```

## Informace o ukázkových uživatelých
V aplikaci existují následující uživatelé.

    HaslarJan:
        username:   HaslarJan
        password:   abublina1
        groups:     ['woker']
        superuser:  False

    SolfronkMartin:
        username:   SolfronkMartin
        password:   abublina1
        groups:     ['woker', 'admin']
        superuser:  False

    TrojakJan:
        username:   TrojakJan
        password:   abublina1
        groups:     ['woker', 'admin']
        superuser:  True    (has access to admin site '.../admin')

V případě, že by se sample data nějakým způsobem pokazila, stačí si z gitu naklonovat originální databázi (jedná se o soubor db.sqlite3)

---
## Rychlé vysvětlení základních sekcí pro lepší orientaci

### Login page [.../](http://localhost:8000/)
Tato stránka slouží pro přihlášení se do aplikace. V případě, že uživatel zapomene heslo, může si ho kliknutím na odkaz resetovat.
![Login page](./img/login.png)
### Dash Board [.../report/](http://localhost:8000/report/)
Stránka slouží jako rychlý přehed pro uživatele. Najde zde základní grafy, rychlé součty a rychlé přehledové tabulky.

![Dash Board page](./img/dashBoard.png)
### Přehled [.../report/over_view/](http://localhost:8000/report/over_view/)
Zde najde uživatel kompletní data o dříve podaných výkazech. Data se dají filtrovat za pomocí formuláře v horní části obrazovky.

Z této stránky lze generovat dokumenty. Konkrétně lze aktuálně zobrazený přehled exportovat do formátu *pdf*, nebo *csv*.

Zároveň lze z této stránky editovat, mazat a klonovat již vytvořené výkazy. Toto lze provádět pomocí tlačítek v sekci operace. V případě, že přihlášený uživatel není administrátor, tak může upravovat a mazat pouze své reporty.

![Report page](./img/reports.png)
### Přidat nový záznam [.../report/new/](http://localhost:8000/report/new/)
V této sekci lze vytvořit nový pracovný výkaz. Jediné omezení pro výkaz je pro ne-admin uživatele, kteří nemohou vykazovat práci jiným užiavetlům.

![New report page](./img/new_report.png)
### Přidat nový project [.../report/new_project/](http://localhost:8000/report/new_project/)
Tato stránka slouží pouze k rychlému přidávání projektů do aplikace.

### Admin stránka [.../admin/](http://localhost:8000/admin)
Tato stránka slouží k administraci aplikace. Plná práva má pouze uživatel, který je označen jako superuser.

Na této stránce lze editovat data uložená v databázi
![Adimn page](./img/admin.png)