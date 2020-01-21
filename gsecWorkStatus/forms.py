from django import forms
from django.forms import ModelForm,Textarea,Select
from gsecWorkStatus.models import  UserProfileInfo,User,agenda
from django.contrib.auth.models import User
from django import forms
from django.forms import (formset_factory, modelformset_factory)


Agenda_choices= [
                ('Completed', 'Completed'),
                ('Ongoing-Long-Term', 'Ongoing-Long-Term'),
                ('Ongoing-Short-Term', 'Ongoing-Short-Term'),
                ('Not-Started', 'Not-Started'),
                ('Broken', 'Broken'),
                ('Not-Evaluated', 'Not-Evaluated'),
                ('Not-Evaluated-Subjective', 'Not-Evaluated-Subjective'),
]

# class Agendaform(forms.ModelForm):
#     class Meta():
#         model=agenda
#         Title = forms.CharField(
#         # label='Title',
#             widget=forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Your Agenda here'
#             })
#         )
#         AgendaCategory = forms.CharField(
#         # make it drop down
#         # label='Book Name',
#             widget=forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Book Name here'
#             })
#         )
#         Description = forms.CharField(
#         # label='Book Name',
#             widget=forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows':'4',
#                 'placeholder': 'Enter Description here'
#             })
#         )
#         Status = forms.CharField(
#         # make it drop down
#         # label='Book Name',
#             widget=forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Book Name here'
#             })
#         )
#         Comment = forms.CharField(
#         # make it drop down
#         # label='Book Name',
#             widget=forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Comment here'
#             })
#         )
# "faccho dhang se padho"
Agendaformset = modelformset_factory(
            agenda,

            fields=('title','agendaCategory','unapprovedComment','unapprovedStatus','description'),
            extra=1,
            widgets={
                'title':forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Your Agenda Name here',
                    'required':True
                }),
                'agendaCategory':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Agenda category here'
            }),
                'unapprovedComment':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Comment here'
            }),
                'description':forms.Textarea(attrs={
                'class': 'form-control',
                'rows':'4',
                'placeholder': 'Enter Description here'
            })
            }

        )


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # first_name =
    class Meta():
        model =User
        fields = ('username','email','password','first_name','last_name')
        labels = {
            # "username":("Webmail username"),
            "email":("Webmail id"),
            "first_name": ("User Type"),
            "last_name" : ("Full Name")

        }

        type = (

            ('CIS','CIS'),
            ('GS','GS'),
        )
        widgets = {'first_name': Select(choices=type)}

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('post_description','image','youtube','pdf')
        labels = {
            "image": ("Profile Pic"),
            "youtube": ("Youtube video link"),
            "pdf":("Agenda Pdf")

        }


class AgendaForm(forms.ModelForm):
    class Meta():
        model=agenda
        fields = ['user','title','agendaCategory','description','StatusCategory','unapprovedComment','unapprovedStatus',]
        widgets = {
            'description': Textarea,
            'representativeComments':Textarea(attrs={'rows': 3 }),
        }

class UpdateStatusForm(forms.ModelForm):
    class Meta():
        model = agenda
        fields = ['title','unapprovedStatus','unapprovedComment','status']


