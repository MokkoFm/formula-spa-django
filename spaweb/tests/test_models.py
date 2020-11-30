from django.test import TestCase
from spaweb.models import Topic, BusinessDirection, ProductCategory, City


class BusinessDirectionTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.business_direction = BusinessDirection.objects.create(
            title="Программы",
            slug="programs"
        )

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.business_direction.title, str)
        self.assertIsInstance(self.business_direction.slug, str)

    def test_max_length_of_title(self):
        business_direction = BusinessDirection.objects.get(
            title="Программы"
        )
        max_length = business_direction._meta.get_field(
            "title").max_length
        self.assertGreaterEqual(max_length, len(business_direction.title))


class TopicModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.business_direction = BusinessDirection.objects.create(
            title="Программы",
            slug="programs"
        )
        self.topic = Topic.objects.create(
            title="Для одного",
            business_direction=self.business_direction,
            slug='single'
        )

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.topic.title, str)
        self.assertEquals(
            self.topic.business_direction.title, self.business_direction.title)
        self.assertIsInstance(self.topic.slug, str)

    def test_max_length_of_title(self):
        max_length = self.topic._meta.get_field("title").max_length
        self.assertGreaterEqual(max_length, len(self.topic.title))


class ProductCategoryTest(TestCase):
    @classmethod
    def setUpTestData(self):
        business_direction = BusinessDirection.objects.create(
            title="Программы",
            slug="programs"
        )
        self.topic = Topic.objects.create(
            title="Для одного",
            business_direction=business_direction,
            slug='single'
        )
        self.category = ProductCategory.objects.create(
            name="Спа-массажи",
            topic=self.topic,
            slug="spa-massage"
        )

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.category.name, str)
        self.assertEquals(self.category.topic.title, self.topic.title)
        self.assertIsInstance(self.category.slug, str)

    def test_max_length_of_title(self):
        max_length = self.category._meta.get_field("name").max_length
        self.assertGreaterEqual(max_length, len(self.category.name))


class CityTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.city = City.objects.create(name="Сыктывкар")

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.city.name, str)

    def test_max_length_of_name(self):
        max_length = self.city._meta.get_field("name").max_length
        self.assertGreaterEqual(max_length, len(self.city.name))
