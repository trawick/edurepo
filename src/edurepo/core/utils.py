#### from https://gist.github.com/robhudson/3848832

import json
import urllib2

from django.http import HttpResponse
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse


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
    print objective_id
    print repo_provider

    base_objective_url = '%srepo/api/learningobjective/' % repo_provider
    url = '%s%s/?format=json' % (base_objective_url, objective_id)
    response = urllib2.urlopen(url)
    body = response.read()
    json_body = json.loads(body)
    return json_body['description']
