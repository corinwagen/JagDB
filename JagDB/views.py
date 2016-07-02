from django.http import HttpResponse
from django.shortcuts import render
from question_categorizer.models import Tossup, Bonus
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def home(request):
    context = {}
#    if request.session['user']:
#        context.user = request.session['user']
#    else:
    user = {'name': 'ari'}
    context['user'] = user
    return render(request, 'home.html', context)

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/home/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")

@login_required
def view_questions (request):
    context = {}
    questions = []
    question = request.GET.get('question', '')  
    answer = request.GET.get('answer', '')
    min_diff = request.GET.get('min_diff', 1)
    max_diff = request.GET.get('max_diff', 10)
    
    tossups = Tossup.objects.filter(question__icontains=question, answer__icontains=answer, packet__tournament__difficulty__range=(min_diff, max_diff))
#    bonuses = Bonus.objects.filter(question__icontains=question, answer__icontains=answer, packet__tournament__difficulty__range=(min_diff, max_diff))
    
    for tossup in tossups[:50]:
        tossup_text = "{} <strong> {} </strong>".format(tossup.question.encode("utf-8"), tossup.answer.encode("utf-8"))
        tossup_dict = {"text": tossup_text.decode('utf-8'), "category": tossup.subject.subject}
        questions.append(tossup_dict)

    context["questions"] = questions
    context["question"] = question
    context["answer"] = answer 
    context["min_diff"] = min_diff
    context["max_diff"] = max_diff
    return render(request, 'view_questions.html', context)

@login_required
def add_questions (request): 
    context = {}
    return render(request, 'add_questions.html', context)
