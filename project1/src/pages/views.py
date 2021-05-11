from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account, Transaction, Message
from django.db.models import Q


@login_required
@requires_csrf_token
def transferView(request):
	
	if request.method == 'POST':
		userFrom = User.objects.get(username=request.user)
		userTo = User.objects.get(username=request.POST['to'])
		sumOfMoney = request.POST['amount']

		accountFrom = Account.objects.get(user=userFrom)
		accountTo = Account.objects.get(user=userTo)

		transaction = Transaction(sender=accountFrom.user.username,reciever=accountTo.user.username,amount=request.POST['amount'])
		transaction.save()

		if accountFrom.balance >= int(sumOfMoney) and int(sumOfMoney) >= 0:
			accountFrom.balance -= int(sumOfMoney)
			accountTo.balance += int(sumOfMoney)

			accountTo.save()
			accountFrom.save()

		else:
			return redirect('/')

	return redirect('/')

@login_required
def messageView(request):
	if request.method == 'POST':
		to = request.POST['to']
		text = request.POST['content']
		message = Message(content=text,reciever=to)
		message.save()
	return redirect('/')


@login_required
def homePageView(request):
	accounts = Account.objects.all()
	messages = Message.objects.filter(reciever=request.user)
	transactions = Transaction.objects.filter(Q(sender=request.user.username) | Q(reciever=request.user.username))
	return render(request, 'pages/index.html', {'accounts': accounts, 'transactions': transactions, 'messages': messages})