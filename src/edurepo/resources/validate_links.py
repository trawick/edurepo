import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'edurepo.settings')

import sys
sys.path.append('.')

from django.utils.timezone import utc
from datetime import datetime, timedelta
from optparse import OptionParser
from bs4 import BeautifulSoup
from resources.models import Resource, ResourceVerification
import requests


def now():
    return datetime.utcnow().replace(tzinfo=utc)


def get_content_type(debug, rsp):
    """Return content-type in lower case with anything else (e.g., charset)
    stripped off.  Return empty string if no content-type is available."""
    ct_hdr = rsp.headers['Content-Type']
    if not ct_hdr:
        return ''
    fields = ct_hdr.split(';')
    if not fields:
        return ''
    return fields[0].strip().lower()


def create_verification(debug, url):

    def handle_request_error(url):
        verification = ResourceVerification(url=url,
                                            last_failure=now())
        verification.save()
        resources = Resource.objects.filter(url=url)
        print 'Affected learning objectives:'
        for r in resources:
            print r.objective
        print ''

    if debug:
        print url
    # www.livescience.com does a permanent redirect to a mobile site
    # when using the default urllib2 user-agent string.  (I haven't
    # checked that again after switching from urllib2 to requests.)
    headers = {"User-Agent": "Mozilla/5.0 (edurepo link validity checker"}
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        print 'Failed now: ' + url
        print sys.exc_info()
        handle_request_error(url)
        return
    # temporary hack for https://github.com/kennethreitz/requests/issues/2192
    except requests.packages.urllib3.exceptions.ProtocolError:
        print 'Failed now: ' + url
        print sys.exc_info()
        handle_request_error(url)
        return
    except:
        print 'Failed now: ' + url
        print sys.exc_info()
        handle_request_error(url)
        return

    if response.status_code != 200:
        print 'Failed now with HTTP error code %s: %s' % (response.status_code, url)
        if response.status_code != 404:
            print response.text
        handle_request_error(url)
        return

    ct = get_content_type(debug, response)

    if debug:
        print response.status_code
        print response.headers['Content-Type'] + ' => ' + ct

    if ct == 'text/html':
        contents = response.text
        try:
            soup = BeautifulSoup(contents)
        except:
            print 'Failed to parse: ' + url
            print sys.exc_info()
            soup = None

        if soup and soup.title:
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
    else:
        title = ''

    verification = ResourceVerification(url=url,
                                        last_success=now(),
                                        document_title=title,
                                        content_type=ct)
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
        elif verification.last_success < oldest_valid_success:
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
max_success_age = timedelta(days=12)
re_verify(options.debug, now() - max_success_age)
