import json, os, sys

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
        print("Nebyly nalezeny žádné volně přístupné kontejnery. ")

    return dic_kontejnery

def data_adresy(adresy):
    """ pass """

    dic_adresy = {}

    for a in adresy:
        a_ulice = a["properties"]["addr:street"]
        a_cp = a["properties"]["addr:housenumber"]
        a_geo = a["geometry"]["coordinates"]

        a_adresa = a_ulice + " " + a_cp

        dic_adresy[a_adresa] = a_geo

    return dic_adresy

# ? zavedení proměnných
kontejnery_json = nahraj_geojson("kontejnery")["features"]
adresy_json = nahraj_geojson("adresy")["features"]

print(data_adresy(adresy_json))

