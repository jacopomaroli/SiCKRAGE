# -*- coding: utf-8 -*-
# Author: Daniel Heimans
# URL: http://code.google.com/p/sickbeard
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import logging
import math
import socket
import time
from datetime import datetime

import jsonrpclib

import classes
import scene_exceptions
import sickbeard
from common import cpu_presets
from sickbeard import providers
from sickbeard import tvcache
from sickbeard.helpers import sanitizeSceneName


class BTNProvider(providers.TorrentProvider):
    def __init__(self):
        super(BTNProvider, self).__init__("BTN")

        self.supportsBacklog = True

        self.supportsAbsoluteNumbering = True

        self.api_key = None
        self.ratio = None

        self.cache = BTNCache(self)

        self.urls = {'base_url': 'http://api.btnapps.net',
                     'website': 'http://broadcasthe.net/',}

        self.url = self.urls['website']

    def _checkAuth(self):
        if not self.api_key:
            logging.warning("Invalid api key. Check your settings")

        return True

    def _checkAuthFromData(self, parsedJSON):

        if parsedJSON is None:
            return self._checkAuth()

        if 'api-error' in parsedJSON:
            logging.debug("Incorrect authentication credentials: % s" % parsedJSON['api-error'])
            raise AuthException(
                    "Your authentication credentials for " + self.name + " are incorrect, check your config.")

        return True

    def _doSearch(self, search_params, search_mode='eponly', epcount=0, age=0, epObj=None):

        self._checkAuth()

        results = []
        params = {}
        apikey = self.api_key

        # age in seconds
        if age:
            params[b'age'] = "<=" + str(int(age))

        if search_params:
            params.update(search_params)
            logging.debug("Search string: %s" % search_params)

        parsedJSON = self._api_call(apikey, params)
        if not parsedJSON:
            logging.debug("No data returned from provider")
            return results

        if self._checkAuthFromData(parsedJSON):

            if 'torrents' in parsedJSON:
                found_torrents = parsedJSON[b'torrents']
            else:
                found_torrents = {}

            # We got something, we know the API sends max 1000 results at a time.
            # See if there are more than 1000 results for our query, if not we
            # keep requesting until we've got everything.
            # max 150 requests per hour so limit at that. Scan every 15 minutes. 60 / 15 = 4.
            max_pages = 150
            results_per_page = 1000

            if 'results' in parsedJSON and int(parsedJSON[b'results']) >= results_per_page:
                pages_needed = int(math.ceil(int(parsedJSON[b'results']) / results_per_page))
                if pages_needed > max_pages:
                    pages_needed = max_pages

                # +1 because range(1,4) = 1, 2, 3
                for page in range(1, pages_needed + 1):
                    parsedJSON = self._api_call(apikey, params, results_per_page, page * results_per_page)
                    # Note that this these are individual requests and might time out individually. This would result in 'gaps'
                    # in the results. There is no way to fix this though.
                    if 'torrents' in parsedJSON:
                        found_torrents.update(parsedJSON[b'torrents'])

            for torrentid, torrent_info in found_torrents.iteritems():
                (title, url) = self._get_title_and_url(torrent_info)

                if title and url:
                    logging.debug("Found result: %s " % title)
                    results.append(torrent_info)

        # FIXME SORT RESULTS
        return results

    def _api_call(self, apikey, params={}, results_per_page=1000, offset=0):

        server = jsonrpclib.Server(self.urls['base_url'])
        parsedJSON = {}

        try:
            parsedJSON = server.getTorrents(apikey, params, int(results_per_page), int(offset))
            time.sleep(cpu_presets[sickbeard.CPU_PRESET])

        except jsonrpclib.jsonrpc.ProtocolError, error:
            if error.message == 'Call Limit Exceeded':
                logging.warning(
                        "You have exceeded the limit of 150 calls per hour, per API key which is unique to your user account")
            else:
                logging.error("JSON-RPC protocol error while accessing provicer. Error: %s " % repr(error))
            parsedJSON = {'api-error': error}
            return parsedJSON

        except socket.timeout:
            logging.warning("Timeout while accessing provider")

        except socket.error, error:
            # Note that sometimes timeouts are thrown as socket errors
            logging.warning("Socket error while accessing provider. Error: %s " % error[1])

        except Exception, error:
            errorstring = str(error)
            if errorstring.startswith('<') and errorstring.endswith('>'):
                errorstring = errorstring[1:-1]
            logging.warning("Unknown error while accessing provider. Error: %s " % errorstring)

        return parsedJSON

    @staticmethod
    def _get_title_and_url(parsedJSON):

        # The BTN API gives a lot of information in response,
        # however SickRage is built mostly around Scene or
        # release names, which is why we are using them here.

        if 'ReleaseName' in parsedJSON and parsedJSON[b'ReleaseName']:
            title = parsedJSON[b'ReleaseName']

        else:
            # If we don't have a release name we need to get creative
            title = ''
            if 'Series' in parsedJSON:
                title += parsedJSON[b'Series']
            if 'GroupName' in parsedJSON:
                title += '.' + parsedJSON[b'GroupName'] if title else parsedJSON[b'GroupName']
            if 'Resolution' in parsedJSON:
                title += '.' + parsedJSON[b'Resolution'] if title else parsedJSON[b'Resolution']
            if 'Source' in parsedJSON:
                title += '.' + parsedJSON[b'Source'] if title else parsedJSON[b'Source']
            if 'Codec' in parsedJSON:
                title += '.' + parsedJSON[b'Codec'] if title else parsedJSON[b'Codec']
            if title:
                title = title.replace(' ', '.')

        url = None
        if 'DownloadURL' in parsedJSON:
            url = parsedJSON[b'DownloadURL']
            if url:
                # unescaped / is valid in JSON, but it can be escaped
                url = url.replace("\\/", "/")

        return title, url

    @staticmethod
    def _get_season_search_strings(ep_obj):
        search_params = []
        current_params = {'category': 'Season'}

        # Search for entire seasons: no need to do special things for air by date or sports shows
        if ep_obj.show.air_by_date or ep_obj.show.sports:
            # Search for the year of the air by date show
            current_params[b'name'] = str(ep_obj.airdate).split('-')[0]
        elif ep_obj.show.is_anime:
            current_params[b'name'] = "%d" % ep_obj.scene_absolute_number
        else:
            current_params[b'name'] = 'Season ' + str(ep_obj.scene_season)

        # search
        if ep_obj.show.indexer == 1:
            current_params[b'tvdb'] = ep_obj.show.indexerid
            search_params.append(current_params)
        else:
            name_exceptions = list(
                    set(scene_exceptions.get_scene_exceptions(ep_obj.show.indexerid) + [ep_obj.show.name]))
            for name in name_exceptions:
                # Search by name if we don't have tvdb id
                current_params[b'series'] = sanitizeSceneName(name)
                search_params.append(current_params)

        return search_params

    @staticmethod
    def _get_episode_search_strings(ep_obj, add_string=''):

        if not ep_obj:
            return [{}]

        to_return = []
        search_params = {'category': 'Episode'}

        # episode
        if ep_obj.show.air_by_date or ep_obj.show.sports:
            date_str = str(ep_obj.airdate)

            # BTN uses dots in dates, we just search for the date since that
            # combined with the series identifier should result in just one episode
            search_params[b'name'] = date_str.replace('-', '.')
        elif ep_obj.show.anime:
            search_params[b'name'] = "%i" % int(ep_obj.scene_absolute_number)
        else:
            # Do a general name search for the episode, formatted like SXXEYY
            search_params[b'name'] = "S%02dE%02d" % (ep_obj.scene_season, ep_obj.scene_episode)

        # search
        if ep_obj.show.indexer == 1:
            search_params[b'tvdb'] = ep_obj.show.indexerid
            to_return.append(search_params)
        else:
            # add new query string for every exception
            name_exceptions = list(
                    set(scene_exceptions.get_scene_exceptions(ep_obj.show.indexerid) + [ep_obj.show.name]))
            for cur_exception in name_exceptions:
                search_params[b'series'] = sanitizeSceneName(cur_exception)
                to_return.append(search_params)

        return to_return

    def _doGeneralSearch(self, search_string):
        # 'search' looks as broad is it can find. Can contain episode overview and title for example,
        # use with caution!
        return self._doSearch({'search': search_string})

    def findPropers(self, search_date=None):
        results = []

        search_terms = ['%.proper.%', '%.repack.%']

        for term in search_terms:
            for item in self._doSearch({'release': term}, age=4 * 24 * 60 * 60):
                if item[b'Time']:
                    try:
                        result_date = datetime.fromtimestamp(float(item[b'Time']))
                    except TypeError:
                        result_date = None

                    if result_date:
                        if not search_date or result_date > search_date:
                            title, url = self._get_title_and_url(item)
                            results.append(classes.Proper(title, url, result_date, self.show))

        return results

    def seedRatio(self):
        return self.ratio


class BTNCache(tvcache.TVCache):
    def __init__(self, provider_obj):
        tvcache.TVCache.__init__(self, provider_obj)

        # At least 15 minutes between queries
        self.minTime = 15

    def _getRSSData(self):
        # Get the torrents uploaded since last check.
        seconds_since_last_update = math.ceil(time.time() - time.mktime(self._getLastUpdate().timetuple()))

        # default to 15 minutes
        seconds_minTime = self.minTime * 60
        if seconds_since_last_update < seconds_minTime:
            seconds_since_last_update = seconds_minTime

        # Set maximum to 24 hours (24 * 60 * 60 = 86400 seconds) of "RSS" data search, older things will need to be done through backlog
        if seconds_since_last_update > 86400:
            logging.debug(
                    "The last known successful update was more than 24 hours ago, only trying to fetch the last 24 hours!")
            seconds_since_last_update = 86400

        return {'entries': self.provider._doSearch(search_params=None, age=seconds_since_last_update)}
