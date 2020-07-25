from django.test import TestCase
from ..models import Content
from rest_framework.test import APIClient
from rest_framework import status
from django.shortcuts import reverse
from ..serializers import ContentSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class GetAllContentTestCase(TestCase):

  def setUp(self):
    self.client = APIClient()
    user = User.objects.create_user(email="karan@email.com",password="IamKaran",full_name="Karan Maurya",phone=9999999999,pincode=221007)
    token = user.auth_token
    self.client.force_authenticate(user=user,token=token)
    Content.objects.create(title="Title",owner=user,body="body",summary="summary")
    Content.objects.create(title="Title 2",owner=user,body="body 2",summary="summary 2")
    Content.objects.create(title="Title 3",owner=user,body="body 3",summary="summary 3")

  def test_get_all_content(self):
    response = self.client.get(reverse('get_post_content'))
    contents = Content.objects.all()
    serializer = ContentSerializer(contents,many=True)
    self.assertEqual(response.data,serializer.data)
    self.assertEqual(response.status_code,status.HTTP_200_OK)
  
  def test_get_search_content(self):
    response = self.client.get("%s?search=title"%reverse('get_post_content'))
    contents = Content.objects.filter(title__contains="title")
    serializer = ContentSerializer(contents,many=True)
    self.assertEqual(response.data,serializer.data)

  def test_force_authentication(self):
    new_client = APIClient()
    response = new_client.get(reverse('get_delete_update_content',kwargs={'pk':2}))
    self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

class GetSingleContentTestCase(TestCase):

  def setUp(self):
    self.client = APIClient()
    user = User.objects.create_user(email="karan@email.com",password="IamKaran",full_name="Karan Maurya",phone=9999999999,pincode=221007)
    self.client.force_authenticate(user=user)
    self.content1 = Content.objects.create(title="Title",owner=user,body="body",summary="summary")
    self.content2 = Content.objects.create(title="Title 2",owner=user,body="body 2",summary="summary 2")
  
  def test_get_valid_content(self):
    response = self.client.get(reverse('get_delete_update_content',kwargs={'pk':self.content1.pk}))
    content = Content.objects.get(pk=self.content1.pk)
    serializer = ContentSerializer(content)
    self.assertEqual(response.data,serializer.data)
    self.assertEqual(response.status_code,status.HTTP_200_OK)

  def test_get_invalid_content(self):
    response = self.client.get(reverse('get_delete_update_content',kwargs={'pk':20}))
    self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

class PostContentTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    user = User.objects.create_user(email="karan@email.com",password="IamKaran",full_name="Karan Maurya",phone=9999999999,pincode=221007)
    self.client.force_authenticate(user=user)
    self.valid_content = {
      'title':"Title",'owner':user.id,'body':"body",'summary':"summary"
    }
    self.invalid_content1 = {
      'title':"",'owner':user.id,'body':"body",'summary':"summary"
    }
    self.invalid_content2 = {
      'title':"Title",'owner':user.id,'body':"",'summary':"summary"
    }
    self.invalid_content3 = {
      'title':"Title",'owner':user.id,'body':"body",'summary':""
    }

  def test_valid_content_post(self):
    response = self.client.post(reverse('get_post_content'),data=self.valid_content,format="json")
    self.assertEqual(response.status_code,status.HTTP_201_CREATED)

  def test_invalid_content_post(self):
    response1 = self.client.post(reverse('get_post_content'),data=self.invalid_content1,format="json")
    response2 = self.client.post(reverse('get_post_content'),data=self.invalid_content2,format="json")
    response3 = self.client.post(reverse('get_post_content'),data=self.invalid_content3,format="json")
    self.assertEqual(response1.status_code,status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response2.status_code,status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response3.status_code,status.HTTP_400_BAD_REQUEST)


class PutContentTestCase(TestCase):
  def setUp(self):

    self.client = APIClient()
    user = User.objects.create_user(email="karan@email.com",password="IamKaran",full_name="Karan Maurya",phone=9999999999,pincode=221007)
    self.client.force_authenticate(user=user)
    self.content = Content.objects.create(title="Title",owner=user,body="body",summary="summary")
    self.valid_content = {
      'title':"Title",'owner':user.id,'body':"body",'summary':"summary"
    }
    self.invalid_content1 = {
      'title':"",'owner':user.id,'body':"body",'summary':"summary"
    }
    self.invalid_content2 = {
      'title':"Title",'owner':user.id,'body':"",'summary':"summary"
    }
    self.invalid_content3 = {
      'title':"Title",'owner':user.id,'body':"body",'summary':""
    }

  def test_valid_put_content(self):
    response = self.client.put(reverse('get_delete_update_content',kwargs={'pk':self.content.pk}),data=self.valid_content,format="json")
    updated_content = Content.objects.get(pk=self.content.pk)
    serializer = ContentSerializer(updated_content)
    self.assertEqual(response.data,serializer.data)
    self.assertEqual(response.status_code,status.HTTP_200_OK)
  
  def test_invalid_put_content(self):
    response1 = self.client.put(reverse('get_delete_update_content',kwargs={'pk':self.content.pk}),data=self.invalid_content1,format="json")
    response2 = self.client.put(reverse('get_delete_update_content',kwargs={'pk':self.content.pk}),data=self.invalid_content2,format="json")
    response3 = self.client.put(reverse('get_delete_update_content',kwargs={'pk':self.content.pk}),data=self.invalid_content3,format="json")
    self.assertEqual(response1.status_code,status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response2.status_code,status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response3.status_code,status.HTTP_400_BAD_REQUEST)


class DeleteContentTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    user = User.objects.create_user(email="karan@email.com",password="IamKaran",full_name="Karan Maurya",phone=9999999999,pincode=221007)
    self.client.force_authenticate(user=user)
    self.content1 = Content.objects.create(title="Title",owner=user,body="body",summary="summary")
    self.content2 = Content.objects.create(title="Title 2",owner=user,body="body 2",summary="summary 2")

  def test_delete_valid_content(self):
    response = self.client.delete(reverse('get_delete_update_content',kwargs={'pk':self.content2.pk}))
    self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
  
  def test_delete_invalid_content(self):
    response = self.client.delete(reverse('get_delete_update_content',kwargs={'pk':200}))
    self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)