import json, os, sys
from math import sqrt, inf
from pyproj import CRS, Transformer

def nahraj_geojson(jmeno_souboru):
    """ Načte soubor typu geojson a ošetří nekorektní vstupy. """
    try:
        with open(os.path.join(sys.path[0], jmeno_souboru+".geojson"), "r", encoding="UTF-8") as file:
                data = json.load(file)

    except FileNotFoundError:
        print(f"Soubor {jmeno_souboru} nebyl nenalezen.")
        exit()
    except ValueError:
        print(f"Soubor {jmeno_souboru} je chybný.")
        exit()
    except PermissionError:
        print(f"Soubor {jmeno_souboru} není přístupný. Povolte přístup.")
        exit()

    return data 

def data_kontejnery(kontejnery):
    """ Vytvoří slovník pro volně přístupné kontejnery [adresa:souřadnice]. """

    dic_kontejnery = {} 

    for k in kontejnery:
        k_adresa = k["properties"]["STATIONNAME"]
        k_geo = k["geometry"]["coordinates"]
        k_pristup = k["properties"]["PRISTUP"]

        if k_pristup == "volně":
            dic_kontejnery[k_adresa] = k_geo

        
    if len(dic_kontejnery) == 0:
        print("Chyba: do slovníku nebyl přidán žádný záznam. Program končí.")
        exit()

    return dic_kontejnery

def data_adresy(adresy):
    """ Vytvoří slovník pro adresní body [adresa:souřadnice] a převede je na S-JTSK"""

    dic_adresy = {}

    for a in adresy:
        a_ulice = a["properties"]["addr:street"]
        a_cp = a["properties"]["addr:housenumber"]
        a_geo_wgs = a["geometry"]["coordinates"]

        #? WGS » S-JTSK
        # nutnost použít crs a transformer z pyproj2 (náhrada pyproj1)
        wgs = CRS.from_epsg(4326)  # WGS-84
        jtsk = CRS.from_epsg(5514)  # S-JTSK
        wgis_jtsk = Transformer.from_crs(wgs, jtsk)

        a_geo_jtsk = wgis_jtsk.transform(a_geo_wgs[1], a_geo_wgs[0])
        a_adresa = a_ulice + " " + a_cp
 
        dic_adresy[a_adresa] = a_geo_jtsk
    
    if len(dic_adresy) == 0:
        print("Chyba: do slovníku nebyl přidán žádný záznam. Program končí.")
        exit()

    return dic_adresy

def vypocet_vzdalenosti(x1, x2, y1,y2):
    """ Obecná funkce pro výpočet vzdálenosti ze souřadnic dvou bodů pomocí Pythagorovy věty. """

    a = abs(x1 - y1)
    b = abs(x2 - y2)
    c = sqrt((a*a) + (b*b))

    return c

def nejblizsi(dic_kontejnery, dic_adresy):
    """ Pro každou adresu hledá nejkratší vzdálenost ke kontejneru. """

    dic_vzdalenosti = {}

    # Projíždí každou adresu ze souboru
    for (a_adresa, a_geo) in dic_adresy.items():
        adresa_x = a_geo[0]
        adresa_y = a_geo[1]

        min_vzdalenost = inf  # původní minimální vzdálenost je nekonečno (inf)
        
        # projíždí každý kontejner ze souboru
        for k_geo in dic_kontejnery.values():
            kontejner_x = k_geo[0]
            kontejner_y = k_geo[1]

            # vypočte vzdálenost pro každý kontejner od dané adresy
            vzdalenost = vypocet_vzdalenosti(adresa_x, adresa_y, kontejner_x, kontejner_y)
            # pokud je vzdálenost menší než minimální, přepíše se
            if min_vzdalenost > vzdalenost:
                min_vzdalenost = vzdalenost

        dic_vzdalenosti[a_adresa] = min_vzdalenost
    
    return dic_vzdalenosti

def prumerna_vzdalenost(dic_value, dic_len):
    """ PASS """

    avg = int(sum(dic_value.values()) / len(dic_len))

    return avg

# ? načtení vstupních dat 
kontejnery_json = nahraj_geojson("kontejnery")["features"]
adresy_json = nahraj_geojson("adresy")["features"]

# ? vytvoření slovníků s určitými proměnnými ze vstupních geojson souborů
dic_kontejnery = data_kontejnery(kontejnery_json)
dic_adresy = data_adresy(adresy_json)

# ? nalezení nejmenších vzáleností
nejkratsi_vzdalenosti = nejblizsi(dic_kontejnery, dic_adresy)

# ! VÝSTUP PROGRAMU
print("Načteno adresních bodů:", len(dic_adresy))
print("Načteno kontejnerů na třízený odpad:", len(dic_kontejnery), "\n")
print("Nejvyšší vzdálenost ke kontejneru je", int(max(nejkratsi_vzdalenosti.values())), "m.")
print("Průměrná vzdálenost ke kontejneru je", prumerna_vzdalenost(nejkratsi_vzdalenosti, nejkratsi_vzdalenosti), "m.")
print("Průměrná vzdálenost ke všem kontejnerům je", prumerna_vzdalenost(nejkratsi_vzdalenosti, kontejnery_json), "m.")
