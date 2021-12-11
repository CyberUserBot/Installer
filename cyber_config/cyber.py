# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/CyberUserBot/Installer/ >
# Please read the MIT license in
# <https://www.github.com/CyberUserBot/Installer/blob/master/LICENSE/>.

# Təkrar istifadəyə icazə verilmir.
# Yeniden kullanıma izin verilmiyor.
# Reuse is not allowed.

import os
from requests import get

class CyberConfig(object):
    REPO_BRANCH = "master"
    DESTINATION = "./cyberuserbot/"
    

   
# TEST = get('https://raw.githubusercontent.com/FaridDadashzade/deploy/main/installer.py').json()
