# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import math


# def insert_data(obj):
#     obj.save()
#     return obj.id
#
#
# class User(models.Model):
#
#     username = models.CharField(max_length=250, null=False)
#     password = models.IntegerField(null=False, default="123")
#     location = models.IntegerField(null=False, default="")
#
#     def __str__(self):
#         return str(self.username)+' || '+str(self.password)+' || '+str(self.location)
#
#     @staticmethod
#     def calc_manhattan(user_data, db_data, users_id):
#         pass
#
#
# class Job(models.Model):
#     jobID = models.CharField(null=False)
#     subject = models.CharField(max_length=450)
#     WorkType = models.CharField(default="")
#     FileName = models.CharField()
#     Priority = models.CharField(null=False, max_length=1)
#
#     def __str__(self):
#         return str(self.jobID)+' || '+str(self.subject)+' || '+str(self.WorkType) + '||' + str(self.FileName) +\
#                '||' + str(self.Priority)
#
#
# class Job_Task(models.Model):
#     audio_update = models.FloatField() ## if he tried to elave the page(update last stop point)
#     UName = models.ForeignKey(User, on_delete=models.CASCADE)
#     JID = models.ForeignKey(Job, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.UName) + ' , ' + str(self.JID) + ', ' + str(self.audio_update)
