# Asennusohjeet Linuxille  
## Vaatimukset:  
  * Python 3.5 tai uudempi
  * Python pip
  * Python venv
  * PostgreSQL  
  
#### Pikaopas PostgreSQL tietokannan asetukseen:  
``` $ sudo apt-get update```  
``` $ sudo apt-get install postgresql postgresql-contrib```  
``` $ sudo -i -u postgres```  
``` $ psql```  
Korvaa password haluamallasi salasanallasi  
``` $ ALTER USER postgres WITH ENCRYPTED PASSWORD 'password';```  
Korvaa tietokannan_nimi haluamallasi tietokannan nimellä  
``` $ create database tietokannan_nimi;```  
``` $ \q```  

## Asennus:  

### Projektin lataus:  
Lataa ruokaholvin git repo zip ja purkaa se haluamasi paikkaan.  
Avaa konsoli ja siirry konsolissa purkaamasi kansion sisälle.  

### Virtuaaliympäristö:  
Asenna virtuaaliympäristö ja aktivoi se:  
``` $ python3 -m venv venv ```  
``` $ source venv/bin/activate ```  

### Kirjastot:  
Asenna vaaditut kirjastot:  
``` $ pip install -r requirements.txt ```

### Määritä tietokannan env muuttuja:  
``` export DATABASE_URL="oma_postgresql_tietokanta_tähän" ```  
Tietokannan muuttuja on muotoa  
postgresql://postgres:salasana@localhost/tietokannan_nimi ,
jossa salasana on oma postgres käyttäjälle määrittämä salasana ja tietokannan_nimi tietokanta, jota aijot käyttää.

### Käynnistä sovellus:  
``` $ python3 run.py ```  

# Käyttö:  
Käytä admin tunnuksia tai rekisteröi uusi käyttäjä.  
Admin tunnarit ovat oletuksena dev-puolella:  

admin  
salasana  

Ohjelmisto on tarkoitettu pitämään kirjaa omista ruoka-asioista.  
Käyttäjät pystyvät lisämään ja näkemään oman jääkaappinsa sisällön sovelluksen 'My items' osiossa. Lisäyksen yhteydessä voi myös lisätä tuotteen parasta ennen päiväyksen, joka vaikuttaa tuotteiden järjestykseen näkymässä. Näin pysyt kärryillä, mikä on lähiaikoina menossa vanhaksi. Tuotteita voi myös poistaa tai merkitä käytetyksi/vanhaksi menneeksi. Näillä on käytännön eroa tulevaisuudessa, kun sovellukseen tulee statistiikkaa omasta ruokahävikistä.  

Käyttäjät pystyvät myös lisämään reseptejä 'New recipe' osiossa. Ensin lisätään reseptin nimi, ohjeet sekä kuvan, mikäli semmoisen haluaa lisätä. Kun nämä on lisätty ja painetaan 'Next' päästään raakaine osioon, jossa voidaan lisätä reseptin raaka-aineita ja vapaaehtoisesti määrän yksi kerrallaan. Painamalla 'Complete' reseptin teko on valmis.  

Kaikki sivuston reseptit näkyvät 'Recipes' osiossa. Reseptit ovat järjestetty käyttäjän tuotteidena mukaan. Jokaisen reseptin kohdalla myös näkee, kuinka monta reseptin raaka-aineista käyttäjällä jo on. Klikkaamalla haluttua reseptiä pääsee katsomaan reseptiä tarkemmin. Tässä osiossa reseptin tekijä ja adminit pysyvät myös muokkaamaan tai poistamaan reseptiä. Reseptin muokkauksessa käytetään samaa näkymää kuin sen luomisessa.  

'My items' osioissa clickaamalla jotain tiettyä raaka-ainetta pääse listaukseen, missä näyetetään vain ne reseptit, jotka käyttävät kyseistä raaka-ainetta.
