from django.db import models
from toolshare.models import Usercorn, Tool, Request
from django.db.models.signals import post_save
from django.dispatch import receiver

class Notification(models.Model):
	title = models.CharField(max_length=250)
	message = models.TextField()
	viewed = models.BooleanField(default=False)
	sentby = models.IntegerField()
	receivedby = models.IntegerField()
	tool = models.IntegerField()
	requestID = models.IntegerField()
	# sentby = models.IntegerField()
	# receivedby = models.IntegerField()
	# tool = model.IntegerField()

@receiver(post_save, sender = Request)
def borrow_notification(sender, **kwargs):
	if kwargs.get('created', False):
		r = kwargs.get('instance')
		if r.rtype == 'B':
			n = Notification.objects.create(sentby = r.borrowerId,
		                                    receivedby = r.ownerId,
		                                    tool = r.toolId,
		                                    title = "Borrow Request for ",
		                                    message = r.message,
		                                    requestID = r.id
		                                    )
    # TODO: Create a logger for notification messages