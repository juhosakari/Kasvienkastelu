## Kasvienkastelu
Munkan kasvienkastelu projekti

Asennus:
  -Lataa uusin versio githubista
  -asenna python3 ja tarvittavat krjastot (requirements.txt)
  -Käynnistä pigpiod (sudo pigpiod) ja aseta se automaattisesti käynnistyväksi
  -Määritä flask_app ympäristö muuttuja (export FLASK_APP=run_app.py)
  -Luo tietokanta (flask db upgrade)
  -Luo käyttäjät (python3 create_user.py)
  -Käynnistä ohjelma (python3 run_app.py)
