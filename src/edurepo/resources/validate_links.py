# TODO: Fix the TZ crap
#       We should only care about UTC, picking that up from the settings module.
#       But I'm getting the naive time errors here and there.

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'edurepo.settings')

import sys
sys.path.append('.')

import urllib2
from datetime import datetime, timedelta
from optparse import OptionParser
from bs4 import BeautifulSoup
from resources.models import Resource, ResourceVerification


def create_verification(debug, url):
    if debug:
        print url
    try:
        rsp = urllib2.urlopen(url, None, 10)
    except:
        verification = ResourceVerification(url=url,
                                            last_failure=datetime.now())
        verification.save()
        return

    if debug:
        print rsp.getcode()
    contents = rsp.read()
    soup = BeautifulSoup(contents)
    if soup.title:
        title = soup.title.string
        title = title.strip()
        title = title.replace('\r', '')
        if title.count('\n') > 1:
            # assume the worst and set the title to the text up through the 1st \n
            title = title.split('\n')[0]
        else:
            title = title.replace('\n', ' ')
        if debug:
            print ' ', title.encode("utf8")
    else:
        title = ''
        if debug:
            print "  (no title)"
    verification = ResourceVerification(url=url,
                                        last_success=datetime.now(),
                                        document_title=title)
    verification.save()


def verify_all_resources(debug):
    resources = Resource.objects.all()
    for resource in resources:
        try:
            verification = ResourceVerification.objects.get(url=resource.url)
            if debug:
                print verification
        except ResourceVerification.DoesNotExist:
            create_verification(debug, resource.url)


def re_verify(debug, oldest_valid_success):
    verifications = ResourceVerification.objects.all()
    for verification in verifications:
        if verification.last_success is None:
            if debug:
                print "never worked: " + verification.url
            create_verification(debug, verification.url)
        elif verification.last_failure and verification.last_failure > verification.last_success:
            if debug:
                print "most recently failed: " + verification.url
            create_verification(debug, verification.url)
        elif verification.last_success.replace(tzinfo=None) < oldest_valid_success.replace(tzinfo=None):
            if debug:
                print "not tested in a while: " + verification.url
            create_verification(debug, verification.url)

parser = OptionParser()
parser.add_option("-d", "--debug", dest="debug",
                  action="store_true",
                  help="show debug messages")

(options, args) = parser.parse_args()

# First, ensure that all resources have a verification record.
# Only newly-added resources won't have one.
verify_all_resources(options.debug)

# Re-verify as necessary
max_success_age = timedelta(days=14)
re_verify(options.debug, datetime.now() - max_success_age)
