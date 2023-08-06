"""Module containing the implementation of ParameterStore class."""
# pylint: disable=protected-access

import datetime
import boto3


__all__ = [
    # Class exports
    'ParameterStore'
]


class ParameterStore:
    """Provide a dict-like interface to access AWS Parameter Store."""
    def __init__(self, path=None, ssm_client=None, ttl=None):
        self._path = (path or '').rstrip('/') + '/'
        self._client = ssm_client or boto3.client('ssm')
        self._keys = None
        self._substores = {}
        self._ttl = ttl

    def get(self, name, **kwargs):
        """Retrieves the value or sub-parameters of a given parameter name."""
        assert name, 'Name can not be empty'
        if self._keys is None:
            self.refresh()

        abs_key = "%s%s" % (self._path, name)
        if name not in self._keys:
            if 'default' in kwargs:
                return kwargs['default']

            raise KeyError(name)

        if self._keys[name]['type'] == 'path':
            if abs_key not in self._substores:
                store = self.__class__(path=abs_key, ssm_client=self._client, ttl=self._ttl)
                store._keys = self._keys[name]['children']
                self._substores[abs_key] = store

            return self._substores[abs_key]

        return self._get_value(name, abs_key)

    def refresh(self):
        """Refreshes the originally fetched parameters."""
        self._keys = {}
        self._substores = {}

        paginator = self._client.get_paginator('describe_parameters')
        pager = paginator.paginate(
            ParameterFilters=[
                dict(Key="Path", Option="Recursive", Values=[self._path])
            ]
        )

        for pages in pager:
            for page in pages['Parameters']:
                paths = page['Name'][len(self._path):].split('/')
                self._update_keys(self._keys, paths)

    @classmethod
    def _update_keys(cls, keys, paths):
        name = paths[0]

        # this is a path
        if len(paths) > 1:
            if name not in keys:
                keys[name] = {'type': 'path', 'children': {}}

            cls._update_keys(keys[name]['children'], paths[1:])
        else:
            keys[name] = {'type': 'parameter', 'expire': None}

    def keys(self):
        """Returns the keys that an instance has already fetched before."""
        if self._keys is None:
            self.refresh()

        return self._keys.keys()

    def _get_value(self, name, abs_key):
        entry = self._keys[name]

        # Simple TTL implementation
        if self._ttl is False or (entry['expire'] and entry['expire'] <= datetime.datetime.now()):
            entry.pop('value', None)

        if 'value' not in entry:
            parameter = self._client.get_parameter(Name=abs_key, WithDecryption=True)['Parameter']
            value = parameter['Value']
            if parameter['Type'] == 'StringList':
                value = value.split(',')

            entry['value'] = value

            if self._ttl:
                entry['expire'] = datetime.datetime.now() + datetime.timedelta(seconds=self._ttl)
            else:
                entry['expire'] = None

        return entry['value']

    def __contains__(self, name):
        try:
            self.get(name)
            return True
        except:  # pylint: disable=bare-except
            return False

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __delitem__(self, name):
        raise NotImplementedError()

    def __repr__(self):
        return f'ParameterStore(path={self._path!r})'
