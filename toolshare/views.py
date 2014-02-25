from django.contrib import messages 
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext, loader
from toolshare.forms import *
from toolshare.models import *
from notification.models import *
from datetime import *
from django.db.models import Q

"""
register_home is the view presented to any user not logged in. It contains information about the site, a registration
form, and a link to the login page for existing users.
@request is the information request from the django framework
@return: rendered view home page
"""    
def register_home(request):
    if request.method == 'POST': # If the form has been submitted
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            em = form.cleaned_data['email']
            if((Usercorn.objects.filter(username=user).exists() == True) or
               Usercorn.objects.filter(email=em).exists() == True):
                return HttpResponseRedirect('')
            fname = form.cleaned_data['firstname']
            lname = form.cleaned_data['lastname']
            pw = form.cleaned_data['password']
            zip = form.cleaned_data['zip']
            Usercorn.objects.create_user(first_name=fname, last_name=lname, username=user, email=em, password=pw, sharezone=zip)
            user = authenticate(username=user, password=pw)
            if user is not None:
                user.save()
                login(request, user)
            return HttpResponseRedirect('')
        else:
            return render(request, 'register_home.html', {'regform': form,})
    else: # Otherwise display registration page
        if request.user.is_authenticated():
            return HttpResponseRedirect("/dashboard/")
        else:
            form = RegisterForm()
            return render(request, 'register_home.html', {'regform': form,})


"""
log_in view presents a simple form for existing users to log in.

@request is the information request from the django framework
@return: rendered view of the login form
"""     
def log_in(request):
    if request.method == 'POST': # If the form has been submitted
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=user, password=pw)
            if user is not None:
                login(request, user)
                if request.GET.get('next') is not None:
                    return HttpResponseRedirect(request.GET.get('next'))
                else:
                    return HttpResponseRedirect('/dashboard/')
            else:
                return render(request, 'login.html', { 'logform': form, 'error': True})
        else:
            return render(request, 'login.html', { 'logform': form, 'error': True})
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect("/dashboard/")
        else:
            form = LoginForm()
            return render(request, 'login.html', { 'logform': form, })
"""
Logs out the currently logged in user who visits this page.

@request is the information request from the django framework
@return: an HTTP redirect to the register_home view
"""    
@login_required 
def log_out(request):
    logout(request)
    return redirect('/')

"""
The main page for logged in users. Displays an overview of the user's information and provides liks to
all major functions of the site.

@request is the information request from the django framework
@return: rendered view of the dashboard page
"""    
@login_required
def dashboard(request):
    borrowed_tools = Tool.objects.filter(borrower = request.user.id)
    loaned_tools = Tool.objects.filter(owner = request.user.id).exclude(borrower = None)
    
    context = {'borrowed_tools': borrowed_tools,
               'loaned_tools' : loaned_tools,
               'Usercorn' : Usercorn.objects,
               'Request' : Request.objects,
               }	
    return render(request, 'dashboard.html', context)

"""
tool_index is a function that pulls the data from the tool database and returns a rendered UI view of the tools that are available

@request is the information request from the django framework
@return: rendered view of the index of tools
"""    
@login_required
def tools_index(request):
    user = Usercorn.objects.get(id = request.user.id)
    search = request.GET.get('query')
    q1 = Tool.objects.filter(sharezone = user.sharezone).exclude(shed = 0)
    q2 = q1.filter( Q(name__contains=(search)) | Q(category__contains=(search)) | Q(description__contains=(search)) )
    tools_list = q2.order_by('-registered')
    context = {'tools': tools_list, 'search':search}
    return render(request, 'toolindex.html', context)

"""
view_tool is a function that pulls the data from the tool database and returns a rendered UI view of the specific tool that is requested by ID

@request is the information request from the django framework
@tool_id is the id in the database of the specific tool that is being requested
@return: rendered view for a tool
""" 
@login_required
def view_tool(request,tool_id):
    tool=get_object_or_404(Tool,pk=tool_id)
    if tool.shed is not 0:
        shed = ToolShed.objects.get(pk=tool.shed).name
    else:
        shed = "None"
    if shed == "None" and request.user.id != tool.owner:
        return HttpResponseForbidden()
    shed_options = {0 : "None (private)"}
    for entry in ToolShed.objects.filter(manager = request.user.id):
        shed_options[entry.id] = entry.name
    for entry in ToolShed.objects.filter(homeShare = False):
        shed_options[entry.id] = entry.name
    if Request.objects.filter(borrowerId = request.user.id, toolId = tool_id, rstatus="P").count() != 0:
        pending_request = True
    else:
        pending_request = False
    return render(request, 'toolView.html', {'tool':tool, 'toolowner':tool.get_owner(), 'toolshed':shed, 'shed_options':shed_options, 'pending_request':pending_request})

"""
personal_inventory is a function that pulls the data from the tool database and returns a rendered UI view of the tools that are owned by the specific user requested by ID

@request is the information request from the django framework
@user_id is the id of the database entry for the requested user
@return: rendered view of the user's inventory
""" 
@login_required
def personal_inventory(request):
    users_tools=Tool.objects.filter(owner=request.user.id)
    return render(request,'usertoolindex.html', {'users_tools':users_tools})

"""
add_tool is a function that appends a new tool to the tool database based on the user input from a form

@request is the information request from the django framework
@return: rendered view for adding a tool
""" 
@login_required
def addtool(request):
    """
    Adds a tool to the database where the owner is the current logged in user
    and the date tool is registered is the current time
    """
    if request.method == 'POST':
        form = ToolForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = Usercorn.objects.get(id=request.user.id)
            tool = form.save(commit=False)
            tool.owner = current_user.id
            tool.sharezone = current_user.sharezone
            tool.shed = 0
            form.save()
            messages.success(request, '"' + tool.name + '"' + ' has been created.')
            return HttpResponseRedirect('/toolView/'+str(tool.id))
    else :
        form = ToolForm()
            
    #  context of tool form fields to be shown
    return render(request, 'addtool.html', {'form': form})


"""
edit_tool is a function that allows users to edit tools they own and change the data of them

@request is the information request from the django framework
@tool_id is the requested tool id to edit
@return: rendered view for editing a tool
""" 
@login_required
def edittool(request, tool_id):
    tool = Tool.objects.get(pk=tool_id)
    
    if tool.owner != request.user.id:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form =  ToolForm(request.POST, request.FILES, instance=tool)
        if form.is_valid():
            form.save()
            messages.success(request, '"' + tool.name + '"' + ' has been updated.')
            return HttpResponseRedirect('/toolView/'+str(tool.id))
    
    else:
        form = ToolForm(instance=tool)
        
    return render(request, 'edittool.html', {'form': form, 'toolid': tool.id})

"""
remove_tool is a function that allows users to remove tools they own from the database 

@request is the information request from the django framework
@tool_id is the requested tool id to remove
@return: redirect to the tool_index
""" 
@login_required
def removetool(request, tool_id):
    tool = Tool.objects.get(pk=tool_id)
    toolname = tool.name
    tool.delete()
    messages.success(request, '"' + toolname + '"' + ' has been deleted.')
    return HttpResponseRedirect('/inventory/')


"""
make_Shed is a function that generates a form fills it with user input, generates a new shed,
then adds it to the database

@request is the information request from the django framework
@return: rendered view for adding a new shed
"""
@login_required
def make_Shed(request):
    if request.method == 'POST':
        user = Usercorn.objects.get(id = request.user.id)
        form = ShedForm(request.POST)
        if form.is_valid():
            #if(form.homeShare == True and user.shed != -1):
             #   return HttpResponseRedirect('/shedindex/')
            shed = form.save(commit=False)
#            if(shed.homeShare == True and user.shed != -1):
#                shed.delete()
#                return HttpResponseRedirect('/shedindex/')
#            elif(shed.homeShare == True):
#                user.shed = shed.id
            shed.sharezone = Usercorn.objects.get(pk = request.user.id).get_sharezone()
            shed.manager = request.user.id
            shed.managerName = request.user.username
            form.save()
            messages.success(request, '"' + shed.name + '"' + ' has been created.')
            return HttpResponseRedirect('/shedView/'+str(shed.id))

    else:
        form=ShedForm()
    
    return render(request,'makeshed.html',{'form':form})

"""
view_shed is a function that allows the user to view a registered public 
shed in the database

@request is the information request from the django framework
@tool_id is the id in the database of the specific shed that is being requested
@return: rendered view for a tool
""" 
@login_required
def view_shed(request,shed_id):
    shed=get_object_or_404(ToolShed,pk=shed_id)
    shed_tools=Tool.objects.filter(shed = shed.id)      
    return render(request, 'view_shed.html', {'shed': shed,'tools': shed_tools})

"""
Moves a tool into the specified shed

@request A request as specified by the Django Framework
@tool_id the database id of the tool to be moved
@shed_id the database id of the shed which the tool is to be moved into 
"""
@login_required
def move_tool(request):
    tool_id = request.GET.get('tool')
    shed_id = request.GET.get('shed')
    tool = get_object_or_404(Tool,pk=tool_id)
    if shed_id == '0' and tool is not None:
        tool.shed = 0
        tool.save()
        return HttpResponseRedirect('/toolView/' + str(tool.id))
    shed = get_object_or_404(ToolShed,pk=shed_id)
    if shed is not None and tool is not None:
        if request.user.id == shed.manager or not shed.homeShare:
            tool.shed = shed.id
            tool.save()
            return HttpResponseRedirect('/toolView/' + str(tool.id))
    return HttpResponseForbidden()

"""
Function is used to return a list of all Sheds in the sharezone
of the user

@param request A request as specified by the Django Framework
@return a list of all Sheds in the sharezone of the user
"""
@login_required
def shed_index(request):
    user = get_object_or_404(Usercorn, pk=request.user.id)
    sharezone_sheds=ToolShed.objects.filter(sharezone = user.sharezone)
    return render(request, 'shedIndex.html', {'sharezone_sheds': sharezone_sheds})

"""
Function used for a manager to delete a shed from the database

@param request A request as specified by the Django Framework
@param shed_id Id of the shed that you are deleting
@return The shed updated shed index after deletion if you have
permission to remove the shed
"""
def delete_shed(request, shed_id):
    shed = get_object_or_404(ToolShed, pk=shed_id)
    if (request.user.id == shed.manager):
        shed_tools=Tool.objects.filter(shed = shed.id) 
        for tool in shed_tools:
            tool.shed = 0
            tool.save()
        shed.delete()
        messages.success(request, '"' + shed.name + '"' + ' has been deleted.')
        return HttpResponseRedirect('/shedindex/')
    else:
        return HttpResponseForbidden()

"""
Used to find a list of all the requests that can be viewed by the user
@param request A request as specified by the Django Framework
@return A rendered views Listing of all indexes that can be viewed by the user
"""
@login_required
def request_index(request):
    user = Usercorn.objects.get(pk=request.user.id)
    q1 = Request.objects.filter(ownerId = user.id)
    q2 = Request.objects.filter(borrowerId = user.id)
    request_list = list(q1) + list(q2)
    context = {'request_list': request_list}
    return render(request, 'requestindex.html', context)


"""
Displays all of the requests
@param request A request as specified by the Django Framework
@return a rendered view of the notification
"""
@login_required
def notification(request):
    new_share_request = Request.objects.filter(ownerId = request.user.id, viewed_owner = False)
    new_borrow_request = Request.objects.filter(borrowerId = request.user.id, viewed_borrower = False)
    lend_request = Request.objects.filter(ownerId = request.user.id, viewed_owner = True)
    borrow_request = Request.objects.filter(borrowerId = request.user.id, viewed_borrower = True)
    return render_to_response('notificationcenter.html',
                                {'username': request.user.username},
                                {'new_share': new_share_request},
                                {'new_borrow': new_borrow_request},
                                {'share' : lend_request},
                                {'borrow' : borrow_request}
                                )

"""
Creates a new Request
@param tool_id Id of the tool that is under question
@param request A request as specified by the Django Framework
@param return a redirected view of the tool 
"""
@login_required
def make_request(request, tool_id):
    if Request.objects.filter(borrowerId = request.user.id, toolId = tool_id, rstatus = "P").count() != 0:
        return HttpResponseRedirect('/requestview/'+ str(Request.objects.get(borrowerId = request.user.id).id))
    if request.method == 'POST':
        form=RequestForm(request.POST)
        if form.is_valid():
            current_user = request.user
            req = form.save(commit=False)
            req.borrowerId = current_user.id
            req.ownerId= Tool.objects.get(id=tool_id).owner
            req.toolId = tool_id
            req.dueDate = datetime.now()+timedelta(days=7)
            form.save()
            messages.success(request, 'Borrow request created.')
            return HttpResponseRedirect('/requestview/' + str(req.id))
        else:
            tool = Tool.objects.get(pk=tool_id)
            return render(request, 'makerequest.html', {'form': form, 'tool': tool})
    else:
        form = RequestForm()
        tool = Tool.objects.get(pk=tool_id)
        return render(request, 'makerequest.html', {'form': form, 'tool': tool})

"""
Function is used to view a request. Sets the request as seen for the
user
@param request_id A id of the request object
@param request A request as specified by the Django Framework
@return a rendered view of the request
"""
@login_required      
def view_request(request, request_id):
    req = get_object_or_404(Request, pk=request_id)
    tool = get_object_or_404(Tool, pk=req.toolId)
    if (request.user.id == req.ownerId or request.user.id == req.borrowerId):
        lender_view = False
        if (request.user.id == req.ownerId):
            lender_view = True
            req.viewed_owner = True;
            req.save()
        if (request.user.id == req.borrowerId):
            req.viewed_borrower = True;
            req.save()
        return render(request,'requestview.html', {'req':req, 'tool':tool, 'lender_view':lender_view,
                                                   'borrower':Usercorn.objects.get(pk=req.borrowerId),
                                                   'lender':Usercorn.objects.get(pk=req.ownerId), })
    else:
        return HttpResponseForbidden()

"""
Function called when a request is accepted. It handles any type of
request
@param request A request as specified by the Django Framework
@param request_id The id for the request that is being accepted
@return the view of the updated requestindex  or httpForbidden if 
you don't have the correct permissions 
"""
@login_required
def accept_request(request, request_id):
    req = get_object_or_404(Request, pk=request_id) 
    tool = get_object_or_404(Tool, pk=req.toolId)
    if (req.rtype == 'B' and request.user.id == req.ownerId):
        req.rstatus = 'A'
        req.viewed_borrower = False;
        tool.borrower = req.borrowerId
        tool.dueDate = datetime.now() + timedelta(days=7)
        tool.save()
        req.save()
        messages.success(request, 'Tool request accepted.')
        return HttpResponseRedirect('/requestindex')
    elif (req.rtype == 'R' and request.user.id == req.ownerId):
        tool.borrower = None
        tool.dueDate = None 
        tool.save()
        req.delete()
        messages.success(request, 'Tool return request confirmed.')
        return HttpResponseRedirect('/requestindex/')
    else:
        return HttpResponseForbidden()

"""
Function called when a request is rejected. It handles any type of
request
@param request A request as specified by the Django Framework
@param request_id The id for the request that is being rejected
@return the view of the updated requestindex  or httpForbidden if 
you don't have the correct permissions 
"""
@login_required
def reject_request(request, request_id):
    req = get_object_or_404(Request, pk=request_id) 
    tool = get_object_or_404(Request, pk=req.toolId)
    
    if(request.user.id == req.ownerId):
        if (req.rtype == 'B'):
            req.rstatus = 'D'
            req.view_borrower = False 
            req.save()
            messages.success(request, 'Tool request declined.')
            return HttpResponseRedirect('/requestindex/')
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

"""
Function called when a request is being made to
return a too. It handles any type of request
@param request A request as specified by the Django Framework
@param request_id The id for the request that is being altered
@return a view of the request or httpForbidden if you don't have 
the correct permissions 
"""
@login_required  
def set_return(request, tool_id):
    tool = get_object_or_404(Tool, pk=tool_id)
    req = get_object_or_404(Request, toolId=tool.id)
#    borrowerId = req.borrowerId
#    ownerId= req.ownerId
#    toolId = req.toolId
#    dueDate = req.dueDate
    if(request.user.id == req.borrowerId):
        if (request.method == 'POST'):
            form = RequestForm(request.POST)
            if form.is_valid():
                print("I am in the right place")
                req.rtype = 'R'
                req.rstatus = 'P'
                req.view_owner = False
#                req.borrowerId = borrowerId
#                req.ownerId = ownerId
#                req.toolId = toolId
#                req.dueDate = dueDate
                #form.save()
                req.save()
                return HttpResponseRedirect('/requestview/' + str(req.id))
            else:
                tool = Tool.objects.get(pk=req.toolId)
                return render(request, 'setReturn.html', {'form': form, 'tool': tool})
        else:
            req.message = ""
            form = RequestForm()
            tool = Tool.objects.get(pk=req.toolId)
            return render(request, 'setReturn.html', {'form': form, 'tool': tool})
    else:
        return HttpResponseForbidden()
    
"""
Function used to view all the community statistics regarding
the usage of the website
NOTE NO LOGIN IS REQUIRED TO VIEW THE STATISTICS
@param request A request as specified by the Django Framework
@return a rendered view of the page holding the community statistics
"""
def community_statistics(request):
    if request.GET.get('sharezone') != None:
        sz = request.GET.get('sharezone')
    elif request.user.is_authenticated():
        sz = Usercorn.objects.get(pk=request.user.id).sharezone
    else:
        return HttpResponseForbidden()
    sz_requests = []
    for req in Request.objects.all():
        if Usercorn.objects.get(pk=req.ownerId).sharezone == sz:
            sz_requests.append(req)
    sz_tools = Tool.objects.filter(sharezone = sz)
    active_transactions= len(sz_requests)
    total_tools = sz_tools.count()
    available_tools = sz_tools.filter(borrower = None).count()
    shed_lst = ToolShed.objects.filter(sharezone = sz)
    total_sheds = shed_lst.count()
    
    all_sharezones = []
    total_sharezones = 0
    for c_user in Usercorn.objects.all():
        if c_user.sharezone not in all_sharezones:
            all_sharezones.append(c_user.sharezone)
            total_sharezones = total_sharezones + 1
    total_users = Usercorn.objects.filter(sharezone = sz).count()
    
    context = {
               'sharezone' : sz,
               'active_transactions': active_transactions,
               'total_tools': total_tools,
               'available_tools': available_tools,
               'total_sheds': total_sheds,
               'total_sharezones': total_sharezones,
               'total_users': total_users
               }
    return render(request, 'communityStats.html', context)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
     
