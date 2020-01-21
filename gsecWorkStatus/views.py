from django.shortcuts import render,redirect
import pickle
import os
from django.contrib import messages
from graphos.sources.simple import SimpleDataSource
from graphos.renderers import gchart
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from  django.views import generic
from django.http import HttpResponse,HttpResponseRedirect
from  django.contrib.auth import authenticate,login,logout
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from gsecWorkStatus.models import User,UserProfileInfo,agenda,votes
from gsecWorkStatus.forms import UserProfileInfoForm,UserForm,AgendaForm,UpdateStatusForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, reverse, redirect


from django.views import generic

from .forms import (
    Agendaformset
)
# from .models import Agenda1

@login_required
def create_Agenda1(request):
    # a=agenda(request.POST)
    if request.user.first_name == "GS":
        template_name = 'create_Agenda1.html'
        # heading_message = 'Formset Demo'
        if request.method == 'GET':
            formset = Agendaformset(queryset=agenda.objects.none())
        elif request.method == 'POST':
            formset = Agendaformset(request.POST)
            if formset.is_valid():
                for form in formset:
                    if(form.is_valid()):
                    # form.user=request.user.username
                        agd=form.save(commit=False)
                        agd.user=request.user
                        agd.StatusCategory=agd.unapprovedStatus
                        agd.save()
                return render(request, 'agendaadded.html', {'some_flag': True})
                # return HttpResponse("agenda added")
            else:
                return render(request,'agendaadded.html',{'flag':True})
        return render(request, template_name, {'formset': formset})
    else:
        return HttpResponse("You are not allowed to visit this page :(    contact - Rishikesh   ")

# sign_in_url = get_signin_url(redirect_uri)


# def gettoken1(request):
#     #################################
#     # Set redirect after saving token
#     redirect_url = request.GET["next"]
#     ################################
#
#     # get Token from code
#     auth_code = request.GET['code']
#     redirect_uri = request.build_absolute_uri(reverse('authentication:gettoken'))
#     token = get_token_from_code(auth_code, redirect_uri)
#     access_token = token['access_token']
#
#     # Save the token in session
#     request.session['access_token'] = access_token
#
#     # redirect_url = request.session.get('redirect_url', None)
#
#     if redirect_url is None:
#
#         #####################
#         # Get user from token
#         user = get_me(access_token)
#
#         return HttpResponse("Token: %s<br>Name: %s<br>Roll Number: %s<br> Mail: %s" % (
#         access_token, user['displayName'], user['surname'], user['mail']))
#     else:
#         return redirect(redirect_url)

@login_required(login_url='authentication:home')
def jugaad(request,pname):
    user_id = request.user.id
    item_id = pname
    redirect_uri = request.build_absolute_uri('')
    v = votes.objects.filter(item_id=item_id, user_id=user_id)
    if (len(v) > 0):
        return redirect(redirect_uri)
    m = votes(item_id=item_id, user_id=user_id)
    m.save()
    v = votes.objects.filter(item_id=item_id)
    return redirect(redirect_uri)
def vote(request,pname):
    if request.method == 'GET':

        if (request.GET['query'] == 'vote'):
            def nvote(request):
                item_id = request.GET['item_id']
                user_id = request.GET['user_id']
                v = votes.objects.filter(item_id=item_id, user_id=user_id)
                if (len(v) > 0):
                    return HttpResponse(-1)
                m = votes(item_id=item_id, user_id=user_id)
                m.save()
                v = votes.objects.filter(item_id=item_id)
                return HttpResponse(len(v))
            return nvote(request)
        elif request.GET['query']=='votecount':
            item_id=request.GET['item_id']
            total_votes=0
            v=votes.objects.filter(item_id=item_id)
            return HttpResponse(len(v))
            # return HttpResponse(len(v))
        # post_id = request.GET['post_id']
        # likedpost = Post.obejcts.get(pk=post_id)  # getting the liked posts
        # m = Like(post=likedpost)  # Creating Like Object
        # m.save()  # saving it to store in database
        return HttpResponse("0")  # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")
    #             Title = form.cleaned_data.get('Title')
    #             AgendaCategory = form.cleaned_data.get('AgendaCategory')
    #             Description = form.cleaned_data.get('Description')
    #             Status = form.cleaned_data.get('Status')
    #             Comment = form.cleaned_data.get('Comment')
    #             # save book instance
    #             if Agenda1:
    #                 a=Agenda1(Title=Title,
    #                      AgendaCategory=AgendaCategory,
    #                      Description=Description,
    #                      Status=Status,
    #                      Comment=Comment)
    #                 a.save()
    #         return redirect('store:book_list')
    #
    # return render(request, template_name, {
    #     'formset': formset,
    #     'heading': heading_message,
    # })

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_DIR = os.path.join(BASE_DIR, 'script_dir', 'dict_dir')

post_list = ['Vice_President', 'Technical', 'Cultural', 'Sports', 'Welfare', 'HAB','senator1']
post_name = ['vp', 'technical', 'cultural', 'sports', 'welfare', 'hab','senator1']


def comparechart(post1,post2,compare1,compare2):
    data = []
    templist=['status']
    templist.append(post1)
    templist.append(post2)
    data.append(templist)
    d1={}
    d2={}
    d1=draw_chart1(compare1)
    d2=draw_chart1(compare2)
    candidate1 = d1['data']
    candidate2 = d2['data']
    # agendapercent=[]

    # ['completed', 20, 40, 20]
    # ['Completed', 31.03448275862069],
    for i in range (1,8):
        agendapercent=[]
        agendapercent.append(candidate1[i][0])
        agendapercent.append(candidate1[i][1])
        agendapercent.append(candidate2[i][1])
        if agendapercent[1] or agendapercent[2]:
            data.append(agendapercent.copy())

    print("abc:")
    print(data)
    data_source = SimpleDataSource(data=data)
    # Chart object
    chart = gchart.ColumnChart(data_source)
    return chart


# [["Completed" , count], ...]
def draw_chart(post_dict):
    data = []
    data.append(['status', 'No of task'])
    for status, temp_dict in post_dict.items():
        data.append([status, len(temp_dict)])

    print(data)
    # DataSource object
    # options = { 'width': 400,'height': 240,'title': "Toppings I Like On My Pizza",'colors': ["#00b300", "#e6693e", "#ec8f6e", "#f3b49f", "#e60000"]}
    data=[
            ['status', 'General Secretary, Technical Board 2018-19', 'Vice-President, Gymkhana Council 2017-18'],
            ['Completed', 0.0, 31.03448275862069],
            ['Ongoing-Long-Term', 0.0, 0.0],
            ['Ongoing-Short-Term', 0.0, 0.0],
            ['Not-Evaluated', 0.0, 20.689655172413794],
            ['Not-Evaluated-Subjective', 0.0, 0.0],
            ['Not-Started', 100.0, 37.93103448275862],
            ['Broken', 0.0, 10.344827586206897]
          ]

    data_source = SimpleDataSource(data=data)
    # Chart object
    chart = gchart.ColumnChart(data_source)
    return chart


def compare(request):
    if request.method=="POST":
        compare1=request.POST.get('compare1')
        compare2 = request.POST.get('compare2')



        obj1 = agenda.objects.filter(user__userprofileinfo__post_description=compare1)
        obj2 = agenda.objects.filter(user__userprofileinfo__post_description=compare2)
        print(compare1)
        print(compare2)


        chart=comparechart(compare1,compare2,obj1,obj2)
        # print(chart)
        return render(request,'gsecWorkStatus/compareview.html',{'chart':chart})
        # return HttpResponseRedirect(reverse('candidate:vp'))
    else:
        members = UserProfileInfo.objects.all()

        senators = User.objects.filter(username__contains="senator")
        return render(request, 'gsecWorkStatus/compare.html', {'members': members, 'senators': senators})
    # if request.method == "POST":

def pastchart(agendas):
    data = []
    options = {'title': "Comparsion Chart",
               'colors': ["#109618", "#660066", "#ff9900", "#3366cc", "#0099c6", "#ff6600", "#dc3912"]}
    userlist=[]
    print("users")
    for proposal in agendas:
        pd=proposal.user.userprofileinfo.post_description
        print("bpd",pd)
        if "General Secretary," in pd:
            pd=pd[18:]
            print("pd",pd)
        if pd in userlist:
            # print(proposal.user.userprofileinfo.post_description)
            pass
        else:
            # pd=proposal.user.userprofileinfo.post_description

            userlist.append(pd)
    print("userlist: ",userlist)
    candidateinfo=[]
    for rep in userlist:
        repagenda=agendas.filter(user__userprofileinfo__post_description__contains=rep)
        ch={}
        ch=draw_chart1(repagenda)
        candidateinfo.append(ch['data'].copy())
    # j=int(0)

    allchartdata={}



    for i in range(1,8):
        templist=[]
        templist.append(['candidate','percentage'])
        j=0

        for candidate in userlist:
            temp = []
            temp.append(candidate)
            # temp.append(candidateinfo[]
            # temp.append(candidate)
            temp.append(candidateinfo[j][i][1])
            # print(candidateinfo[j][i][1])
            templist.append(temp.copy())
            # print('templist',templist)
            j=j+1
        allchartdata[candidateinfo[0][i][0]] = templist
    print(allchartdata)
    return allchartdata


    # # options = {'title': 'My Average Day', 'width': 550, 'height': 400}
    # # var options = {'title':'My Average Day', 'width':550, 'height':400};
    # print(data)
    # # DataSource object
    # data_source = SimpleDataSource(data=data)
    # # Chart object
    # chart = gchart.PieChart(data_source, options=options)
    # sum = 0
    # for i in range(1, 8):
    #     sum = int(data[i][1]) + int(sum)
    #
    # for i in range(1, 8):
    #     if sum != 0:
    #         data[i][1] = (int(data[i][1]) / int(sum)) * 100
    #
    # # del data[0]
    # print(data)
    # return {'chart': chart, 'data': data}
def check(chartinfo):
    n=len(chartinfo)
    for i  in range(1,n):
        if chartinfo[i][1]>0 :
            return 1
    return 0

def comparepast(request):
    if request.method == "POST":
        designation = request.POST.get('designation')
        # compare2 = request.POST.get('senator2')
        print("in")
        incldingsenator = agenda.objects.filter(user__userprofileinfo__post_description__contains=designation)
        obj1 =incldingsenator.exclude(user__username__contains="senator")
        # agenda.objects.filter(user__userprofileinfo__p)
        # obj2 = agenda.objects.filter(user__username=compare2)

        print(designation)
        # print(obj1)
        # print(compare2)
        chartdict={}

        chartdict = pastchart(obj1)
        options1 = {'title': "Completed",
                   'colors': ["#109618"]
                    }
        flag=check(chartdict['Completed'])

        chartcompleted=''
        chartsubjective=''
        chartnotevaluated=''
        chartnotstarted=''
        chartongoinshort=''
        chartongoinlong=''
        chartbroken=''
        if flag==1:
            data_source = SimpleDataSource(data=chartdict['Completed'])
            chartcompleted = gchart.ColumnChart(data_source,options=options1)
            # type(chartcompleted)
        flag=check(chartdict['Ongoing-Long-Term'])
        if flag==1 :
            options2={}
            options2['title']="Ongoing-Long-Term"
            options2['colors']=["#660066"]
            # options['colors']=[""]

            data_source = SimpleDataSource(data=chartdict['Ongoing-Long-Term'])
            chartongoinlong = gchart.ColumnChart(data_source,options=options2)

        flag = check(chartdict['Ongoing-Short-Term'])
        if flag == 1:

            options3 = {}
            options3['colors']=["#ff9900"]
            options3['title'] = "Ongoing-Short-Term"
            data_source = SimpleDataSource(data=chartdict['Ongoing-Short-Term'])
            chartongoinshort = gchart.ColumnChart(data_source,options=options3)

        flag = check(chartdict['Not-Evaluated'])
        if flag == 1:

            options4 = {}
            options4['colors']=["#3366cc"]
            options4['title'] = "Not-Evaluated"
            data_source = SimpleDataSource(data=chartdict['Not-Evaluated'])
            chartnotevaluated = gchart.ColumnChart(data_source,options=options4)

        flag = check(chartdict['Not-Evaluated-Subjective'])
        if flag == 1:

            options5 = {}
            options5['colors']=["#0099c6"]
            options5['title']="Not-Evaluated-Subjective"
            data_source = SimpleDataSource(data=chartdict['Not-Evaluated-Subjective'])

            chartsubjective = gchart.ColumnChart(data_source,options=options5)
            print(chartsubjective)
        flag = check(chartdict['Not-Started'])
        if flag == 1:

            options6={}
            options6['colors']=["#ff6600"]
            options6['title']="Not-Started"
            data_source = SimpleDataSource(data=chartdict['Not-Started'])
            chartnotstarted = gchart.ColumnChart(data_source, options=options6)
        flag = check(chartdict['Broken'])
        if flag == 1:

            options7={}
            options7['colors']=["#dc3912"]
            options7['title']="Broken"
            data_source = SimpleDataSource(data=chartdict['Broken'])
            chartbroken = gchart.ColumnChart(data_source,options=options7)



        # print(chart)
        return render(request, 'gsecWorkStatus/compareview.html', {'chartcompleted':chartcompleted,'chartbroken':chartbroken,'chartnotstarted':chartnotstarted,'chartsubjective':chartsubjective,'chartnotevaluated':chartnotevaluated,'chartongoinshort':chartongoinshort,'chartongoinlong':chartongoinlong})
        # return HttpResponseRedirect(reverse('candidate:vp'))

    else:
        # members = UserProfileInfo.objects.all()
        # senators = User.objects.filter(username__contains="senator")
        return render(request, 'gsecWorkStatus/compare.html')


def comparesenator(request):
    if request.method=="POST":
        compare1=request.POST.get('senator1')
        compare2 = request.POST.get('senator2')



        obj1 = agenda.objects.filter(user__username=compare1)
        obj2 = agenda.objects.filter(user__username=compare2)
        print(compare1)
        print(compare2)


        chart=comparechart(compare1,compare2,obj1,obj2)
        # print(chart)
        return render(request,'gsecWorkStatus/compareview.html',{'chart':chart})
        # return HttpResponseRedirect(reverse('candidate:vp'))
    else:
        members = UserProfileInfo.objects.all()
        senators = User.objects.filter(username__contains="senator")
        return render(request,'gsecWorkStatus/compare.html',{'members':members,'senators':senators})
    # if request.method == "POST":


def draw_chart1(agendas):
    data = []
    options = { 'title': "Agenda Chart",
               'colors': ["#109618","#660066","#ff9900","#3366cc","#0099c6","#ff6600","#dc3912"]}
    data.append(['status', 'No of task'])
    # for status, temp_dict in post_dict.items():
    #     data.append([status, len(temp_dict)])

    CompletedStatus = agendas.filter(status="Completed").count()
    # if CompletedStatus !=0 :
    data.append(["Completed", CompletedStatus])
    OngoingLongTermStatus = agendas.filter(status="Ongoing-Long-Term").count()
    # if OngoingLongTermStatus !=0 :
    data.append(["Ongoing-Long-Term",OngoingLongTermStatus])
    OngoingShortTermStatus = agendas.filter(status="Ongoing-Short-Term").count()
    # if OngoingShortTermStatus !=0 :
    data.append(["Ongoing-Short-Term",OngoingShortTermStatus])


    NotEvaluatedStatus = agendas.filter(status="Not-Evaluated").count()
    # if NotEvaluatedStatus !=0 :
    data.append(["Not-Evaluated",NotEvaluatedStatus])
    NotEvaluatedSubjectiveStatus = agendas.filter(status="Not-Evaluated-Subjective").count()
    # if NotEvaluatedSubjectiveStatus !=0 :
    data.append(["Not-Evaluated-Subjective",NotEvaluatedSubjectiveStatus])
    NotStartedStatus = agendas.filter(status="Not-Started").count()
    # if NotStartedStatus !=0 :
    data.append(["Not-Started",NotStartedStatus])
    BrokenStatus = agendas.filter(status="Broken").count()
    # if BrokenStatus !=0 :
    data.append(["Broken", BrokenStatus])

    # options = {'title': 'My Average Day', 'width': 550, 'height': 400}
    # var options = {'title':'My Average Day', 'width':550, 'height':400};
    print(data)

    # DataSource object
    data_source = SimpleDataSource(data=data)
    # Chart object
    chart = gchart.PieChart(data_source,options=options)
    sum=0
    for i in range(1,8):
        sum=int(data[i][1])+int(sum)

    for i in range(1, 8):
        if sum != 0:
            data[i][1] = (int(data[i][1])/int(sum))*100

    # del data[0]
    print(data)
    return {'chart':chart,'data':data}


# def comparecurrent(request):



#auxialliary function
def fetch_dict_file(post_name):
    fname = os.path.join(DICT_DIR, post_name + '.pkl')

    fin = open(fname, 'rb')
    post_dict = pickle.load(fin)

    fin.close()
    fname = os.path.join(DICT_DIR, 'candidate_info' + '.pkl')
    fin = open(fname, 'rb')
    candidate_info = pickle.load(fin)
     # print("location ", candidate_info)
    fin.close()
    return post_dict, candidate_info[post_name]

def statusfunc(agendas):
    statuslist=[]
    OngoingLongTermStatus = agendas.filter(status="Ongoing-Long-Term").count()
    OngoingShortTermStatus = agendas.filter(status="Ongoing-Short-Term").count()
    CompletedStatus = agendas.filter(status="Completed").count()
    NotStartedStatus = agendas.filter(status="Not-Started").count()
    BrokenStatus = agendas.filter(status="Broken").count()
    NotEvaluatedStatus = agendas.filter(status="Not-Evaluated").count()
    NotEvaluatedSubjectiveStatus = agendas.filter(status="Not-Evaluated-Subjective").count()
    if (NotStartedStatus != 0):
        statuslist.append("Not-Started")
    if (CompletedStatus != 0):
        statuslist.append("Completed")
    if (OngoingLongTermStatus != 0):
        statuslist.append("Ongoing-Long-Term")
    if (OngoingShortTermStatus != 0):
        statuslist.append("Ongoing-Short-Term")
    if (BrokenStatus != 0):
        statuslist.append("Broken")
    if (NotEvaluatedSubjectiveStatus != 0):
        statuslist.append("Not-Evaluated-Subjective")
    if (NotEvaluatedStatus != 0):
        statuslist.append("Not-Evaluated")
    return statuslist

def vp(request,pname):


    template_name = 'gsecWorkStatus/gsec.html'
    info = UserProfileInfo.objects.get(user__username=pname)
    if(info.user.first_name=="GS"):
        agendas = agenda.objects.filter(user__username=pname,StatusCategory="")
        chartdict={}
        chartdict = draw_chart1(agendas)
        chart=chartdict['chart']
        chartdata=chartdict['data']
        statuslist=[]
        statuslist=statusfunc(agendas)

        print(statuslist)
        # print(post_dict)
        # del chartdata[0]
        return render(request, template_name, { 'pie_chart' : chart,
                                             'info':info,'agendas':agendas,'statuslist':statuslist,'pname':pname,'chartdata':chartdata,'i':0  })
    else:
        return HttpResponse("thats a invalid request")



def home(request):
    post_dict, candidate_info = fetch_dict_file(post_name[0])
    template_name = 'gsecWorkStatus/gsec.html'
    info = UserProfileInfo.objects.get(user__username="vp2k19")
    agendas = agenda.objects.filter(user__username="vp2k19",StatusCategory="")
    pname="vp2k19"
    chartdict = draw_chart1(agendas)
    chart=chartdict['chart']
    chartdata=chartdict['data']
    statuslist=[]
    statuslist=statusfunc(agendas)

    print(statuslist)
    # print(post_dict)

    return render(request, template_name, { 'pie_chart' : chart,
                                         'info':info,'agendas':agendas,'statuslist':statuslist,'pname':pname,'chartdata':chartdata  })


#
# def senator1(request):
#     # post_dict, candidate_info = fetch_dict_file(post_name[6])
#     print("senator1")
#     template_name = 'gsecWorkStatus/base.html'
#     # chart = draw_chart(post_dict)
#     info = UserProfileInfo.objects.get(post_description="senator1")
#     agendas = agenda.objects.filter(user_id=8)
#
#     statuslist = statusfunc(agendas)
#     print(statuslist)
#
#     # print(post_dict)
#     chart = draw_chart1(agendas)
#
#     return render(request, template_name, {'pie_chart':chart,'info': info, 'agendas': agendas, 'statuslist': statuslist})
#

# def technical(request):
#     post_dict, candidate_info = fetch_dict_file(post_name[1])
#     template_name = 'gsecWorkStatus/{0}.html'.format(post_list[1])
#     chart = draw_chart(post_dict)
#     print(post_dict)
#     return render(request, template_name, {'post_dict': post_dict, 'candidate_info': candidate_info, 'pie_chart' : chart,})
#
#
# def cultural(request):
#     post_dict, candidate_info = fetch_dict_file(post_name[2])
#     template_name = 'gsecWorkStatus/{0}.html'.format(post_list[2])
#     chart = draw_chart(post_dict)
#     return render(request, template_name, {'post_dict': post_dict, 'candidate_info': candidate_info, 'pie_chart' : chart,
#                                            })
#
#
# def sports(request):
#     post_dict, candidate_info = fetch_dict_file(post_name[3])
#     template_name = 'gsecWorkStatus/{0}.html'.format(post_list[3])
#     chart = draw_chart(post_dict)
#     return render(request, template_name, {'post_dict': post_dict, 'candidate_info': candidate_info, 'pie_chart' : chart,
#                                            })
#
#
# def welfare(request):
#
#     post_dict, candidate_info = fetch_dict_file(post_name[4])
#     template_name = 'gsecWorkStatus/{0}.html'.format(post_list[4])
#     chart = draw_chart(post_dict)
#     return render(request, template_name, {'post_dict': post_dict, 'candidate_info': candidate_info, 'pie_chart' : chart,
#                                            })
#
#
# def hab(request):
#     post_dict, candidate_info = fetch_dict_file(post_name[5])
#     template_name = 'gsecWorkStatus/{0}.html'.format(post_list[5])
#     chart = draw_chart(post_dict)
#     return render(request, template_name, {'post_dict': post_dict, 'candidate_info': candidate_info, 'pie_chart' : chart,
#                                            })


def user_login(request):
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    login(request,user)
                    if(user.first_name=="GS"):
                        return render(request,'gsecWorkStatus/base1.html',{})
                    else:
                        return HttpResponseRedirect(reverse('candidate:verify'))

                else:
                    return HttpResponse("User Not Active,contact swc ")
            else:
                print("login failed")
                print(username,password)
                return render(request, 'gsecWorkStatus/login.html', {'failed_login':"yes"})
        else:
            # if request.user.is_au
            if request.user.is_authenticated:
                return HttpResponseRedirect(reverse('candidate:vp'))
            else:
                return render(request,'gsecWorkStatus/login.html',{'failed_login':"no"})


# @login_required
def register(request):
    registered = False
    if request.method=="POST":
        user_form = UserForm(data=request.POST)
        profile_form =UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)


            user.save()

            profile = profile_form.save(commit=False)
            profile.user =user
            if 'image' in request.FILES :
                profile.image =request.FILES['image']

            if 'pdf' in request.FILES :
                profile.pdf =request.FILES['pdf']

            profile.save()
            registered =True
        else :
            print("errors")
            print(user_form.errors,profile_form.errors)

    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request,'gsecWorkStatus/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered })

@login_required
def addagenda(request):
    agenda_form = AgendaForm()
    if request.user.first_name =="CIS":
        if request.method == 'POST':
            agenda_form = AgendaForm(request.POST)

            if agenda_form.is_valid:
                agenda_form.save(commit=True)
                return render(request, 'agendaadded.html', {'some_flag': True})
        return render(request,'gsecWorkStatus/addagenda.html',{'agenda_form':agenda_form})
    else:
        return HttpResponse("You are not allowed to visit this page :(    contact - shivam   ")

#
# def updatestatus(request,id):
#         agendaupdate= agenda.objects.get(pk=id)
#         if request.method == 'POST':
#             update_form=AgendaForm(data=request.POST)
#             agendaupdate.unapprovedComment=update_form.unapprovedComment
#             agendaupdate.un
#         else:

@login_required()
def approvestatus(request):
    if request.user.first_name == "CIS":
        all_agenda = agenda.objects.all()
        return render(request,'gsecWorkStatus/verify.html',{'all_agenda':all_agenda})
    else:
        return HttpResponse("<h2>Sorry u are not allowed to visit this page,Please contact SWC </h2>")

@login_required
def verifysatus(request,pk):
    if request.method == "POST":

        approvagenda = agenda.objects.get(id=pk)
        approvagenda.representativeComments=approvagenda.unapprovedComment
        approvagenda.currentStatus=approvagenda.unapprovedStatus
        approvagenda.status=approvagenda.StatusCategory #updated status category(complete,broken....)
        approvagenda.StatusCategory=""
        approvagenda.unapprovedStatus=""
        approvagenda.unapprovedComment=""
        approvagenda.approvedBy=request.user.last_name
        approvagenda.save()
        return JsonResponse({"status": True})


@login_required
def disapprove(request,pk2):
    if request.method == "POST":
        approvagenda = agenda.objects.get(id=pk2)

        approvagenda.StatusCategory=approvagenda.status #updated status category(complete,broken....)
        approvagenda.unapprovedStatus=""
        approvagenda.unapprovedComment=""
        approvagenda.StatusCategory=""
        approvagenda.save()
        return JsonResponse({"status": True})
@login_required
def updatestatus(request,pk1):
    if request.method == "POST":
        form = UpdateStatusForm(data=request.POST)

        inst = agenda.objects.get(pk=pk1)
        # print("in")
        print(request.POST.get('unapprovedComment'))
        inst.unapprovedComment=request.POST.get('unapprovedComment')
        inst.unapprovedStatus=request.POST.get('unapprovedStatus')
        inst.StatusCategory=request.POST.get('status') #actually the status change updated by gsec

        inst.save()
        nexturl = request.user

        # print(nexturl)
        return HttpResponseRedirect(reverse('candidate:gs',args=[nexturl]))
    else:
        form = UpdateStatusForm()
        inst = agenda.objects.get( pk=pk1)
        return render(request,'gsecWorkStatus/update.html',{'form':form,'inst':inst})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('candidate:login'))


class UpdateAgenda(UpdateView):
    
    model = agenda
    fields = ['title','unapprovedComment','unapprovedStatus']


    def get_success_url(self,*args,**kargs):
        return reverse_lazy('candidate:vp')

@login_required
def change_password(request):
    print("in1")
    if request.method == 'POST':
        print("in2")
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print("in3")
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'gsecWorkStatus/change_password.html', {
        'form': form
    })




