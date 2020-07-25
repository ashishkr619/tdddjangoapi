from django.test import TestCase
from ..models import CustomUser
from rest_framework.authtoken.models import Token

class ModelTestCase(TestCase):
  def setUp(self):
    self.valid_email = 'karan@gmail.com'
    self.valid_password = "IamKaran"
    self.invalid_email = 'karan.com'
    self.invalid_password = "password"
    self.full_name="Karan Maurya"
    self.phone = 9999999999
    self.pin = 221007

  def test_user_create(self):
    user = CustomUser.objects.create_user(email=self.valid_email,password=self.valid_password,full_name=self.full_name,phone=self.phone,pincode=self.pin)
    token = Token.objects.get(user=user)
    self.assertEqual(user.email, self.valid_email)
    self.assertEqual(user.full_name, self.full_name)
    self.assertEqual(user.phone, self.phone)
    self.assertEqual(token,user.auth_token)
    self.assertEqual(user.pincode, self.pin)
    self.assertFalse(user.is_admin)
    self.assertTrue(user.is_active)
    self.assertEqual(str(user),user.full_name)
    try:
        self.assertIsNone(user.username)
    except AttributeError:
        pass
    with self.assertRaises(TypeError):
        CustomUser.objects.create_user()
    with self.assertRaises(ValueError):
        CustomUser.objects.create_user(email=self.invalid_email,password=self.valid_password,full_name=self.full_name,phone=self.phone,pincode=self.pin)
    with self.assertRaises(ValueError):
        CustomUser.objects.create_user(email=self.valid_email, password="foo",full_name=self.full_name,phone=self.phone,pincode=self.pin)
    with self.assertRaises(ValueError):
      CustomUser.objects.create_user(email="", password=self.valid_password,full_name=self.full_name,phone=self.phone,pincode=self.pin)
    with self.assertRaises(ValueError):
      CustomUser.objects.create_user(email=self.valid_email, password="",full_name=self.full_name,phone=self.phone,pincode=self.pin)
    with self.assertRaises(ValueError):
      CustomUser.objects.create_user(email=self.valid_email, password=self.invalid_password,full_name=self.full_name,phone=self.phone,pincode=self.pin)

  def test_super_user_create(self):
    user = CustomUser.objects.create_superuser(email=self.valid_email,password=self.valid_password,full_name=self.full_name,phone=self.phone,pincode=self.pin)
    self.assertEqual(user.email, self.valid_email)
    self.assertEqual(user.full_name, self.full_name)
    self.assertEqual(user.phone, self.phone)
    self.assertEqual(user.pincode, self.pin)
    self.assertTrue(user.is_admin)
    self.assertTrue(user.is_active)