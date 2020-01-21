from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# COLOR_CHOICES = (
#        ('green','GREEN'),
#        ('blue', 'BLUE'),
#        ('red','RED'),
#        ('orange','ORANGE'),
#        ('black','BLACK'),
#     )
# class Agenda1(models.Model):
#
#     Title = models.CharField(max_length=255)
#     AgendaCategory = models.CharField(max_length=255)
#     Description = models.CharField(max_length=1000)
#     Status = models.CharField(max_length=250)
#     Comment = models.CharField(max_length=1000)
#
#     class Meta:
#         db_table = 'agenda1'
#
#     def __str__(self):
#         return self.name


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post_description = models.CharField(max_length=255)
    image = models.ImageField( blank=True)
    youtube = models.URLField(blank=True)
    pdf = models.FileField(blank=True)


    def __str__(self):
        return  self.user.username
#method to have drop down w ith fixed choice
# COLOR_CHOICES = (
#     ('green','GREAgeEN'),
#     ('blue', 'BLUE'),
#     ('red','RED'),
#     ('orange','ORANGE'),
#     ('black','BLACK'),
# )
#
# class MyModel(models.Model):
#   color = models.CharField(max_length=6, choices=COLOR_CHOICES, default='green')
class votes(models.Model) :
    vote_id=models.AutoField(primary_key=True)
    item_id=models.IntegerField(null=True)
    user_id=models.CharField(max_length=1000)

    def __str__(self):
        return str(self.vote_id)


class agenda(models.Model) :
    status_choice=(('Completed','COMPLETED'),('Ongoing-Long-Term','ONGOING-LONG-TERM'),('Ongoing-Short-Term',
                    'ONGOING-SHORT-TERM'),('Not-Started','NOT_STARTED'),('Broken','BROKEN'),('Not-Evaluated','NOT-EVALUATED'),
               ('Not-Evaluated-Subjective', 'NOT-EVALUATED-SUBJECTIVE'))
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    title =models.CharField(max_length=1000)
    agendaCategory=models.CharField(max_length=1500)
    description = models.CharField(max_length=1000) #agenda description
    status= models.CharField(max_length=100, choices=status_choice, default='Select')  #completed/notcompleted/ongoing ong term etc
    representativeComments = models.CharField(max_length=1000,blank=True)
    currentStatus  = models.CharField(max_length=1000,blank=True)
    unapprovedComment = models.CharField(max_length=1000,blank=True)
    unapprovedStatus = models.CharField(max_length=100, choices=status_choice, default='Select')
    approvedBy = models.CharField(max_length=200,blank=True)
    StatusCategory = models.CharField(max_length=250,blank=True)


    def get_absolute_url(self):
        return reverse('gsec:vp')

    def __str__(self):
        return self.title
#first the user will login
#if user is a CIS member its firstname will b CIS
#if user is gensec then its firstname name will be GS
#if user is a CIS member then allow him to check comment but the comment will go in unapproved comment
#when a cis member sees the comment it will lead to calling of a function that will set the unapproved to blank and
#update the representatve comment and status as  per approval and change the approved value to 1
