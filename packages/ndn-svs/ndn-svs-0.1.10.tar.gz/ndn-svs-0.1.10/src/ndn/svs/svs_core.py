"""
    @Author: Justin C Presley
    @Author-Email: justincpresley@gmail.com
    @Project: NDN State Vector Sync Protocol
    @Source-Code: https://github.com/justincpresley/ndn-python-svs
    @Pip-Library: https://pypi.org/project/ndn-svs/
"""

# Basic Libraries
import asyncio as aio
import logging
from enum import Enum
from random import uniform
from typing import Callable, Optional
# NDN Imports
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
# Custom Imports
from .state_vector import StateVector
from .async_scheduler import AsyncScheduler

class MissingData:
    __slots__ = ('nid','lowSeqNum','highSeqNum')
    def __init__(self, nid:str, lowSeqNum:int, highSeqNum:int) -> None:
        self.nid        = nid
        self.lowSeqNum  = lowSeqNum
        self.highSeqNum = highSeqNum

class SVSyncCore_State(Enum):
    STEADY     = 0
    SUPRESSION = 1

class SVSyncCore:
    def __init__(self, app:NDNApp, syncPrefix:Name, nid:Name, updateCallback:Callable) -> None:
        logging.info(f'SVSyncCore: started svsync core')
        self.state = SVSyncCore_State.STEADY
        self.app = app
        self.nid = nid
        self.updateCallback = updateCallback
        self.syncPrefix = syncPrefix
        self.vector = StateVector()
        self.seqNum = 0
        self.interval = 30000 # time in milliseconds
        self.randomPercent = 0.1
        self.briefInterval = 200 # time in milliseconds
        self.briefRandomPercent = 0.5
        self.app.route(self.syncPrefix)(self.onSyncInterest)
        logging.info(f'SVSyncCore: started listening to {Name.to_str(self.syncPrefix)}')
        self.scheduler = AsyncScheduler(self.sendSyncInterest, self.interval, self.randomPercent)
        self.scheduler.skip_interval()
    async def asyncSendSyncInterest(self) -> None:
        name = self.syncPrefix + [ self.vector.to_component() ]
        logging.info(f'SVSyncCore: sent sync {Name.to_str(name)}')
        try:
            data_name, meta_info, content = await self.app.express_interest(
                name, must_be_fresh=True, can_be_prefix=True, lifetime=1000)
        except (InterestNack, InterestTimeout, InterestCanceled, ValidationFailure) as e:
            pass
    def sendSyncInterest(self) -> None:
        aio.get_event_loop().create_task(self.asyncSendSyncInterest())
    def mergeStateVector(self, otherVector:StateVector) -> None:
        myVectorNew = False
        otherVectorNew = False
        missingList = []

        # check if other vector has a newer state
        for key in otherVector.keys():
            mySeq = self.vector.get(key)
            otherSeq = otherVector.get(key)

            if mySeq < otherSeq:
                otherVectorNew = True
                temp = MissingData(key, mySeq+1, otherSeq)
                self.vector.set(key, otherSeq)
                missingList.append(temp)

        # callback if missing data found
        if missingList:
            self.updateCallback(missingList)

        # check if my vector has a newer state
        for key in self.vector.keys():
            mySeq = self.vector.get(key)
            otherSeq = otherVector.get(key)
            if otherVector.get(key) < self.vector.get(key):
                myVectorNew = True

        # return bools
        return (myVectorNew, otherVectorNew)
    def onSyncInterest(self, int_name:FormalName, int_param:InterestParam, _app_param:Optional[BinaryStr]) -> None:
        logging.info(f'SVSyncCore: received sync {Name.to_str(int_name)}')
        incomingVector = StateVector(int_name[-1])

        myVectorNew, incomingVectorNew = self.mergeStateVector(incomingVector)
        self.state = SVSyncCore_State.SUPRESSION if myVectorNew else SVSyncCore_State.STEADY

        # reset the sync timer if STEADY
        # supress the timer if SUPPRESION
        if self.state == SVSyncCore_State.STEADY:
            self.scheduler.set_cycle()
        else:
            delay = self.briefInterval + round( uniform(-self.briefRandomPercent,self.briefRandomPercent)*self.briefInterval )
            if self.scheduler.get_time_left() > delay:
                self.scheduler.set_cycle(delay)
        logging.info(f'SVSyncCore: state {self.state.name}')
        logging.info(f'SVSyncCore: vector {self.vector.to_str()}')
    def updateStateVector(self, seqNum:int, nid:Name=None) -> None:
        if not nid:
            nid = self.nid
        if Name.to_str(nid) == Name.to_str(self.nid):
            self.seqNum = seqNum
        self.vector.set(Name.to_str(nid), seqNum)
        self.scheduler.skip_interval()
    def getSeqNum(self) -> int:
        return self.seqNum
    def getStateVector(self) -> StateVector:
        return self.vector