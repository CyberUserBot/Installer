# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/CyberUserBot/Installer/ >
# Please read the MIT license in
# <https://www.github.com/CyberUserBot/Installer/blob/master/LICENSE/>.

# Təkrar istifadəyə icazə verilmir.
# Yeniden kullanıma izin verilmiyor.
# Reuse is not allowed.

from rich.console import Console
from rich.panel import Panel
from rich.live_render import LiveRender
import sys
import os
import shutil

console = Console()

def hata (text):
   console.print(text, style="bold red")
def bilgi (text):
   console.print(text, style="blue")
def basarili (text):
   console.print(f"[bold green]{text}[/]")
def onemli (text):
   console.print(text, style="bold cyan")
def soru (soru):
   return console.input(f"[bold yellow]{soru}[/]")
def logo (dil = "Yoxdur"):
   surum = str(sys.version_info[0]) + "." + str(sys.version_info[1])
   console.print(Panel(f"[bold white]CYBΞR USΞRBOT[/]\n\n[bold blue]Versiya: [/][i]3.0[/]\n[bold red]Python: [/][i]{surum}[/]\n[bold green]Dil: [/][i]{dil}[/]"), justify="center")                         
def tamamlandi (saniye):
   console.print(Panel(f"[bold green]Qurulum Tamamlandı!\n[i]Botu {round(saniye)} saniyə içində qurdunuz.[/]\n\n[bold green]Bir neçə dəqiqə sonra hər-hansı bir qrupa .alive yazaraq test edə bilərsiniz.[/]"), justify="center")                         

def rm_r(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)
    else:
        shutil.rmtree(path)
