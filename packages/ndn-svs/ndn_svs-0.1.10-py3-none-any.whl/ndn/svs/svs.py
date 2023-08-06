"""
    @Author: Justin C Presley
    @Author-Email: justincpresley@gmail.com
    @Project: NDN State Vector Sync Protocol
    @Source-Code: https://github.com/justincpresley/ndn-python-svs
    @Pip-Library: https://pypi.org/project/ndn-svs/
"""

# Basic Libraries
from typing import Callable, Optional
# NDN Imports
from ndn.app import NDNApp
from ndn.encoding import Name
from ndn_python_repo import Storage
# Custom Imports
from .svs_base import SVSyncBase

class SVSync(SVSyncBase):
    def __init__(self, app:NDNApp, groupPrefix:Name, nid:Name, updateCallback:Callable, storage:Optional[Storage]=None) -> None:
        self.groupPrefix = groupPrefix
        preSyncPrefix = self.groupPrefix
        preDataPrefix = nid + self.groupPrefix
        super().__init__(app, preSyncPrefix, preDataPrefix, nid, updateCallback, storage)
    def getDataName(self, nid:Name, seqNum:int) -> Name:
        return ( nid + self.groupPrefix + Name.from_str( "/epoch-"+str(seqNum) ) )