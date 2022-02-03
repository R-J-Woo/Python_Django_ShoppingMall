from functools import reduce
from django.shortcuts import redirect
from .models import User


def login_required(function):
    def wrap(request, *args, **kwargs):  # wrapping한 함수와, 기존 함수의 인자값을 맞춰주어야 한다
        user = request.session.get('user')
        if user is None or not user:  # user가 None이거나 비어있거나
            return redirect('/login')
        return function(request, *args, **kwargs)

    return wrap


def admin_required(function):
    def wrap(request, *args, **kwargs):  # wrapping한 함수와, 기존 함수의 인자값을 맞춰주어야 한다
        user = request.session.get('user')
        if user is None or not user:  # user가 None이거나 비어있거나
            return redirect('/login')

        user = User.objects.get(email=user)
        if user.level != 'admin':
            return redirect('/')

        return function(request, *args, **kwargs)

    return wrap
