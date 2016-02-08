import os, evbrite, unittest
from django.test import TestCase

# Create your tests here.
class TestCategoryFunctions(unittest.TestCase):
    def test_category_to_id_pairs(self):
        category_list = [
            {
                u'short_name': u'Auto, Boat & Air',
                u'short_name_localized': u'Auto, Boat & Air',
                u'id': u'118',
                u'resource_uri': u'https://www.eventbriteapi.com/v3/categories/118/',
                u'name_localized': u'Auto, Boat & Air',
                u'name': u'Auto, Boat & Air'
            },
            {
                u'short_name': u'Home & Lifestyle',
                u'short_name_localized': u'Home & Lifestyle',
                u'id': u'117',
                u'resource_uri': u'https://www.eventbriteapi.com/v3/categories/117/',
                u'name_localized': u'Home & Lifestyle',
                u'name': u'Home & Lifestyle'
            }
        ]

        pairs = evbrite.categories_to_id_pairs(category_list)
        self.assertEqual(pairs, [('118', 'Auto, Boat & Air'), ('117', 'Home & Lifestyle')])


class TestAPIFunctions(unittest.TestCase):
    os.environ['API_TOKEN'] = "RFCEYTQBPPOPTIJJ32B4"

    def test_safe_request(self):
        # Testing with incorrect token (categories vs scattergories)
        incorrect_token = 'ABCDEFGHIJK'
        valid_token = str(os.environ['API_TOKEN'])
        test_valid_url = "https://www.eventbriteapi.com/v3/" + "events/search/?categories=101"
        token_error = {
                        u'status_code': 401, u'error_description':
                        u'The OAuth token you provided was invalid.',
                        u'error': u'INVALID_AUTH'
                      }

        self.assertEqual(token_error, evbrite.safe_request(test_valid_url, 'ABCDEFGHIJK'))
        # Ensure there is no error after a request with a valid token
        self.assertNotIn('error', evbrite.safe_request(test_valid_url, valid_token))

if __name__ == '__main__':
    unittest.main()
