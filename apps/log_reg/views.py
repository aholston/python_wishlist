from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.

def index(request):
    return render(request, 'log_reg/index.html')

def additem(request):
    return render(request, 'log_reg/additem.html')

def register(request):
    errors = User.objects.validate(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        pwHash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        newUser = User.objects.create(name=request.POST['name'], username=request.POST['username'], email=request.POST['email'], date_hired=request.POST['date_hired'], password=pwHash)
        request.session['userid'] = newUser.id

    return redirect('/success')

def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    wishlist = user.wishlist.all()
    items = Item.objects.exclude(wished_by=user)
    context = {
        'user': user,
        'wishlist': wishlist,
        'items': items
    }
    return render(request, 'log_reg/success.html', context)

def login(request):

    try:
        user = User.objects.get(username=request.POST['username'])

        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['userid'] = user.id
            return redirect('/success')
        else:
            message.error(request, 'Password invalid')
            return redirect('/')
    except Exception:
        messages.error(request, 'Username not found, please register or use a different username')
        return redirect('/')

def add(request):
    errors = Item.objects.validate(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/additem')
    else:
        user = User.objects.get(id=request.session['userid'])
        item = Item.objects.create(name=request.POST['item'], added_by=user)
        user.wishlist.add(item)
        user.save()

        return redirect('/success')

def delete(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('/success')

def remove(request, id):
    user = User.objects.get(id=request.session['userid'])
    item = user.wishlist.get(id=id)
    user.wishlist.remove(item)
    user.save()
    return redirect('/success')

def add_wish(request, id):
    user = User.objects.get(id=request.session['userid'])
    item = Item.objects.get(id=id)
    user.wishlist.add(item)
    return redirect('/success')

def show(request, id):
    item = Item.objects.get(id=id)
    context = {
        'item': item
    }
    return render(request, 'log_reg/show.html', context)

def logout(request):
    del request.session['userid']
    return redirect('/')
