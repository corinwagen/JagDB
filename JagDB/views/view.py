from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from question_categorizer.models import Tossup, Bonus, AuthUser, Subject, Tournament
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import operator
import warnings 
import pickle

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
    display_num = int(request.GET.get("num", 50))
    page_num    = int(request.GET.get("page", 1))
    packet_id   = request.GET.get("packet_id", '')

    if page_num < 1:
        page_num = 1 
    min_question = (page_num - 1) * display_num
    max_question = page_num * display_num

    prev_page = page_num - 1
    if prev_page < 1:
        prev_page = 1
 
    if (quest_type == "tossup"): 
        tossups = Tossup.objects.filter(question__icontains=question, answer__icontains=answer, packet__tournament__difficulty__range=(min_diff, max_diff))
        if packet_id : 
            tossups = tossups.filter(packet_id=packet_id)
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

        for tossup in tossups[min_question:max_question]:
            questions.append(tossup.objectify())

    elif (quest_type == "bonus"): 
        bonuses = Bonus.objects.filter(packet__tournament__difficulty__range=(min_diff, max_diff))
        if packet_id : 
            bonuses = bonuses.filter(packet_id=packet_id)
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
        
        for bonus in bonuses[min_question:max_question]:
            questions.append(bonus.objectify())

    subject_list = Subject.objects.all()
    tournament_list = Tournament.objects.order_by("-year")

    params = "question={}&answer={}&min_diff={}&max_diff={}&flagged={}&type={}&num={}&page={}&order_by={}".format(question, answer, min_diff, max_diff, flagged, quest_type, display_num, page_num, order_by,)
    for subject in subjects:
        params = params + "&subjects=" + subject
    for tournament in tournaments:
        params = params + "&tournaments=" + tournament
  
    context["questions"]        = questions
    context["subjects"]         = subjects
    context["tournaments"]      = tournaments
    context["subject_list"]     = subject_list
    context["tournament_list"]  = tournament_list
    context["question"]         = question
    context["answer"]           = answer 
    context["min_diff"]         = min_diff
    context["max_diff"]         = max_diff
    context["order_by"]         = order_by
    context["flagged"]          = flagged
    context["type"]             = quest_type 
    context["num"]              = display_num
    context["page"]             = page_num
    context["prev_page"]        = prev_page
    context["next_page"]        = page_num + 1
    context["params"]           = params
    return render(request, 'view_questions.html', context)

