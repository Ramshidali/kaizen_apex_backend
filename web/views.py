#standerd
from datetime import date, timedelta
#django
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
# third party

# Create your views here.
def index(request):
    today_date = timezone.now().date()
    last_month_start = (today_date - timedelta(days=today_date.day)).replace(day=1)
    
    context = {
        'page_title' : 'Home | KAIZEN APEX',
        'is_dashboard': True,   
    }
  
    return render(request,'web/index.html', context)