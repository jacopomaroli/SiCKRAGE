# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
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


from hashlib import md5

from CodernityDB3.hash_index import HashIndex


class MainVersionIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainVersionIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'version' and data.get('database_version'):
            key = data.get('database_version')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainTVShowsIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainTVShowsIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'tv_shows' and data.get('indexer_id'):
            key = data.get('indexer_id')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainTVEpisodesIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainTVEpisodesIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'tv_episodes' and data.get('showid'):
            key = data.get('showid')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainIMDBInfoIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainIMDBInfoIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'imdb_info' and data.get('indexer_id'):
            key = data.get('indexer_id')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainSceneNumberingIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainSceneNumberingIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'scene_numbering' and data.get('indexer_id'):
            key = data.get('indexer_id')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainXEMRefreshIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainXEMRefreshIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'xem_refresh' and data.get('indexer_id'):
            key = data.get('indexer_id')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainIndexerMappingIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainIndexerMappingIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'indexer_mapping' and data.get('indexer_id'):
            key = data.get('indexer_id')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainHistoryIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainHistoryIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'history' and data.get('showid'):
            key = data.get('showid')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainBlacklistIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainBlacklistIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'blacklist' and data.get('show_id'):
            key = data.get('show_id')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainWhitelistIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainWhitelistIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'whitelist' and data.get('show_id'):
            key = data.get('show_id')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainFailedSnatchesIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainFailedSnatchesIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'failed_snatches' and data.get('release'):
            key = data.get('release')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None


class MainFailedSnatchHistoryIndex(HashIndex):
    _version = 1

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(MainFailedSnatchHistoryIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        if not isinstance(key, bytes):
            if not isinstance(key, str):
                key = str(key)
            key = key.encode()
        return md5(key).hexdigest().encode()

    def make_key_value(self, data):
        if data.get('_t') == 'failed_snatch_history' and data.get('showid'):
            key = data.get('showid')
            if not isinstance(key, bytes):
                if not isinstance(key, str):
                    key = str(key)
                key = key.encode()
            return md5(key).hexdigest().encode(), None
