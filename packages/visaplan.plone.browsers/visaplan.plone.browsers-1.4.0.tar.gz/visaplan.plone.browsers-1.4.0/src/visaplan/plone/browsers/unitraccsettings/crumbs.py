# Setup tools:
import pkg_resources

try:
    pkg_resources.get_distribution('zope.deprecation')
except pkg_resources.DistributionNotFound:
    'Imports from old location not supported'
else:
    # Zope:
    from zope.deprecation import moved
    moved('visaplan.plone.browsers.unitraccsettings.oldcrumbs', 'version 1.5')

