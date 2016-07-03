from django.http import HttpResponse
from django.shortcuts import render
from question_categorizer.models import Tossup, Bonus, AuthUser
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def home(request):
    context = {}
#    if request.session['user']:
#        context.user = request.session['user']
#    else:
    return render(request, 'home.html', context)

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

@login_required
def user_view(request, user_id):
    context = {}
    user = AuthUser.objects.get(id=user_id)
    if request.POST:
        user.username   = request.POST.get("username", user.username)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name  = request.POST.get("last_name", user.last_name)
        user.email      = request.POST.get("email", user.email)
        user.save()

    request.user.refresh_from_db()

    t_added = Tossup.objects.filter(created_by__id = user_id).count()
    b_added = Bonus.objects.filter(created_by__id = user_id).count()
    a_added = t_added + b_added
  
    t_count = Tossup.objects.count()
    b_count = Bonus.objects.count()
    a_count = t_count + b_count
   
    t_percent = "{percent:.2%}".format(percent=(t_added / t_count)) 
    b_percent = "{percent:.2%}".format(percent=(b_added / b_count)) 
    a_percent = "{percent:.2%}".format(percent=(a_added / a_count))

    stats = []
    stats.append({"name": "questions", "num": a_added, "percent": a_percent})
    stats.append({"name": "tossups", "num": t_added, "percent": t_percent})
    stats.append({"name": "bonuses", "num": b_added, "percent": b_percent})

    context["stats"] = stats

    return render(request, 'user_view.html', context)
