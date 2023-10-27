import re
import random
import pandas as pd

import telebot
from telebot import types

from config import CFG
from kinopoisk_api import Kinopoisk
from kinomax_scrap import cinema_primers_data
from help_functions import clear_msg, clean_link


data = pd.read_csv(CFG.PATH_DATA, sep=',')
primers_data = open(CFG.PRIMERS_DATA, "r", encoding="utf8").read()

client = telebot.TeleBot(CFG.TG_BOT_TOKEN)

kino = Kinopoisk(CFG.KINOPOIS_API_KEY)




#                                                 ПРИВЕТСТВИЕ+ДОБАВЛЕНИЕ КНОПОК
@client.message_handler(func=lambda c: c.text == '/start')
def start(message):
	mess = f'Привет, {message.from_user.first_name}, Что хотите посмотреть?!'
	client.send_message(message.chat.id, mess, parse_mode='html')
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn_start = types.InlineKeyboardButton('/start')
	btn_movie_ser = types.InlineKeyboardButton('Фильм/Сериал')
	btn_rnd_movie = types.InlineKeyboardButton('Cлучайный фильм/сериал')
	btn_rnd_actor = types.InlineKeyboardButton('Cлучайный актер')
	btn_actor = types.InlineKeyboardButton('Актер')
	KPoisk = types.InlineKeyboardButton('Как смотреть бесплатно???')
	FF = types.InlineKeyboardButton('Премьеры в кинотеатре')
	markup.add(btn_movie_ser, btn_actor)
	markup.add(btn_rnd_movie, btn_rnd_actor)
	markup.add(FF)
	markup.row(KPoisk)
	client.send_message(message.chat.id, '👋', reply_markup=markup)


#                                                ФУНКЦИЯ(КНОПКА) РАНДОМНЫЙ ФИЛЬМ
@client.message_handler(func=lambda c: c.text == "Cлучайный фильм/сериал")
def rand_film(message):
	name = random.choice(data['movie'])
	for i in range(len(data)):
		if clear_msg(name) == clear_msg(data['movie'][i]):
			client.send_message(message.chat.id,
								f"●  Название: [{data.loc[i][1].replace(';', ',')}]({clean_link(data.loc[i][9])})\n●  Год: {data.loc[i][2]}\n●  Страна: {data.loc[i][3]}\n●  Рейтинг: {round(data.loc[i][4], 2)}\n●  Режиссер: {data.loc[i][6].replace(';', ',')}\n●  Оператор: {data.loc[i][7].replace(';', ',')}\n●  Актеры: {data.loc[i][8].replace(';', ',')}\n●  Описание: {data.loc[i][5].replace(';', '')}\n●  Кинопоиск: https://www.kinopoisk.ru/film/{re.sub('[^0-9]', '', data.loc[i][9].replace('_', ' '))[3:]} ", parse_mode='Markdown')


#                      							 Гайд
@client.message_handler(func=lambda c: c.text == "Как смотреть бесплатно???")
def kino_guied(message):
	# client.send_sticker(
		# message.chat.id, 'CAACAgIAAxkBAAEEXjJiSwfIw1ah_TA_UvVJpESIffzeoQACOwMAArVx2gYYSwbSVVPLRCME')
	client.send_message(message.chat.id, CFG.QQ)
	# client.send_message(message, "Aboba")
#                      							 ФИЛЬМ/СЕРИАЛ


@client.message_handler(func=lambda c: c.text == "Фильм/Сериал")
def film_ser(message):
	# client.send_sticker(
	# 	message.chat.id, 'CAACAgIAAxkBAAEEYgABYkyX0Kr38I_YdHOwiricZqzI4MoAAvgSAAJCTllKAAFziHtpqojNIwQ')
	client.send_message(
		message.chat.id, 'Приготовь вкусняшек!\nНапишите полное название фильма/сериала...\n⬇️⬇️⬇')

#                      							 HELP функция


@client.message_handler(func=lambda c: c.text == "/help")
def help(message):
	# client.send_sticker(
	# 	message.chat.id, 'CAACAgIAAxkBAAEEXqhiSxYKOT32r_p8GIlLxTkee_QCQgACJyAAAulVBRjTVPZqymtoFyME')
	client.send_message(message.chat.id, 'Запутались в кнопках?\n\n●  Фильм/Сериал--выводит по вашему запросу Фильм/Сериал, что вам нужен!\n●  Cлучайный фильм/сериал--если вам нечего посмотреть, то воспользуйтесь этой кнопкой и ищите то, что вам понравится.\n●  Актер--выводит по вашему запросу Актера/Актриссу.\n●  Случайный Актер--если вы хотите познакомиться с новым Актером/Актриссой, то воспользуйтесь этой кнопкой и ищите фильмы с их участием!')



#												 Премьеры в кинотеатре
@client.message_handler(func=lambda c: c.text == "Премьеры в кинотеатре")
def primers(message):
	# print(cinema_primers_data(CFG.kinomax_link))
	client.send_message(message.chat.id, primers_data)
	


#                      							 РАНДОМНЫЕ АКТЕРЫ
@client.message_handler(func=lambda c: c.text == "Cлучайный актер")
def acrtist(message):
	st_act = []
	for i in range(len(data)):
		st_act.append(data['actors'][i].split(';'))
	set_actors = list(set([x for l in st_act for x in l]))
	act = random.choice(set_actors)
	actor = f"Фильмы, в которых играл(а) {act}\n⬇️⬇️⬇️"
	client.send_message(message.chat.id, actor, parse_mode='html')
	for i in range(len(data)):
		if clear_msg(act) in clear_msg(data['actors'][i]):
			client.send_message(message.chat.id,
								f"Название: {data.loc[i][1].replace(';', ',')}\nРейтинг: {round(data.loc[i][4], 2)}")


@client.message_handler(func=lambda c: c.text == "Актер")
def acrtist__1(message):
	# client.send_sticker(
	# 	message.chat.id, 'CAACAgIAAxkBAAEEYadiTH_B6nbGGJCzxkPXPqbSlieFxgACQQIAAs4XpwuAhLkjXAPfNSME')
	what_actor = 'Введите полное имя актера/актрисы...\n⬇️⬇️⬇️'
	client.send_message(message.chat.id, what_actor, parse_mode='html')


#                                                         РАСПОЗНОВАНИЕ ФИЛЬМОВ

@client.message_handler(content_types=["text"])
def start(message):
	found = False
	kino = Kinopoisk(CFG.KINOPOIS_API_KEY)
	film = kino.search(message.text)

	if film and film['count']:
		found = True
		client.send_message(message.chat.id, 'Выполняется поиск...')
		client.send_message(message.chat.id,
							f"●  Название: [{film['name']}]({film['photo']})\n●  Год: {film['year']}\n●  Страна: {', '.join(film['country'])}\n●  Рейтинг: {film['rating']}\n●  Режиссер: {film['director']}\n●  Актеры: {', '.join(film['actors'])}\n●  Описание: {film['description']}\n●  Кинопоиск: {film['link']}",
							parse_mode='Markdown')
	# print(*film['actors'],sep=', ')
	# print(film)
	else:
		actor = kino.search(message.text, actor=True)
		if actor:
			found = True
			client.send_message(
				message.chat.id, f"●  Имя: [{actor['name']}]({actor['posterUrl']})\n●  Фильмы: {', '.join(actor['films'])}\n●  Кинопоиск: {actor['kinlink']}", parse_mode='Markdown')

	if not found:
		client.send_message(
			message.chat.id, "Я не понял ваш запрос! Попробуйте написать название фильма на английском")


print('start')

if __name__ == '__main__':
    client.polling(none_stop=True)