"""
    @Author: Justin C Presley
    @Author-Email: justincpresley@gmail.com
    @Project: NDN State Vector Sync Protocol
    @Source-Code: https://github.com/justincpresley/ndn-python-svs
    @Pip-Library: https://pypi.org/project/ndn-svs/
"""

# Basic Libraries
import logging
from typing import Optional, Callable
# NDN Imports
from ndn.app import NDNApp
from ndn.encoding import Name, make_data, MetaInfo, parse_data, InterestParam, BinaryStr, FormalName
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn_python_repo import Storage
# Custom Imports
from .svs_core import SVSyncCore
from .svs_storage import SVSyncStorage

# Abstract Class to Derive Different SVSyncs from
class SVSyncBase():
    def __init__(self, app:NDNApp, syncPrefix:Name, dataPrefix:Name, nid:Name, updateCallback:Callable, storage:Optional[Storage]=None) -> None:
        logging.info(f'SVSync: started svsync')
        self.app = app
        self.storage = SVSyncStorage() if not storage else storage
        self.syncPrefix = syncPrefix
        self.dataPrefix = dataPrefix
        self.nid = nid
        self.updateCallback = updateCallback
        self.core = SVSyncCore(self.app, self.syncPrefix, self.nid, self.updateCallback)
        self.app.route(self.dataPrefix)(self.onDataInterest)
        logging.info(f'SVSync: started listening to {Name.to_str(self.dataPrefix)}')
    def onDataInterest(self, int_name:FormalName, int_param:InterestParam, _app_param:Optional[BinaryStr]) -> None:
        data_bytes = self.storage.get_data_packet(int_name, int_param.can_be_prefix)
        if data_bytes:
            _, _, content, _ = parse_data(data_bytes)
            logging.info(f'SVSync: served data {bytes(content)}')
            self.app.put_data(int_name, content=bytes(content), freshness_period=500)
    async def fetchData(self, nid:Name, seqNum:int, retries:int=0) -> Optional[bytes]:
        name = self.getDataName(nid, seqNum)
        while retries+1 > 0:
            try:
                logging.info(f'SVSync: fetching data {Name.to_str(name)}')
                ex_int_name, meta_info, content = await self.app.express_interest(name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
                logging.info(f'SVSync: received data {bytes(content)}')
                return bytes(content) if content else None
            except InterestNack as e:
                logging.warning(f'SVSync: nacked with reason={e.reason}')
            except InterestTimeout:
                logging.warning(f'SVSync: timeout')
            except InterestCanceled:
                logging.warning(f'SVSync: canceled')
            except ValidationFailure:
                logging.warning(f'SVSync: data failed to validate')
            except Exception as e:
                logging.warning(f'SVSync: unknown error has occured: {e}')

            retries = retries - 1
            if retries+1 > 0:
                logging.info(f'SVSync: retrying fetching data')
        return None
    def publishData(self, data:bytes) -> None:
        name = self.getDataName(self.nid, self.core.getSeqNum()+1)
        data_packet = make_data(name, MetaInfo(freshness_period=5000), content=data)
        logging.info(f'SVSync: publishing data {Name.to_str(name)}')
        self.storage.put_data_packet(name, data_packet)
        self.core.updateStateVector(self.core.getSeqNum()+1)
    def getCore(self) -> SVSyncCore:
        return self.core
    def getDataName(self, nid:Name, seqNum:int) -> Name:
        raise NotImplementedError