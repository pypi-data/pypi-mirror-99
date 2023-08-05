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

IUserInbox_VERSION = "4.1.54978"

class IUserInbox(BaseEndpoint):
    def __init__(self, apiKey, url ,domainUid ,userUid ):
        self.url = url
        self.apiKey = apiKey
        self.base = url +'/inbox/{domainUid}/{userUid}'
        self.domainUid_ = domainUid
        self.base = self.base.replace('{domainUid}',domainUid)
        self.userUid_ = userUid
        self.base = self.base.replace('{userUid}',userUid)

    def unseen (self):
        postUri = "/_unseen";
        __data__ = None
        __encoded__ = None
        queryParams = {  };

        response = requests.get( self.base + postUri, params = queryParams, verify=False, headers = {'X-BM-ApiKey' : self.apiKey, 'Accept' : 'application/json', 'X-BM-ClientVersion' : IUserInbox_VERSION}, data = __encoded__);
        return self.handleResult__(serder.INT, response)
