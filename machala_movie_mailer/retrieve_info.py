import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
from machala_movie_mailer.private_variables import api_key


def get_movies(city):
    city_dict = {'Machala': ["https://cinepass.com.ec/mla/complejos/supercines-machala/hoy/"],
                 'Cuenca': ["https://cinepass.com.ec/cue/complejos/multicines-millenium-plaza/hoy/",
                            "https://cinepass.com.ec/cue/complejos/multicines-mall-del-rio/hoy/"],
                 'Ibarra': ['https://cinepass.com.ec/ira/complejos/starcines/hoy/'],
                 'Riobamba': ['https://cinepass.com.ec/rba/complejos/supercines-riobamba/hoy/'],
                 'La Libertad': ['https://cinepass.com.ec/lta/complejos/supercines-la-peninsula/hoy/'],
                 'Latacunga': ['https://cinepass.com.ec/lga/complejos/malteria-plaza/hoy/'],
                 'Guayaquil': ['https://cinepass.com.ec/gye/complejos/cinemark-malldelsur/hoy/',
                               'https://cinepass.com.ec/gye/complejos/cinemark-citymall/hoy/',
                               'https://cinepass.com.ec/gye/complejos/cinemark-malldelsol/hoy/',
                               'https://cinepass.com.ec/gye/complejos/cinemark-village-plaza/hoy/',
                               'https://cinepass.com.ec/gye/complejos/supercines-el-dorado/hoy/',
                               'https://cinepass.com.ec/gye/complejos/supercines-entrerios/hoy/',
                               'https://cinepass.com.ec/gye/complejos/supercines-losceibos/hoy/',
                               'https://cinepass.com.ec/gye/complejos/supercines-sanmarino/hoy/',
                               'https://cinepass.com.ec/gye/complejos/supercines-sur/hoy/',
                               'https://cinepass.com.ec/gye/complejos/supercines-norte/hoy/'],
                 'Quito': ['https://cinepass.com.ec/uio/complejos/cinemark-paseo-san-francisco/hoy/',
                           'https://cinepass.com.ec/uio/complejos/cinemark-plaza-las-americas/hoy/',
                           'https://cinepass.com.ec/uio/complejos/cineplex/hoy/',
                           'https://cinepass.com.ec/uio/complejos/multicines-cci/hoy/',
                           'https://cinepass.com.ec/uio/complejos/mis-cines/hoy/',
                           'https://cinepass.com.ec/uio/complejos/multicines-condado/hoy/',
                           'https://cinepass.com.ec/uio/complejos/multicines-recreo/hoy/',
                           'https://cinepass.com.ec/uio/complejos/multicines-scala/hoy/',
                           'https://cinepass.com.ec/uio/complejos/supercines-6-de-diciembre/hoy/',
                           'https://cinepass.com.ec/uio/complejos/supercines-quicentrosur/hoy/',
                           'https://cinepass.com.ec/uio/complejos/supercines-sanluis/hoy/']}
    urls = city_dict[city]
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        yield list(soup.findAll('div', {"class": "carteleraItem"})), soup, url


def get_theater_name(_soup, url):
    return _soup.find('div', {"class": "cinecover"}).text.strip(), url


def get_movie_info(movie):
    """
    :param movie: piece of HTML representing a single movie
    :return: a list of dicts containing a movie's name, director, and a link to the trailer
    """
    movie_info = movie.find_next('script', {"type": "application/ld+json"})
    move_info_cleaned = movie_info.text.replace(',}', '}')
    json_data = json.loads(move_info_cleaned, strict=False)
    return {'title': json_data['name'], 'director': json_data['director'], "trailer": json_data['sameAs']}


def get_show_times(movie):
    """
    Get the a showing's language and times
    :param movie: piece of HTML representing a single movie
    :return: a list of dicts containing each showing's language and times
    """
    show_types = movie.findAll('table', {"id": "horariotabla"})
    showings = []
    for show in show_types:
        show_times = [json.loads(showing.text.replace(',}', '}'))['doorTime'] for showing in
                      show.findAll('script', {"type": "application/ld+json"})]
        showings.append({'Language': (show.p.text).replace("Subtitulada", "English"),
                         'Times': ", ".join(show_times)})
    return showings


def deal_with_year_error(api_key, title):
    """
    Helper function for get_ratings - deals with older movies
    :param api_key: api key for accessing OMDB
    :param title: a string movie title
    :return: a dictionary with the imdb and rt
    scores for the film OR None if that can't be found
    """
    years = 1
    for _ in range(5):
        current_year = (datetime.now() - relativedelta(years=years)).year
        url_imdb = "http://www.omdbapi.com/?apikey={}&t={}&y={}".format(api_key, title, current_year)
        raw_content = requests.get(url_imdb).content
        raw_content = str(raw_content.decode('utf8'))
        json_content = json.loads(raw_content)
        if json_content.get("Error"):
            years += 1
        else:
            return json_content
    if json_content.get("Error"):
        return None


def get_ratings(title, api_key=api_key):
    """
    Get the movie title's ratings from imdb
    :param title: a string movie title
    :param api_key: api key for accessing OMDB
    :return: a dictionary with the imdb and rt scores for the film
    """
    current_year = datetime.now().year
    url_imdb = 'http://www.omdbapi.com/?apikey={}&t={}&y={}'.format(api_key, title, current_year)
    raw_content = requests.get(url_imdb).content
    raw_content = str(raw_content.decode('utf8'))
    json_content = json.loads(raw_content, strict=False)
    if json_content.get("Error"):
        json_content = deal_with_year_error(api_key, title)
        if not json_content:
            return {'imdb': "*No IMDB Rating Available*", 'rt': "*No RT Score Available*"}
    try:
        rotten_tomatoes_rating = json_content['Ratings'][1]['Value']
    except IndexError:
        rotten_tomatoes_rating = "*No Score Available*"
    current_year = (datetime.now() - relativedelta(years=1)).year
    # imdb_rating = json_content['imdbRating']
    # Get the imdb score
    imdb_id = json_content['imdbID']
    imdb_url = 'https://www.imdb.com/title/{}/'.format(imdb_id)
    response = requests.get(imdb_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    imdb_rating = soup.find('span', {"itemprop": "ratingValue"}).text
    #
    return {'imdb': imdb_rating, 'rt': rotten_tomatoes_rating}
