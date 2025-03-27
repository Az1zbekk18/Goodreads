from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

from books.models import Book, BookReview
from goodreads.users.models import CustomUser

class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="admin", first_name="Azizbek")
        self.user.set_password("somepass")
        self.user.save()
        self.client.login(username="admin", password="somepass")

    def test_book_review_detail(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="12312")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.get(reverse('api:review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Very good book")
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Book1')
        self.assertEqual(response.data['book']['description'], 'Description1')
        self.assertEqual(response.data['book']['isbn'], '12312')
        self.assertEqual(response.data['user']['first_name'], "Azizbek")

    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username="somebody", first_name="Somebody")
        book = Book.objects.create(title="Book1", description="Description1", isbn="12312")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=3, comment="Not good")

        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['results'][0]['id'], br_two.id)
        self.assertEqual(response.data['results'][0]['stars_given'], br_two.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br_two.comment)
        self.assertEqual(response.data['results'][1]['id'], br.id)
        self.assertEqual(response.data['results'][1]['stars_given'], br.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], br.comment)
