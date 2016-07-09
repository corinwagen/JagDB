from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from question_categorizer.models import Tossup, Bonus, AuthUser, Subject, Tournament
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
import operator
import warnings 
import pickle

@login_required
def home(request):
    context = {}
    return render(request, 'home.html', context)

@login_required
def view_questions (request):
    context     = {}
    questions   = []
    question    = request.GET.get('question', '')  
    answer      = request.GET.get('answer', '')
    min_diff    = int(request.GET.get('min_diff', 1))
    max_diff    = int(request.GET.get('max_diff', 10))
    subjects    = request.GET.getlist('subjects', '')
    tournaments = request.GET.getlist('tournaments', '')
    flagged     = request.GET.get("flagged", '')
    quest_type  = request.GET.get("type", 'tossup')
    order_by    = request.GET.get('order_by', 'packet__tournament__difficulty');
    display_num = int(request.GET.get("num", '50'))
  
    if (quest_type == "tossup"): 
        tossups = Tossup.objects.filter(question__icontains=question, answer__icontains=answer, packet__tournament__difficulty__range=(min_diff, max_diff))
        tossups = tossups.order_by(order_by)
        if flagged: 
            tossups=tossups.filter(flagged=flagged) 
    
        if subjects : 
            subject_list = []
            for subject_id in subjects:
                subject_list.append(Q(subject__id=subject_id))
                
            tossups = tossups.filter(reduce(operator.or_, subject_list))
        
        if tournaments: 
            tournament_list = []
            for tournament_id in tournaments:
                tournament_list.append(Q(packet__tournament__id=tournament_id))
            
            tossups = tossups.filter(reduce(operator.or_, tournament_list))
        
        for tossup in tossups[:display_num]:
            questions.append(tossup.objectify())

    elif (quest_type == "bonus"): 
        bonuses = Bonus.objects.filter(packet__tournament__difficulty__range=(min_diff, max_diff))
        question_text_list = []
        for field in ["leadin", "part1", "part2", "part3"]:
           question_text_list.append(Q(**{field + "__icontains": question})) 
        bonuses = bonuses.filter(reduce(operator.or_, question_text_list))
        answer_text_list = []
        for field in ["answer1", "answer2", "answer3"]:
           answer_text_list.append(Q(**{field + "__icontains": answer})) 
        bonuses = bonuses.filter(reduce(operator.or_, answer_text_list))
        if flagged: 
            bonuses=bonuses.filter(flagged=flagged) 
    
        if subjects : 
            subject_list = []
            for subject_id in subjects:
                subject_list.append(Q(subject__id=subject_id))
                
            bonuses = bonuses.filter(reduce(operator.or_, subject_list))
        
        if tournaments: 
            tournament_list = []
            for tournament_id in tournaments:
                tournament_list.append(Q(packet__tournament__id=tournament_id))
            
            bonuses = bonuses.filter(reduce(operator.or_, tournament_list))
            
        for bonus in bonuses[:display_num]:
            questions.append(bonus.objectify())

    subject_list = Subject.objects.all()
    tournament_list = Tournament.objects.order_by("-year")
   
    context["questions"]        = questions
    context["subjects"]         = subjects
    context["tournaments"]      = tournaments
    context["subject_list"]     = subject_list
    context["tournament_list"]  = tournament_list
    context["question"]         = question
    context["answer"]           = answer 
    context["min_diff"]         = min_diff
    context["max_diff"]         = max_diff
    context["flagged"]          = flagged
    context["type"]             = quest_type 
    context["order_by"]         = order_by
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


@login_required
def flag_question(request):
    if request.method == 'GET':
        id=int(request.GET.get('id', ''))
        type=request.GET.get('type', '')
        if (type == "tossup"): 
            question = Tossup.objects.get(id=id)
        else:
            question = Bonus.objects.get(id=id)
        success = 1
        question.flag_question()
       
        return JsonResponse({'success': success,}) 
    else: 
        return JsonResponse({'success': 0})

@login_required
def unflag_question(request):
    if request.method == 'GET':
        id=int(request.GET.get('id', ''))
        type=request.GET.get('type', '')
        if (type == "tossup"): 
            question = Tossup.objects.get(id=id)
        else:
            question = Bonus.objects.get(id=id)
        success = 1
        question.unflag_question()
       
        return JsonResponse({'success': success,}) 
    else: 
        return JsonResponse({'success': 0})
