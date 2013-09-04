import unittest
from mockito import when, unstub, verify, any


class TestDjangoSmartSettings(unittest.TestCase):
	def tearDown(self):
		unstub()

	def test_load_settings_from_module(self):
		import django_smart_settings 

		self.assertFalse('A' in locals())
		self.assertFalse('B' in locals())
		self.assertFalse('C' in locals())
		
		django_smart_settings._load_settings_from_module("django_smart_settings.test.sample", locals())
		
		self.assertTrue('A' in locals())
		self.assertTrue('B' in locals())
		self.assertTrue('C' in locals())

		self.assertEqual('avalue', locals()['A'])
		self.assertEqual('value', locals()['B']['key'])
		self.assertEqual('array', locals()['C'][0])

	def test_import_machine_settings(self):
		import django_smart_settings
		import socket 
		when(socket).gethostname().thenReturn('qqqq')
		when(django_smart_settings)._load_settings_from_module("qqqq", any()).thenReturn(None)

		result = dict()

		django_smart_settings._import_machine_settings(result)
		verify(django_smart_settings)._load_settings_from_module("qqqq", any())

	def test_import_user_settings(self):
		import django_smart_settings
		import getpass 
		when(getpass).getuser().thenReturn('uuuu')
		when(django_smart_settings)._load_settings_from_module("uuuu", any()).thenReturn(None)

		result = dict()

		django_smart_settings._import_user_settings(result)
		verify(django_smart_settings)._load_settings_from_module("uuuu", any())

	def test_import_variable_settings(self):
		import django_smart_settings
		import os
		os.environ['DJANGO_ENV'] =  'prod'

		when(django_smart_settings)._load_settings_from_module("prod", any()).thenReturn(None)

		result = dict()
		
		django_smart_settings._import_variable_settings(result)
		verify(django_smart_settings)._load_settings_from_module("prod", any())



if __name__ == '__main__':
    unittest.main()