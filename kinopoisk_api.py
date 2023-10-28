import requests
from urllib.parse import urlencode, quote_plus


class Kinopoisk:
    def __init__(self, api_key):
        self.keywords = None
        self.headers = {'accept': 'application/json', 'X-API-KEY': api_key}
        self.host = 'https://kinopoiskapiunofficial.tech'
        self.path = None
        self.method = None
        self.params = {}

    def search(self, text, film=True, actor=False):
        if actor:
            return self.search_actor(text)
        elif film:
            return self.search_film(text)

    def search_actor(self, text):
        person = self.get_person(text)

        if person and len(person['items']):
            url = {}
            url['path'] = '/api/v1/'
            url['method'] = 'staff/' + str(person['items'][0]['kinopoiskId'])
            url['params'] = None
            actor = self._request(url)
            # print(actor)
            films = []
            for i in actor.get('films')[0:5]:
                if i.get('nameRu'):
                    films.append(i.get('nameRu') +
                                 " (" + str(i.get('rating', '-')) + ")")
                # films.append(i['nameRu'])

            obj = {
                'id': str(actor.get('personId', '-')),
                'name': str(actor.get('nameRu', '-')),
                'films': films,
                'posterUrl': str(actor.get('posterUrl', '-')),
                'kinlink': str(actor.get('webUrl', '-'))
            }
        else:
            obj = None
        return obj

    def search_film(self, text):
        film = self.get_film(text)
        count = self.get_film_count(text)
        # print(count)
        if film:
            staff = self.get_staff(film['filmId'])
            director = self.get_director(staff)
            actors = self.get_actors(staff)
            try:
                obj = {
                    'count': count,
                    'id': film['filmId'],
                    'name': film.get('nameRu', film['nameEn']),
                    'year': film['year'],
                    'country': self.get_country(film['countries']),
                    'rating': film.get('rating'),
                    'director': director,
                    'actors': actors,
                    'description': film.get('description'),
                    'link': 'https://www.kinopoisk.ru/film/' + str(film['filmId']),
                    'photo': film['posterUrl']
                }
            except:
                obj = None
        else:
            obj = None
        return obj

    def _request(self, url):
        if url['params']:
            url_str = self.host + url['path'] + \
                url['method'] + "?" + urlencode(url['params'])
        else:
            url_str = self.host + url['path'] + url['method']

        res = requests.get(url_str, headers=self.headers)
        return res.json()

    def get_film(self, film_name):
        url = {}
        url['path'] = '/api/v2.1/films/'
        url['method'] = 'search-by-keyword'
        url['params'] = {'keyword': film_name, 'page': '1'}
        result = self._request(url)
        return result['films'][0] if len(result['films']) else None

    def get_film_count(self, film_name):
        url = {}
        url['path'] = '/api/v2.2/'
        url['method'] = 'films'
        url['params'] = {'order': 'RATING', 'type': 'ALL', 'ratingFrom': '0',
                         'ratingTo': '10', 'yearFrom': '1000', 'yearTo': '3000', 'keyword': film_name}
        result = self._request(url)
        #print(result)
        return len(result['items'])

    def get_staff(self, film_id):
        url = {}
        url['path'] = '/api/v1/'
        url['method'] = 'staff'
        url['params'] = {'filmId': int(film_id)}
        result = self._request(url)
        return result if result else None

    def get_person(self, name):
        url = {}
        url['path'] = '/api/v1/'
        url['method'] = 'persons'
        url['params'] = {'name': name}
        result = self._request(url)
        return result if result else None

    def get_country(self, countries):
        lst_country = []
        for c in countries:
            lst_country.append(c.get('country'))
        return lst_country if lst_country else None

    def get_director(self, staff):
        director = None
        for s in staff:
            if s['professionKey'] == 'DIRECTOR':
                director = s.get('nameRu')
                break
        return director if director else None

    def get_actors(self, staff):
        actors = []
        cnt = 6
        for s in staff:
            if s['professionKey'] == 'ACTOR' and cnt:
                actors.append(s.get('nameRu'))
                cnt -= 1
        return actors if actors else None
