from django.shortcuts import render


# Create your views here.

def anauthorised_opperation(request):
    return render(request, 'action_result/unauthorise_opperation.html', dict())
