import pytest
import telebot
import pandas as pd
from config import CFG
from help_functions import clear_msg
from unittest.mock import patch, Mock
from bot import kino_guied, help, film_ser, primers, acrtist__1, rand_film, search_films


data = pd.read_csv(CFG.PATH_DATA, sep=',')
data_of_films = list(data["movie"])
for i in range(len(data_of_films)):
    data_of_films[i] = clear_msg(data_of_films[i])

class TestBot:
    @pytest.fixture(autouse=True)
    def setup_bot(self):
        self.bot = telebot.TeleBot(CFG.TG_BOT_TOKEN)
        self.message = Mock()
        self.message.chat.id = 4768659920
        # self.message.text = "/help"

    def test_kin_guied(self):
        with patch('telebot.TeleBot.send_message') as mocked:
            kino_guied(self.message)
            mocked.assert_called_once_with(self.message.chat.id, CFG.QQ)

    def test_help(self):
        with patch("telebot.TeleBot.send_message") as mocked:
            help(self.message)
            mocked.assert_called_once_with(self.message.chat.id, 'Запутались в кнопках?\n\n●  Фильм/Сериал--выводит по вашему запросу Фильм/Сериал, что вам нужен!\n●  Cлучайный фильм/сериал--если вам нечего посмотреть, то воспользуйтесь этой кнопкой и ищите то, что вам понравится.\n●  Актер--выводит по вашему запросу Актера/Актриссу.\n●  Случайный Актер--если вы хотите познакомиться с новым Актером/Актриссой, то воспользуйтесь этой кнопкой и ищите фильмы с их участием!')

    def test_film_ser(self):
        with patch('telebot.TeleBot.send_message') as mocked:
            film_ser(self.message)
            mocked.assert_called_once_with(
                self.message.chat.id, 'Приготовь вкусняшек!\nНапишите полное название фильма/сериала...\n⬇️⬇️⬇')

    def test_primers(self):
        with patch('telebot.TeleBot.send_message') as mocked:
            primers(self.message)
            mocked.assert_called_once_with(self.message.chat.id, open(CFG.PRIMERS_DATA, "r", encoding="utf8").read())
            
    def test_acrtist__1(self):
        with patch('telebot.TeleBot.send_message') as mocked:
            acrtist__1(self.message)
            mocked.assert_called_once_with(self.message.chat.id, 'Введите полное имя актера/актрисы...\n⬇️⬇️⬇️', parse_mode='html')

    def test_rand_film(self):
        with patch('telebot.TeleBot.send_message') as mocked:
            rand_film(self.message)
            assert mocked.called
            args, kwargs = mocked.call_args
            assert clear_msg(args[1].split("[")[1].split("]")[0]) in data_of_films


    @pytest.mark.parametrize("user_message,expected_substring", [
        ("Матрица", f'●  Название: [Матрица]'), 
        ("Хэллоуин", f'●  Название: [Хэллоуин]'),
        ("Киану Ривз", "●  Имя: [Киану Ривз]"),
        ("Бред Пит", "●  Имя: [Брэд Питт]"),
        ("йагйруаушощцоашцуоащоцщоашллд", "Я не понял ваш запрос! Попробуйте написать название фильма на английском"),
        
    ])

    def test_search_films(self, user_message, expected_substring):
        self.message.text = user_message
        with patch('telebot.TeleBot.send_message') as mocked:
            search_films(self.message)
            assert mocked.called
            args, kwargs = mocked.call_args
            assert expected_substring in args[1]

if __name__ == '__main__':
    pytest.main()
