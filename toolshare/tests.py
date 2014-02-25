"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
from toolshare.models import *
from datetime import *
from django.core.urlresolvers import reverse

def create_user(firstname, lastname, uname,):
    return Usercorn.objects.create( first_name = firstname, last_name=lastname, username=uname, email = "email@email.com", password = "password")

 
class UserTestCase(TestCase):
    def test_user_gets(self):
        Usercorn.objects.create(first_name="John", last_name="Sellers", username="John", email="pass@pass.com", password="password", sharezone=14623, shed=1)
        ToolShed.objects.create(name="test", location="here",sharezone=14623, manager=0, homeShare=True, transactions=0, managerName="joe")
        john=Usercorn.objects.get(username="John")
        self.assertEqual(john.get_sharezone(), 14623 , "Sharezone assigned incorrectly")
        self.assertEqual(john.get_shed(), ToolShed.objects.get(id=1), "Shed is assigned incorrectly")
      
class ToolTestCase(TestCase):
    def test_Tools(self):
        Tool.objects.create(name="wrench", owner=1, description="hits stuff", condition="G", category="hand tool", registered= datetime.now(), shed=1, borrower=1, sharezone=14623, dueDate=datetime.now())
        Usercorn.objects.create(first_name="John", last_name="Sellers", username="John", email="pass@pass.com", password="password", sharezone=14623)
        ToolShed.objects.create(name="test", location="here",sharezone=14623, manager=0, homeShare=True, transactions=0, managerName="joe")
        john=Usercorn.objects.get(email="pass@pass.com")
        hammer=Tool.objects.get(name= "wrench")
        self.assertEqual(hammer.get_name(), "wrench", "tool name does not copy correctly")
        self.assertEqual(hammer.get_owner(), john, "owner does not copy correctly")
        self.assertEqual(hammer.get_description(), "hits stuff", "tool description does not copy correctly")
        self.assertEqual(hammer.get_category(), "hand tool", "tool catagory does not copy correctly")
        self.assertEqual(hammer.get_borrower(),john,"borrower of tool is not set correctly")
        self.assertEqual(hammer.get_shed(), ToolShed.objects.get(id=1), "shed does not copy correctly")

class ToolShedTestCase(TestCase):
    def test_shed_gets(self):
        Tool.objects.create(name="wrench", owner=1, description="hits stuff", condition="G", category="hand tool", registered= datetime.now(), shed=1, borrower=0, sharezone=14623, dueDate=datetime.now())
        Usercorn.objects.create(first_name="John", last_name="Sellers", username="John", email="pass@pass.com", password="password", sharezone=14623)
        ToolShed.objects.create(name="test", location="here",sharezone=14623, manager=1, homeShare=True, transactions=0, managerName="John")
        shed=ToolShed.objects.get(name="test")
        john=Usercorn.objects.get(email="pass@pass.com")
        self.assertEqual(shed.get_name(),"test","name is not accessed correctly")
        self.assertEqual(shed.get_sharezone(),14623,"sharezone is not accessed correctly" )
        self.assertEqual(shed.get_manager(), john, "manager is not accessed correctly")
        
# class RequestTests(TestCase):
        
    
