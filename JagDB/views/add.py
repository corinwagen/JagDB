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


    batch_text = re.sub(r'Bonuses', "SPLIT", batch_text)
#    halves = re.split(r'Bonuses', batch_text, 2)
    halves = re.split(r'SPLIT', batch_text,)
    tossup_text = halves[0]
    bonus_text  = halves[1]
 
    
    tossup_text = re.sub(r'ANSWER:(?P<answer>(.|\n)*?)(?P<next_num>\d{1,2}\.)', 'ANSWER:\g<answer> SPLIT \g<next_num>', tossup_text )
    tossups = re.split(r'SPLIT', tossup_text)
    number = 1
    for question in tossups : 
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
        formatted_questions.append({"number": number, "question_text": text, "answer": answer, "type": "tossup"});    
        number += 1
   
    if 20 > number :
        for num in range(len(tossups) + 1, 21):  #### off-by-one error. lol. 
            formatted_questions.append({"number": num, "question_text": '', "answer": '', "type": "tossup" });
    
    bonus_text = re.sub(r'ANSWER:(?P<answer>((?!\[10\]).|\n)*?)(?P<next_num>\d{1,2}\.)', 'ANSWER:\g<answer> SPLIT \g<next_num>', bonus_text )
    bonuses = re.split(r'SPLIT', bonus_text)
    number = 1
    for question in bonuses: 
        question    = re.sub(r'\n', ' ', question)
        question    = re.sub(r'\"', '&quot;', question)

        question    = re.sub(r'^ \d{1,2}\.', '', question)
#        parts       = re.split(r'(ANSWER:|\[10\])', question, 7)
        question    = re.sub(r'(ANSWER:|\[10\])', 'SPLIT', question)
        parts       = re.split(r'SPLIT', question, 7)
      
        leadin  = ''
        part1   = ''
        answer1 = ''
        part2   = ''
        answer2 = ''
        part3   = ''
        answer3 = ''
        if len(parts) == 7 :
            leadin  = parts[0].encode('utf-8', 'xmlcharrefreplace') 
            part1   = parts[1].encode('utf-8', 'xmlcharrefreplace') 
            answer1 = parts[2].encode('utf-8', 'xmlcharrefreplace')
            part2   = parts[3].encode('utf-8', 'xmlcharrefreplace') 
            answer2 = parts[4].encode('utf-8', 'xmlcharrefreplace')
            part3   = parts[5].encode('utf-8', 'xmlcharrefreplace') 
            answer3 = parts[6].encode('utf-8', 'xmlcharrefreplace')
        else :
            text = ''.join(parts)
            alerts.append('Autoparsing question {} failed.'.format(number)) 
        formatted_questions.append({
            "number": number,
            "leadin": leadin, 
            "part1": part1,
            "answer1": answer1, 
            "part2": part2,
            "answer2": answer2, 
            "part3": part3,
            "answer3": answer3, 
            "type": "bonus",
        });    
        number += 1

    if 20 > number :
        for num in range(len(bonuses) + 1, 21):  #### off-by-one error. lol. 
            formatted_questions.append({
                "number": num, 
                "leadin": '',
                "part1": '',
                "part2": '',
                "part3": '',
                "answer1": '', 
                "answer2": '', 
                "answer3": '', 
                "type": "bonus" 
            });
    
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
        if request.POST.get('type_{}'.format(num), '') == "tossup": 
            question    = request.POST.get('question_{}'.format(num), None)
            if question is None or question=='':
                break
#            question    = question.encode('utf-8', 'xmlcharrefreplace') 
            answer      = request.POST.get('answer_{}'.format(num), None)
            if answer is None:
                break
#            answer      = answer.encode('utf-8', 'xmlcharrefreplace') 
            subject     = request.POST.get('subject_{}'.format(num), '')
           
            question_obj = Tossup(question=question, answer=answer, subject_id=subject, packet_id=packet_id)
            question_obj.created_by_id  = request.user.id
            question_obj.created_at     = datetime.datetime.now()
            question_obj.save()
        elif request.POST.get('type_{}'.format(num), '') == "bonus": 
            leadin    = request.POST.get('leadin_{}'.format(num), None)
#            leadin    = leadin.encode('utf-8', 'xmlcharrefreplace') 
            part1     = request.POST.get('part1_{}'.format(num), None)
#            part1     = part1.encode('utf-8', 'xmlcharrefreplace') 
            answer1   = request.POST.get('answer1_{}'.format(num), None)
            if answer1 is None:
                break
#            answer1     = answer1.encode('utf-8', 'xmlcharrefreplace') 
            part2     = request.POST.get('part2_{}'.format(num), None)
#            part2     = part2.encode('utf-8', 'xmlcharrefreplace') 
            answer2   = request.POST.get('answer2_{}'.format(num), None)
            if answer2 is None:
                break
#            answer2     = answer2.encode('utf-8', 'xmlcharrefreplace') 
            part3     = request.POST.get('part3_{}'.format(num), None)
#            part3     = part3.encode('utf-8', 'xmlcharrefreplace') 
            answer3   = request.POST.get('answer3_{}'.format(num), None)
            if answer3 is None:
                break
#            answer3     = answer3.encode('utf-8', 'xmlcharrefreplace') 
            subject     = request.POST.get('subject_{}'.format(num), '')
           
            question_obj = Bonus(leadin=leadin, part1=part1, answer1=answer1, part2=part2, answer2=answer2, part3=part3, answer3=answer3, subject_id=subject, packet_id=packet_id)
            question_obj.created_by_id  = request.user.id
            question_obj.created_at     = datetime.datetime.now()
            question_obj.save()

    return redirect("{}".format(reverse('view_questions')))
