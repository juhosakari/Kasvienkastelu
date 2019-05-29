## Kasvienkastelu
Munkan kasvienkastelu projekti

Asennus:
  1. Lataa uusin versio githubista
  2. asenna python3 ja tarvittavat krjastot (requirements.txt)
  3. Käynnistä pigpiod (sudo pigpiod) ja aseta se automaattisesti käynnistyväksi
  4. Määritä flask_app ympäristö muuttuja (export FLASK_APP=run_app.py)
  5. Luo tietokanta (flask db upgrade)
  6. Luo käyttäjät (python3 create_user.py)
  7. Käynnistä ohjelma (python3 run_app.py)
