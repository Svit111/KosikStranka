from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()

templates = Jinja2Templates(directory="templates")



Ovocie = {
    "jablko": 1,
    "banan": 2,
    "hruska": 3
}

Zelenina = {
    "rajcina": 2,
    "melon": 3
}

Zviera = {
    "pes": 10,
    "macka": 20
}


# Sklad
Mnozstvo = {
    "jablko": 5,
    "banan": 3,
    "hruska": 4,
    "rajcina": 2,
    "melon": 1,
    "pes": 1,
    "macka": 2
}



kosicek = []



def vsetky_produkty():
    produkty = {}

    for nazov, cena in Ovocie.items():
        produkty[nazov] = {
            "nazov": nazov,
            "cena": cena,
            "kategoria": "ovocie",
            "sklad": Mnozstvo[nazov]
        }

    for nazov, cena in Zelenina.items():
        produkty[nazov] = {
            "nazov": nazov,
            "cena": cena,
            "kategoria": "zelenina",
            "sklad": Mnozstvo[nazov]
        }

    for nazov, cena in Zviera.items():
        produkty[nazov] = {
            "nazov": nazov,
            "cena": cena,
            "kategoria": "zviera",
            "sklad": Mnozstvo[nazov]
        }

    return produkty



@app.get("/")
def domov(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )



# Vráti všetky produkty
@app.get("/api/products")
def produkty():
    return vsetky_produkty()


# Pridanie produktu do košíka
class ProduktRequest(BaseModel):
    nazov: str


@app.post("/api/cart/add")
def pridat_do_kosika(data: ProduktRequest):

    nazov = data.nazov

    if nazov not in Mnozstvo:
        return {
            "success": False,
            "message": "Produkt neexistuje."
        }

    if Mnozstvo[nazov] <= 0:
        return {
            "success": False,
            "message": "Produkt je vypredaný."
        }

    Mnozstvo[nazov] -= 1
    kosicek.append(nazov)

    return {
        "success": True,
        "message": f"{nazov} bol pridaný do košíka."
    }


# Zobrazí košík
@app.get("/api/cart")
def zobrazit_kosik():

    produkty = vsetky_produkty()

    zoznam = []
    cena = 0

    for nazov in kosicek:
        produkt = produkty[nazov]

        zoznam.append({
            "nazov": nazov,
            "cena": produkt["cena"],
            "kategoria": produkt["kategoria"]
        })

        cena += produkt["cena"]

    return {
        "kosicek": zoznam,
        "cena": cena
    }


# Kupón
class KuponRequest(BaseModel):
    kupon: str


@app.post("/api/coupon")
def pouzit_kupon(data: KuponRequest):

    # Najprv spočítame cenu
    produkty = vsetky_produkty()

    cena = 0

    for nazov in kosicek:
        cena += produkty[nazov]["cena"]

    if data.kupon == "Kupon1":
        nova_cena = cena * 0.8

        return {
            "success": True,
            "message": "Zľava 20 %",
            "povodna_cena": cena,
            "cena": nova_cena
        }

    elif data.kupon == "Kupon2":
        nova_cena = cena * 0.1

        return {
            "success": True,
            "message": "Zľava 90 %",
            "povodna_cena": cena,
            "cena": nova_cena
        }

    else:
        return {
            "success": False,
            "message": "Kupón neexistuje.",
            "cena": cena
        }