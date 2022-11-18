from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from users.models import Subscription, User


class UsersViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = APIClient()

        cls.user = User.objects.create_user(username="authorized_user")
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

        cls.test_user = User.objects.create_user(username="testusername")

        cls.user_vasya = User.objects.create_user(
            email="Alexiy@gmail.com",
            username="Alexiy.popka",
            first_name="Константин",
            last_name="Христорождественский",
        )

        Subscription.objects.create(
            user=cls.user,
            author=cls.user_vasya,
        )

        cls.ingredient_orange = Ingredient.objects.create(
            name="test апельсин",
            measurement_unit="шт.",
        )
        cls.ingredient_jam = Ingredient.objects.create(
            name="test джем",
            measurement_unit="ложка",
        )
        cls.tag_breakfast = Tag.objects.create(
            name="test Завтрак",
            color="#6AA84FFF",
            slug="breakfast",
        )
        cls.tag_dinner = Tag.objects.create(
            name="test Ужин",
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
        cls.recipe_orange_jam = Recipe.objects.create(
            author=cls.user,
            name="test рецепт",
            text="описание тестового рецепта",
            cooking_time=4,
        )
        cls.recipe_orange_jam.tags.add(cls.tag_breakfast)
        cls.recipe_orange_jam.ingredients.add(
            cls.ingredientamount_orange,
            cls.ingredientamount_jam,
        )
        cls.recipe_breakfast = Recipe.objects.create(
            author=cls.user,
            name="test рецепт 2",
            text="описание тестового рецепта 2",
            cooking_time=10,
        )
        cls.recipe_breakfast.tags.add(cls.tag_breakfast)
        cls.recipe_breakfast.ingredients.add(
            cls.ingredientamount_orange,
            cls.ingredientamount_jam,
        )

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    def test_get_users_list_unauthorized_user(self):
        url = "/api/users/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_users_list(self):
        url = "/api/users/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "email": "",
                    "id": 1,
                    "username": "authorized_user",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": False,
                },
                {
                    "email": "",
                    "id": 2,
                    "username": "testusername",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": False,
                },
                {
                    "email": "Alexiy@gmail.com",
                    "id": 3,
                    "username": "Alexiy.popka",
                    "first_name": "Константин",
                    "last_name": "Христорождественский",
                    "is_subscribed": True,
                },
            ],
        }
        self.assertEqual(response.json(), test_json)

    def test_create_user(self):
        url = "/api/users/"
        users_count = User.objects.count()
        data = {
            "email": "Alexiy@gmail.com",
            "username": "Alexiy.popka",
            "first_name": "Константин",
            "last_name": "Христорождественский",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), users_count + 1)
        test_json = {
            "email": "Alexiy@gmail.com",
            "id": users_count + 1,
            "username": "Alexiy.popka",
            "first_name": "Константин",
            "last_name": "Христорождественский",
        }
        self.assertEqual(response.json(), test_json)

    def test_create_user_with_simple_password(self):
        url = "/api/users/"
        data = {
            "email": "Alexiy@yandex.ru",
            "username": "Alexiy",
            "first_name": "Конст",
            "last_name": "Христ",
            "password": "123",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "password": [
                (
                    "Введённый пароль слишком короткий. "
                    + "Он должен содержать как минимум 8 символов."
                ),
                "Введённый пароль слишком широко распространён.",
                "Введённый пароль состоит только из цифр.",
            ]
        }
        self.assertEqual(response.json(), test_json)

    def test_create_user_without_password(self):
        url = "/api/users/"
        data = {
            "email": "Alex@gmail.com",
            "username": "Alex.popka",
            "first_name": "Константин",
            "last_name": "Христорождественский",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"password": ["Обязательное поле."]}
        )

    def test_create_user_without_email(self):
        url = "/api/users/"
        data = {
            "username": "Ale.popka",
            "first_name": "Константин",
            "last_name": "Христорождественский",
            "password": "cknvkjcn2313556vkjdfvq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"email": ["Обязательное поле."]})

    def test_create_user_without_username(self):
        url = "/api/users/"
        data = {
            "email": "Al@gmail.com",
            "first_name": "Константин",
            "last_name": "Христорождественский",
            "password": "fdgk4556dfmgkfdmglkfd",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"username": ["Обязательное поле."]}
        )

    def test_create_user_without_first_name(self):
        url = "/api/users/"
        data = {
            "email": "Alexiyop@gmail.com",
            "username": "Alexiyop.popka",
            "last_name": "Христорождественский",
            "password": "dvdvnmsfn44567klmlvmkdf",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"first_name": ["Обязательное поле."]}
        )

    def test_create_user_without_last_name(self):

        url = "/api/users/"
        data = {
            "email": "Alexiyopa@gmail.com",
            "username": "Alexiyopa.popka",
            "first_name": "Константин",
            "password": "dmkdfks567tokgho",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"last_name": ["Обязательное поле."]}
        )

    def test_create_user_without_first_last_names(self):

        url = "/api/users/"
        data = {
            "email": "Alexiyjopa@gmail.com",
            "username": "Alexiyjopa.popka",
            "password": "vmkdfmbkfmbklfldggmbk4567",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "first_name": ["Обязательное поле."],
                "last_name": ["Обязательное поле."],
            },
        )

    def test_user_profile(self):
        user = self.user_vasya
        client_vasya = APIClient()
        client_vasya.force_authenticate(user)
        url = f"/api/users/{user.id}/"
        response = client_vasya.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "email": "Alexiy@gmail.com",
            "id": 3,
            "username": "Alexiy.popka",
            "first_name": "Константин",
            "last_name": "Христорождественский",
            "is_subscribed": False,
        }
        self.assertEqual(response.json(), test_json)

    def test_user_profileby_by_authorized_user(self):
        user = self.user_vasya
        url = f"/api/users/{user.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "email": "Alexiy@gmail.com",
            "id": 3,
            "username": "Alexiy.popka",
            "first_name": "Константин",
            "last_name": "Христорождественский",
            "is_subscribed": True,
        }
        self.assertEqual(response.json(), test_json)

    def test_user_profile_by_unauthorized_user(self):
        user = self.user_vasya
        url = f"/api/users/{user.id}/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_user_profile_404(self):
        count = User.objects.count()
        url = f"/api/users/{count + 1}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)

    def test_current_user_profile(self):
        user = User.objects.get(username="authorized_user")
        url = "/api/users/me/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "email": "",
            "id": user.id,
            "username": "authorized_user",
            "first_name": "",
            "last_name": "",
            "is_subscribed": False,
        }
        self.assertEqual(response.json(), test_json)

    def test_current_user_profile_401(self):
        url = "/api/users/me/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_set_password(self):
        url = "/api/users/set_password/"
        user = User.objects.create_user(
            username="test_user",
            password="fggkfgme345",
        )
        client = APIClient()
        client.force_authenticate(user)
        data = {
            "new_password": "qorperplfb56",
            "current_password": "fggkfgme345",
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_set_password_incorrect_current_password(self):
        url = "/api/users/set_password/"
        user = User.objects.create_user(
            username="test_user",
            password="1wkfy267snsndndnd",
        )
        client = APIClient()
        client.force_authenticate(user)
        data = {
            "new_password": "yydhdhdje81ihnsksd",
            "current_password": "123",
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"current_password": ["Неправильный пароль."]}
        self.assertEqual(response.json(), test_json)

    def test_set_password_no_new_password(self):
        url = "/api/users/set_password/"
        user = User.objects.create_user(
            username="test_user",
            password="1wkfy267snsndndnd",
        )
        client = APIClient()
        client.force_authenticate(user)
        data = {
            "current_password": "1wkfy267snsndndnd",
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"new_password": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_set_password_401(self):
        url = "/api/users/set_password/"
        data = {
            "new_password": "yydhdhdje81ihnsksd",
            "current_password": "1wkfy267snsndndnd",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_get_authorization_token(self):
        url = "/api/auth/token/login/"
        User.objects.create_user(
            username="test_user",
            password="1wkfy267snsndndnd",
            email="test@mail.ru",
        )
        data = {"password": "1wkfy267snsndndnd", "email": "test@mail.ru"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("auth_token" in response.json().keys())

    def test_get_authorization_token_with_invalid_data(self):

        url = "/api/auth/token/login/"
        data = {"password": "string", "email": "string"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "non_field_errors": [
                "Невозможно войти с предоставленными учетными данными."
            ]
        }
        self.assertEqual(response.json(), test_json)

    def test_deleting_token(self):
        url = "/api/auth/token/logout/"
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_token_401(self):
        url = "/api/auth/token/logout/"
        response = self.guest_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_subscribe_authorized_client(self):
        user = self.user_vasya
        client_vasya = APIClient()
        client_vasya.force_authenticate(user)
        count = Subscription.objects.count()
        url = f"/api/users/{self.user.id}/subscribe/"
        response = client_vasya.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), count + 1)
        test_json = {
            "email": "",
            "id": 1,
            "username": "authorized_user",
            "first_name": "",
            "last_name": "",
            "is_subscribed": True,
            "recipes": [
                {
                    "id": 2,
                    "name": "test рецепт 2",
                    "image": None,
                    "cooking_time": 10,
                },
                {
                    "id": 1,
                    "name": "test рецепт",
                    "image": None,
                    "cooking_time": 4,
                },
            ],
            "recipes_count": 2,
        }
        self.assertEqual(response.json(), test_json)

    def test_subscribe_yourself_not_allowed(self):
        url = f"/api/users/{self.user.id}/subscribe/"
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"errors": "Нельзя подписаться на самого себя"}
        self.assertEqual(response.json(), test_json)

    def test_subscribe_user_twice(self):
        test_user = self.test_user
        authorized_client = APIClient()
        authorized_client.force_authenticate(test_user)
        count = Subscription.objects.count()
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), count + 1)
        response = authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"errors": "Вы уже подписаны на данного пользователя"}
        self.assertEqual(response.json(), test_json)

    def test_subscribe_guest_client(self):
        url = f"/api/users/{self.user.id}/subscribe/"
        response = self.guest_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_subscribe_404(self):
        user_count = User.objects.count()
        url = f"/api/users/{user_count + 1}/subscribe/"
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)

    def test_unsubscribe_authorized_client(self):
        test_user = self.test_user
        authorized_client = APIClient()
        authorized_client.force_authenticate(test_user)
        count = Subscription.objects.count()
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), count + 1)
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unsubscribe_from_user_you_are_not_subscribing(self):
        test_user = self.test_user
        authorized_client = APIClient()
        authorized_client.force_authenticate(test_user)
        count = Subscription.objects.count()
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), count + 1)
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"errors": "Вы не подписаны на данного пользователя"}
        self.assertEqual(response.json(), test_json)

    def test_unsubscribe_guest_client(self):
        url = f"/api/users/{self.user.id}/subscribe/"
        response = self.guest_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_unsubscribe_404(self):
        count = User.objects.count()
        url = f"/api/users/{count + 1}/subscribe/"
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)

    def test_subscriptions(self):
        test_author_6 = User.objects.create(username="test_author_6")
        test_author_7 = User.objects.create(username="test_author_7")
        test_author_5 = User.objects.create(username="test_author_5")
        test_author_1 = User.objects.create(username="test_author_1")
        test_author_3 = User.objects.create(username="test_author_3")
        test_author_4 = User.objects.create(username="test_author_4")
        test_author_2 = User.objects.create(username="test_author_2")

        Subscription.objects.bulk_create(
            [
                Subscription(user=self.user, author=test_author_6),
                Subscription(user=self.user, author=test_author_4),
                Subscription(user=self.user, author=test_author_2),
                Subscription(user=self.user, author=test_author_1),
                Subscription(user=self.user, author=test_author_3),
                Subscription(user=self.user, author=test_author_5),
                Subscription(user=self.user, author=test_author_7),
            ]
        )

        url = "/api/users/subscriptions/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "count": 8,
            "next": "http://testserver/api/users/subscriptions/?page=2",
            "previous": None,
            "results": [
                {
                    "email": "",
                    "id": 5,
                    "username": "test_author_7",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
                {
                    "email": "",
                    "id": 6,
                    "username": "test_author_5",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
                {
                    "email": "",
                    "id": 8,
                    "username": "test_author_3",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
                {
                    "email": "",
                    "id": 7,
                    "username": "test_author_1",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
                {
                    "email": "",
                    "id": 10,
                    "username": "test_author_2",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
                {
                    "email": "",
                    "id": 9,
                    "username": "test_author_4",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
            ],
        }
        self.assertEqual(response.json(), test_json)

    def test_subscriptions_authentication_credentials_were_not_provided(self):
        url = "/api/users/subscriptions/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)
