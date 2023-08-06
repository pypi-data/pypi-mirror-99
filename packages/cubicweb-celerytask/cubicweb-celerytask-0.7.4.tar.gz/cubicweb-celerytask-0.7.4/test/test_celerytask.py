# coding: utf-8
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

"""cubicweb-celerytask automatic tests"""

import collections
import datetime
import json
import logging
import time
import os.path

import six
import celery
import celery.result
import mock

from cubicweb.devtools import testlib  # noqa

from cubicweb_celerytask.ccplugin import CeleryMonitorCommand
from cubicweb_celerytask.entities import (start_async_task, StartCeleryTaskOp,
                                          run_all_tasks)
from cubicweb_celerytask.testutils import BaseCeleryTaskTC

from cw_celerytask_helpers.monitor import MONITOR_KEY
from cw_celerytask_helpers.utils import get_redis_client
from cw_celerytask_helpers.filelogger import get_log_filename


def wait_until(func, timeout=10, retry=1):
    start = time.time()
    while abs(time.time() - start) < timeout:
        if func():
            break
        time.sleep(retry)
    else:
        raise AssertionError(
            'predicate has not been verified since %ds' % timeout)


class CeleryTaskTC(BaseCeleryTaskTC):

    def test_success_task(self):
        with self.admin_access.repo_cnx() as cnx:
            cwtask_eid = start_async_task(cnx, 'success', 42).eid
            cnx.commit()
            cwtask = cnx.entity_from_eid(cwtask_eid)
            run_all_tasks(cnx)
            self.wait_async_task(cnx, cwtask.task_id)
            result = cwtask.cw_adapt_to('ICeleryTask').result
            self.assertEqual(result.get(), 42)
            wf = cwtask.cw_adapt_to('IWorkflowable')
            self.assertEqual(wf.state, 'done')

    def test_fail_task(self):
        with self.admin_access.repo_cnx() as cnx:
            cwtask_eid = start_async_task(cnx, 'fail').eid
            cnx.commit()
            run_all_tasks(cnx)
            cwtask = cnx.entity_from_eid(cwtask_eid)
            self.wait_async_task(cnx, cwtask.task_id)
            result = cwtask.cw_adapt_to('ICeleryTask').result
            tb = result.traceback
            self.assertTrue(result.failed())
            self.assertTrue(tb.startswith('Traceback (most recent call last)'))
            self.assertTrue(tb.endswith('RuntimeError: fail\n'))
            wf = cwtask.cw_adapt_to('IWorkflowable')
            self.assertEqual(wf.state, 'failed')

    def test_exc_encoding(self):
        with self.admin_access.repo_cnx() as cnx:
            cwtask_eid = start_async_task(cnx, 'exc_encoding').eid
            cnx.commit()
            run_all_tasks(cnx)
            cwtask = cnx.entity_from_eid(cwtask_eid)
            self.wait_async_task(cnx, cwtask.task_id)
            wf = cwtask.cw_adapt_to('IWorkflowable')
            self.assertEqual(wf.state, 'failed')
            logs = cwtask.cw_adapt_to('ICeleryTask').logs.decode('utf-8')
            if six.PY2:
                self.assertIn(
                    (u"""raise RuntimeError(u'Cette tâche a échoué'."""
                     u"""encode('utf8'))"""), logs)
            else:
                self.assertIn(
                    u"""raise RuntimeError('Cette tâche a échoué')""",
                    logs)
            self.assertIn(u"""RuntimeError: Cette tâche a échoué""", logs)

    def test_start_celerytask_op(self):
        with self.admin_access.repo_cnx() as cnx:
            # Task must run even if there is no data on current transaction
            task = celery.signature("success", kwargs={"n": 10})
            task_id = task.freeze().task_id
            cwtask = cnx.create_entity('CeleryTask', task_name=u'dummy',
                                       task_id=six.text_type(task_id))
            cnx.commit()
            cnx.transaction_data['celerytask'] = {cwtask.eid: task}
            StartCeleryTaskOp.get_instance(cnx).add_data(cwtask.eid)
            cnx.commit()
            run_all_tasks(cnx)
            result = self.wait_async_task(cnx, task_id)
            self.assertEqual(result.get(), 10)

    def test_logs(self):
        with self.admin_access.repo_cnx() as cnx:
            cwtask_eid = start_async_task(cnx, 'log').eid
            cnx.commit()
            run_all_tasks(cnx)
            cwtask = cnx.entity_from_eid(cwtask_eid)
            self.wait_async_task(cnx, cwtask.task_id)
            logs = cwtask.cw_adapt_to('ICeleryTask').logs
            self.assertIn(b'out should be in logs', logs)
            self.assertIn(b'err should be in logs', logs)
            self.assertIn(b'cw warning should be in logs', logs)
            for name in (b'cw', b'celery'):
                for key in (b'error', b'critical', b'exception'):
                    self.assertIn(name + b' ' + key + b' should be in logs',
                                  logs)
            self.assertIn(b'cw critical should be in logs', logs)
            self.assertNotIn(b'should not be in logs', logs)
            self.assertIn(b'raise Exception("oops")', logs)

    def test_task_deleted(self):
        rdb = get_redis_client()
        with self.admin_access.cnx() as cnx:
            # this 'buggy_task_revoked' key is used simulate the 'revoke' since
            # it's not handled by celery in threaded solo mode that we use in
            # tests
            rdb.set('buggy_task_revoked', 'no')
            task = start_async_task(cnx, 'buggy_task')
            cnx.commit()
            run_all_tasks(cnx)
            cnx.commit()
            task = cnx.entity_from_eid(task.eid)
            wait_until(lambda: b'evil' in task.cw_adapt_to('ICeleryTask').logs)
            task.cw_delete()
            with mock.patch('celery.app.control.Control.revoke') as revoke:
                cnx.commit()
            rdb.set('buggy_task_revoked', 'yes')
            revoke.assert_called_once_with([task.task_id], signal='SIGKILL',
                                           terminate=True)
            self.assertFalse(os.path.exists(get_log_filename(task.task_id)))

    def test_workflow_chain(self):
        with self.admin_access.repo_cnx() as cnx:
            s = celery.signature
            task = celery.chain(s("add", (2, 2)), s("add", (4,)))
            cwtask = start_async_task(cnx, task)
            cnx.commit()
            run_all_tasks(cnx)
            result = self.wait_async_task(cnx, cwtask.task_id)
            self.assertEqual(result.get(), 8)

            children = cwtask.reverse_parent_task
            self.assertEqual(len(children), 1)
            result = children[0].cw_adapt_to('ICeleryTask').result
            self.assertEqual(result.get(), 4)

    def test_workflow_group(self):
        with self.admin_access.repo_cnx() as cnx:
            s = celery.signature
            task = celery.group(s("add", (2, 3)), s("add", (4, 5)))
            cwtask = start_async_task(cnx, task)
            cnx.commit()
            self.assertEqual(cwtask.task_name, u'celery.group')
            run_all_tasks(cnx)
            # FIXME: investigate why this hang since update from celery 3 to 4
            # results = run_all_tasks(cnx)
            # self.wait_async_task(cnx, cwtask.task_id)
            # self.assertEqual(results[cwtask.eid].get(), [5, 9])
            subtasks = cwtask.reverse_parent_task
            self.assertEqual(len(subtasks), 2)
            for subtask, expected in zip(subtasks, [5, 9]):
                self.wait_async_task(cnx, subtask.task_id)
                result = subtask.cw_adapt_to('ICeleryTask').result.get()
                self.assertEqual(result, expected)

    def test_workflow_chord(self):
        with self.admin_access.repo_cnx() as cnx:
            s = celery.signature
            task = celery.chord([s("success", (i,)) for i in range(10)],
                                s("tsum", []))
            cwtask = start_async_task(cnx, task)
            cnx.commit()
            self.assertEqual(cwtask.task_name, u'celery.chord')
            run_all_tasks(cnx)
            result = self.wait_async_task(cnx, cwtask.task_id)
            self.assertEqual(result.get(), 45)

            children = cwtask.reverse_parent_task
            self.assertEqual([child.task_name for child in children],
                             [u'success'] * 10)
            self.assertCountEqual(
                [t.cw_adapt_to('ICeleryTask').result.get() for t in children],
                range(10))

    def test_workflow_subtasks(self):
        with self.admin_access.repo_cnx() as cnx:
            logging.getLogger('cubicweb.appobject').setLevel(logging.DEBUG)
            s = celery.signature
            task = s("spawn")
            cwtask = start_async_task(cnx, task)
            cnx.commit()
            self.assertEqual(cwtask.task_name, u'spawn')
            run_all_tasks(cnx)
            asresult = self.wait_async_task(cnx, cwtask.task_id)
            result = celery.result.result_from_tuple(
                asresult.result["celerytask_subtasks"])
            self.assertEqual(0, result.get())
            cwtask = cnx.entity_from_eid(cwtask.eid)
            self.assertEqual(cwtask.cw_adapt_to('IWorkflowable').state, "done")
            children = cwtask.reverse_parent_task
            self.assertEqual(len(children), 11)
            counter = collections.Counter()
            states = []
            for child in children:
                counter[child.task_name] += 1
                states.append(child.cw_adapt_to('IWorkflowable').state)
            self.assertEqual(dict(counter), {'success': 10, 'add': 1})

            tsum = cnx.find('CeleryTask', task_name='tsum').one()
            self.assertEqual(tsum.cw_adapt_to('IWorkflowable').state, 'done')
            # XXX: this task should have "spawn" as parent_task ?
            self.assertEqual(tsum.parent_task, ())
            self.assertEqual(tsum.reverse_parent_task, ())

    def test_revoke(self):
        with self.admin_access.cnx() as cnx:
            task = start_async_task(cnx, celery.signature("success"))
            cnx.commit()
            with mock.patch('celery.app.control.Control.revoke') as revoke:
                task.cw_adapt_to('ICeleryTask').revoke()
            revoke.assert_called_once_with([task.task_id], signal='SIGKILL',
                                           terminate=True)

    def test_multi_revoke(self):
        with self.admin_access.cnx() as cnx:

            def success():
                return celery.signature("success")

            task = start_async_task(cnx, celery.group(success(), success()))
            cnx.commit()
            task_ids = set([t.task_id for t in task.child_tasks()])
            # we have a task group containing two subtasks = 3 tasks
            self.assertEqual(len(task_ids), 3)
            with mock.patch('celery.app.control.Control.revoke') as revoke:
                task.cw_adapt_to('ICeleryTask').revoke()
            self.assertEqual(revoke.call_count, 1)
            args, kwargs = revoke.call_args
            self.assertEqual(len(args), 1)
            self.assertEqual(set(task_ids), set(args[0]))
            self.assertEqual({'terminate': True, 'signal': 'SIGKILL'}, kwargs)

    def test_celery_monitor_requeue(self):
        with self.admin_access.cnx() as cnx:
            t1 = start_async_task(cnx, "success", 42)
            t2 = start_async_task(cnx, "success", 42)
            t1.cw_set(creation_date=(
                datetime.datetime.utcnow() - datetime.timedelta(hours=2)))
            cnx.commit()
            rdb = get_redis_client()
            self.assertEqual(rdb.lrange(MONITOR_KEY, 0, -1), [])
            CeleryMonitorCommand.requeue(cnx, rdb)
            self.assertEqual(
                [json.loads(data.decode())
                 for data in rdb.lrange(MONITOR_KEY, 0, -1)],
                [{'task_id': t2.task_id, 'task_name': None}])


class StartAsyncTaskTC(testlib.CubicWebTC):

    def setUp(self):
        super(StartAsyncTaskTC, self).setUp()
        celery.current_app.conf.task_always_eager = True

    def test_task_creating_task(self):
        with self.admin_access.cnx() as cnx:

            @celery.current_app.task(name='task_a')
            def task_a():
                with self.admin_access.cnx() as admin_cnx:
                    start_async_task(admin_cnx, 'task_b')
                    admin_cnx.commit()
                return 'a'

            @celery.current_app.task(name='task_b')
            def task_b():
                return 'b'

            @celery.current_app.task(name='task_c')
            def task_c():
                return 'c'

            start_async_task(cnx, 'task_a')
            start_async_task(cnx, 'task_c')
            cnx.commit()
            results = run_all_tasks(cnx)
            self.assertCountEqual(
                [r.get() for r in results.values()], ['a', 'b', 'c'])


class SegfaultTC(BaseCeleryTaskTC):
    worker_args = ['-P', 'prefork', '-c', '1', '-l', 'info']

    def test_segfault(self):
        with self.admin_access.cnx() as cnx:
            task = start_async_task(cnx, 'segfault')
            cnx.commit()
            run_all_tasks(cnx)
            self.wait_async_task(cnx, task.task_id, timeout=15)
            wf = cnx.entity_from_eid(task.eid).cw_adapt_to('IWorkflowable')
            self.assertEqual(wf.state, 'failed')
            self.assertEqual(wf.latest_trinfo().comment, (
                'Worker exited prematurely: signal 11 (SIGSEGV).'))


if __name__ == '__main__':
    from unittest import main
    main()
