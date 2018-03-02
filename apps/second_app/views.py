# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from ..lr_app.models import User
from models import Idea
from django.db.models import Sum, Count

# Create your views here.

def success(request):
    
    user = User.objects.get(id=request.session['user_id'])
    #allUsers = User.objects.all()
    #theUsers = User.objects.get(id=id)
    otherLikes = Idea.objects.exclude(favorited_by=request.session['user_id'])
    myLikes = Idea.objects.filter(favorited_by=request.session['user_id'])

    context = {
        "current_user": user.username,
        "all_ideas": Idea.objects.all().annotate(num_likes=Count('favorited_by')).order_by("-num_likes"),
        #"totalLikes": (len(otherLikes) + len(myLikes))
        # "otherLikes": Idea.objects.exclude(favorited_by=request.session['user_id']),
        # "myLikes": Idea.objects.filter(favorited_by=request.session['user_id'])
        


    }

    return render(request, "second_templates/index.html", context)


# def likes(request, id):
#     theUsers = User.objects.get(id=id)

#     context ={
#         'totalLikes': len(Idea.objects.filter(favorited_by = theUsers))
#     }
#     return redirect(request, "/second_app/success", context)




def createIdea(request):
    print "$$$$$$$$$$ in createIdea $$$$$$$$$$$$$$"
    results = Idea.objects.basic_validation(request.POST, request.session['user_id'])
    
    if results[0]:
        request.session['idea_id'] = results[1].id
        print "***********You Made An Idea**************"
        return redirect("/second_app/success")
    else:
        for err in results[1]:
            messages.error(request, err)
        return redirect("/second_app/success")
    
    return redirect("/second_templates/index.html")

def detail(request, id):
                                                                # joining one to many from the User to the ManyToMany("message_poster__favorited_by")
    #theUser = User.objects.get(id = id).annotate(num_likes=Count('message_poster__favorited_by')).aggregate(total_likes=Sum('num_likes'))
                                                    #creating 2 fields, one to Idea, one to User
    theUser = User.objects.get(id = id)
    context = {
        #"UserPosts": results,
        'stuff': theUser,
        'stormer': Idea.objects.filter(added_by = theUser),
        #"my_posted_quotes": Quote.objects.filter(added_by=request.session['user_id']),
        'totalCount': len(Idea.objects.filter(added_by = theUser)),
        'totalLikes': len(Idea.objects.filter(favorited_by = id))

    }
    return render(request, 'second_templates/userDetails.html', context)

def ideaDetail(request, id):
    results = Idea.objects.get(id=id)
    context = {
        "BrightIdeas": results,
        "LikeMinded": results.favorited_by.all(),
        # "thisIdea": Idea.objects.get(id=id)

    }
    return render(request, 'second_templates/ideaDetails.html', context)

def favorite(request, id):
    i = Idea.objects.get(id=id)
    u = User.objects.get(id=request.session['user_id'])

    i.favorited_by.add(u)
    print "********** Like Created ***********"
    return redirect("/second_app/success")


def remove(request, id):
    Idea.objects.get(id=id).delete()
    return redirect("/second_app/success")