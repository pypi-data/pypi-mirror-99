# Copyright (c) 2016 Cloudbase Solutions Srl
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""A Hyper-V Cluster Nova Compute driver."""

from compute_hyperv.nova.cluster import driver

# NOTE: nova changed the way it imports drivers. All drivers must belong
# in the nova.virt namespace.

HyperVClusterDriver = driver.HyperVClusterDriver
