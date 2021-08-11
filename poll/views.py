# from django.http.response import HttpResponse
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic 
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name="poll/index.html"
    context_object_name  = 'latest_questions'

    def get_queryset(self):
        ''' 
        Get 5 latest questions which do not have pub date in future
        '''
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "poll/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "poll/result.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])    
    except (KeyError, Choice.DoesNotExist):
        #If error occurs, Redisplay form with error message
        return render(request, "poll/detail.html", {"question": question, "error_message": "You dint select choice" })
    
    else:
        #CAUTION: race condition
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

