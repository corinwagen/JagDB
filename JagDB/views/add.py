from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from question_categorizer.models import Tossup, Bonus, AuthUser, Subject, Tournament, Packet
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
import datetime
import operator
import warnings 
import pickle
import re

@login_required
@permission_required('polls.can_add_and_flag')
def add_questions (request): 
    context = {}
    tournament_list = Tournament.objects.order_by("-year")
    context['tournament_list'] = tournament_list
    return render(request, 'add_questions.html', context)

@login_required
@permission_required('polls.can_add_and_flag')
def process_batch_import(request):
    context = {}
    alerts  = []
    formatted_questions = []
    batch_text      = request.POST.get('batch_text', '')
    tournament_id   = request.POST.get('tournament_id', '')
    if tournament_id == "create_new" :
        name = request.POST.get('new_tournament_name', '')
        year = request.POST.get('new_tournament_year', '')
        diff = request.POST.get('new_tournament_diff', '')
        if Tournament.objects.filter(name=name, year=year).count():
            context['tournament'] = Tournament.objects.get(name=name, year=year)
            alerts.append('Tournament already exists - using existing tournament.')
        else: 
            tournament = Tournament(name=name, year=year, difficulty=diff)
            tournament.created_by_id  = request.user.id
            tournament.created_at     = datetime.datetime.now()
            tournament.save()
            context['tournament'] = tournament
    else:
        context['tournament'] = Tournament.objects.get(pk=tournament_id)
    
    packet_name = request.POST.get('packet_name', '')
    
    if Packet.objects.filter(name=packet_name, tournament_id=context['tournament'].id).count():
        context['packet'] = Packet.objects.get(name=packet_name, tournament_id=context['tournament'].id)
    else: 
        packet      = Packet(name=packet_name)
        packet.created_by_id  = request.user.id
        packet.created_at     = datetime.datetime.now()
        packet.tournament_id  = context['tournament'].id
        packet.save()
        context['packet'] = packet

    batch_text = re.sub(r'\r[\n]?', '\n', batch_text ) #### Carriage returns are the worst. 
    
    if re.search(r'{%', batch_text):
        alerts.append("Django template tags detected... you're not funny.")
    batch_text = re.sub(r'{%', '', batch_text )
    batch_text = re.sub(r'%}', '', batch_text )

    batch_text = re.sub(r'ANSWER:(?P<answer>(.|\n)*?)(?P<next_num>\d{1,2}\.)', 'ANSWER:\g<answer> SPLIT \g<next_num>', batch_text )
    questions = re.split(r'SPLIT', batch_text)
    number = 1
    for question in questions : 
        question    = re.sub(r'\n', ' ', question)
        question    = re.sub(r'\"', '&quot;', question)

        question    = re.sub(r'^ \d{1,2}\.', '', question)
        parts       = re.split(r'ANSWER:', question)
      
        text = ''
        answer = '' 
        if len(parts) == 2 :
            text    = parts[0].encode('utf-8', 'xmlcharrefreplace') 
            answer  = parts[1].encode('utf-8', 'xmlcharrefreplace')
        else :
            text = ''.join(parts)
            alerts.append('Autoparsing question {} failed.'.format(number)) 
        formatted_questions.append({"number": number, "question_text": text, "answer": answer});    
        number += 1
   
    if 20 > len(questions) :
        for num in range(len(questions) + 1, 21):  #### off-by-one error. lol. 
            formatted_questions.append({"number": num, "question_text": '', "answer": '' });
    
    subject_list = Subject.objects.all()
    context['subject_list'] = subject_list
    
    context["questions"] = formatted_questions
    context["alerts"] = alerts
    context["batch_text"] = batch_text.encode('utf-8', 'xmlcharrefreplace')
    return render(request, 'process_batch_import.html', context)

@login_required
@permission_required('polls.can_add_and_flag')
def batch_import(request):
    context = {}
    alerts  = []
   
    packet_id = request.POST.get('packet_id', None)
    if packet_id is None: 
        alerts.append("No packet ID - something has gone terribly wrong")
    packet_id = packet_id.encode('utf-8')
     
    for num in xrange(1,30):   
        question    = request.POST.get('question_{}'.format(num), None)
        if question is None or question=='':
            break
        question    = question.encode('utf-8', 'xmlcharrefreplace') 
        answer      = request.POST.get('answer_{}'.format(num), None)
        if answer is None:
            break
        answer      = answer.encode('utf-8', 'xmlcharrefreplace') 
        subject     = request.POST.get('subject_{}'.format(num), '')
       
        question_obj = Tossup(question=question, answer=answer, subject_id=subject, packet_id=packet_id)
        question_obj.created_by_id  = request.user.id
        question_obj.created_at     = datetime.datetime.now()
        question_obj.save()
    
    return redirect("{}?packet_id={}".format(reverse('view_questions'), packet_id)); 
