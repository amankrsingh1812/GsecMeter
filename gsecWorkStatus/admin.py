from django.contrib import admin
from gsecWorkStatus.models import  User,UserProfileInfo,agenda,votes
#
# # Register your models here.
admin.site.register(agenda)
admin.site.register(votes)
admin.site.register(UserProfileInfo)
# admin.site.register(Status)
# admin.site.register(Headline)
# admin.site.register(User)
