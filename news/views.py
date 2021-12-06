from django.shortcuts import render,redirect
from django.http import HttpResponse
from newsapi import NewsApiClient
from datetime import date, timedelta
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout, login
from .models import Bookmark

import json
consumer_key= 'NUkOrdTkVSd5AKqKetajGWVaO' #API_KEY(Twitter)
consumer_secret= 'ZooIHc9DrgVTuTU96XDYGvZF54wavk3aNKWd3fyZLzIGxGgbF6' 
access_token= '877839641344430080-knj2CUZn4LbZ1O57mgJEbRQ1fVdUODP' 
access_token_secret= 'mv34QLXYsUab0qgvXOHQWV5dp7vfPuXwFDhcYkFrDl5JJ' 
APIKEY="141f860e070f4dc4a86c383f9d5604fc"
import urllib.parse
import tweepy as tw

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

newsapi = NewsApiClient(api_key=APIKEY) #newsAPI
current_date = date.today().isoformat()   
days_before = (date.today()-timedelta(days=25)).isoformat()

def clean_input(tag):
    tag = tag.replace(" ", "")
    if tag.startswith('#'):
        return tag[1:].lower()
    else:
        return tag.lower()

def return_all_hashtags(tweets, tag):
    all_hashtags = []
    for tweet in tweets:
        for word in tweet.split():
            if word.startswith('#') and word.lower() != '#' + tag.lower():
                all_hashtags.append(word.lower())
    return all_hashtags

def get_hashtags(tag):
    search_tag = clean_input(tag)
    tweets = tw.Cursor(api.search,q='#' + search_tag,lang="en").items(50)
    tweets_list = []
    for tweet in tweets:
        tweets_list.append(tweet.text)
    all_tags = return_all_hashtags(tweets_list, tag)
    frequency = {}
    for item in set(all_tags):
        frequency[item] = all_tags.count(item)
    return {k: v for k, v in sorted(frequency.items(), key=lambda item: item[1], reverse=True)}

#######.............................................................
# print(current_date, days_before)
# all_indian_sources=newsapi.get_sources(language='en',country='in')
# all_indian_sources=all_indian_sources['sources']
# print(all_indian_sources)

def index(request):
    page_no = int(request.GET.get('page_no', 1))
    topheadlines=newsapi.get_top_headlines(sources='google-news-in,the-hindu,the-times-of-india,espn',language='en',page_size=6, page=int(page_no))
    articles=topheadlines['articles']
    # print(articles)
    desc = []
    news = []
    img = []
    auth = []
    pubat = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]
        url.append(myarticles['url'])
        auth.append(myarticles['author'])
        time = myarticles['publishedAt']
        temp= time[8:10]+'-'+time[5:7]+'-'+time[:4] + " @ " + time[11:19]
        pubat.append(temp)
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])

    mylist = zip(news, desc, img, auth, pubat, url)

    return render(request, 'index.html', {"mylist": mylist, "page_no": page_no})

def search(request):
    if request.method == 'GET':
        query=request.GET.get('search_for',None)

        if query is None:
            return redirect('')
        else:
            page_no = int(request.GET.get('page_no', 1))
            tag =str(query)
            particular_topic = newsapi.get_everything(qintitle=query,from_param=days_before,to=current_date,sources='google-news-in,the-hindu,the-times-of-india,espn',language='en',sort_by='publishedAt',page_size=6, page=page_no)
            articles=particular_topic['articles']
            desc = [] 
            news = [] 
            img = [] 
            auth = [] 
            pubat = [] 
            url = [] 
            for i in range(len(articles)):
                myarticles = articles[i]
                url.append(myarticles['url'])
                auth.append(myarticles['author'])
                time = myarticles['publishedAt']
                temp= time[8:10]+'-'+time[5:7]+'-'+time[:4] + " @ " + time[11:19]
                pubat.append(temp)
                news.append(myarticles['title'])
                desc.append(myarticles['description'])
                img.append(myarticles['urlToImage'])

            mylist = zip(news, desc, img, auth, pubat, url)
            all_tags = get_hashtags(tag)
            return render(request, 'search.html', {'mylist':mylist , 'query':query, 'data':all_tags, 'page_no': page_no},)

def sports(request):
    page_no = int(request.GET.get('page_no', 1))
    topheadlines_sports=newsapi.get_top_headlines(category='sports',country='in',language='en',page_size=6, page=page_no)
    articles=topheadlines_sports['articles']
    # print(len(articles))
    desc = []
    news = []
    img = []
    auth = []
    pubat = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]
        url.append(myarticles['url'])
        auth.append(myarticles['author'])
        time = myarticles['publishedAt']
        temp= time[8:10]+'-'+time[5:7]+'-'+time[:4] + " @ " + time[11:19]
        pubat.append(temp)
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])    

    mylist = zip(news, desc, img, auth, pubat, url)
    return render(request, 'sports.html', {"mylist": mylist, 'page_no': page_no,})

def about(request):
    return render(request, 'about.html')

def business(request):
    page_no = int(request.GET.get('page_no', 1))
    topheadlines_sports=newsapi.get_top_headlines(category='business',country='in',language='en',page_size=6, page=page_no)
    articles=topheadlines_sports['articles']
    # print(len(articles))
    desc = []
    news = []
    img = []
    auth = []
    pubat = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]
        url.append(myarticles['url'])
        auth.append(myarticles['author'])
        time = myarticles['publishedAt']
        temp= time[8:10]+'-'+time[5:7]+'-'+time[:4] + " @ " + time[11:19]
        pubat.append(temp)
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])    

    mylist = zip(news, desc, img, auth, pubat, url)
    return render(request, 'business.html', {"mylist": mylist, 'page_no': page_no,})

def entertainment(request):
    page_no = int(request.GET.get('page_no', 1))
    topheadlines_sports=newsapi.get_top_headlines(category='entertainment',country='in',language='en',page_size=6, page=page_no)
    articles=topheadlines_sports['articles']
    # print(len(articles))
    desc = []
    news = []
    img = []
    auth = []
    pubat = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]
        url.append(myarticles['url'])
        auth.append(myarticles['author'])
        time = myarticles['publishedAt']
        temp= time[8:10]+'-'+time[5:7]+'-'+time[:4] + " @ " + time[11:19]
        pubat.append(temp)
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])    

    mylist = zip(news, desc, img, auth, pubat, url)
    return render(request, 'entertainment.html', {"mylist": mylist, 'page_no': page_no,})

def general(request):
    page_no = int(request.GET.get('page_no', 1))
    topheadlines_sports=newsapi.get_top_headlines(category='general',country='in',language='en',page_size=6, page=page_no)
    articles=topheadlines_sports['articles']
    # print(len(articles))
    desc = []
    news = []
    img = []
    auth = []
    pubat = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]
        url.append(myarticles['url'])
        auth.append(myarticles['author'])
        time = myarticles['publishedAt']
        temp= time[8:10]+'-'+time[5:7]+'-'+time[:4] + " @ " + time[11:19]
        pubat.append(temp)
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])    

    mylist = zip(news, desc, img, auth, pubat, url)
    return render(request, 'general.html', {"mylist": mylist, 'page_no': page_no,})

def globoal(request):
    page_no = int(request.GET.get('page_no', 1))
    topheadlines_sports=newsapi.get_top_headlines(category='global',language='en',page_size=6, page=page_no)
    articles=topheadlines_sports['articles']
    # print(len(articles))
    desc = []
    news = []
    img = []
    auth = []
    pubat = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]
        url.append(myarticles['url'])
        auth.append(myarticles['author'])
        time = myarticles['publishedAt']
        temp= time[8:10]+'-'+time[5:7]+'-'+time[:4] + " @ " + time[11:19]
        pubat.append(temp)
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])    

    mylist = zip(news, desc, img, auth, pubat, url)
    return render(request, 'global.html', {"mylist": mylist, 'page_no': page_no,})

def health(request):
    page_no = int(request.GET.get('page_no', 1))
    topheadlines_sports=newsapi.get_top_headlines(category='health',language='en',page_size=6, page=page_no)
    articles=topheadlines_sports['articles']
    # print(len(articles))
    desc = []
    news = []
    img = []
    auth = []
    pubat = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]
        url.append(myarticles['url'])
        auth.append(myarticles['author'])
        time = myarticles['publishedAt']
        temp= time[8:10]+'-'+time[5:7]+'-'+time[:4] + " @ " + time[11:19]
        pubat.append(temp)
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])    

    mylist = zip(news, desc, img, auth, pubat, url)
    return render(request, 'health.html', {"mylist": mylist, 'page_no': page_no,})

def science(request):
    page_no = int(request.GET.get('page_no', 1))
    topheadlines_sports=newsapi.get_top_headlines(category='science',language='en',page_size=6, page=page_no)
    articles=topheadlines_sports['articles']
    # print(len(articles))
    desc = []
    news = []
    img = []
    auth = []
    pubat = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]
        url.append(myarticles['url'])
        auth.append(myarticles['author'])
        time = myarticles['publishedAt']
        temp= time[8:10]+'-'+time[5:7]+'-'+time[:4] + " @ " + time[11:19]
        pubat.append(temp)
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])    

    mylist = zip(news, desc, img, auth, pubat, url)
    return render(request, 'science.html', {"mylist": mylist, 'page_no': page_no,})

def technology(request):
    page_no = int(request.GET.get('page_no', 1))
    topheadlines_sports=newsapi.get_top_headlines(category='technology',language='en',page_size=6, page=page_no)
    articles=topheadlines_sports['articles']
    # print(len(articles))
    desc = []
    news = []
    img = []
    auth = []
    pubat = []
    url = []

    for i in range(len(articles)):
        myarticles = articles[i]
        url.append(myarticles['url'])
        auth.append(myarticles['author'])
        time = myarticles['publishedAt']
        temp= time[8:10]+'-'+time[5:7]+'-'+time[:4] + " @ " + time[11:19]
        pubat.append(temp)
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])    

    mylist = zip(news, desc, img, auth, pubat, url)
    return render(request, 'technology.html', {"mylist": mylist, 'page_no': page_no,})

def signup(request):
    if request.method=='POST':
        if User.objects.filter(username=request.POST['username']).exists() or User.objects.filter(username=request.POST['username']).exists():
            print("User already exist")
            return redirect('/login')
        else:
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            user.save()
            print("User signup successful")
            return redirect('/')

    elif request.method=='GET':
        return render(request, 'signup.html')

def login_user(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            print("Login Success")
            return redirect('/')
        else:
            print("Login Failed")
            return redirect('/login/')
    elif request.method=='GET':
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def bookmark(request):
    if request.method=='GET':
        print("===================================== ", request.GET['url'], " ========================================")
        bmk = Bookmark(username=request.user.username, url=request.GET['url'])
        bmk.save()
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return redirect('/')

def show_bookmarks(request):
    if request.method=='GET':
        bmks = Bookmark.objects.filter(username=request.user.username)
        arr = []
        for el in bmks:
            arr.append(el.url)
        return render(request, "bookmarks.html",{"urls" : arr})




