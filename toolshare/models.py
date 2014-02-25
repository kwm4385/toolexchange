from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import *
from datetime import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.messages import constants as message_constants
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
import uuid
import os

MESSAGE_TAGS = {
    message_constants.DEBUG: 'info',
    message_constants.ERROR: 'danger',
}

"""
Generates a random, unique name for a file.
"""
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename   


"""
Defines the Model of a User of Toolshare application  
"""
class Usercorn(User):
    sharezone = models.IntegerField()
    shed = models.IntegerField(default=-1)
    
    def __str__(self):
        return self.username
    
    def get_sharezone(self):
        return self.sharezone
    
    def get_shed(self):
        return ToolShed.objects.get(id=self.shed)

"""
Defines the Model for a Tool in the TolShare application
"""
class Tool(models.Model): 
    CONDITIONS = [('P', 'Poor'),
                  ('F', 'Fair'),
                  ('G', 'Good'),
                  ('N', 'New'),
                  ]
    
    name = models.CharField(max_length=30)
    owner = models.IntegerField()   # Stores owner's id
    description = models.CharField(max_length=250, blank=True)
    image = models.FileField(default="default.jpg", upload_to=get_file_path)
    condition = models.CharField(max_length=1, choices=CONDITIONS, default ='G')
    category = models.CharField(max_length=100)     # Stores keys for the item
    registered = models.DateField(auto_now_add=True)
    shed = models.IntegerField(blank = True, null = True)    # Stores the home shed id
    borrower = models.IntegerField(blank = True, null = True)
    sharezone = models.PositiveIntegerField(max_length=5)
    dueDate = models.DateField(blank = True, null = True)
    
    def __str__(self):
        return self.name
    
    def get_name(self):
        return self.name
    
    def get_owner(self):
        # Returns a Usercorn object
        return Usercorn.objects.get(id=self.owner)
    
    def get_description(self):
        return self.description
    
    def get_category(self):
        return self.category
    
    def get_location(self):
        return self.location
    
    def get_borrower(self):
        return Usercorn.objects.get(id = self.borrower)
    
    def get_shed(self):
        return ToolShed.objects.get(id=self.shed)

"""
Defines the Model of a ToolShed in the ToolShare application
"""
class ToolShed(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    sharezone = models.IntegerField(blank=True)   # zipcode
    manager = models.IntegerField(blank=True)     # Stores manager id
    homeShare = models.BooleanField(verbose_name = "Home Share")
    transactions = models.IntegerField(default = 0)
    managerName = models.CharField(blank=True, max_length=15)
    
    def __str__(self):
        return self.name
    
    def get_name(self):
        return self.name
    
    def get_sharezone(self):
        return self.sharezone
    
    def get_manager(self):
        # Returns a Usercorn object
        return Usercorn.objects.get(id=self.manager)
     
"""
Defines the Model of a Request model in the ToolShare application
"""    
class Request(models.Model):
    REQUEST_TYPE = [
           ('B', 'Borrow'),               
           ('R', 'Return'),
           ]
    REQUEST_STATUS=[
            ('P','Pending'),
            ('A','Accepted'),
            ('D','Denied'),
            ]
    rtype = models.CharField(max_length=1, choices=REQUEST_TYPE, default ='B')
    rstatus = models.CharField(max_length=1, choices=REQUEST_STATUS, default ='P')
    toolId = models.IntegerField()
    ownerId = models.IntegerField()
    borrowerId = models.IntegerField()
    message = models.TextField(blank=False)
    dueDate = models.DateField()
    viewed_borrower=models.BooleanField(default=True)
    viewed_owner=models.BooleanField(default=False)

    def __str__(self):
        if self.rtype == 'B':
            if self.rstatus == 'A':
                return 'Accepted Borrow Request'
            elif self.rstatus == 'D':
                return 'Denied Borrow Request'
            else:
                return 'Pending Borrow Request'
        elif self.rtype == 'R':
            if self.rstatus == 'A':
                return 'Accepted Return Request'
            else:
                return 'Pending Return Request'
            
@receiver(post_delete, sender=Tool)
def tool_post_delete_handler(sender, **kwargs):
    tool = kwargs['instance']
    storage, path = tool.image.storage, tool.image.path
    if not "default.jpg" in path:
        storage.delete(path)
   
            