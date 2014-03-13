import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'edurepo.settings')

import sys
sys.path.append('.')

from django.utils.timezone import utc
from datetime import datetime, timedelta
from optparse import OptionParser
from resources.models import Resource, ResourceVerification


def now():
    return datetime.utcnow().replace(tzinfo=utc)


def purge_unreachable_resources(debug, min_success_time):
    verifications = ResourceVerification.objects.all()
    for verification in verifications:
        if debug:
            print 'Checking %s...' % verification
        purge = False
        if verification.last_success is None:
            purge = True
            reason = 'Link never worked'
        elif verification.last_success < min_success_time:
            purge = True
            reason = 'Link did not work recently'
        if purge:
            print 'Purge resources with URL %s (%s):' % (verification, reason)
            resources = Resource.objects.filter(url=verification.url)
            for resource in resources:
                print '  %s' % resource


def purge_inappropriate_resources(debug):
    resources = Resource.objects.all().exclude(inappropriate_flags=0)
    for resource in resources:
        print 'Purge inappropriate resource %s (%d)' % (resource, resource.inappropriate_flags)

parser = OptionParser()
parser.add_option("-d", "--debug", dest="debug",
                  action="store_true",
                  help="show debug messages")

(options, args) = parser.parse_args()

# Identify resources for removal based on failed verification.
purge_unreachable_resources(options.debug, now() - timedelta(days=7))

# Identify resources for removal based on inappropriate flags.
purge_inappropriate_resources(options.debug)
