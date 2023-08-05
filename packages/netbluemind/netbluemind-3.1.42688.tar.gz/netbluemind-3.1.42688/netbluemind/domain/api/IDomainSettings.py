#
#  BEGIN LICENSE
#  Copyright (c) Blue Mind SAS, 2012-2016
# 
#  This file is part of BlueMind. BlueMind is a messaging and collaborative
#  solution.
# 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of either the GNU Affero General Public License as
#  published by the Free Software Foundation (version 3 of the License).
# 
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# 
#  See LICENSE.txt
#  END LICENSE
#
import requests
import json
from netbluemind.python import serder
from netbluemind.python.client import BaseEndpoint

IDomainSettings_VERSION = "3.1.42688"

class IDomainSettings(BaseEndpoint):
    def __init__(self, apiKey, url ,containerUid ):
        self.url = url
        self.apiKey = apiKey
        self.base = url +'/domains/{containerUid}'
        self.containerUid_ = containerUid
        self.base = self.base.replace('{containerUid}',containerUid)

    def set (self, settings ):
        postUri = "/_settings";
        __data__ = None
        __encoded__ = None
        __data__ = serder.MapSerDer(serder.STRING).encode(settings)
        __encoded__ = json.dumps(__data__)
        queryParams = {   };

        response = requests.put( self.base + postUri, params = queryParams, verify=False, headers = {'X-BM-ApiKey' : self.apiKey, 'Accept' : 'application/json', 'X-BM-ClientVersion' : IDomainSettings_VERSION}, data = __encoded__);
        return self.handleResult__(None, response)
    def get (self):
        postUri = "/_settings";
        __data__ = None
        __encoded__ = None
        queryParams = {  };

        response = requests.get( self.base + postUri, params = queryParams, verify=False, headers = {'X-BM-ApiKey' : self.apiKey, 'Accept' : 'application/json', 'X-BM-ClientVersion' : IDomainSettings_VERSION}, data = __encoded__);
        return self.handleResult__(serder.MapSerDer(serder.STRING), response)
