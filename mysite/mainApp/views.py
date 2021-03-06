from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login, logout
from .forms import CommentForm, BackCallForm, LoginForm
from .models import Comment, Order, BackCall, Category
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib import messages
from .serializers import BackCallSerializer

class BackCallView(APIView):
    def get(self, request):
        backcall = BackCall.objects.all()
        serializer = BackCallSerializer(backcall, many=True)
        return Response({"backcall": serializer.data})

def index(request):
    comments = Comment.objects.filter(published=True).order_by('-datetime')
    amount = Comment.objects.filter(published=True).count()
    return render(request, 'index.html', {'comments':comments, 'amount': amount})

def profile(request):
    response = requests.get('http://api.ipstack.com/check?access_key=5f76bbb6c812076967c64cbde6084147')
    geodata = response.json()
    amount = BackCall.objects.all().count()
    return render(request, 'registration/profile.html', {
        'ip': geodata['ip'],
        'country': geodata['country_name'],
        'amount':amount,
    })

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Вход выполнен успешно!')
                return redirect('profile')
            else:
                messages.success(request, 'Аккаунт не существует')
        else:
            messages.warning(request, 'Пожалуйста, введите коректные имя пользователя и пароль.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('home')

def add_ajax(request):
    if request.is_ajax():
        first_text = 'Нашим клиентам мы гарантируем отличное качество обслуживания, короткие сроки изготовления заказа, высокий уровень профессионализма. '
        second_text = 'Обратившись в нашу компанию, Вы получите полную консультацию. Начиная от предварительной оценки объекта, которую Вы можете узнать как лично, так и по телефону, Viber, Telegram, WhatsApp или E-mail. Заканчивая изготовлением отчёта по экспертной оценке и полной консультацией по документам и налогам, необходимым для сделки.'

        response = {'first-text': first_text,
                    'second-text': second_text,}

        return JsonResponse(response)
    else:
        raise Http404

def aboutus(request):
    comments = Comment.objects.filter(published=True).order_by('-datetime')
    return render(request, 'about.html', {'comments':comments})

def contact(request):
    if request.method == 'POST':
        form = BackCallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = BackCallForm()

    return render(request, 'contact.html', {'form': form})

def comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks_for_the_comment')
    else:
        form = CommentForm()

    return render(request, 'comment.html', {'form': form})

def service(request):
    return render(request, 'service.html')

def order_online(request):
    return render(request, 'order_online.html')

def thanks_for_the_comment(request):
    return render(request, 'thanks_for_the_comment.html')

def thanks(request):
    return render(request, 'thanks.html')