# lahjalista
Sovellus, jolla voit ilmaista vieraillesi, mitä lahjoja toivot juhlissasi.

## Tavoite
- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- [x] Käyttäjä pystyy lisäämään sovellukseen lahjatoivelistoja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään listoja.
- [x] Käyttäjä näkee sovellukseen lisätyt lahjalistat. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämiä lahjalistoja.
- [x] Käyttäjä pystyy etsimään lahjalistoja hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä listoja.
- [x] Käyttäjä pystyy valitsemaan lahjalistalle yhden tai useamman luokittelun (esim. onko kyseessä syntymäpäivä- tai hääjuhla). Mahdolliset luokat ovat tietokannassa.
- [x] Sovelluksessa on pääasiallisen lahjalistan lisäksi toissijainen lista, joka ilmaisee, onko toinen käyttäjä ostamassa lahjaa. Käyttäjä pystyy siis ilmoittamaan ostavansa listalla toivotun lahjan.
- [x] Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät lahjalistat. Kirjautuneelle käyttäjälle näytetään lahjat, jotka käyttäjä on ilmoittanut ostavansa.

### Sovelluksen alustus
**Tietokantatiedoston luonti**
```console
sqlite3 database.db < schema.sql
```
**Luokat tietokantaan**
```console
python3 init.py
```
**Sovellus käyntiin**
```console
python3 app.py
```

## Suuri tietomäärä
Sovellukseen luodaan testidataa ajamalla
```console
python3 seed.py
```
Etusivun sivutus toimi nopeasti ilman tietokannan indeksiä 10 000:lla käyttäjällä, 1 000 000 lahjalistalla ja 10 000 000 lahjalla. Sivujen vaihtamiseen meni aikaa 0.0 - 0.22 sekuntia.
