# Domácí úkol č.2 

Program zjistí ze vstupních souborů typu `geojson` průměrnou a maximální vzdálenost k nejbližšímu veřejnému kontejneru na třízený odpad z adresních bodů. 

**Vstupy**

Vstupem jsou dva soubory typu `geojson`. První soubor s názvem `adresy.geojson` obsahuje adresní body (pracuje se s klíči `addr:street` a `addr:housenumber`) byl stáhnut z webu [Overpass Turbo](http://overpass-turbo.eu/s/119J). Druhý soubor s názvem `kontejnery.geojson` obsahuje kontejnery na třízený odpad (pracuje se s atributy `STATIONNAME` a `PRISTUP`) byl získán z [pražského Geoportálu](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB). Program ze souboru s adresama vyselektuje jejich adresy (ulice a čp) a dané souřadnice, z druhého souboru vybere kontejnery, které jsou jen volně přístupné a taktéž souřadnice. 


**Výstupy**

Program vypíše počet adresních bodů a kontejnerů, které zařadil do analýzy. Dále vypíše maximální a průměrnou vzdálenost ke kontejnerům, navíc udává i informaci, jaká je průměrná vzdálenost ke kontejnerům v případě, že do analýzy zahrne všechny kontejnery (tedy nejen ty volně přístupné, ale i kontejnery, které jsou určené jen pro obyvatele domu). 

Příklad výstupu pro městskou část Praha - Nusle:
```
Načteno adresních bodů: 2018
Načteno kontejnerů na třízený odpad: 3441 

Nejvyšší vzdálenost ke kontejneru je 282 m.
Průměrná vzdálenost ke kontejneru je 92 m.
Průměrná vzdálenost ke všem kontejnerům je 33 m.
```

