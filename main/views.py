from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from afisha.models import Event
from afisha.serializers import EventSerializer
from django.utils import timezone


TEMP_DATA = {
    "history": {
        "id": 21,
        "imageUrl": "https://picsum.photos/870/520",
        "title": "История Марины и Алины"
    },
    "place": {
        "chosen": True,
        "id": 31,
        "title": "Сплав на байдарках в две строки",
        "name": "усадьба Архангельское в две строки",
        "info": "Девока, 10 лет. Активный отдых",
        "description": "Аннотация статьи в несколько абзацев. В тот момент, "
                       "как ребёнок научился говорить, и не одно слово, "
                       "а задавать бесконечное количество вопросов, "
                       "жизнь меняется. Вы будете не понимать друг друга,  "
                       "потом понимать чуть лучше и, Аннотация статьи в "
                       "несколько абзацев. В тот момент, как ребёнок "
                       "научился говорить, и не одно слово, а задавать "
                       "бесконечное количество вопросов, жизнь меняется. Вы "
                       "будете не понимать друг друга,  потом понимать чуть "
                       "лучше и,\nАннотация статьи в несколько абзацев. В "
                       "тот момент, как ребёнок научился говорить, и не одно "
                       "слово, а задавать бесконечное количество вопросов, "
                       "жизнь меняется. Вы будете не по Аннотация статьи в "
                       "несколько абзацев. В тот момент, как ребёнок "
                       "научился говорить, и не одно слово, а задавать "
                       "бесконечное количество вопросов, жизнь меняется.",
        "imageUrl": "https://picsum.photos/1125/394",
        "link": "https://www.moscowzoo.ru/"
    },
    "articles": [
        {
            "id": 41,
            "color": "#C8D1FF",
            "title": "Развитие детей-сирот отличается от развития детей, "
                     "живущих в семьях. Все  этапы развития у детей-сирот "
                     "проходят с искажениями и имеют ряд негативных "
                     "особенностей. "
        },
        {
            "id": 42,
            "color": "#8CDD94",
            "title": "У таких детей возникает ощущение отверженности. Оно "
                     "приводит к напряженности и  недоверию к людям и, как "
                     "итог, к реальному неприятию себя и окружающих."
        }
    ],
    "movies": [
        {
            "id": 51,
            "imageUrl": "https://picsum.photos/420/239",
            "title": "Жутко громко и запредельно близко",
            "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
            "link": "https://youtu.be/8VzzlhOyOSI",
            "tags": [
                {
                    "id": 551,
                    "name": "рубрика",
                    "slug": "rubric"
                },
                {
                    "id": 552,
                    "name": "рубрика",
                    "slug": "rubric"
                }
            ]
        },
        {
            "id": 52,
            "imageUrl": "https://picsum.photos/420/239",
            "title": "Жутко громко и запредельно близко",
            "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
            "link": "https://youtu.be/8VzzlhOyOSI",
            "tags": [
                {
                    "id": 551,
                    "name": "рубрика",
                    "slug": "rubric"
                },
                {
                    "id": 552,
                    "name": "рубрика",
                    "slug": "rubric"
                }
            ]
        },
        {
            "id": 53,
            "imageUrl": "https://picsum.photos/420/239",
            "title": "Жутко громко и запредельно близко",
            "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
            "link": "https://youtu.be/8VzzlhOyOSI",
            "tags": [
                {
                    "id": 551,
                    "name": "рубрика",
                    "slug": "rubric"
                },
                {
                    "id": 552,
                    "name": "рубрика",
                    "slug": "rubric"
                }
            ]
        },
        {
            "id": 54,
            "imageUrl": "https://picsum.photos/420/239",
            "title": "Жутко громко и запредельно близко",
            "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
            "link": "https://youtu.be/8VzzlhOyOSI",
            "tags": [
                {
                    "id": 551,
                    "name": "рубрика",
                    "slug": "rubric"
                },
                {
                    "id": 552,
                    "name": "рубрика",
                    "slug": "rubric"
                }
            ]
        }
    ],
    "video": {
        "id": 61,
        "title": "Эфир с выпускником нашей программы",
        "info": "Иван Рустаев, выпускник программы",
        "link": "https://youtu.be/H980rXfjdq4",
        "imageUrl": "https://picsum.photos/1199/675",
        "duration": 134
    },
    "questions": [
        {
            "id": 71,
            "tags": [
                {
                    "id": 771,
                    "name": "рубрика",
                    "slug": "rubric"
                }
            ],
            "title": "Я боюсь, что ребёнок ко мне слишком сильно привяжется. "
                     "Что делать?"
        },
        {
            "id": 72,
            "tags": [
                {
                    "id": 771,
                    "name": "рубрика",
                    "slug": "rubric"
                }
            ],
            "title": "Возможно ли продлить срок участия в программе, если и я "
                     "и мой «младший» хотим остаться в программе?"
        },
        {
            "id": 73,
            "tags": [
                {
                    "id": 771,
                    "name": "рубрика",
                    "slug": "rubric"
                }
            ],
            "title": "Что делать если Ваш младший решил закрыть пару, т.к. "
                     "слишком занят с учебой и друзьями?"
        }
    ]
}


class MainView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        context = {}
        event = Event.objects.get(start_at__gt=timezone.now())
        event_serializer = EventSerializer(event)
        context['event'] = {**event_serializer.data}
        context.update(**TEMP_DATA)
        return Response(context)
