from toolshare.models import *
from django.db import connection

def pending_requests(request):
    q1 = Request.objects.filter(ownerId = request.user.id, viewed_owner=False)
    q2 = Request.objects.filter(borrowerId = request.user.id, viewed_borrower=False)
    new_requests = len(list(q1) + list(q2))
    return {"new_requests" : new_requests,
            "num_queries" : len(connection.queries)
            }