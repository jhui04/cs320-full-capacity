from django.test import TestCase, Client
from django.core.urlresolvers import reverse

# Create your tests here.

class ViewTestCases(TestCase):
	def setUp(self):
		self.client = Client()

	def test_home_view(self):
		resp = self.client.get(reverse('home-view'))
		self.assertEqual(resp.status_code, 302)#200)


	def test_test_view(self):
		resp = self.client.get(reverse('test-view'))
		self.assertEqual(resp.status_code, 302)#200)


	def test_api_view(self):
		resp = self.client.get('/api/')
		self.assertEqual(resp.status_code, 200)


	def test_devices_api_view(self):
		resp = self.client.get('/api/all_devices/')
		self.assertEqual(resp.status_code, 200)


	def test_home_view1(self):
		resp = self.client.get(reverse('home-view'))
		self.assertEqual(resp.status_code, 302)#200)

	def test_home_view2(self):
		resp = self.client.get(reverse('home-view'))
		self.assertEqual(resp.status_code, 302)#200)

	def test_home_view3(self):
		resp = self.client.get(reverse('home-view'))
		self.assertEqual(resp.status_code, 302)#200)

	def test_home_view4(self):
		resp = self.client.get(reverse('home-view'))
		self.assertEqual(resp.status_code, 302)#200)

	def test_home_view5(self):
		resp = self.client.get(reverse('home-view'))
		self.assertEqual(resp.status_code, 302)#200)

	def test_home_view6(self):
		resp = self.client.get(reverse('home-view'))
		self.assertEqual(resp.status_code, 302)#200)

	def test_home_view7(self):
		resp = self.client.get(reverse('home-view'))
		self.assertEqual(resp.status_code, 302)#200)

	def test_home_view8(self):
		resp = self.client.get(reverse('home-view'))
		self.assertEqual(resp.status_code, 302)#200)