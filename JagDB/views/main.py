from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from question_categorizer.models import Tossup, Bonus, AuthUser, Subject, Tournament
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Min, Sum, Avg, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
import datetime
import operator
import warnings 
import pickle


@login_required
def home(request):
    context = {}
    subjects = Subject.objects.annotate(Count('tossup_subject', distinct=True)).annotate(Count('bonus_subject', distinct=True)) 
    d3_data = []
    for row in subjects:
        label = row.subject
        value = int(row.tossup_subject__count) + int(row.bonus_subject__count)
        d3_data.append({'label': label, 'value': value })
    return render(request, 'home.html', context)

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
@permission_required('polls.can_add_and_flag')
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
@permission_required('polls.can_add_and_flag')
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


@login_required
def export(request):
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

        for tossup in tossups:
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

        for bonus in bonuses:
            questions.append(bonus.objectify())

    context["questions"] = questions 
    return render(request, 'export.html', context) 

@login_required 
@permission_required('polls.can_edit_and_delete')
def edit_question(request, type, question_id, params):
    context = {}
    question = ''
    if type == "tossup":
        question = Tossup.objects.get(id=question_id)
        question.question       = request.POST.get("question_text", question.question)
        question.answer         = request.POST.get("answer", question.answer)
        question.packet_id      = request.POST.get("packet_id", question.packet.id)
        question.subject_id     = request.POST.get("subject_id", question.subject_id)
        question.updated_by_id  = request.user.id
        question.updated_at     = datetime.datetime.now()
        question.save()
    elif type == "bonus":
        question = Bonus.objects.get(id=question_id)
        question.leadin         = request.POST.get("leadin", question.leadin)
        question.part1          = request.POST.get("part1", question.part1)
        question.part2          = request.POST.get("part2", question.part2)
        question.part3          = request.POST.get("part3", question.part3)
        question.answer1        = request.POST.get("answer1", question.answer1)
        question.answer2        = request.POST.get("answer2", question.answer2)
        question.answer3        = request.POST.get("answer3", question.answer3)
        question.packet_id      = request.POST.get("packet_id", question.packet.id)
        question.subject_id     = request.POST.get("subject_id", question.subject_id)
        question.updated_by_id  = request.user.id
        question.updated_at     = datetime.datetime.now()
        question.save()

    context["view_url"] = "{}?{}".format(reverse('view_questions'), params); 
    context["question"] = question
    context["subject_list"] = Subject.objects.all()
    return render(request, 'edit_question.html', context)    

@login_required
@permission_required('polls.can_edit_and_delete')
def delete_question(request):
    if request.method == 'GET':
        id=int(request.GET.get('id', ''))
        type=request.GET.get('type', '')
        if (type == "tossup"): 
            question = Tossup.objects.get(id=id)
        else:
            question = Bonus.objects.get(id=id)
        success = 1
        question.delete()
       
        return JsonResponse({'success': success,}) 
    else: 
        return JsonResponse({'success': 0})


@login_required 
def get_subject_data(request):
    subjects = Subject.objects.annotate(Count('tossup_subject', distinct=True)).annotate(Count('bonus_subject', distinct=True)) 
    d3_data = []
    for row in subjects:
        label = row.subject
        value = int(row.tossup_subject__count) + int(row.bonus_subject__count)
        d3_data.append({'label': label, 'value': value })
    return JsonResponse({ 'success': 1, 'd3_data': d3_data });
