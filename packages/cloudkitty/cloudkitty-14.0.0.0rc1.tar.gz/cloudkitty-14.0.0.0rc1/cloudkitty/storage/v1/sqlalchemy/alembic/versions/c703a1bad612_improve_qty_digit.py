# Copyright 2017 OpenStack Foundation
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

"""improve_qty_digit

Revision ID: c703a1bad612
Revises: 307430ab38bc
Create Date: 2017-04-01 09:33:41.434750

"""

# revision identifiers, used by Alembic.
revision = 'c703a1bad612'
down_revision = '307430ab38bc'

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade():
    with op.batch_alter_table('rated_data_frames') as batch_op:
        batch_op.alter_column(
            'qty',
            type_=sa.Numeric(15, 5),
            existing_type=sa.Numeric())
