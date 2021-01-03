# Domácí úkol č.2 

Program zjistí ze vstupních souborů typu `geojson` průměrnou a maximální vzdálenost k nejbližšímu veřejnému kontejneru na třízený odpad z adresních bodů. 

**Vstupy**

Vstupem jsou dva soubory typu `geojson`. První soubor s názvem `adresy.geojson` obsahuje adresní body (pracuje se s klíči `addr:street` a `addr:housenumber`) byl stáhnut z webu [Overpass Turbo](http://overpass-turbo.eu/s/119J). Druhý soubor s názvem `kontejnery.geojson` obsahuje kontejnery na třízený odpad (pracuje se s atributy `STATIONNAME` a `PRISTUP`) byl získán z [pražského Geoportálu](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB). Program ze souboru s adresama vyselektuje jejich adresy (ulice a čp) a dané souřadnice, z druhého souboru vybere kontejnery a jejich adresy, souřadnice a druh přístupu (volně přístupné / obyvatelům domu). 

Souřadnicové systémy vstupních souborů:
- adresy.geojson : `WGS-84 (4326)`
- kontejnery.geojson: `S-JTSK (5514)`


**Výstupy**

Program vypíše počet adresních bodů a kontejnerů, které zařadil do analýzy. Dále vypíše maximální a průměrnou vzdálenost ke kontejnerům, navíc udává i informaci o mediánu. Statistika (maximum, medián a průměr) počítá jak s kontejnery volně přístupnými, tak kontejnery, které jsou přístupné pouze pro obyvatele domu. Pokud se shoduje adresa domu s adresou kontejneru, který je přístupný pouze pro obyvatele domu, program nastaví hodnotu vzálenosti jako 0 metrů. Výstup je ošetřen i pro podezřelá vstupní data, tedy pokud minimální vzálenost přesáhne 10 km, dostane uživatel upozornění a program se ukončí. 

Příklad výstupu pro městskou část Praha - Nusle:
```
Načteno adresních bodů: 2018
Načteno kontejnerů na třízený odpad: 3441 

Nejvyšší vzdálenost ke kontejneru je 282 m.
Průměrná vzdálenost ke kontejneru je 92 m.
Průměrná vzdálenost ke všem kontejnerům je 33 m.
```

Poznámka:
*Pro sestavení kódu bylo využito rozšíření pro Visual Studio Code [`Better Comments`](https://marketplace.visualstudio.com/items?itemName=aaron-bond.better-comments), které zvýrazňuje komentáře dle příšlušného znaku za `křížkem (#)`. Tyto znaky však neplní žádnou jinou funkci, než větší přehlednost kódu při používání tohoto rozšíření.*

**Autor:**
- Petr Janoš
- čtvrtý ročník BSGG
- obor Sociální geografie a geoinformatiky