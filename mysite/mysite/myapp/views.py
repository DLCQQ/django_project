from django.shortcuts import render, redirect

from django.views.generic import ListView

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login

# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world!")


def home(request):
    return render(request, 'home.html')


def product(request):
    # Заглушки данных о заказах
    orders = [
        {'id': 1, 'name': 'Заказ 1'},
        {'id': 2, 'name': 'Заказ 2'},
        {'id': 3, 'name': 'Заказ 3'}
    ]

    return render(request, 'product.html', {'orders': orders})


@csrf_protect
def my_view(request):
    if request.method == 'POST':
        # Получение данных из запроса
        data = request.POST.get('data')

        # Вывод данных в консоль
        print(data)

        return HttpResponse('Success')  # Возвращаем ответ

    else:
        return HttpResponse('Invalid request method')  # Возвращаем ошибку, если метод запроса не POST


