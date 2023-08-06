from __future__ import print_function
import sys
import os
import logging
import json
import copy
from os.path import dirname
from jsonschema import validate
import importlib
import pkgutil
import tempfile
import uuid
from halocli.exception import HaloPluginException
from halocli.util import Util

logger = logging.getLogger(__name__)

logging.root.setLevel(logging.INFO)

"""
the bian plugin
---------------

1. extend bian swagger files

2. add proprietary bank fields from legacy - done

3. add mappings from legacy to bian fields

4. generate collection-filter parameter list

5. add sub BQ as needed

6. add new endpoints as needed

7. refactor bian types in specific fields where type is generic(string, etc..)

8. add version metadata for control and traceability

"""

class Plugin():

    def __init__(self,halo):
        #init vars
        self.halo = halo

        #init work on halo config
        #if self.halo.config ...

        self.name = 'extend'
        self.desc = 'extend bian swagger file'

        # set commands
        self.commands = {
            'swagger': {
                'usage': "Create an extended swagger file",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's',
                        'required': True
                    },
                    'path': {
                        'usage': 'Path of the swagger file dir',
                        'shortcut': 'p',
                        'required': True
                    },
                    'fields': {
                        'usage': 'add fields',
                        'shortcut': 'f'
                    },
                    'refactor': {
                        'usage': 'refactor existing fields',
                        'shortcut': 'r'
                    },
                    'headers': {
                        'usage': 'add headers',
                        'shortcut': 'h'
                    },
                    'errors': {
                        'usage': 'add errors',
                        'shortcut': 'e'
                    },
                    'all': {
                        'usage': 'run all options',
                        'shortcut': 'a'
                    }
                },
            },
            'mappings': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's'
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    }
                },
            },
            'filter': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's'
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    }
                },
            },
        }

        # set hooks
        self.hooks = {
            'before:swagger:generate': self.before_swagger_generate,
            'swagger:generate': self.swagger_generate,
            'after:swagger:generate': self.after_swagger_generate,
            'swagger:write': self.swagger_write,
            'mapping:generate': self.mapping_generate,
            'mapping:write': self.mapping_write,
            'filter:generate': self.filter_generate,
            'filter:write': self.filter_write,
        }

        #logger.info('finished plugin')

    def run_plugin(self,options):
        self.options = options
        #do more


    def before_swagger_generate(self):
        for o in self.options:
            if 'service' in o:
                self.service = o['service']
            if 'path' in o:
                self.path = o['path']
            if 'all' in o:
                self.all = o['all']
            if 'fields' in o:
                self.fields = o['fields']
            if 'refactor' in o:
                self.refactor = o['refactor']
            if 'headers' in o:
                self.headers = o['headers']
            if 'errors' in o:
                self.errors = o['errors']
        if not self.service:
            raise Exception("no service found")
        urls = self.halo.settings['mservices'][self.service]['record']['path']
        self.data = Util.analyze_swagger(urls)
        if "methods" in self.halo.settings['mservices'][self.service]['record']:
            self.methods = self.halo.settings['mservices'][self.service]['record']['methods']
            if "exclude" in self.halo.settings['mservices'][self.service]['record']:
                self.exclude = self.halo.settings['mservices'][self.service]['record']['exclude']
            else:
                self.exclude = False
        else:
            self.methods = []

    def swagger_generate(self):
        data = self.data
        tmp = {}
        clear = []
        for d in data['paths']:
            m = data['paths'][d]
            for o in m:
                if m[o]['operationId'] in self.methods:
                    new_m = copy.deepcopy(m)
                    tmp[d] = new_m
                    break
            if self.exclude:
                if d not in tmp:
                    clear.append(d)
        for d in clear:
            del data['paths'][d]
        if self.refactor or self.all:
            for k in tmp:
                new_m = tmp[k]
                for o in new_m:
                    if '200' in new_m[o]['responses']:
                        if 'items' in new_m[o]['responses']['200']['schema']:
                            props = new_m[o]['responses']['200']['schema']['items']['properties']
                        else:
                            props = new_m[o]['responses']['200']['schema']['properties']
                    else:
                        if 'items' in new_m[o]['responses']['201']['schema']:
                            props = new_m[o]['responses']['201']['schema']['items']['properties']
                        else:
                            props = new_m[o]['responses']['201']['schema']['properties']
                    mthd = new_m[o]['operationId']
                    for p in props:
                        for target in self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['refactor']:
                            fields = target['field'].split(".")
                            propsx = props
                            for name in fields:
                                if name in propsx:
                                    propsx = propsx[name]
                                else:
                                    if 'properties' in propsx:
                                        propsx = propsx['properties'][name]
                                    else:
                                        propsx = None
                                        break
                            if propsx:
                                propsx['type'] = target['type']
                                if "format" in target:
                                    propsx['format'] = target['format']
                                if 'properties' in target:
                                    propsx['properties'] = {}
                data['paths'][k] = new_m
            self.halo.cli.log("finished refactor successfully")
        # fix the response and add
        if self.fields or self.all:
            # fix name
            if "company" in self.halo.settings['mservices'][self.service]['record']:
                data["info"]["title"] = self.halo.settings['mservices'][self.service]['record']['company'] + " - " + \
                                        data["info"]["title"]
            for k in tmp:
                new_m = tmp[k]
                for o in new_m:
                    if '200' in new_m[o]['responses']:
                        if 'items' in new_m[o]['responses']['200']['schema']:
                            props = new_m[o]['responses']['200']['schema']['items']['properties']
                        else:
                            props = new_m[o]['responses']['200']['schema']['properties']
                    else:
                        if 'items' in new_m[o]['responses']['201']['schema']:
                            props = new_m[o]['responses']['201']['schema']['items']['properties']
                        else:
                            props = new_m[o]['responses']['201']['schema']['properties']
                    mthd = new_m[o]['operationId']
                    for p in props:
                        for target in self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['added_fields']:
                            fields = target.split(".")
                            propsx = props
                            for name in fields:
                                if name in propsx:
                                    propsx = propsx[name]
                                else:
                                    if 'properties' in propsx:
                                        propsx = propsx['properties'][name]
                                    else:
                                        propsx = None
                                        break
                            if propsx:
                                for fld in self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['added_fields'][target]:
                                    type = self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['added_fields'][target][fld]
                                    propsx['properties'][fld] = type
                                    self.halo.cli.log(new_m['get']['operationId'] + ":" +fld)
                data['paths'][k] = new_m
            self.halo.cli.log("finished fields successfully")
        if self.headers or self.all:
            self.halo.cli.log("finished headers successfully")
        if self.errors or self.all:
            self.halo.cli.log("finished errors successfully")
        self.halo.cli.log("finished extend successfully")


    def after_swagger_generate(self):
        data = self.data
        Util.validate_swagger(data)

    def swagger_write(self):
        self.file_write()

    def file_write(self):
        try:
            path = self.path
            if path:
                file_path = os.path.join(path, str(uuid.uuid4()) + "_extend.json")
            else:
                dir_tmp = tempfile.TemporaryDirectory()
                file_path = os.path.join(dir_tmp.name, str(uuid.uuid4()) + "_extend.json")
            logger.debug(file_path)
            f = open(file_path, "a")
            f.write("")
            f.close()
            Util.dump_file(file_path, self.data)
            logging.debug("Swagger file generated:" + file_path)
            """
            with open(file_path, 'r') as fi:
                f = fi.read()
                print(str(f))
                return f
            """
        except Exception as e:
            raise HaloPluginException(str(e))

    def refactor_generate(self):
        data = self.data
        tmp = {}
        for d in data['paths']:
            m = data['paths'][d]
            if 'get' in m:
                if 'ReferenceIdsExtend' in m['get']['operationId']:
                    new_m = copy.deepcopy(m)
                    tmp[d] = new_m
        # fix the response and add
        for k in tmp:
            # bq methods
            ref_m = tmp[k]
            new_m = copy.deepcopy(ref_m)
            if '200' in new_m['get']['responses']:
                if 'items' in new_m['get']['responses']['200']['schema']:
                    props = new_m['get']['responses']['200']['schema']['items']['properties']
                else:
                    props = new_m['get']['responses']['200']['schema']['properties']
            else:
                if 'items' in new_m['get']['responses']['201']['schema']:
                    props = new_m['get']['responses']['201']['schema']['items']['properties']
                else:
                    props = new_m['get']['responses']['201']['schema']['properties']
            for p in props:
                if "methods" in self.halo.settings['mservices'][self.service]['record']:
                    for mthd in self.halo.settings['mservices'][self.service]['record']['methods']:
                        if mthd == new_m['get']['operationId']:
                            for target in self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['refactor']:
                                fields = target['field'].split(".")
                                if p.endswith(fields[0]):
                                    #self.halo.cli.log(new_m['get']['operationId']+":"+p)
                                    size = len(fields)
                                    i = 1
                                    propsx = props[p]
                                    while i < size:
                                        name = fields[i]
                                        propsx = propsx['properties'][name]
                                        i = i + 1
                                    type = target['type']
                                    propsx['type'] = type
            data['paths'][k] = new_m

    def after_refactor_generate(self):
        pass

    def refactor_write(self):
        self.file_write()

    def mapping_generate(self):
        pass

    def mapping_write(self):
        pass

    def filter_generate(self):
        pass

    def filter_write(self):
        pass