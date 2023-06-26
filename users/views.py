from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from main.models import *
from django.db.models import Prefetch

def mypage(request, id):
    user = get_object_or_404(User, pk=id)
    result = TestResult.objects.first()
    posts = Post.objects.filter(writer=user)
    volunteers = []
    for post in posts:
        post_volunteers = Volunteer.objects.filter(post=post)
        volunteers.append({
            'post': post,
            'volunteers': post_volunteers
        })
    apply = Volunteer.objects.filter(user=user)
    context = {
        'user': user,
        'volunteers': volunteers,
        'result': result,
        'apply' : apply
    }
    return render(request, "users/mypage.html", context)
    
def measure(request):
    return render(request, 'users/measure.html')

def profile(request):
    return render(request, 'users/profile.html')

def approve_member(request, volunteer_id):
    volunteer = Volunteer.objects.get(id=volunteer_id)
    volunteer.info = 'accepted'
    volunteer.save()

    return redirect('users:mypage', id=volunteer.post.writer.profile.id)

def reject_member(request, volunteer_id):
    volunteer = Volunteer.objects.get(id=volunteer_id)
    volunteer.info = 'rejected'
    volunteer.save()

    return redirect('users:mypage', id=volunteer.post.writer.profile.id)