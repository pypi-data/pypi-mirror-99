"""Dependency between tasks and tokens"""

from enum import Enum
from .utils import logger
from typing import Set
from .locking import Lock
import threading


class Dependents:
    """Encapsulate the access to the dependents"""

    def __init__(self):
        self.lock = threading.Lock()
        self._dependents: Set[Dependency] = set()  # as source

    def add(self, dependency):
        with self.lock:
            self._dependents.add(dependency)

    def __enter__(self):
        # Returns the set after locking
        self.lock.__enter__()
        return self._dependents

    def __exit__(self, *args):
        self.lock.__exit__(*args)


class Resource:
    def __init__(self):
        self.dependents = Dependents()


class DependencyStatus(Enum):
    WAIT = 0
    """Waiting for dependency to be available"""

    OK = 1
    """Dependency can be locked"""

    FAIL = 2
    """Dependency won't be availabe in the foreseeable future"""


class Dependency:
    # Dependency status

    def __init__(self, origin):
        # Origin and target are two resources
        self.origin = origin
        self.target = None
        self.currentstatus = DependencyStatus.WAIT

    def status(self) -> DependencyStatus:
        raise NotImplementedError()

    def lock(self) -> Lock:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return "Dep[{origin}->{target}]/{currentstatus}".format(**self.__dict__)

    def check(self):
        status = self.status()
        logger.debug("Dependency check: %s", self)
        if status != self.currentstatus:
            logger.debug(
                "Dependency %s is %s (was: %s)", self, status, self.currentstatus
            )
            self.target.dependencychanged(self, self.currentstatus, status)
            self.currentstatus = status
