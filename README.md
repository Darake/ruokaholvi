# Ruokaholvi
Rukaholvi on keskitetty sovellus kaikkeen ruokaan liittyvään. Käyttäjä pystyy lisämään sovellukseen tuotteitansa ja reseptejään. Omien reseptien lisäksi sovelluksessa on mahdollista käyttää muiden käyttäjien reseptejä. Reseptejä näytetään 
käyttäjälle riippuen siitä, mitä tuotteita häneltä jo löytyy. Myös ostoslistojen teko on mahdollista. Tällöin kaupassa ruksatut 
tuotteet siirtyvät automaattisesti käyttäjän omiin tuotteisiin.

Ruokaholvin tavoitteisiin kuuluu myös ruokahävikin vähentäminen. Tuotteisiin voi lisätä parasta ennen päiväyksen, jolloinka sovellus näyttää käyttäjälle lähiaikoina huonoksi menevät tuotteet ja ehdottaa reseptejä, joissa tuotteita voisi käyttää. Omasta profiilista on lisäksi mahdollista seurata oman ruokahävikin määrää.  

Toimintoja:  
  * Kirjautuminen  
  * Tuotteiden lisääminen, poistaminen ja muokkaaminen  
  * Reseptien lisääminen, poistaminen ja muokkaaminen  
  * Reseptien listaus omista tuotteista  
  * Ostoslistojen luonti sekä niiden muokkaaminen  
  * Tuotteiden listaus 'parasta ennen' päivämäärän mukaan  
  * Raportti omasta ruokahävikistä  

[Käyttötapaukset](https://github.com/Darake/ruokaholvi/blob/master/documentation/User%20Stories.md)  
[Tietokantakaavio](https://github.com/Darake/ruokaholvi/blob/master/documentation/database%20diagram.png)  

[Linkki sovellukseen](https://ruokaholvi.herokuapp.com/)  
Testikäyttäjätunnukset:  
Username: user  
Password: user

## Asennusohjeet Linuxille  
### Vaatimukset:  
  * Python 3.5 tai uudempi
  * Python pip
  * Python venv
  * PostgreSQL  
  * Cloudinary ilmainen tunnus

#### Projektin lataus:  
Lataa ruokaholvin git repo zip ja purkaa se haluamasi paikkaan.  
Avaa konsoli ja siirry konsolissa purkaamasi kansion sisälle.  

#### Virtuaaliympäristö:  
Asenna virtuaaliympäristö ja aktivoi se:  
``` $ python3 -m venv venv ```  
``` $ source venv/bin/activate ```  

#### Kirjastot:  
Asenna vaaditut kirjastot:  
``` $ pip install -r requirements.txt ```

#### Määritä env muuttujat:  
Tietokannan url:  
``` & export DATABASE_URL="oma_postgresql_tietokanta_tähän" ```  
Autentikoinnin salainen avain:  
``` & export FV_SECRET_KEY="oma_salainen_avain_tähän" ```  
admin tunnuksen salasana:  
``` & export ADMIN_PASSWORD="haluamasi_salasana_tähän" ```  
Pilvipalvelun salainen url:  
``` & export CLOUDINARY_URL="cloudinary_tunnuksesi_salainen_url" ```  

#### Käynnistä sovellus:  
``` $ python3 run.py ```  
