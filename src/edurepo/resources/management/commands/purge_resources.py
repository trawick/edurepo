from datetime import datetime, timedelta
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from resources.models import Resource, ResourceVerification


def purge_unreachable_resources(debug=False, min_success_time=None, purge_stranded=False):
    verifications = ResourceVerification.objects.all()
    for verification in verifications:
        if debug:
            print 'Checking %s...' % verification
        resources = Resource.objects.filter(url=verification.url)
        if len(resources) == 0:
            if purge_stranded:
                print ''
                print '*** This verification record is being purged: %s ***' % verification
                print ''
                verification.delete()
            else:
                print 'Purge stranded verification record %s' % verification
            continue
        purge = False
        reason = ''
        if verification.last_success is None:
            purge = True
            reason = 'Link never worked'
        elif verification.last_success < min_success_time:
            purge = True
            reason = 'Link did not work recently'
        if purge:
            if resources:
                print 'Purge resources with URL %s (%s):' % (verification, reason)
                for resource in resources:
                    print '  %s' % resource


def purge_inappropriate_resources(debug):
    resources = Resource.objects.all().exclude(inappropriate_flags=0)
    for resource in resources:
        if debug:
            print 'Checking %s...' % resource
        print 'Consider purging inappropriate resource %s (%d)' % (resource, resource.inappropriate_flags)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "--debug", dest="debug",
            action="store_true",
            help="show debug messages",
        ),
        make_option(
            "--purge-stranded", action="store_true",
            help="automatically purge stranded resource verification records",
        ),
    )

    def handle(self, *args, **options):
        # Identify resources for removal based on failed verification.
        #
        # The time delta needs to be in sync with validate_links, or
        # we'll identify resources for purge that haven't been tried
        # recently.
        purge_unreachable_resources(debug=options['debug'],
                                    min_success_time=now() - timedelta(days=14),
                                    purge_stranded=options['purge_stranded'])

        # Identify resources for removal based on inappropriate flags.
        purge_inappropriate_resources(options['debug'])
