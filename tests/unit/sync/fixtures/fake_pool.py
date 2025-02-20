# Copyright (c) "Neo4j"
# Neo4j Sweden AB [https://neo4j.com]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pytest

from neo4j._conf import PoolConfig
from neo4j._sync.io._pool import IOPool


__all__ = [
    "fake_pool",
]


@pytest.fixture
def fake_pool(fake_connection_generator, mocker):
    pool = mocker.MagicMock(spec=IOPool)
    assert not hasattr(pool, "acquired_connection_mocks")
    pool.buffered_connection_mocks = []
    pool.acquired_connection_mocks = []
    pool.pool_config = PoolConfig()

    def acquire_side_effect(*_, **__):
        if pool.buffered_connection_mocks:
            connection = pool.buffered_connection_mocks.pop()
        else:
            connection = fake_connection_generator()
        pool.acquired_connection_mocks.append(connection)
        return connection

    pool.acquire.side_effect = acquire_side_effect
    return pool
