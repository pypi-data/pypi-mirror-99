# Copyright 2019 Objectif Libre
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
#
from unittest import mock

from cloudkitty.api.v2.summary import summary
from cloudkitty import tests

from cloudkitty.utils import tz as tzutils


class TestSummaryEndpoint(tests.TestCase):

    def setUp(self):
        super(TestSummaryEndpoint, self).setUp()
        self.endpoint = summary.Summary()

    def test_type_filter_is_passed_separately(self):
        policy_mock = mock.patch('cloudkitty.common.policy.authorize')
        with mock.patch.object(self.endpoint._storage, 'total') as total_mock:
            with policy_mock, mock.patch('flask.request') as fmock:
                total_mock.return_value = {'total': 0, 'results': []}
                fmock.args.lists.return_value = [
                    ('filters', 'a:b,type:awesome')]
                self.endpoint.get()
                total_mock.assert_called_once_with(
                    begin=tzutils.get_month_start(),
                    end=tzutils.get_next_month(),
                    groupby=None,
                    filters={'a': 'b'},
                    metric_types=['awesome'],
                    offset=0,
                    limit=100,
                    paginate=True,
                )
