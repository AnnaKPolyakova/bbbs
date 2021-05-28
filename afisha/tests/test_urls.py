from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse

from users.factories import UserFactory
from common.factories import CityFactory


class StaticURLTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = CityFactory(name="Воркута")
        cls.mentor = UserFactory(
            profile__role="mentor",
            profile__city=cls.city,
        )
        cls.moderator_reg = UserFactory(
            profile__role="moderator_reg",
            profile__city=cls.city,
        )
        cls.moderator_gen = UserFactory(
            profile__role="moderator_gen",
            profile__city=cls.city,
        )
        cls.admin = UserFactory(
            profile__role="admin",
            profile__city=cls.city,
        )
        cls.users = [
            cls.mentor,
            cls.moderator_reg,
            cls.moderator_gen,
            cls.admin,
        ]
        cls.unauthorized_client = APIClient()

        cls.path_events_participants = reverse("event-participants-list")
        cls.path_events = reverse("events")

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_events_unauthorized_client(self):
        client = self.unauthorized_client
        response = client.get(self.path_events)
        self.assertEqual(
            response.status_code,
            401,
            msg=(
                f"Проверьте что неавторизованный пользователь не имеет "
                f"доступ к '{self.path_events}'."
            ),
        )

    def test_events_participants_unauthorized_client(self):
        client = self.unauthorized_client
        response = client.get(self.path_events_participants)
        self.assertEqual(
            response.status_code,
            401,
            msg=(
                f"Проверьте что неавторизованный пользователь не имеет доступ "
                f"к '{self.path_events_participants}'."
            ),
        )

    def test_events(self):
        for user in self.users:
            client = self.return_authorized_user_client(user=user)
            response = client.get(self.path_events)
            self.assertEqual(
                response.status_code,
                200,
                msg=(
                    f"Проверьте что пользователь с ролью "
                    f"'{user.profile.role}' "
                    f"имеет доступ к "
                    f"'{self.path_events_participants}'."
                ),
            )

    def test_event_participants(self):
        for user in self.users:
            client = self.return_authorized_user_client(user=user)
            response = client.get(self.path_events_participants)
            self.assertEqual(
                response.status_code,
                200,
                msg=(
                    f"Проверьте что пользователь с ролью "
                    f"'{user.profile.role}' "
                    f"имеет доступ к "
                    f"'{self.path_events_participants}'."
                ),
            )

    def test_page_not_found(self):
        client = self.unauthorized_client
        response = client.get("/the_page_that_doesnt_exist/")
        self.assertEqual(
            response.status_code,
            404,
            msg=(
                "Проверьте что ошибка 404 возвращается для несуществующих "
                "эндпоинтов."
            ),
        )
