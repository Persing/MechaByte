# import asyncio
# import unittest
#
# import unittest
# from unittest.mock import MagicMock, patch
#
# from MechaByte.SentenceComparatorApi import SentenceComparator
#
#
# class TestSentenceComparator(unittest.TestCase):
#     def setUp(self):
#         self.store = MagicMock()
#
#     @patch('MechaByte.SentenceComparatorApi.query')
#     def test_get_response(self, mock_query):
#         # Set up mock data
#         questions = ['How are you?', 'What is your name?', 'What can you do?']
#         self.store.get_all_keys.return_value = questions
#         self.store.get.side_effect = lambda guild_id, question, key: f"{question} = {key}"
#
#         # Test with exact question match
#         comp = SentenceComparator(self.store)
#         result = asyncio.run(comp.get_response('guild1', 'What can you do?'))
#         self.assertEqual(result, 'What can you do? = What can you do?')
#
#         # Test without exact question match
#         mock_query.return_value = [0.5, 0.2, 0.3]
#         result = comp.get_response('guild1', 'What are you doing?')
#         self.assertEqual(result, 'What are you doing? = How are you?')
#
#         # Test with no questions in store
#         self.store.get_all_keys.return_value = []
#         result = comp.get_response('guild1', 'What can you do?')
#         self.assertEqual(result, "I haven't learned anything yet.")
#
#
# if __name__ == '__main__':
#     unittest.main()
