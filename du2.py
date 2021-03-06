import json, os, sys, statistics, argparse
from math import sqrt, inf
from pyproj import CRS, Transformer

def nahraj_geojson(jmeno_souboru):
    """ Načte soubor typu geojson a ošetří nekorektní vstupy. """
    try:
        with open(os.path.join(sys.path[0], jmeno_souboru+".geojson"), "r", encoding="UTF-8") as file:
                data = json.load(file)
        
    except PermissionError:
        print(f"K souboru {jmeno_souboru} nemá program přístup.")
        exit()
    except FileNotFoundError:
        print(f"Soubor {jmeno_souboru} nebyl nenalezen.")
        exit()
    except ValueError:
        print(f"Soubor {jmeno_souboru} je chybný.")
        exit()
    
    return data 

def data_kontejnery(kontejnery):
    """ Vytvoří slovník z kontejnerů [adresa:souřadnice, přístup]. """

    dic_kontejnery = {} 

    for k in kontejnery:
        k_adresa = k["properties"]["STATIONNAME"]
        k_geo = k["geometry"]["coordinates"]
        k_pristup = k["properties"]["PRISTUP"]

        dic_kontejnery[k_adresa] = k_geo, k_pristup

        
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

        a_geo_jtsk = wgs_jtsk(a_geo_wgs[1], a_geo_wgs[0])
        a_adresa = a_ulice + " " + a_cp
 
        dic_adresy[a_adresa] = a_geo_jtsk
    
    if len(dic_adresy) == 0:
        print("Chyba: do slovníku nebyl přidán žádný záznam. Program končí.")
        exit()

    return dic_adresy

def wgs_jtsk(x, y):
    """ Převod souřadnic z WGS na S-JTSK. """

    # nutnost použít crs a transformer z pyproj2 (náhrada pyproj1)
    wgs = CRS.from_epsg(4326)  # WGS-84
    jtsk = CRS.from_epsg(5514)  # S-JTSK
    wgs_jtsk = Transformer.from_crs(wgs, jtsk)

    now_jtsk = wgs_jtsk.transform(x, y)

    return now_jtsk

def vypocet_vzdalenosti(geo_a, geo_k):
    """ Obecná funkce pro výpočet vzdálenosti ze souřadnic dvou bodů pomocí Pythagorovy věty. """

    a = geo_a[0] - geo_k[0]
    b = geo_a[1] - geo_k[1]
    c = sqrt((a*a) + (b*b))

    return c

def nejblizsi(dic_kontejnery, dic_adresy):
    """ Pro každou adresu hledá nejkratší vzdálenost ke kontejneru. """

    dic_vzdalenosti = {}

    # Projíždí každou adresu ze souboru
    for (a_adresa, a_geo) in dic_adresy.items():
        min_vzdalenost = inf  # původní minimální vzdálenost je nekonečno (inf)        

        # projíždí každý kontejner ze souboru
        for (k_geo, k_pristup) in dic_kontejnery.values():
            # pokud je přístup pouze pro obyvatele domu
            if k_pristup == "obyvatelům domu":
                for k_adresa in dic_kontejnery.keys():
                    # zkontroluje, zda je adresa domu stejná jako adresa kontejneru
                    if k_adresa == a_adresa:
                        min_vzdalenost = 0
            # pokud je přístup volný, vypočte k němu vzdálebost
            elif k_pristup == "volně":
                vzdalenost = vypocet_vzdalenosti(a_geo, k_geo)
                # pokud je vzdálenost menší než minimální, přepíše se
                if min_vzdalenost > vzdalenost:
                    min_vzdalenost = vzdalenost


        # ošetření nejbližšího kontejneru vzdálenho +10 km 
        if min_vzdalenost > 10000:
            print("Nejbližší kontejner je vzdálený více jak 10 km od adresního bodu.\n Program bude ukončen.")
            exit()

        dic_vzdalenosti[a_adresa] = min_vzdalenost
    
    return dic_vzdalenosti

def maximalni(dic):
    """ Vypíše maximální vzálenost ke kontejneru s příslušnou adresou. """

    max_v = max(nejkratsi_vzdalenosti.values())

    for (adresa, vzdalenost) in dic.items():
        if vzdalenost == max_v:
            max_a = adresa

    return max_v, max_a

# ? načtení vstupních dat 
kontejnery_json = nahraj_geojson("kontejnery")["features"]
adresy_json = nahraj_geojson("adresy")["features"]

# ? vytvoření slovníků s určitými proměnnými ze vstupních geojson souborů
dic_kontejnery = data_kontejnery(kontejnery_json)
dic_adresy = data_adresy(adresy_json)

# ? nalezení nejmenších vzáleností
nejkratsi_vzdalenosti = nejblizsi(dic_kontejnery, dic_adresy)

# ? PROMĚNNÉ K VÝSTUPŮM
nejdelsi_vzdalenost = maximalni(nejkratsi_vzdalenosti)
median_vzdalenosti = statistics.median(nejkratsi_vzdalenosti.values())
prumer_vzdalenosti = statistics.mean(nejkratsi_vzdalenosti.values())

# ! VÝSTUP PROGRAMU
print("Načteno adresních bodů:", len(dic_adresy))
print("Načteno kontejnerů na třízený odpad:", len(dic_kontejnery), "\n")

print("Medián vzdáleností ke kontejneru je " f"{median_vzdalenosti:.0f} metrů" )
print("Průměrná vzdálenost ke kontejneru je " f"{prumer_vzdalenosti:.0f} metrů")
print("Maximální vzálenost ke kontejneru je " f"{nejdelsi_vzdalenost[0]:.0f} metrů a to z adresy", nejdelsi_vzdalenost[1])
