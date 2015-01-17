import logging

from django.http import HttpResponse
import requests
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse

logger = logging.getLogger(__name__)


#### from https://gist.github.com/robhudson/3848832
class CORSResource(object):
    """
    Adds CORS headers to resources that subclass this.
    """
    def create_response(self, *args, **kwargs):
        response = super(CORSResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join(map(str.upper, allowed))

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method
#### end gist


def ellipsis(input_str, max_output_len):
    if len(input_str) > max_output_len:
        return input_str[:max_output_len - 3] + '...'
    return input_str


def description_for_objective(objective_id, repo_provider):
    assert repo_provider
    base_objective_url = '%srepo/api/learningobjective/' % repo_provider
    url = '%s%s/' % (base_objective_url, objective_id)
    try:
        logger.info('Fetching %s' % url)
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logger.exception('Error retrieving URL %s:' % url)
        return None
    # temporary hack for https://github.com/kennethreitz/requests/issues/2192
    except requests.packages.urllib3.exceptions.ProtocolError:
        logger.exception("Error retrieving %s" % url)
        return None
    try:
        json_body = response.json()
    except ValueError:
        logger.error('Failed to parse %d response of type %s as JSON' % (
            response.status_code, response.headers['content-type']
        ))
        raise
    return json_body['description']


def objectives_for_course(course_id, repo_provider):
    assert repo_provider
    base_course_url = '%srepo/api/learningobjective/' % repo_provider
    url = '%s?course__id=%s' % (base_course_url, course_id)
    try:
        logger.info('Fetching %s' % url)
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logger.exception('Error retrieving URL %s:' % url)
        return None
    # temporary hack for https://github.com/kennethreitz/requests/issues/2192
    except requests.packages.urllib3.exceptions.ProtocolError:
        logger.exception('Error retrieving URL %s:' % url)
        return None
    try:
        json_body = response.json()
    except ValueError:
        logger.error('Failed to parse %d response of type %s as JSON' % (
            response.status_code, response.headers['content-type']
        ))
        raise
    results = []
    for o in json_body['objects']:
        results += [(o['id'], o['description'])]
    return results
