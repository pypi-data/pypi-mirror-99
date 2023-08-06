# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.breadcrumbs.base import (
    RootedCrumbWithChild,
    register,
    registered,
    )
from visaplan.tools.minifuncs import translate_dummy as _

# Local imports:
# Nicht mehr nötig mit visaplan.plone.breadcrumbs 1+:
from visaplan.plone.browsers.management.oldcrumbs import imported


# -------------------------------------------- [ Initialisierung ... [
def register_crumbs():
    management_base_crumb = registered('management_view')
    _page_id = 'manage_settings'
    settings_crumb = RootedCrumbWithChild(_page_id,
                                          _('Miscellaneous Settings'),
                                          'key',
                                          [management_base_crumb])
    register(settings_crumb, _page_id)

register_crumbs()
# -------------------------------------------- ] ... Initialisierung ]

OK = True
