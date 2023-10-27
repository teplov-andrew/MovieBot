import pytest
import telebot
import pandas as pd
from config import CFG
from unittest.mock import patch, Mock
from bot import kino_guied, help, film_ser, primers, acrtist__1, rand_film


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



if __name__ == '__main__':
    pytest.main()
