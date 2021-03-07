# gaming-event-planner - tsoha-harjoitustyö

## Sisällysluettelo

- [Sisällysluettelo](#sisällysluettelo)
    - [Kuvaus](#kuvaus)
    - [Käyttö](#käyttö)
        - [Ryhmän luonti](#ryhmän-luonti,-siihen-liittyminen-ja-kaveripyynnöt)
        - [Tapahtuman luonti](#tapahtuman-luonti)
        - [Tapahtumakäyttöliittymä](#tapahtumakäyttöliittymä)
    - [Asennus](#asennus)
        - [Asennus ja ajo lokaalisti](#asennus-ja-ajo-lokaalisti)
        - [Asennus ja ajo Herokussa](#asennus-ja-ajo-herokussa)
    - [Toiminnallisuudet](#toiminnallisuudet)
    - [Taulut](#taulut)
## Kuvaus

Websovellus peli-iltojen suunnitteluun. Sovelluksella voi sopia ryhmien kesken peliaikoja ja valita pelattavia pelejä.

Sovellusta voi testata [täällä](https://gaming-event-planner.herokuapp.com/).

## Käyttö

Sivun käyttäminen vaatii javascriptin päälläolon. Sivun käyttämisen voi aloittaa luomalla käyttäjän 'sign up' -napista.

### Ryhmän luonti, siihen liittyminen ja kaveripyynnöt

'My groups' -paneelissa on 'create or join group' -nappi. Tämän kautta voi sekä luoda ryhmiä että lähettää liittymispyyntöjä niihin. Jos ryhmän nimi on vapaa, ryhmä luodaan suoraan. Jos taas ryhmän nimi on jo käytössä, lähetetään ryhmään liittymispyyntö jonka ryhmän luojan pitää hyväksyä.

Kaveripyyntöjen lähettäminen toimii samalla logiikalla. (dialogi ei herjaa jos pyynnön lähettää olemattomalle käyttäjälle, tämä on tietoinen valinta)

Pyynnön hyväksyminen näkyy käyttöliittymässä refreshin jälkeen.

### Tapahtuman luonti

Tapahtumaa luodessa valitaan ensin, valitaanko tapahtuman peli suoraan vai annetaanko käyttäjien äänestää pelattavaa peliä. Jälkimmäistä ominaisuutta en ehtinyt toteuttaa loppuun, joten se on lukittuna käyttöliittymässä.

Pelin valinnan jälkeen tapahtumalle valitaan nimi, päättymispäivä sekä käyttäjäryhmä. Päättymispäivä rajaa päiviä joille sopivia pelihetkiä voi ehdottaa, sekä poistaa tapahtuman käyttöliittymästä kun päivä saavutetaan.

Käyttäjäryhmässä customryhmän valinta lähettää tapahtumasta kutsut kaikille ryhmään nyt tai myöhemmin kuuluville, kun taas 'friends' -ryhmän valitessa kutsut täytyy lähettää manuaalisesti.

### Tapahtumakäyttöliittymä

Sekä ryhmätapahtumakutsut, että manuaaliset kutsut ilmestyvät 'open invites' -paneeliin. Kutsun hyväksymisen jälkeen tapahtumasta syntyy painike tapahtumakäyttöliittymän avaamiseen, 'upcoming events' -paneeliin. Itse luodut tapahtumat taas siirtyy 'My events' -paneeliin.

Tapahtumakäyttöliittymässä tavallinen käyttäjä pystyy lisäämään tapahtumaan kommentteja, sekä ilmoittamaan päiviä ja tunteja jolloin tapahtumaan osallistuminen sopisi.

Ajankohtaäänestyksen saa auki 'date' -nappia painamalla. Käyttäjän lisättyä ensimmäisen ajankohdan, lisätty ajankohta syntyy käyttöliittymään painikkeena jolla voi nopeasti kopioida lisätyn päivämäärän lisäyskäyttöliittymään, päivien lisäilyn nopeuttamiseen.

Ajankohtaäänestykset päivittyy 'overlapping dates' -paneeliin, joka näyttää top-5 parasta ajankohtaa tapahtumalle päivän tunneiksi jaettuna heatmappina. Mitä kirkkaampi vihreä heatmapissa, sitä useampi käyttäjä on äänestänyt kyseistä ajankohtaa sopivaksi. Top-5 listan järjestelyperuste on 1) järjestely suurimman osallistujamäärän mukaan päällekäisissä ajankohdissa, 2) järjestely ihmistuntien mukaan per päivä.

Jos on tapahtuman luoja, käyttäjälle näkyy myös erillinen hallintapaneeli. Hallintapaneelista pystyy muuttamaan tapahtuman kuvausta ja päättymispäivää (sekä suodatinta joka rajaa tapahtuman näkyvyyttä käyttäjille peliäänestysten perusteella, tämä ominaisuus on vielä toteuttamatta). Hallintapaneeliin avautuu myös näkymä käyttäjien kutsumiseen kaverilistalta, jos tapahtuman ryhmäksi on asetettu 'friends'.

## Jatkokehitys

Pelipreferensseistä äänestäminen jäi toteuttamatta, mikä olisi ollut hyvä lisä tapahtumien suunnitteluun. Jos pelaajien pelitottumuksia voisi aggregoida, tapahtumien kutsuja voisi rajata vain tapahtuman pelistä kiinnostuneille. Vastaavasti tapahtumissa joissa pelistä äänestetään, äänestysvaihtoehtoja voisi rajata siten että saadaan tapahtumaan mahdollisimman laaja osallistujamäärä.

Sivun frontend alkaa jo olla vaikeasti ylläpidettävä, joten sen voisi uudelleentoteuttaa esimerkiksi reactilla. Sivun front- ja backendiin voisi myös lisätä tuen socketeille, jolloin muiden käyttäjien tekemiä muutoksia olisi helpompi päivittää muille yhdistäneille käyttäjille.

## Asennus

### Asennus ja ajo lokaalisti

Lataa repositorio ja siirry sen juureen

    git clone https://github.com/sainigma/gaming-event-planner.git
    cd gaming-event-planner/

Luo ja säädä .env tiedosto, joka sijaitsee polussa /gaming-event-planner/backend/:in juuressa. Sovelluksen ajaminen vaatii todennuksen Internet Games Databasen rajapintaan. [Ohjeet IGDB authin hakemiseen](https://api-docs.igdb.com/#about).

.env tiedoston rakenne:

    SECRET=salaisuusTähän
    DATABASE_URL=postgresql://jne
    SQL=psql
    DEBUG=0
    IGDBID=igdbidtähän
    IGDBKEY=igdbavaintähän

SQL muuttujan ollessa sqlite, sovellus ajetaan sqlite3:lla, jolloin sovellusta voi ajaa ilman postgresql-asennusta. Debug muuttujan ollessa 1, sovelluksen tietokantapyynnöt logataan komentolinjalle. SQL muuttujan ollessa sqlite ja Debug muuttujan ollessa 1, sovellus täyttää tietokannan dummy-arvoilla jotka on määritetty [täällä](./backend/database/dummy.db).

Jos käytät sovelluksessa postgresql -tietokantaa, määritä sen yhdistysosoite .env-muuttujaan.

Anna ajoskriptalle ajo-oikeudet ja aja se:

    chmod +x ./backend/run.sh
    ./backend/run.sh

Jos käyttöön määritetty tietokanta on sqlite, sen sisältö poistetaan kun sovelluksen ajo päättyy.

### Asennus ja ajo Herokussa

Lataa repositorio, mene sen juureen, luo sille herokuappi ja liitä sen remote projektiin:

    git clone https://github.com/sainigma/gaming-event-planner.git
    cd gaming-event-planner/
    heroku create apps:create sovelluksennimi
    heroku git:remote -a sovelluksennimi

Asenna postgresql addon herokuun ja lisää schema:

    heroku addons:create heroku-postgresql
    heroku psql < ./backend/schema.sql

Määritä ympäristömuuttujat:

    heroku config:set SECRET=salaisuustähän
    heroku config:set IGDBID=idtähän
    heroku config:set IGDBKEY=avaintähän
    heroku config:set SQL=psql
    heroku config:set DEBUG=0

Pushaa projekti herokuun:

    git push heroku HEAD:master

## Toiminnallisuudet

- Käyttäjien luonti, kirjautuminen, keksillä kirjautuminen
- Käyttäjäryhmät, ryhmäoikeudet
- Käyttäjärelaatiot
- Tapahtumia voi järjestää ryhmille tai kavereille
- Tapahtumat ovat aktiivisia rajallisen aikaa
- Tapahtumassa on viestiketju
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
    - Tapahtuman epäaktivoituminen ja arkistointi

## Taulut

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
    - IGDB id
    - cachetettu sisältö

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