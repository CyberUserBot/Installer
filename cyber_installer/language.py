from json import loads
from rich.prompt import Prompt
from . import logo, console, bilgi

def importlang ():
    console.clear()
    logo()
    bilgi("\n[1] Azərbaycanca\n[2] Türkçe\n[3] English\n[4] O'zbek\n[5] India")
    Dil = Prompt.ask("[bold yellow]Xahiş edirəm bir dil seçin[/]", choices=["1", "2", "3", "4", "5"], default="1")

    if Dil == "1":
        COUNTRY = "Azerbaijan"
        LANGUAGE = "AZ"
        TZ = "Asia/Baku"
    elif Dil == "2":
        COUNTRY = "Turkey"
        LANGUAGE = "TR"
        TZ = "Europe/Istanbul"
    elif Dil == "3":
        COUNTRY = "United Kingdom"
        LANGUAGE = "EN"
        TZ = "Europe/London"
    elif Dil == "4":
        COUNTRY = "Uzbekistan"
        LANGUAGE = "UZ"
        TZ = "Asia/Tashkent"
    if Dil == "5":
        COUNTRY = "India"
        LANGUAGE = "IN"
        TZ = "Asia/Colombo"

    return COUNTRY, LANGUAGE, TZ


COUNTRY, LANGUAGE, TZ = importlang()
LANG = loads(open(f"./cyber_installer/language/{LANGUAGE}.cyberjson", "r").read())["STRINGS"]
