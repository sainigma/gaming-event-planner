# tsoha-harjoitustyo

## Sisällysluettelo

- [Sisällysluettelo](#sisällysluettelo)
    - [Kuvaus](#kuvaus)
    - [Asennus](#asennus)
        - [Asennus ja ajo lokaalisti](#asennus-ja-ajo-lokaalisti)
        - [Asennus ja ajo Herokussa](#asennus-ja-ajo-herokussa)
    - [Dokumentaatio](#dokumentaatio)
        - [Perustoiminnallisuudet](#perustoiminnallisuudet)
        - [Taulut](#taulut)
        - [Jatkokehitys](#jatkokehitys)

## Kuvaus

Websovellus peli-iltojen suunnitteluun. Sovelluksella voi sopia ryhmien kesken peliaikoja ja valita pelattavia pelejä.

### Sovelluksen nykytilanne

Sovelluksessa toimii tällä hetkellä kirjautuminen, tapahtumien luonti, käyttäjien kutsuminen tapahtumaan, tapahtumakutsun hyväksyminen, pelien haku tietokannasta sekä tapahtuman kommentointi.

Testailua varten käyttäjä/salasanakombinaation voi tarkastaa [täältä](./backend/database/dummy.json). Tapahtumaan voi kutsua tällä hetkellä vain kaverilistalta. Koska kaverilistan laajentamiseen ei ole vielä käyttöliittymää, debugkäyttäjistä Alice ja Carol ovat asetettu valmiiksi kavereiksi.

Kriittisiä puuttuvia ominaisuuksia tällä hetkellä ovat:
 - Käyttäjien luonti
 - Kaverilista
 - Ryhmien luonti
 - Äänestyskäyttöliittymä päivämäärille ja peliehdotuksille
 - Admintyökalut tapahtumille

Sovellusta voi testata [täällä](https://gaming-event-planner.herokuapp.com/).

## Asennus

### Asennus ja ajo lokaalisti

Lataa repositorio ja siirry sen juureen

    git clone https://github.com/sainigma/gaming-event-planner.git
    cd gaming-event-planner/

Luo ja säädä .env tiedosto, joka sijaitsee polussa /gaming-event-planner/backend/:in juuressa. Sovelluksen ajaminen vaatii todennuksen Internet Games Databasen rajapintaan. [Ohjeet IGDB authin hakemiseen](https://api-docs.igdb.com/#about).

    echo SECRET=salasanaTähän >> ./backend/.env
    echo IGDBID=IGDBidTähän >> ./backend/.env
    echo IGDBKEY=IGDBavainTähän >> ./backend/.env

Anna ajoskriptalle ajo-oikeudet ja aja se:

    chmod +x ./backend/run.sh
    ./backend/run.sh

### Asennus ja ajo Herokussa

Lataa repositorio, mene sen juureen, luo sille herokuappi ja liitä sen remote projektiin:

    git clone https://github.com/sainigma/gaming-event-planner.git
    cd gaming-event-planner/
    heroku create apps:create sovelluksennimi
    heroku git:remote -a sovelluksennimi

Määritä ympäristömuuttujat:

    heroku config:set SECRET=salasanatähän
    heroku config:set IGDBID=idtähän
    heroku config:set IGDBKEY=avaintähän

Pushaa projekti herokuun:

    git push heroku HEAD:master    

## Dokumentaatio

### Perustoiminnallisuudet

- Käyttäjien luonti, kirjautuminen, keksillä kirjautuminen
- Käyttäjäryhmät, ryhmäoikeudet
- Käyttäjärelaatiot
- Tapahtumat voivat olla ryhmäkohtaisia tai julkisia
- Tapahtumat ovat aktiivisia rajallisen aikaa
- Tapahtumaan voi liittyä viestiketju
    - Viestien replyhaarautuminen
- Tapahtumia voi suunnitella joko peli- tai käyttäjävetoisesti
    - Pelivetoisessa tapahtumasuunnittelussa tapahtuman luoja ohittaa pelistä äänestyksen, ja kutsun tapahtumaan voi lähettää vain käyttäjille jotka eivät ole opt-outanneet kyseisen pelin pelaamisesta
    - Käyttäjävetoisessa tapahtumasuunnittelussa tapahtumaan voi valita pelin vain peleistä joista tapahtumaan kutsutut käyttäjät eivät ole opt-outanneet
        - Opt-outin määritelmän voi valita tapahtumaa luodessa
            - Opt-out = halukkuus pelata peliä tiettyä raja-arvoa pienempi tai korkeampi. Jälkimmäisessä tapauksessa tapahtumasta suljetaan peliä fanittavat pois ja tapahtumaan kutsutaan vain pelaajat jotka eivät absoluuttisesti halua pelata peliä (esim. case mario party tai monopoli)
- Normaali kulku tapahtumalle:
    - Tapahtuman luonti
    - (jos pelivetoinen suunnittelu) Pelin valinta
    - Käyttäjien kutsuminen
    - (jos käyttäjävetoinen suunnittelu) Pelattavasta pelistä äänestys
    - Peliajasta äänestys
    - Tapahtuman epäaktivoituminen ja arkistointi (joko manuaalisesti tai ajan perusteella)

### Taulut

- Käyttäjät
    - id
    - nimimerkki
    - salasanahash

- Keksit
    - Käyttäjän id
    - verifikaatiotunnus
    - timeout

- Käyttäjärelaatiot
    - käyttäjän id
    - kohteen id
    - relaatiotyyppi

Tyypit, 1 = kaveri, 0 = blokattu. Kaveruus vaatii kummaltakin käyttäjältä saman relaatiotyypin, blokkaukseen riittää merkintä vain toiselta. Kaveruuden poisto ei merkitse relaatiota nollaksi, vaan poistaa tietueen.

- Halukkuus pelata peliä -taulu
    - käyttäjän id
    - pelin id
    - liukuasteikko pelin pelaamishalukkuudelle, 0-10

Opt-out mekanismin kannalta oletan että pelin pelaamishalukkuudella ja taitotasolla pelissä on suora korrelaatio. Muutoin taitotason voisi ottaa erilliseksi lisäkentäksi.

- Viestit
    - id
    - juuri id (esim ryhmä, tapahtuma, käyttäjä tai toinen viesti)
    - lähettäjän id
    - sisältö
    - timestamp

- Pelit
    - id
    - nimi
    - GiantBomb id
    - cachetettu sisältö

Pelaajien maksimimäärä olisi nice-to-have ominaisuus pelien filtteröintiin, tätä tietoa ei vaan saa suoraan ulos giantbombin apista/määritelmä hämärtyy entisestään kun ottaa huomioon että peleissä pelaajamäärät vaihtelee pelimuodon mukaan

- Tapahtumat
    - id
    - luojan id
    - ryhmän id
    - nimi
    - kuvaus
    - luontiaika
    - aktiivisuusaika
    - opt-out alempi raja-arvo
    - opt-out ylempi raja-arvo

- Kutsut
    - tapahtuman id
    - käyttäjän id

Jos käyttäjä peruu/hyväksyy kutsun tapahtumaan, kutsu poistetaan taulusta. Hyväksymisen tapauksessa Liittymiset - tauluun lisätään merkintä.

- Liittymiset
    - käyttäjän id
    - tapahtuman id

- Peliäänestykset
    - äänestäjän id
    - tapahtuman id
    - pelin id
    - äänestys, liukuluku 0-10

Äänestyksiä voi tehdä yhteen tapahtumaan rajattomasti, kuitenkin siten että yhdestä pelistä on kultakin käyttäjältä vain yksi ääni

- Päivämäärä-äänestykset
    - äänestäjän id
    - tapahtuman id
    - päivämäärä
    - kellonaika (tunnin tarkkuudella)

- Ryhmät
    - id
    - nimi

- Ryhmäjäsenyydet
    - käyttäjän id
    - kutsujan id
    - ryhmän id
    - käyttäjäryhmä
    - kuitattu

Jäsenyys vaatii kutsujan ja kuittauksen. Jos käyttäjä hakee ryhmän jäsenyyttä, jäsenyys vaatii "kutsun" moderaattorilta tai adminilta. Jos käyttäjä kutsutaan ryhmään, jäsenyys vaatii kuittauksen käyttäjältä. Käyttäjäryhmät 0 = jäsen, 1 = moderaattori, 2 = admin

- Discordkäyttäjät
    - discord id
    - käyttäjä id
    - discord tili tunnistettu

- Discordkanavat
    - ryhmän id
    - kanavan nimi
    - tapahtuman id

### Jatkokehitys

Web-käyttöliittymän tueksi discord-botti, jolla voi päivittää kanaville/käyttäjille tapahtumasuunnittelun ja äänestyksien etenemistä.