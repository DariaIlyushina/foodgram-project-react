import shutil
import tempfile
import unittest

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

from ..models import (Favorite, Ingredient, IngredientAmount, Recipe,
                      ShoppingCart, Tag)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RecipeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = APIClient()

        cls.user = User.objects.create_user(username="authorized_user")
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

        cls.admin_user = User.objects.create_superuser(username="admin_user")
        cls.admin_client = APIClient()
        cls.admin_client.force_authenticate(cls.admin_user)

        cls.test_user = User.objects.create_user(username="testusername")
        cls.test_client = APIClient()
        cls.test_client.force_authenticate(cls.test_user)

        cls.ingredient_orange = Ingredient.objects.create(
            name="test апельсин",
            measurement_unit="шт.",
        )
        cls.ingredient_jam = Ingredient.objects.create(
            name="test варенье",
            measurement_unit="ложка",
        )
        cls.tag_breakfast = Tag.objects.create(
            name="test Завтрак",
            color="#6AA84FFF",
            slug="breakfast",
        )
        cls.tag_dinner = Tag.objects.create(
            name="test Обед",
            color="#6AA84FFF",
            slug="dinner",
        )
        cls.ingredientamount_orange = IngredientAmount.objects.create(
            ingredient=cls.ingredient_orange,
            amount=5,
        )
        cls.ingredientamount_jam = IngredientAmount.objects.create(
            ingredient=cls.ingredient_jam,
            amount=1,
        )
        cls.small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        cls.uploaded = SimpleUploadedFile(
            name="small.gif",
            content=cls.small_gif,
            content_type="image/gif",
        )
        cls.recipe_breakfast = Recipe.objects.create(
            author=cls.user,
            name="test рецепт",
            image=cls.uploaded,
            text="описание тестового рецепта",
            cooking_time=4,
        )
        cls.recipe_breakfast.tags.add(cls.tag_breakfast)
        cls.recipe_breakfast.ingredients.add(
            cls.ingredientamount_orange,
            cls.ingredientamount_jam,
        )

        cls.small_gif_test = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        cls.uploaded_test = SimpleUploadedFile(
            name="small_1.gif",
            content=cls.small_gif_test,
            content_type="image/gif",
        )
        cls.recipe = Recipe.objects.create(
            author=cls.user,
            name="тестовый рецепт",
            image=cls.uploaded_test,
            text="описание тестового рецепта",
            cooking_time=4,
        )
        cls.recipe.tags.add(cls.tag_breakfast)
        cls.recipe.ingredients.add(cls.ingredientamount_orange)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_cool_test(self):
        self.assertEqual(True, True)

    def test_get_recipes_list_unauthorized_user(self):
        url = "/api/recipes/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_recipes_list_authorized_client(self):
        url = "/api/recipes/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 2,
                    "tags": [
                        {
                            "id": 1,
                            "name": "test Завтрак",
                            "color": "#6AA84FFF",
                            "slug": "breakfast",
                        }
                    ],
                    "author": {
                        "email": "",
                        "id": 1,
                        "username": "authorized_user",
                        "first_name": "",
                        "last_name": "",
                        "is_subscribed": False,
                    },
                    "ingredients": [
                        {
                            "id": 1,
                            "name": "test апельсин",
                            "measurement_unit": "шт.",
                            "amount": 5,
                        }
                    ],
                    "is_favorited": False,
                    "is_in_shopping_cart": False,
                    "name": "тестовый рецепт",
                    "image": (
                        "http://testserver/media/recipes/images/small_1.gif"
                    ),
                    "text": "описание тестового рецепта",
                    "cooking_time": 4,
                },
                {
                    "id": 1,
                    "tags": [
                        {
                            "id": 1,
                            "name": "test Завтрак",
                            "color": "#6AA84FFF",
                            "slug": "breakfast",
                        }
                    ],
                    "author": {
                        "email": "",
                        "id": 1,
                        "username": "authorized_user",
                        "first_name": "",
                        "last_name": "",
                        "is_subscribed": False,
                    },
                    "ingredients": [
                        {
                            "id": 1,
                            "name": "test апельсин",
                            "measurement_unit": "шт.",
                            "amount": 5,
                        },
                        {
                            "id": 2,
                            "name": "test варенье",
                            "measurement_unit": "ложка",
                            "amount": 1,
                        },
                    ],
                    "is_favorited": False,
                    "is_in_shopping_cart": False,
                    "name": "test рецепт",
                    "image": (
                        "http://testserver/media/recipes/images/small.gif"
                    ),
                    "text": "описание тестового рецепта",
                    "cooking_time": 4,
                },
            ],
        }
        self.assertEqual(response.json(), test_json)

    def test_get_recipe_detail_unauthorized_client(self):
        url = f"/api/recipes/{self.user.id}/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "test Завтрак",
                    "color": "#6AA84FFF",
                    "slug": "breakfast",
                }
            ],
            "author": {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
                "is_subscribed": False,
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "test апельсин",
                    "measurement_unit": "шт.",
                    "amount": 5,
                },
                {
                    "id": 2,
                    "name": "test варенье",
                    "measurement_unit": "ложка",
                    "amount": 1,
                },
            ],
            "is_favorited": False,
            "is_in_shopping_cart": False,
            "name": "test рецепт",
            "image": "http://testserver/media/recipes/images/small.gif",
            "text": "описание тестового рецепта",
            "cooking_time": 4,
        }
        self.assertEqual(response.json(), test_json)

    def test_get_recipe_detail_authorized_client(self):
        url = f"/api/recipes/{self.user.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "test Завтрак",
                    "color": "#6AA84FFF",
                    "slug": "breakfast",
                }
            ],
            "author": {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
                "is_subscribed": False,
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "test апельсин",
                    "measurement_unit": "шт.",
                    "amount": 5,
                },
                {
                    "id": 2,
                    "name": "test варенье",
                    "measurement_unit": "ложка",
                    "amount": 1,
                },
            ],
            "is_favorited": False,
            "is_in_shopping_cart": False,
            "name": "test рецепт",
            "image": "http://testserver/media/recipes/images/small.gif",
            "text": "описание тестового рецепта",
            "cooking_time": 4,
        }
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_unauthorized_client(self):
        url = "/api/recipes/"
        recipe_count = Recipe.objects.count()
        data = {
            "ingredients": [
                {"id": self.ingredient_orange.id, "amount": 10},
                {"id": self.ingredient_jam.id, "amount": 30},
            ],
            "tags": [self.tag_breakfast.id, self.tag_dinner.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.guest_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Recipe.objects.count(), recipe_count)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_ingredients(self):
        url = "/api/recipes/"
        data = {
            "tags": [self.tag_breakfast.id, self.tag_dinner.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"ingredients": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_tags(self):
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_orange.id, "amount": 10},
                {"id": self.ingredient_jam.id, "amount": 30},
            ],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"tags": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_name(self):
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_orange.id, "amount": 10},
                {"id": self.ingredient_jam.id, "amount": 30},
            ],
            "tags": [self.tag_breakfast.id, self.tag_dinner.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"name": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_text(self):
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_orange.id, "amount": 10},
                {"id": self.ingredient_jam.id, "amount": 30},
            ],
            "tags": [self.tag_breakfast.id, self.tag_dinner.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "Тестовый рецепт обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"text": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_cooking_time(self):
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_orange.id, "amount": 10},
                {"id": self.ingredient_jam.id, "amount": 30},
            ],
            "tags": [self.tag_breakfast.id, self.tag_dinner.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"cooking_time": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_without_ingredients_tags(self):
        url = "/api/recipes/"
        data = {
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": 30,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "ingredients": ["Обязательное поле."],
            "tags": ["Обязательное поле."],
        }
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_with_empty_data(self):
        url = "/api/recipes/"
        data = {}
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "ingredients": ["Обязательное поле."],
            "tags": ["Обязательное поле."],
            "image": ["Ни одного файла не было отправлено."],
            "name": ["Обязательное поле."],
            "text": ["Обязательное поле."],
            "cooking_time": ["Обязательное поле."],
        }
        self.assertEqual(response.json(), test_json)

    def test_create_recipe_negative_cooking_time(self):
        url = "/api/recipes/"
        data = {
            "ingredients": [
                {"id": self.ingredient_orange.id, "amount": 10},
                {"id": self.ingredient_jam.id, "amount": 30},
            ],
            "tags": [self.tag_breakfast.id, self.tag_dinner.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "Тестовый рецепт обеда",
            "text": "Описание тестового рецепта обеда",
            "cooking_time": -1,
        }
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "cooking_time": [
                "Убедитесь, что это значение больше либо равно 1."
            ]
        }
        self.assertEqual(response.json(), test_json)

    def test_patch_recipe_unauthorized_client_401(self):
        url = f"/api/recipes/{self.recipe.id}/"
        data = {
            "ingredients": [
                {"id": self.ingredient_orange.id, "amount": 10},
                {"id": self.ingredient_jam.id, "amount": 30},
            ],
            "tags": [self.tag_breakfast.id, self.tag_dinner.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "обновленный тестовый рецепт",
            "text": "обновленное описание тестового рецепта",
            "cooking_time": 21,
        }
        response = self.guest_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_patch_recipe_not_author(self):
        test_user = self.test_user
        test_user_client = APIClient()
        test_user_client.force_authenticate(test_user)

        recipe = self.recipe
        data = {
            "ingredients": [
                {"id": self.ingredient_orange.id, "amount": 10},
                {"id": self.ingredient_jam.id, "amount": 30},
            ],
            "tags": [self.tag_breakfast.id, self.tag_dinner.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "обновленный тестовый рецепт",
            "text": "обновленное описание тестового рецепта",
            "cooking_time": 21,
        }

        url = f"/api/recipes/{recipe.id}/"
        response = test_user_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        test_json = {
            "detail": (
                "У вас недостаточно прав для "
                + "выполнения данного действия."
            )
        }
        self.assertEqual(response.json(), test_json)

    def test_patch_recipe_404(self):
        data = {
            "ingredients": [
                {"id": self.ingredient_orange.id, "amount": 10},
                {"id": self.ingredient_jam.id, "amount": 30},
            ],
            "tags": [self.tag_breakfast.id, self.tag_dinner.id],
            "image": (
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA"
                + "AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAO"
                + "xAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            ),
            "name": "обновленный тестовый рецепт",
            "text": "обновленное описание тестового рецепта",
            "cooking_time": 21,
        }
        count = Recipe.objects.count()
        url = f"/api/recipes/{count + 1}/"
        response = self.authorized_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)

    @unittest.expectedFailure
    def test_patch_recipe_400_without_all_fields(self):
        recipe = self.recipe
        data = {}
        url = f"/api/recipes/{recipe.id}/"
        response = self.authorized_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "ingredients": ["Обязательное поле."],
            "tags": ["Обязательное поле."],
            "image": ["Ни одного файла не было отправлено."],
            "name": ["Обязательное поле."],
            "text": ["Обязательное поле."],
            "cooking_time": ["Обязательное поле."],
        }
        self.assertEqual(response.json(), test_json)

    def test_delete_recipe(self):
        recipe = self.recipe
        url = f"/api/recipes/{recipe.id}/"
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_recipe_404(self):
        count = Recipe.objects.count()
        url = f"/api/recipes/{count + 1}/"
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_recipe_unauthorized_client_401(self):
        url = f"/api/recipes/{self.recipe.id}/"
        response = self.guest_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_recipe_not_author_403(self):
        test_user = self.test_user
        test_user_client = APIClient()
        test_user_client.force_authenticate(test_user)
        recipe = self.recipe
        url = f"/api/recipes/{recipe.id}/"
        response = test_user_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        test_json = {
            "detail": (
                "У вас недостаточно прав для выполнения данного действия."
            )
        }
        self.assertEqual(response.json(), test_json)

    def test_delete_recipe_by_administrator(self):
        recipe = self.recipe
        url = f"/api/recipes/{recipe.id}/"
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_recipe_detail_get_is_favorited_authorized_client(self):
        Favorite.objects.create(user=self.user, recipe=self.recipe)
        url = f"/api/recipes/{self.recipe.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json().get("is_favorited"))
        test_json = {
            "id": 2,
            "tags": [
                {
                    "id": 1,
                    "name": "test Завтрак",
                    "color": "#6AA84FFF",
                    "slug": "breakfast",
                }
            ],
            "author": {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
                "is_subscribed": False,
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "test апельсин",
                    "measurement_unit": "шт.",
                    "amount": 5,
                }
            ],
            "is_favorited": True,
            "is_in_shopping_cart": False,
            "name": "тестовый рецепт",
            "image": "http://testserver/media/recipes/images/small_1.gif",
            "text": "описание тестового рецепта",
            "cooking_time": 4,
        }
        self.assertEqual(response.json(), test_json)

    def test_recipe_detail_get_is_favorited_guest_client(self):
        Favorite.objects.create(user=self.user, recipe=self.recipe)
        url = f"/api/recipes/{self.recipe.id}/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json().get("is_favorited"))
        test_json = {
            "id": 2,
            "tags": [
                {
                    "id": 1,
                    "name": "test Завтрак",
                    "color": "#6AA84FFF",
                    "slug": "breakfast",
                }
            ],
            "author": {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
                "is_subscribed": False,
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "test апельсин",
                    "measurement_unit": "шт.",
                    "amount": 5,
                }
            ],
            "is_favorited": False,
            "is_in_shopping_cart": False,
            "name": "тестовый рецепт",
            "image": "http://testserver/media/recipes/images/small_1.gif",
            "text": "описание тестового рецепта",
            "cooking_time": 4,
        }
        self.assertEqual(response.json(), test_json)

    def test_recipe_list_get_is_favorited_authorized_client(self):
        Favorite.objects.create(user=self.user, recipe=self.recipe)
        Recipe.objects.create(
            author=self.user,
            name="тестовый рецепт",
            text="описание тестового рецепта",
            cooking_time=4,
        )
        url = "/api/recipes/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 3,
                    "tags": [],
                    "author": {
                        "email": "",
                        "id": 1,
                        "username": "authorized_user",
                        "first_name": "",
                        "last_name": "",
                        "is_subscribed": False,
                    },
                    "ingredients": [],
                    "is_favorited": False,
                    "is_in_shopping_cart": False,
                    "name": "тестовый рецепт",
                    "image": None,
                    "text": "описание тестового рецепта",
                    "cooking_time": 4,
                },
                {
                    "id": 2,
                    "tags": [
                        {
                            "id": 1,
                            "name": "test Завтрак",
                            "color": "#6AA84FFF",
                            "slug": "breakfast",
                        }
                    ],
                    "author": {
                        "email": "",
                        "id": 1,
                        "username": "authorized_user",
                        "first_name": "",
                        "last_name": "",
                        "is_subscribed": False,
                    },
                    "ingredients": [
                        {
                            "id": 1,
                            "name": "test апельсин",
                            "measurement_unit": "шт.",
                            "amount": 5,
                        }
                    ],
                    "is_favorited": True,
                    "is_in_shopping_cart": False,
                    "name": "тестовый рецепт",
                    "image": (
                        "http://testserver/media/recipes/images/small_1.gif"
                    ),
                    "text": "описание тестового рецепта",
                    "cooking_time": 4,
                },
                {
                    "id": 1,
                    "tags": [
                        {
                            "id": 1,
                            "name": "test Завтрак",
                            "color": "#6AA84FFF",
                            "slug": "breakfast",
                        }
                    ],
                    "author": {
                        "email": "",
                        "id": 1,
                        "username": "authorized_user",
                        "first_name": "",
                        "last_name": "",
                        "is_subscribed": False,
                    },
                    "ingredients": [
                        {
                            "id": 1,
                            "name": "test апельсин",
                            "measurement_unit": "шт.",
                            "amount": 5,
                        },
                        {
                            "id": 2,
                            "name": "test варенье",
                            "measurement_unit": "ложка",
                            "amount": 1,
                        },
                    ],
                    "is_favorited": False,
                    "is_in_shopping_cart": False,
                    "name": "test рецепт",
                    "image": (
                        "http://testserver/media/recipes/images/small.gif"
                    ),
                    "text": "описание тестового рецепта",
                    "cooking_time": 4,
                },
            ],
        }
        self.assertEqual(response.json(), test_json)

    def test_add_recipe_to_favorites_authorized_client(self):
        count = Favorite.objects.count()
        url = f"/api/recipes/{self.recipe_breakfast.id}/favorite/"
        response = self.test_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favorite.objects.count(), count + 1)
        test_json = {
            "id": 1,
            "name": "test рецепт",
            "image": "http://testserver/media/recipes/images/small.gif",
            "cooking_time": 4,
        }
        self.assertEqual(response.json(), test_json)

    def test_add_recipe_to_favorites_guest_client(self):
        url = f"/api/recipes/{self.recipe.id}/favorite/"
        response = self.guest_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_add_recipe_to_favorites_authorized_client_400(self):
        url = f"/api/recipes/{self.recipe.id}/favorite/"
        response = self.test_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.test_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"errors": "Рецепт уже добавлен в избранное"}
        self.assertEqual(response.json(), test_json)

    def test_delete_recipe_to_favorites_authorized_client(self):
        url = f"/api/recipes/{self.recipe.id}/favorite/"
        response = self.test_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.test_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_recipe_to_favorites_guest_client(self):
        url = f"/api/recipes/{self.recipe.id}/favorite/"
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.guest_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_delete_recipe_to_favorites_authorized_client_400(self):
        url = f"/api/recipes/{self.recipe.id}/favorite/"
        response = self.test_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.test_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.test_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"errors": "Рецепт уже удален из избранного"}
        self.assertEqual(response.json(), test_json)

    def test_recipe_detail_shopping_cart_authorized_client(self):
        ShoppingCart.objects.create(
            user=self.user,
            recipe=self.recipe_breakfast,
        )
        url = f"/api/recipes/{self.recipe_breakfast.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json().get("is_in_shopping_cart"))
        test_json = {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "test Завтрак",
                    "color": "#6AA84FFF",
                    "slug": "breakfast",
                }
            ],
            "author": {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
                "is_subscribed": False,
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "test апельсин",
                    "measurement_unit": "шт.",
                    "amount": 5,
                },
                {
                    "id": 2,
                    "name": "test варенье",
                    "measurement_unit": "ложка",
                    "amount": 1,
                },
            ],
            "is_favorited": False,
            "is_in_shopping_cart": True,
            "name": "test рецепт",
            "image": "http://testserver/media/recipes/images/small.gif",
            "text": "описание тестового рецепта",
            "cooking_time": 4,
        }
        self.assertEqual(response.json(), test_json)

    def test_recipe_detail_get_is_in_shopping_cart_guest_client(self):
        recipe = self.recipe_breakfast
        ShoppingCart.objects.create(user=self.user, recipe=recipe)
        url = f"/api/recipes/{recipe.id}/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json().get("is_in_shopping_cart"))
        test_json = {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "test Завтрак",
                    "color": "#6AA84FFF",
                    "slug": "breakfast",
                }
            ],
            "author": {
                "email": "",
                "id": 1,
                "username": "authorized_user",
                "first_name": "",
                "last_name": "",
                "is_subscribed": False,
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "test апельсин",
                    "measurement_unit": "шт.",
                    "amount": 5,
                },
                {
                    "id": 2,
                    "name": "test варенье",
                    "measurement_unit": "ложка",
                    "amount": 1,
                },
            ],
            "is_favorited": False,
            "is_in_shopping_cart": False,
            "name": "test рецепт",
            "image": "http://testserver/media/recipes/images/small.gif",
            "text": "описание тестового рецепта",
            "cooking_time": 4,
        }
        self.assertEqual(response.json(), test_json)

    def test_recipe_list_get_is_in_shopping_cart_authorized_client(self):
        ShoppingCart.objects.create(user=self.user, recipe=self.recipe)
        Recipe.objects.create(
            author=self.user,
            name="тестовый рецепт",
            text="описание тестового рецепта",
            cooking_time=4,
        )
        url = "/api/recipes/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 3,
                    "tags": [],
                    "author": {
                        "email": "",
                        "id": 1,
                        "username": "authorized_user",
                        "first_name": "",
                        "last_name": "",
                        "is_subscribed": False,
                    },
                    "ingredients": [],
                    "is_favorited": False,
                    "is_in_shopping_cart": False,
                    "name": "тестовый рецепт",
                    "image": None,
                    "text": "описание тестового рецепта",
                    "cooking_time": 4,
                },
                {
                    "id": 2,
                    "tags": [
                        {
                            "id": 1,
                            "name": "test Завтрак",
                            "color": "#6AA84FFF",
                            "slug": "breakfast",
                        }
                    ],
                    "author": {
                        "email": "",
                        "id": 1,
                        "username": "authorized_user",
                        "first_name": "",
                        "last_name": "",
                        "is_subscribed": False,
                    },
                    "ingredients": [
                        {
                            "id": 1,
                            "name": "test апельсин",
                            "measurement_unit": "шт.",
                            "amount": 5,
                        }
                    ],
                    "is_favorited": False,
                    "is_in_shopping_cart": True,
                    "name": "тестовый рецепт",
                    "image": (
                        "http://testserver/media/recipes/images/small_1.gif"
                    ),
                    "text": "описание тестового рецепта",
                    "cooking_time": 4,
                },
                {
                    "id": 1,
                    "tags": [
                        {
                            "id": 1,
                            "name": "test Завтрак",
                            "color": "#6AA84FFF",
                            "slug": "breakfast",
                        }
                    ],
                    "author": {
                        "email": "",
                        "id": 1,
                        "username": "authorized_user",
                        "first_name": "",
                        "last_name": "",
                        "is_subscribed": False,
                    },
                    "ingredients": [
                        {
                            "id": 1,
                            "name": "test апельсин",
                            "measurement_unit": "шт.",
                            "amount": 5,
                        },
                        {
                            "id": 2,
                            "name": "test варенье",
                            "measurement_unit": "ложка",
                            "amount": 1,
                        },
                    ],
                    "is_favorited": False,
                    "is_in_shopping_cart": False,
                    "name": "test рецепт",
                    "image": (
                        "http://testserver/media/recipes/images/small.gif"
                    ),
                    "text": "описание тестового рецепта",
                    "cooking_time": 4,
                },
            ],
        }
        self.assertEqual(response.json(), test_json)

    def test_add_recipe_to_shopping_cart_authorized_client(self):
        count = ShoppingCart.objects.count()
        url = f"/api/recipes/{self.recipe_breakfast.id}/shopping_cart/"
        response = self.test_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShoppingCart.objects.count(), count + 1)
        test_json = {
            "id": 1,
            "name": "test рецепт",
            "image": "http://testserver/media/recipes/images/small.gif",
            "cooking_time": 4,
        }
        self.assertEqual(response.json(), test_json)

    def test_add_recipe_in_shopping_cart_guest_client(self):
        url = f"/api/recipes/{self.recipe.id}/shopping_cart/"
        response = self.guest_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_add_recipe_in_shopping_cart_authorized_client_400(self):
        url = f"/api/recipes/{self.recipe.id}/shopping_cart/"
        response = self.test_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.test_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"errors": "Рецепт уже добавлен в корзину"}
        self.assertEqual(response.json(), test_json)

    def test_delete_recipe_in_shopping_cart_authorized_client(self):
        url = f"/api/recipes/{self.recipe.id}/shopping_cart/"
        response = self.test_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.test_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_recipe_in_shopping_cart_guest_client(self):
        url = f"/api/recipes/{self.recipe.id}/shopping_cart/"
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.guest_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_delete_recipe_in_shopping_cart_authorized_client_400(self):
        url = f"/api/recipes/{self.recipe.id}/shopping_cart/"
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"errors": "Рецепт уже удален из корзины"}
        self.assertEqual(response.json(), test_json)

    def test_download_shopping_cart_unauthorized_user(self):
        url = "/api/recipes/download_shopping_cart/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_get_recipes_filter_by_author(self):
        test_user = User.objects.create(username="test_user")
        url = f"/api/recipes/?author={test_user.id}"
        recipe_1 = Recipe.objects.create(
            author=test_user,
            name="тестовый рецепт 1",
            image=None,
            text="описание тестового рецепта 1",
            cooking_time=4,
        )
        recipe_2 = Recipe.objects.create(
            author=test_user,
            name="тестовый рецепт 2",
            image=None,
            text="описание тестового рецепта 2",
            cooking_time=4,
        )
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_user_recipes_id = [recipe_1.id, recipe_2.id]
        test_recipes_id = [
            recipe["id"] for recipe in response.json()["results"]
        ]
        self.assertEqual(
            sorted(test_user_recipes_id), sorted(test_recipes_id)
        )

    def test_get_recipes_filter_by_tags(self):
        test_user = self.test_user
        recipe_1 = Recipe.objects.create(
            author=test_user,
            name="тестовый рецепт тег 1",
            image=None,
            text="описание тестового рецепта 1",
            cooking_time=4,
        )
        recipe_1.tags.add(self.tag_breakfast)
        recipe_2 = Recipe.objects.create(
            author=test_user,
            name="тестовый рецепт тег 2",
            image=None,
            text="описание тестового рецепта 2",
            cooking_time=4,
        )
        recipe_2.tags.add(self.tag_dinner)
        recipe_3 = Recipe.objects.create(
            author=test_user,
            name="тестовый рецепт тег 1 и 2",
            image=None,
            text="описание тестового рецепта тег 1 и 2",
            cooking_time=4,
        )
        recipe_3.tags.add(self.tag_breakfast, self.tag_dinner)
        url = f"/api/recipes/?tags={self.tag_breakfast.slug}"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag_recipes_id = [
            recipe_1.id,
            recipe_3.id,
            self.recipe_breakfast.id,
            self.recipe.id,
        ]
        test_recipes_id = [
            recipe["id"] for recipe in response.json()["results"]
        ]
        self.assertEqual(sorted(tag_recipes_id), sorted(test_recipes_id))

    def test_get_recipes_filter_by_is_favorited(self):
        test_user = User.objects.create(username="test_user")
        recipe_1 = Recipe.objects.create(
            author=test_user,
            name="избранный рецепт 1",
            image=None,
            text="описание избранного рецепта 1",
            cooking_time=4,
        )
        recipe_2 = Recipe.objects.create(
            author=test_user,
            name="избранный рецепт 2",
            image=None,
            text="описание избранного рецепта 2",
            cooking_time=4,
        )
        Favorite.objects.bulk_create(
            [
                Favorite(
                    user=self.user,
                    recipe=recipe_1,
                ),
                Favorite(
                    user=self.user,
                    recipe=recipe_2,
                ),
            ]
        )
        url = "/api/recipes/?is_favorited=1"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        favorite_recipes_id = [recipe_1.id, recipe_2.id]
        test_recipes_id = [
            recipe["id"] for recipe in response.json()["results"]
        ]
        self.assertEqual(sorted(favorite_recipes_id), sorted(test_recipes_id))

    def test_get_recipes_filter_by_is_favorited_unauthorized_user(self):
        test_user = User.objects.create(username="test_user")
        recipe_1 = Recipe.objects.create(
            author=test_user,
            name="избранный рецепт 1",
            image=None,
            text="описание избранного рецепта 1",
            cooking_time=4,
        )

        Favorite.objects.create(
            user=self.user,
            recipe=recipe_1,
        )
        url = "/api/recipes/?is_favorited=1"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_recipes_id = [
            recipe["id"] for recipe in response.json()["results"]
        ]
        self.assertEqual(test_recipes_id, [])

    def test_get_recipes_filter_by_is_in_shopping_cart(self):
        test_user = User.objects.create(username="test_user")
        recipe_1 = Recipe.objects.create(
            author=test_user,
            name="избранный рецепт 1",
            image=None,
            text="описание избранного рецепта 1",
            cooking_time=4,
        )
        recipe_2 = Recipe.objects.create(
            author=test_user,
            name="избранный рецепт 2",
            image=None,
            text="описание избранного рецепта 2",
            cooking_time=4,
        )
        ShoppingCart.objects.bulk_create(
            [
                ShoppingCart(
                    user=self.user,
                    recipe=recipe_1,
                ),
                ShoppingCart(
                    user=self.user,
                    recipe=recipe_2,
                ),
            ]
        )
        url = "/api/recipes/?is_in_shopping_cart=1"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shoppingcart_recipes_id = [recipe_1.id, recipe_2.id]
        test_recipes_id = [
            recipe["id"] for recipe in response.json()["results"]
        ]
        self.assertEqual(
            sorted(shoppingcart_recipes_id), sorted(test_recipes_id)
        )

    def test_get_recipes_filter_by_is_in_shopping_cart_anonymous(self):
        test_user = User.objects.create(username="test_user")
        recipe_1 = Recipe.objects.create(
            author=test_user,
            name="избранный рецепт 1",
            image=None,
            text="описание избранного рецепта 1",
            cooking_time=4,
        )
        ShoppingCart.objects.create(
            user=self.user,
            recipe=recipe_1,
        )
        url = "/api/recipes/?is_in_shopping_cart=1"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_recipes_id = [
            recipe["id"] for recipe in response.json()["results"]
        ]
        self.assertEqual(sorted(test_recipes_id), [])

    def test_get_ingredients_search_by_name(self):
        ingredient_1 = Ingredient.objects.create(
            name="ингредиент 1",
            measurement_unit="шт",
        )
        ingredient_2 = Ingredient.objects.create(
            name="ингредиент 2",
            measurement_unit="шт",
        )

        url = "/api/ingredients/?name=ингредиент"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient_ids = [ingredient_1.id, ingredient_2.id]
        test_ingredient_ids = [
            ingredient["id"] for ingredient in response.json()
        ]
        self.assertEqual(sorted(ingredient_ids), sorted(test_ingredient_ids))

        url = "/api/ingredients/?name=ингре"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient_ids = [ingredient_1.id, ingredient_2.id]
        test_ingredient_ids = [
            ingredient["id"] for ingredient in response.json()
        ]
        self.assertEqual(sorted(ingredient_ids), sorted(test_ingredient_ids))

        url = "/api/ingredients/?name=ингредиент 1"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient_ids = [ingredient_1.id]
        test_ingredient_ids = [
            ingredient["id"] for ingredient in response.json()
        ]
        self.assertEqual(sorted(ingredient_ids), sorted(test_ingredient_ids))

        url = "/api/ingredients/?name=диент"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient_ids = [ingredient_1.id, ingredient_2.id]
        test_ingredient_ids = [
            ingredient["id"] for ingredient in response.json()
        ]
        self.assertEqual(sorted(ingredient_ids), sorted(test_ingredient_ids))

        url = "/api/ingredients/?name=test"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient_ids = [self.ingredient_orange.id, self.ingredient_jam.id]
        test_ingredient_ids = [
            ingredient["id"] for ingredient in response.json()
        ]
        self.assertEqual(sorted(ingredient_ids), sorted(test_ingredient_ids))

        url = "/api/ingredients/?name=TEST"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient_ids = [self.ingredient_orange.id, self.ingredient_jam.id]
        test_ingredient_ids = [
            ingredient["id"] for ingredient in response.json()
        ]
        self.assertEqual(sorted(ingredient_ids), sorted(test_ingredient_ids))
