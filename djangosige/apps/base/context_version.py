# -*- coding: utf-8 -*-

from djangosige import __version__


def sige_version(request):
    return {'versao': __version__}
