# -*- coding: utf-8 -*-
import unittest

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, with_transaction, ModuleTestCase
from trytond.config import config


config.add_section('elastic_search')
config.set('elastic_search', 'server_uri', 'http://localhost:9200')


class IndexBacklogTestCase(ModuleTestCase):
    """
    Tests Index Backlog
    """
    module = 'elastic_search'

    def setUp(self):
        trytond.tests.test_tryton.install_module('elastic_search')
        self.IndexBacklog = POOL.get('elasticsearch.index_backlog')
        self.Configuration = POOL.get('elasticsearch.configuration')
        self.User = POOL.get('res.user')

    @with_transaction()
    def test_0010_create_IndexBacklog(self):
        """
        Creates index backlog and updates remote elastic search index
        """
        self.Configuration(1).save()
        users = self.User.create([{
            'name': 'user1', 'login': 'user1'
        }, {
            'name': 'user2', 'login': 'user2'
        }])
        # Adds list of active records to IndexBacklog
        self.IndexBacklog.create_from_records(users)
        self.assertEqual(len(self.IndexBacklog.search([])), 2)
        # Updates the remote elastic search index from backlog and deletes
        # the backlog entries
        self.IndexBacklog.update_index()
        self.assertEqual(len(self.IndexBacklog.search([])), 0)

    @with_transaction()
    def test_0900_batch_indexing(self):
        self.Configuration(1).save()
        users = self.User.create([
            {
                'name': 'user%s' % index,
                'login': 'user%s' % index,
            } for index in xrange(1, 201)
        ])
        # Adds list of active records to IndexBacklog
        self.IndexBacklog.create_from_records(users)
        self.assertEqual(len(self.IndexBacklog.search([])), 200)
        # Updates the remote elastic search index from backlog and deletes
        # the backlog entries. Default batch size of 100.
        self.IndexBacklog.update_index()
        self.assertEqual(len(self.IndexBacklog.search([])), 100)
        self.IndexBacklog.update_index()
        self.assertEqual(len(self.IndexBacklog.search([])), 0)


class DocumentTypeTestCase(unittest.TestCase):
    """
    Tests Elastic Search Manage
    """

    def setUp(self):
        trytond.tests.test_tryton.install_module('elastic_search')
        self.IndexBacklog = POOL.get('elasticsearch.index_backlog')
        self.DocumentType = POOL.get('elasticsearch.document.type')
        self.User = POOL.get('res.user')
        self.Model = POOL.get('ir.model')
        self.Trigger = POOL.get('ir.trigger')
        self.Configuration = POOL.get('elasticsearch.configuration')

    def create_defaults(self):
        user_model, = self.Model.search([('model', '=', 'res.user')])

        config = self.Configuration(1)
        config.save()

        dt1, = self.DocumentType.create([{
            'name': 'TestDoc',
            'model': user_model.id,
        }])
        self.assertEqual(dt1.trigger.name, 'elasticsearch_TestDoc')

        dt2, = self.DocumentType.create([{
            'name': 'TestDoc2',
            'model': user_model.id,
        }])
        self.assertEqual(dt2.trigger.name, 'elasticsearch_TestDoc2')

        return {
            'document_type1': dt1,
            'document_type2': dt2,
        }

    def create_users(self):
        return self.User.create([
            {
                'name': 'testuser',
                'login': 'testuser',
                'password': 'testuser',
            },
            {
                'name': 'testuser2',
                'login': 'testuser2',
                'password': 'testuser2',
            }
        ])

    @with_transaction()
    def test_create_update(self):
        '''
        Test registering/unregistering of models for indexing
        '''
        defaults = self.create_defaults()
        dt1 = defaults['document_type1']
        dt2 = defaults['document_type2']

        # update document and check if new trigger is created
        trigger1_id = dt1.trigger.id
        self.DocumentType.write([dt1], {'name': 'testdoc'})
        triggers = self.Trigger.search([
            ('id', '=', trigger1_id)
        ])
        self.assertEqual(len(triggers), 0)
        triggers = self.Trigger.search([
            ('name', '=', 'elasticsearch_testdoc')
        ])
        self.assertEqual(len(triggers), 1)

        # remove the model and check trigger
        trigger2_id = dt2.trigger.id
        self.DocumentType.delete([dt2])
        triggers = self.Trigger.search([('id', '=', trigger2_id)])
        self.assertEqual(len(triggers), 0)

    @with_transaction()
    def test_trigger(self):
        '''
        Test if trigger is invoked and do call handler appropriately
        '''
        self.create_defaults()
        backlog_old_len = self.IndexBacklog.search([], count=True)
        self.create_users()
        backlog_new_len = self.IndexBacklog.search([], count=True)
        self.assertEqual(backlog_old_len + 2, backlog_new_len)


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(IndexBacklogTestCase)
    )
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(DocumentTypeTestCase)
    )
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
