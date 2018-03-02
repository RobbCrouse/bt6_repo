# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..lr_app.models import User
from datetime import datetime

# Create your models here.

class IdeaManager(models.Manager):
    def basic_validation(self, postData, user_id):
        errors = []
        if len(postData['greatWords']) < 2:
            errors.append("Your idea is too short.")
        if len(errors) > 0:
            return (False, errors)

        

        else:
            i = Idea.objects.create(greatWords=postData['greatWords'], added_by=User.objects.get(id=user_id))
            print "************in IdeaManager*************"
            return (True, i)



class Idea(models.Model):
    greatWords = models.TextField(max_length=500)
    wordsmith = models.CharField(max_length=255)#shouldn't need this, leaving it just in case
    count = models.IntegerField(default = 0)

    added_by = models.ForeignKey(User, related_name='message_poster')
    favorited_by = models.ManyToManyField(User, related_name='appreciator')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = IdeaManager()

    def __str__(self):
	    return 'greatWords: {}, wordsmith: {}'.format(self.greatWords, self.wordsmith)