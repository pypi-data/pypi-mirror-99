# Copyright (c) 2020 - 2020 TomTom N.V. All rights reserved.
#
# This software is the proprietary copyright of TomTom N.V. and its subsidiaries and may be
# used for internal evaluation purposes or commercial use strictly subject to separate
# licensee agreement between you and TomTom. If you are the licensee, you are only permitted
# to use this Software in accordance with the terms of your license agreement. If you are
# not the licensee, then you are not authorized to use this software in any manner and should
# immediately return it to TomTom N.V.

from copy import copy
from datetime import datetime
from decimal import Decimal
from typing import (
    Dict,
    Final,
    List,
    Optional,
    Sequence,
    Tuple,
)
import xml.etree.ElementTree as ET

class JUnitError:
    description: str
    message: Optional[str]
    type: Optional[str]

    def __init__(
        self,
        description: str,
        *,
        message: Optional[str] = None,
        type: Optional[str] = None,
    ):


class JUnitTestCase:
    name: str
    assertions: Optional[int] = None
    time: Optional[Decimal] = None
    classname: Optional[str] = None
    status: Optional[str] = None

    extra: Dict[str, str]

    skipped: Optional[JUnitError] = None
    errors: Sequence[JUnitError]
    failures: Sequence[JUnitError]

    stdout: Union[List[str], Tuple[str]]
    stderr: Union[List[str], Tuple[str]]

    def __init__(
        self,
        name: str,
        *,
        assertions: Optional[int] = None,
        time: Optional[Decimal] = None,
        classname: Optional[str] = None,
        status: Optional[str] = None,
        extra: Dict[str, str] = {},
        skipped: Optional[JUnitError] = None,
        errors: Sequence[JUnitError] = (),
        failures: Sequence[JUnitError] = (),
        stdout: Union[List[str], Tuple[str]] = (),
        stderr: Union[List[str], Tuple[str]] = (),
    ):
        self.name = name
        self.assertions = assertions
        self.time = time
        self.classname = classname
        self.status = status
        self.extra = extra
        self.skipped = skipped
        self.errors = copy(errors)


        self.extra = {}
        self.errors = []
        self.failures = []
        self.stdout = []
        self.stderr = []


class JUnitSuite:
    name: str
    hostname: Optional[str]
    id: Optional[int]
    package: Optional[str]
    timestamp: Optional[datetime]

    cases: Sequence[JUnitTestCase]

    def __init__(self, name: str, *, id: Optional[str] = None):

def to_xml(name, cases: List[JUnitTestCase]):
    testsuite = ET.Element("testsuite")
    disabled = 0
    skipped = 0
    errors = 0
    failures = 0
    tests = 0
    time = Decimal()

    for case in cases:
        skipped += len(case.skipped)
        error += len(case.errors)
        failures += len(case.failures)
        tests += 1
        time += case.time
