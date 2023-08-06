# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkrds.endpoint import endpoint_data

class ModifyDBProxyEndpointRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Rds', '2014-08-15', 'ModifyDBProxyEndpoint','rds')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_ConfigDBProxyFeatures(self):
		return self.get_query_params().get('ConfigDBProxyFeatures')

	def set_ConfigDBProxyFeatures(self,ConfigDBProxyFeatures):
		self.add_query_param('ConfigDBProxyFeatures',ConfigDBProxyFeatures)

	def get_DBInstanceId(self):
		return self.get_query_params().get('DBInstanceId')

	def set_DBInstanceId(self,DBInstanceId):
		self.add_query_param('DBInstanceId',DBInstanceId)

	def get_ReadOnlyInstanceWeight(self):
		return self.get_query_params().get('ReadOnlyInstanceWeight')

	def set_ReadOnlyInstanceWeight(self,ReadOnlyInstanceWeight):
		self.add_query_param('ReadOnlyInstanceWeight',ReadOnlyInstanceWeight)

	def get_ReadOnlyInstanceMaxDelayTime(self):
		return self.get_query_params().get('ReadOnlyInstanceMaxDelayTime')

	def set_ReadOnlyInstanceMaxDelayTime(self,ReadOnlyInstanceMaxDelayTime):
		self.add_query_param('ReadOnlyInstanceMaxDelayTime',ReadOnlyInstanceMaxDelayTime)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_DbEndpointAliases(self):
		return self.get_query_params().get('DbEndpointAliases')

	def set_DbEndpointAliases(self,DbEndpointAliases):
		self.add_query_param('DbEndpointAliases',DbEndpointAliases)

	def get_DbEndpointOperator(self):
		return self.get_query_params().get('DbEndpointOperator')

	def set_DbEndpointOperator(self,DbEndpointOperator):
		self.add_query_param('DbEndpointOperator',DbEndpointOperator)

	def get_DbEndpointType(self):
		return self.get_query_params().get('DbEndpointType')

	def set_DbEndpointType(self,DbEndpointType):
		self.add_query_param('DbEndpointType',DbEndpointType)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_DbEndpointReadWriteMode(self):
		return self.get_query_params().get('DbEndpointReadWriteMode')

	def set_DbEndpointReadWriteMode(self,DbEndpointReadWriteMode):
		self.add_query_param('DbEndpointReadWriteMode',DbEndpointReadWriteMode)

	def get_DBProxyEndpointId(self):
		return self.get_query_params().get('DBProxyEndpointId')

	def set_DBProxyEndpointId(self,DBProxyEndpointId):
		self.add_query_param('DBProxyEndpointId',DBProxyEndpointId)

	def get_ReadOnlyInstanceDistributionType(self):
		return self.get_query_params().get('ReadOnlyInstanceDistributionType')

	def set_ReadOnlyInstanceDistributionType(self,ReadOnlyInstanceDistributionType):
		self.add_query_param('ReadOnlyInstanceDistributionType',ReadOnlyInstanceDistributionType)