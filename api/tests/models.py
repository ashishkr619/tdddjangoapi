from django.test import TestCase
from ..models import Content
from django.contrib.auth import get_user_model


User = get_user_model()

class ModelTestCase(TestCase):
  
  def setUp(self):
    user = User.objects.create_user(email="karan@gmail.com",password="IamKaran",full_name="Karan Maurya",phone=9999999999,pincode=221007)
    Content.objects.create(title="Title",owner=user,body="body",summary="summary")

  def test_content_str(self):
    content = Content.objects.get(title="Title")
    self.assertEqual(str(content),"Title")
