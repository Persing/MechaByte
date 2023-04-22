import unittest
import os
import shutil

from MechaByte.key_store import KeyValueStore


class TestUserKeyValueStore(unittest.TestCase):
    def setUp(self):
        self.filename = 'testdata.pkl'
        self.store = KeyValueStore(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists('backups'):
            shutil.rmtree('backups')

    def test_set_and_get(self):
        self.store.set('guild1', 'question-answer', 'who are you?', 'I am a bot.')
        self.store.set('guild2', 'user-preference', 'dark_mode', True)
        self.assertEqual(self.store.get('guild1', 'question-answer', 'who are you?'), 'I am a bot.')
        self.assertEqual(self.store.get('guild2', 'user-preference', 'dark_mode'), True)
        self.assertIsNone(self.store.get('guild1', 'user-preference', 'dark_mode'))

    def test_get_all_keys(self):
        self.store.set('guild1', 'question-answer', 'who are you?', 'I am a bot.')
        self.store.set('guild1', 'question-answer', 'what can you do?', 'I can answer questions.')
        self.assertEqual(set(self.store.get_all_keys('guild1', 'question-answer')), {'who are you?', 'what can you do?'})
        self.assertEqual(set(self.store.get_all_keys('guild1', 'user-preference')), set())

    def test_delete(self):
        self.store.set('guild1', 'question-answer', 'who are you?', 'I am a bot.')
        self.store.set('guild1', 'question-answer', 'what can you do?', 'I can answer questions.')
        self.assertTrue(self.store.delete('guild1', 'question-answer', 'who are you?'))
        self.assertEqual(set(self.store.get_all_keys('guild1', 'question-answer')), {'what can you do?'})
        self.assertFalse(self.store.delete('guild1', 'user-preference', 'dark_mode'))

    def test_delete_all(self):
        self.store.set('guild1', 'question-answer', 'who are you?', 'I am a bot.')
        self.store.set('guild1', 'question-answer', 'what can you do?', 'I can answer questions.')
        self.store.set('guild2', 'user-preference', 'dark_mode', True)
        self.store.delete_all('guild1', 'question-answer')
        self.assertEqual(set(self.store.get_all_keys('guild1', 'question-answer')), set())
        self.assertEqual(set(self.store.get_all_keys('guild2', 'user-preference')), {'dark_mode'})
        backup_files = os.listdir('backups')
        self.assertEqual(len(backup_files), 1)
        self.assertTrue(backup_files[0].startswith('guild1_question-answer_testdata.pkl.bak.'))
