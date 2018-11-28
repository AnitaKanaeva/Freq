
# coding: utf-8


import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import numpy
from scipy.misc import imread
import matplotlib.pyplot as plt 
import random 
from wordcloud import WordCloud


url = 'https://news.google.com/search?q=Russia&hl=en-US&gl=US&ceid=US:en'


def get_html(url):
    """вернуть html-код входного url"""
    try:
        r = requests.get(url)
        return r.text
    except Exception as err:
        print('error in function get_html - ', err)
        raise


def get_article_url(html):
    """получить все ссылки на статьи"""
    try:
        soup = BeautifulSoup(html, 'lxml')
        total_links = []
        a_url = 'https://news.google.com'
        links = soup.find_all('a', class_='VDXfz')
        for link in links:
            l = link.get('href')
            l = l[1:]  # нулевой элемент - лишняя точка, для подстановки в ссылку ее надо удалять
            l1 = a_url + l
            total_links.append(l1)
        return total_links
    except Exception as err:
        print('error in function get_article_url - ', err)
        raise


def get_article_data(b_html):
    """получить содержимое статьи
       
       параметры:
       b_html - html-код страницы
       
       вывод:
       art_data_c - список со словами из статьи
    """
    try:
        art_data_raw = []  # тут будет хранится загрязненный текст
        art_data = []
        b_soup = BeautifulSoup(b_html, 'lxml')
        b_soup = b_soup.find_all('p')
        for bs in b_soup:
            bs = bs.text
            art_data_raw.append(bs.lower())
        for ad in art_data_raw:
            #  удаляем грязь вроде символов перевода строки
            s = ad
            s = re.sub('\\n+', '', s)
            s = re.sub("\\'s+", "", s)
            s = re.sub('\.+', '', s)
            s = re.sub(',+', '', s)
            s = re.sub('\?+', '', s)
            art_data.append(s)
        art_data_str = ''.join(art_data)  # если этого не сделать, split() по буквам разобьет
        art_data_c = art_data_str.split()
        return art_data_c
    except Exception as err:
        print('error in function get_article_data - ', err)
        raise


def erase_conjunctions(dict_article):
    """удалить союзы, местоимения и прочие слова, не несущие большого смысла
       
       параметры:
       dict_article - словарь, содержащий союзы и т.д.
       
       вывод:
       dict_article - тот же самый словаь, но чистенький
    """
    stop_words = ['the', 'to', 'if', 'of', 'a', 'in', 'that', 'is', 'for',
                  'with', 'from', 'has', 'by', 'it', 'was', 'on', 'as', 'have',
                  'an', 'are', 'at', 'be', 'not', 'he', 'mr', 'had', 'this',
                  'its', 'been', 'or', 'who', 'his', 'they', 'about', 'were', 'their',
                  '-', 'but', 'which', 'will', 'also', 'more', 'would', 'other', 'out',
                  'after', 'could', 'one', 'our', 'into', 'up', 'than', 'what', 'can',
                  '=', 'over', 'any', 'we', 'no', 'you', 'some', 'when', 'there',
                  ':', 'It', 'only', 'like', 'your', 'between', 'now', 'do', 'how', 'them',
                  'even', 'most', 'such', 'so', 'then', 'her', 'under', 'i', '||', 'and', 'two',
                  'these', '—', 'she', 'ms', '{', '}', 'while', '+', 'through', 'just', 'before']
    try:
        for stop_word in stop_words:
            del dict_article[stop_word]  # я понимаю, что исходный словарь мутирует, но никому от этого худо не будет
        return dict_article
    except KeyError as err:
        print('some key does not exists in func erase_conjunctions - ', err)
        raise


def get_dict_article(article_links):
    """получить словарь со словами где ключ - слово (str), значение - частота (int)"""
    try:
        articles = []
        dict_article = {}
        for a_link in article_links:
            a_html = get_html(a_link)
            art_art = get_article_data(a_html)
            articles = articles + art_art
        dict_article = Counter(articles)
        dict_article = erase_conjunctions(dict_article)
        return dict_article
    except Exception as err:
        print('error in function get_dict_article - ', err)
        raise


def get_sorted_article_string(dict_article):
    """получить строку, состоящую из 50 самых частых слов,
       где каждое слово повторяется n раз, где n - его частота
       
       параметры:
       dict_article - словарь из пар слово:частота
       
       вывод:
       строка из слов, разделенных пробелом, где каждое слово продублировано
       в соответствии с его частотой
    """
    try:
        da_sorted_by_value = []
        da_sorted_by_value = sorted(dict_article.items(), key=lambda kv: kv[1])
        da_sorted_by_value = da_sorted_by_value[-50:]  # самые частые в конце, поэтому берем 50 последних
        da_string = ''
        for da_sorted_unit in da_sorted_by_value:
            da_string += (da_sorted_unit[0] + ' ')*da_sorted_unit[1]  # в кортеже 0 - это само словоб 1 - его частота
        return da_string
    except Exception as err:
        print('I can not believe - something goes wrong with... sorting?', err)
        raise


def get_wordcloud(text_str):
    """построить облако тегов
       
       параметры:
       text_str - обязательно строка
    """
    try:
        wordcloud = WordCloud(background_color="white", relative_scaling=1.0).generate(text_str)
        plt.imshow(wordcloud) 
        plt.axis("off") 
        plt.show()
    except Exception as err:
        print('error in function get_wordcloud - ', err)
        raise


def main():
    g_html = get_html(url)
    article_links = get_article_url(g_html)
    dict_article = get_dict_article(article_links)
    da_string = get_sorted_article_string(dict_article)
    get_wordcloud(da_string)


if __name__ == '__main__':
    main()
