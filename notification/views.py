from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import Notification
from toolshare.models import Tool, Usercorn

def show_notification(request, notification__id):
	n = Notification.objects.get(pk = notification__id)
	user = Usercorn.objects.get(pk = n.receivedby)
	tool = Tool.objects.get(pk = n.toolId)
	return render_to_response('notification.html', {'notification':n},
													{'username': user},
													{'tool': tool},

													)

def mark_notification(request, notification__id):
	n = Notification.objects.get(id = notification__id)
	n.viewed = True
	n.save()
	return HttpResponseRedirect('toolshare/notificationcenter')