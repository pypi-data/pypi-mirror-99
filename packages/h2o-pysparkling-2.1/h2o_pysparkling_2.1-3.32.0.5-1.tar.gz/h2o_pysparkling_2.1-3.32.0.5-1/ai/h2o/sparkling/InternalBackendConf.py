#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import warnings
from ai.h2o.sparkling.SharedBackendConfUtils import SharedBackendConfUtils


class InternalBackendConf(SharedBackendConfUtils):

    #
    # Getters
    #

    def numH2OWorkers(self):
        return self._get_option(self._jconf.numH2OWorkers())

    def drddMulFactor(self):
        return self._jconf.drddMulFactor()

    def numRddRetries(self):
        return self._jconf.numRddRetries()

    def defaultCloudSize(self):
        return self._jconf.defaultCloudSize()

    def subseqTries(self):
        return self._jconf.subseqTries()

    def hdfsConf(self):
        return self._get_option(self._jconf.hdfsConf())

    def spreadRddRetriesTimeout(self):
        return self._jconf.spreadRddRetriesTimeout()

    def nodeIcedDir(self):
        return self._get_option(self._jconf.nodeIcedDir())


    #
    # Setters
    #

    def setNumH2OWorkers(self, value):
        self._jconf.setNumH2OWorkers(value)
        return self

    def setDrddMulFactor(self, value):
        self._jconf.setDrddMulFactor(value)
        return self

    def setNumRddRetries(self, value):
        self._jconf.setNumRddRetries(value)
        return self

    def setDefaultCloudSize(self, value):
        self._jconf.setDefaultCloudSize(value)
        return self

    def setSubseqTries(self, value):
        self._jconf.setSubseqTries(value)
        return self

    def setHdfsConf(self, value):
        self._jconf.setHdfsConf(value)
        return self

    def setSpreadRddRetriesTimeout(self, value):
        self._jconf.setSpreadRddRetriesTimeout(value)
        return self

    def setNodeIcedDir(self, value):
        self._jconf.setNodeIcedDir(value)
        return self
