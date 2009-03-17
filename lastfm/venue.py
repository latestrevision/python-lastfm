#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm"

from lastfm.base import LastfmBase
from lastfm.mixins import Cacheable, Searchable
from lastfm.lazylist import lazylist
from lastfm.decorators import cached_property

class Venue(LastfmBase, Cacheable, Searchable):
    """A class representing a venue of an event"""
    def init(self,
             api,
             id = None,
             name = None,
             location = None,
             url = None,
             **kwargs):
        if not isinstance(api, Api):
            raise InvalidParametersError("api reference must be supplied as an argument")
        self._api = api
        self._id = id
        self._name = name
        self._location = location
        self._url = url

    @property
    def id(self):
        """id of the venue"""
        return self._id
    
    @property
    def name(self):
        """name of the venue"""
        return self._name

    @property
    def location(self):
        """location of the event"""
        return self._location

    @property
    def url(self):
        """url of the event's page"""
        return self._url

    @cached_property
    def events(self):
        params = self._default_params({'method': 'venue.getEvents'})
        data = self._api._fetch_data(params).find('events')

        return [
                Event.create_from_data(self._api, e)
                for e in data.findall('event')
                ]

    def get_past_events(self,
                      limit = None):
        params = self._default_params({'method': 'venue.getPastEvents'})
        if limit is not None:
            params.update({'limit': limit})

        @lazylist
        def gen(lst):
            data = self._api._fetch_data(params).find('events')
            total_pages = int(data.attrib['totalPages'])

            @lazylist
            def gen2(lst, data):
                for e in data.findall('event'):
                    yield Event.create_from_data(self._api, e)

            for e in gen2(data):
                yield e

            for page in xrange(2, total_pages+1):
                params.update({'page': page})
                data = self._api._fetch_data(params).find('events')
                for e in gen2(data):
                    yield e
        return gen()

    @cached_property
    def past_events(self):
        return self.get_past_events()
    
    def _default_params(self, extra_params = {}):
        if not self.id:
            raise InvalidParametersError("venue id has to be provided.")
        params = {'venue': self.id}
        params.update(extra_params)
        return params
    
    @staticmethod
    def _search_yield_func(api, venue):
        return Venue(
                     api,
                     id = int(venue.findtext('id')),
                     name = venue.findtext('name'),
                     location = Location(
                                         api,
                                         city = venue.findtext('location/city'),
                                         country = Country(
                                            api,
                                            name = venue.findtext('location/country')
                                            ),
                                         street = venue.findtext('location/street'),
                                         postal_code = venue.findtext('location/postalcode'),
                                         latitude = float(venue.findtext(
                                             'location/{%s}point/{%s}lat' % ((Location.XMLNS,)*2)
                                             )),
                                         longitude = float(venue.findtext(
                                             'location/{%s}point/{%s}long' % ((Location.XMLNS,)*2)
                                             )),
                                         ),
                     url = venue.findtext('url')
                     )
    
    @staticmethod
    def _hash_func(*args, **kwds):
        try:
            return hash(kwds['url'])
        except KeyError:
            raise InvalidParametersError("url has to be provided for hashing")

    def __hash__(self):
        return self.__class__._hash_func(url = self.url)

    def __eq__(self, other):
        return self.url == other.url

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return "<lastfm.geo.Venue: %s, %s>" % (self.name, self.location.city)
    
from lastfm.api import Api
from lastfm.event import Event
from lastfm.geo import Location, Country
from lastfm.error import InvalidParametersError