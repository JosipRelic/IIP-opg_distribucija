# IIP-opg_distribucija

- BAZA:
    PostgreSQL Version 16, pgadmin4

- PYTHON:
    Verzija 3.11.

- KREIRANJE VIRTUAL ENVIRONMENTA:
    1. git bash u folder od projekta
        ○ s pip freeze možemo vidjeti koji su paketi instalirani lokalno
    2. za  kreiranje virtual environmenta koristit python -m venv env naredbu unutar git bash-a, pritom env predstavlja proizvoljno ime virtual environmenta (ako virtual env nije prethodno instaliran koristimo komandu pip install virtualenv pa nakon nje python -m venv env)
    3. za aktiviranje virtual environmenta koristimo source env/Scripts/activate (ukoliko se kreiranje virtual environmenta radi na mac-u koristimo source env/bin/activate)
    4. kada smo aktivirali virtual environment instaliramo unutar njega pakete potrebne za projekt kako ne bi došlo do koflikta s paketima koji su instalirani lokalno
    5. za instaliranje potrebnih paketa u trenutnom okruženju koristimo komandu pip install -r requirements.txt (unutar requirements.txt se nalaze svi potrebni paketi za pokretanje projketa)

- INSTALACIJA I PRIPREMA BAZE LOKALNO:
    1. Instalirati postgresql verzija 16 i pgadmin4
    2. Kod kreiranja baze koristiti podatke koji se nalaze u opg_distribucija -> settings.py -> DATABASES
    3. pripremit podatke za kreiranje tablica od konfiguriranih modela sa python manage.py makemigrations
    4. migrirati tablice u bazu sa python manage.py migrate

- POKRETANJE PROJEKTA (UNUTAR ENV):
    python manage.py runserver
        

