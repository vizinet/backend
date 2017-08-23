# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.

"""
# Django Libraries
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from django.core.mail import send_mail

# Custom Django
from forms import UserCreationForm, EditProfileForm
from file_upload.models import Picture
from user_profile.models import AuthToken, AirpactUser
from spirit.user.models import UserProfile as spirit_user

# Other
import json
import random
import string


# TODO:
# Log in with either username or email
#

# Are we debugging?
def debugging():
    return True

# Generate a random string with characters and intigers to act as a new
# password


def random_password(
        size=6,
        chars=string.ascii_uppercase +
        string.digits +
        string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

# Has the user forgotten the password


def forgot_password(request):
    Errors = ""
    Messages = ""

    # Show the user the Form on a get request
    if request.method == 'GET':
        Messages = "Reset Password Here:"

    # Parse the form on a post request
    elif request.method == 'POST':

        entered_username = request.POST['username']

        # Did the user enter an email?
        if '@' in entered_username:
            this_email = entered_username
            user = AirpactUser.objects.filter(email=this_email)
            if len(user) > 0:
                # Grab the first user who matches this email (There should only
                # be one)
                user = user[0]
            else:
                Errors = "That email Does not exist"
                user = None

        # Did the user enter a username?
        else:
            user = AirpactUser.objects.filter(username=entered_username)
            if len(user) < 1:
                Errors = "That username does not exist"
                user = None
            else:
                user = user[0]

        # Do we have a valid user
        if user is not None:
            new_password = random_password(random.randint(6, 12))
            user.set_password(new_password)
            try:
                user.save()
            except Exception as e:
                Errors = "There was an error resetting your password, please try again. "
                print(e)
                return render_to_response(
                    'forgot_password.html', {
                        'Errors': Errors, 'Messages': Messages}, context_instance=RequestContext(request))

            # Send duh email to duh person
            send_mail(
                'Your new Password to airpactfire',
                'This is your new password to airpacfire@eecs.wsu.edu!, please take care of it: ' + new_password,
                'airpactfire@gmail.com',
                ["" + user.email],
                fail_silently=False,
            )
            Messages = "Your password has been successfully reset! Your new password will be sent to your email account."

    return render_to_response('forgot_password.html',
                              {'Errors': Errors,
                               'Messages': Messages},
                              context_instance=RequestContext(request))

# View the user profile


@login_required
def user_profile(request):
    if request.user.is_certified is False:
        return render_to_response('not_certified.html')
    if(request.method == 'POST'):
        form = UserProfileForm(request.POST, instance=request.user.profile)

# Login page


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

# Logout page


@login_required
def logout(request):
    auth.logout(request)
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

# Authenticate the user


def auth_view(request):

    if request.method == 'POST':
        request.POST._mutable = True

        entered_username = request.POST['username']
        password = request.POST['password']

        # Is the user logging in with an email?
        if '@' in entered_username:
            this_email = entered_username
            user = AirpactUser.objects.filter(email=this_email)

            if len(user) > 0:
                user = user[0]

                request.POST['username'] = user.username
                user = auth.authenticate(
                    username=user.username, password=password)

            # There is no user with this email
            else:
                if(debugging()):
                    print("Failed to authenticate!")
                user = None

        # If we are authenticating with a regular username
        else:
            user = auth.authenticate(
                username=entered_username, password=password)

        if debugging():
            print(user)

        if user is not None:
            try:
                request.POST._mutable = False

                if (debugging()):
                    print("Logging in! ")

                test_var = auth.login(request, user)

                if(debugging()):
                    print(test_var)

            except Exception as e:
                print("Failed to log in!")
                return render_to_response(
                    'login.html', {
                        'Errors': e.message}, context_instance=RequestContext(request))

            return HttpResponseRedirect(
                "/user/profile/" + user.username + "/1")

        # User is NOTHING
        else:
            return render_to_response('login.html',
                                      {'Errors': "Invalid username or Password"},
                                      context_instance=RequestContext(request))

    elif request.method == 'GET':
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)

# Correct login page


def loggedin(request):
    return render_to_response('loggedin.html')

# Invalid login page


def invalid_login(request):
    return render_to_response('invalid.html')

# Register / Create a new user


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # Send email to all of the admins
            for admin_user in AirpactUser.objects.filter(is_custom_admin=True):
                send_mail(
                    'A New user has registered on airpacfire.eecs.wsu.edu',
                    'User ' + form.cleaned_data['username'] + ' has registered on the site',
                    'airpactfire@gmail.com',
                    ["" + admin_user.email],
                    fail_silently=False,
                )

            return HttpResponseRedirect('/user/')
        else:
            return render_to_response(
                'register.html', {
                    'form': form}, context_instance=RequestContext(request))
    form = UserCreationForm()
    return render_to_response(
        'register.html', {
            'form': form}, context_instance=RequestContext(request))

# Registration successful page


def register_success(request):
    return render_to_response('register_success.html',
                              {'message': "successfull registration! "},
                              context_instance=RequestContext(request))

# Authentication for the app


@csrf_exempt
def user_app_auth(request):
    if request.method == 'POST':
        userdata = json.loads(request.body)
        user = auth.authenticate(
            username=userdata['username'],
            password=userdata['password'])
        response_data = {}
        if user is not None and user.is_certified:
            # generate secret key
            secret = ''.join(
                random.SystemRandom().choice(
                    string.ascii_uppercase +
                    string.digits) for _ in range(22))
            secretKey = AuthToken(token=secret)
            secretKey.save()
            response_data['isUser'] = 'true'
            response_data['secretKey'] = secret
        else:
            response_data['isUser'] = 'false'
            response_data['secretKey'] = ''
        # print(json.dumps(response_data))
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")
    else:
        return HttpResponse("HI")

# View the user profile


def view_profile(request, name, page=1):
    # we need to get the current user info
    # send it to the view...so lets do that I guess
    thisuser = False
    if request.user.username == name:
        thisuser = True
    user = AirpactUser.objects.get(username=name)
    userpictures = Picture.objects.filter(user=user)
    paginator = Paginator(userpictures, 12)  # show 12 per page
    try:
        pictures = paginator.page(page)
    except PageNotAnInteger:
        pictures = paginator.page(1)
    except EmptyPage:
        pictures = paginator.page(paginator.num_pages)
    return render_to_response('user_profile.html',
                              {'pictures': pictures,
                               'profile_user': user,
                               'thisuser': thisuser},
                              context_instance=RequestContext(request))

# What is used to edit the user's profile


@login_required
def edit_profile(request):
    if request.user.is_certified is False:
        return render_to_response('not_certified.html')

    userob = AirpactUser.objects.get(username=request.user.username)
    if request.method == 'POST':
        # do stuff to save the new user data
        form = EditProfileForm(request.POST)
        if form.is_valid():
            userob.first_name = form.cleaned_data.get('first_name')
            userob.last_name = form.cleaned_data.get('last_name')
            userob.bio = form.cleaned_data.get('bio')

            # Make sure the email is unique
            this_email = form.cleaned_data.get('email')
            other_user = AirpactUser.objects.filter(email=this_email)
            if other_user is not None:
                userob.email = form.cleaned_data.get('email')

            # Set the password
            if form.cleaned_data.get('password') is not None:
                userob.set_password(form.cleaned_data.get('password'))

            userob.save()
        # reidrect back to their profile
        return HttpResponseRedirect(
            '/user/profile/' + request.user.username + '/')
    form = EditProfileForm(instance=userob)
    pictures = Picture.objects.filter(user=userob)
    return render_to_response('edit_profile.html',
                              {'user': request.user,
                               'form': form,
                               'pictures': pictures},
                              context_instance=RequestContext(request))


@login_required
def manage_pictures(request):
    userob = AirpactUser.objects.get(username=request.user.username)
    pictures = Picture.objects.filter(user=userob)
    return render_to_response(
        'manage_pictures.html', {
            'pictures': pictures}, context_instance=RequestContext(request))

# The custom admin page


@csrf_exempt
@login_required
def admin_page(request):
    if request.user.is_custom_admin is False:
        return HttpResponseRedirect('/')
    if request.user.is_certified is False:
        return render_to_response('not_certified.html')

    nusers = AirpactUser.objects.all()
    if(request.method == 'POST'):

        username = request.POST.get("ourUser", False)

        # Nuser is the user for the airpacfire site
        nuser = AirpactUser.objects.get(username=username)

        # Suser is the user for the spirit forums
        suser = spirit_user.objects.get(user=nuser)

        if debugging():
            print("Spirit user: ")
            print(suser)
            print("are we verified?")
            print(suser.is_verified)

        the_type = request.POST['the_type']

        if(the_type == "certify"):
            nuser.is_certified = True
            suser.is_verified = True
            nuser.save()
            suser.save()

            # Send duh email to duh person
            send_mail(
                'You are now airpact certified!',
                'Congradulations! You are now a certified user of airpacfire@eecs.wsu.edu!',
                'airpactfire@gmail.com',
                ["" + nuser.email],
                fail_silently=False,
            )

        # Uncertify the user
        if(the_type == "uncertify"):
            nuser.is_certified = False
            suser.is_verified = False
            nuser.save()
            suser.save()

        # Certify the user
        if(the_type == "make_admin"):
            nuser.is_custom_admin = True
            suser.is_administrator = True
            suser.is_moderator = True
            suser.is_verified = True
            nuser.save()
            suser.save()

            # Send duh email to duh person
            send_mail(
                'You are now an administrator to airpacfire.eecs.wsu.edu',
                'Congradulations! You are now an administrator to airpacfire@eecs.wsu.edu!',
                'airpactfire@gmail.com',
                ["" + nuser.email],
                fail_silently=False,
            )

        # Make the user not an admin
        if(the_type == "unmake_admin"):
            nuser.is_custom_admin = False
            nuser.is_superuser = False
            suser.is_administrator = False
            suser.is_moderator = False
            suser.i_verified = False
            nuser.save()

        # Delete the user
        if(the_type == "delete"):
            nuser.delete()

            # Send duh email to duh person
            send_mail(
                'Your account has been removed from airpacfire.eecs.wsu.edu',
                'Due to unfortunate circumstances, your account is now removed from airpactfire. ' +
                'Please contact your administrator for questions',
                'airpactfire@gmail.com',
                ["" + nuser.email],
                fail_silently=False,
            )

    return render_to_response(
        'custom_admin_page.html', {
            'nusers': nusers}, context_instance=RequestContext(request));
