import json, os, sys

def nahraj_geojson(jmeno_souboru):
    """ Načte soubor typu geojson a ošetří nekorektní vstupy. """
    try:
        with open(os.path.join(sys.path[0], jmeno_souboru+".geojson"), "r", encoding="UTF-8") as file:
                data = json.load(file)

    except FileNotFoundError:
        print(f"Soubor {jmeno_souboru} nenalezen.")
        exit()
    except ValueError:
        print(f"Soubor {jmeno_souboru} je chybný.")
        exit()
    except PermissionError:
        print(f"Soubor {jmeno_souboru} není přístupný. Povolte přístup.")
        exit()

    return data 

