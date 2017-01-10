from django.shortcuts import render, redirect

from django.urls import reverse

from django.http import HttpResponse, Http404, HttpResponseRedirect

from .models import Tweet, Target

from .forms import HandleForm

from django.conf import settings


# Create your views here.


def index(request):


	return render(request, 'twittering/index.html')



def target(request):
	target_user_list = Target.objects.order_by('-target_name')[:5]
	context = {'target_user_list': target_user_list}
	return render(request, 'twittering/target.html', context)

# SORT OF WORKS??
# def tweeting(request):
# 	latest_tweet_list = Tweet.objects.order_by('-tweet_date')[:5]
# 	context = {'lastest_tweet_list': latest_tweet_list,}
# 	return render(request, 'twittering/tweeting.html', context)

def tweeting(request):

	if request.method == 'POST':
	    # create a form instance and populate it with data from the request:
		form = HandleForm(request.POST)

		if form.is_valid():

			target_handle = form.cleaned_data['target_handle']
			number_of_tweets = form.cleaned_data['number_of_tweets']
			
			rawtweepy = settings.AUTHORIZED_USER.user_timeline(screen_name=target_handle, count=number_of_tweets)

			tweets = list(map(lambda t:t.text, rawtweepy))

			context = {'target_handle': target_handle, 'tweets': tweets}

# if a GET (or any other method) we'll create a blank form
	else:
		form = HandleForm()


	
	return render(request, 'twittering/tweeting.html', context)




# def detail(request, tweet_id):
# 	try:
# 		tweet = Tweet.objects.get(pk=tweet_id)
# 	except Tweet.DoesNotExist:
# 		raise Http404("No such tweet!")
# 	else:
# 		return render(request, 'twittering/detail.html', {'tweet': tweet}) 


def detail(request, target_id):
	try:
		target = Target.objects.get(pk=target_id)
	except Target.DoesNotExist:
		raise Http404("No such target!")
	else:
		return render(request, 'twittering/detail.html', {'target': target}) 
