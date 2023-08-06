#
# Copyright (c) 2020 eGauge Systems LLC
#       1644 Conestoga St, Suite 2
#       Boulder, CO 80301
#       voice: 720-545-9767
#       email: davidm@egauge.net
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
'''This module provides helper methods for accessing JSON web services.'''
import logging
import json

import requests

from .error import Error

log = logging.getLogger(__name__)

class JSONAPIError(Error):
    '''Raised if for any JSON API errors.  The first argument to this
    exception is the 401 response received from the web server.

    '''

class UnauthenticatedError(Error):
    '''Raised when a request fails with HTTP status code 401.'''

def get(resource, **kwargs):
    '''Issue GET request for RESOURCE and return the parsed JSON data or
    None if the request failed or returned invalid JSON data.
    Additional keyword arguments are passed on to requests.get().

    '''
    try:
        r = requests.get(resource, **kwargs)
    except requests.exceptions.RequestException as e:
        raise JSONAPIError('requests.get exception.') from e
    if r.status_code == 401:
        raise UnauthenticatedError(r)
    if r.status_code < 200 or r.status_code > 299:
        if log.getEffectiveLevel() <= logging.DEBUG:
            log.exception('HTTP GET status code %s.  Keyword args: %s',
                          r.status_code, kwargs)
        raise JSONAPIError('Unexpected HTTP status code.', r.status_code, r.content)
    try:
        reply = r.json()
    except ValueError as e:
        raise JSONAPIError('Invalid JSON data.', r.content) from e
    return reply

def put(resource, json_data, **kwargs):
    '''Issue PUT request with JSON_DATA as body to RESOURCE and return
    parsed JSON reply or None if the request failed or returned
    invalid JSON data.  Additional keyword arguments are passed on to
    requests.post().

    '''
    headers = kwargs.get('headers', {})
    headers['Content-Type'] = 'application/json'
    kwargs['headers'] = headers
    try:
        r = requests.put(resource, data=json.dumps(json_data), **kwargs)
    except requests.exceptions.RequestException as e:
        raise JSONAPIError('requests.put exception.') from e
    if r.status_code == 401:
        raise UnauthenticatedError(r)
    if not 200 <= r.status_code <= 299:
        if log.getEffectiveLevel() <= logging.DEBUG:
            log.exception('HTTP PUT status code %s.  '
                          'Resource %s, Data: %s, keyword args: %s',
                          r.status_code, resource, json_data, kwargs)
        raise JSONAPIError('Unexpected HTTP status code.', r.status_code, r.content)
    try:
        reply = r.json()
    except ValueError as e:
        raise JSONAPIError('Invalid JSON data.', r.content) from e
    return reply

def post(resource, json_data, **kwargs):
    '''Issue POST request with JSON_DATA as body to RESOURCE and return
    parsed JSON reply or None if the request failed or returned
    invalid JSON data.  Additional keyword arguments are passed on to
    requests.post().

    '''
    headers = kwargs.get('headers', {})
    headers['Content-Type'] = 'application/json'
    kwargs['headers'] = headers
    try:
        r = requests.post(resource, data=json.dumps(json_data), **kwargs)
    except requests.exceptions.RequestException as e:
        raise JSONAPIError('requests.post exception.') from e
    if r.status_code == 401:
        raise UnauthenticatedError(r)
    if not 200 <= r.status_code <= 299:
        if log.getEffectiveLevel() <= logging.DEBUG:
            log.exception('HTTP POST status code %s.  '
                          'Resource %s, Data: %s, keyword args: %s',
                          r.status_code, resource, json_data, kwargs)
        raise JSONAPIError('Unexpected HTTP status code.', r.status_code, r.content)
    try:
        reply = r.json()
    except ValueError as e:
        raise JSONAPIError('Invalid JSON data.', r.content) from e
    return reply

def delete(resource, **kwargs):
    '''Issue DELETE request for RESOURCE and return the parsed JSON data
    or None if the request failed or returned invalid JSON data.
    Additional keyword arguments are passed on to requests.delete().

    '''
    try:
        r = requests.delete(resource, **kwargs)
    except requests.exceptions.RequestException as e:
        raise JSONAPIError('requests.delete exception.') from e
    if r.status_code == 401:
        raise UnauthenticatedError(r)
    if r.status_code < 200 or r.status_code > 299:
        if log.getEffectiveLevel() <= logging.DEBUG:
            log.exception('HTTP DELETE status code %s.  Keyword args: %s',
                          r.status_code, kwargs)
        raise JSONAPIError('Unexpected HTTP status code.', r.status_code, r.content)
    try:
        reply = r.json()
    except ValueError as e:
        raise JSONAPIError('Invalid JSON data.', r.content) from e
    return reply
