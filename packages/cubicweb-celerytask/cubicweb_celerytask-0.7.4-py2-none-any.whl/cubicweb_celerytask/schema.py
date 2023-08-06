# -*- coding: utf-8 -*-
# copyright 2016-2021 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-celerytask schema"""


from yams.buildobjs import RelationDefinition, String

from cubicweb.schema import WorkflowableEntityType


class CeleryTask(WorkflowableEntityType):
    task_id = String(maxsize=40, required=False, indexed=True, unique=True)
    task_name = String(required=True)


class parent_task(RelationDefinition):
    object = 'CeleryTask'
    subject = 'CeleryTask'
    cardinality = '?*'
    composite = 'object'
    inlined = True
