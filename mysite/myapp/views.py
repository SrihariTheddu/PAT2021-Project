from django.views.generic import (TemplateView, DetailView,ListView,UpdateView)
from django.shortcuts import (render, redirect)
from django.contrib import messages
from django.core.cache import cache
from myapp.models import (UserModel,OnlineJudge,MyAdmin)
import pandas as pd


#..........................................................................................
# HomePage
# This is the Home page of website
class HomePageView(TemplateView):
    template_name = "HomePage.html"

    def get_context_data(self, **kwargs):
        kwargs.update({'main_template':'HomeIndexPage.html'})
        return super().get_context_data(**kwargs)

#Login Page(SignInPage) of the website...............
# it takes arguments as user credentials and authenticates the credentials of the user...
class LoginPageView(TemplateView):
    template_name = "HomePage.html"

    def get_context_data(self, **kwargs):
        kwargs.update({'main_template':'SignInPage.html'})
        return super().get_context_data(**kwargs)

    def post(self,request,**kwargs):
        username = request.POST['username']
        password = request.POST['password']
        try:
            # if it is admin..............
            #than redirect to admin Interface
            if username =='admin':
                return redirect('myapp:admin-dashboard')

            user = UserModel.objects.get(username =username)

            # check if user is blocked..........
            if user.is_blocked:
                messages.add_message(request,20,"You are blocked by the admin...")
                return redirect('myapp:home')

            # authenticate the user ................
            if user.authenticate(password):
                cache.set('user',user)
                return redirect("myapp:user-dashboard",pk=user.pk)

        except Exception as e:

            messages.add_message(request,20,"Invalid Username or Password")
            return redirect('myapp:login')

# Registration Form View................................
# This form is used to Register the user
class RegisterUserView(TemplateView):
    template_name = "HomePage.html"

    def get_context_data(self, **kwargs):
        kwargs.update({'main_template':'SignUpPage.html'})
        return super().get_context_data(**kwargs)

    def post(self,request,**kwargs):
        #Trying the create the object with the given data
        try:
            UserModel(username = request.POST['username'], password="password", email=request.POST['mail'], roll_number = request.POST["roll_number"], branch = request.POST["branch"],yop= request.POST["yop"]).save()
            messages.add_message(request,20,"User Registered Successfully")
            return redirect('myapp:login')
        except Exception as e:
            messages.add_message(request,20,'Enter valid data')
            return redirect('myapp:register')




# Student InterFace Views......................................................................................
class StudentDashBoardView(DetailView):
    model = UserModel
    template_name = 'StudentDashBoardPage.html'
    context_object_name = "user"

    def get_context_data(self,**kwargs):
        performers = OnlineJudge.objects.order_by("score")
        reversed(performers)
        total = len(performers)
        kwargs.update({'main_template':"FilterDataPage.html",'accounts':self.object.accounts.all(),'performers':performers,'total':str(total),'count':total})
        return super().get_context_data(**kwargs)

#.................................................................................................................
class StudentOJAccountListView(DetailView):
    model = UserModel
    template_name = 'StudentDashBoardPage.html'
    context_object_name = "user"

    def get_context_data(self,**kwargs):
        kwargs.update({'main_template':"StudentOJAccountListPage.html",'accounts':self.object.accounts.all(),'toppers':reversed(OnlineJudge.objects.order_by("score")),'title':'LeaderBoard'})
        return super().get_context_data(**kwargs)


#.....................................................................................................................
class AddOJAccountView(TemplateView):
    template_name = "StudentDashBoardPage.html"

    def get_context_data(self,**kwargs):
        kwargs.update({'accounts':cache.get('user').accounts.all(),'main_template':'AddOJAccountPage.html','user':cache.get('user')})
        return super().get_context_data(**kwargs)

    def post(self,request,**kwargs):
        #Read the data from the server.........
        cp = OnlineJudge(host = request.POST['host'],username = request.POST['username'],rank = int(request.POST['rank']),stars = int(request.POST['stars']),score=int(request.POST['score']))
        # Trying the save the data
        try:
            cp.save()
            user = cache.get('user')
            user.accounts.add(cp)
            messages.add_message(request,20,f'Account added successfully')
            return redirect('myapp:user-accounts',pk=user.pk)
        except:
            messages.add_message(request,20,"Invalid data")
            return redirect('myapp:add-account')




class AccountUpdatePageView(DetailView):
    model = OnlineJudge
    template_name = "StudentDashBoardPage.html"
    context_object_name = 'account'

    def get_context_data(self,**kwargs):
        kwargs.update({'accounts':cache.get('user').accounts.all(),'main_template':'StudentUpdateAccountPage.html','user':cache.get('user')})
        return super().get_context_data(**kwargs)

def updateAccount(request,**kwargs):
    account = OnlineJudge.objects.get(user_id=request.POST['user_id'])
    account.rank = int(request.POST['rank'])
    account.stars = int(request.POST['stars'])
    account.score= int(request.POST['score'])
    try:
        account.save()
        messages.add_message(request,20,f'Account updated successfully')
        return redirect('myapp:user-accounts',pk=cache.get('user').pk)
    except:
        messages.add_message(request,20,"Invalid data")
        return redirect('myapp:add-account')



class UserProfileView(DetailView):
    model = UserModel
    template_name = 'StudentDashBoardPage.html'
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        kwargs.update({'main_template': "StudentPersonalInfoPage.html",'accounts':cache.get('user').accounts.all()})
        return super().get_context_data(**kwargs)


class LogOutView(TemplateView):
    template_name = "SignOutPage.html"

    def post(self,request,**kwargs):
        cache.set('user',None)
        messages.add_message(request,20,'Logged Out Successfully............')
        return redirect("myapp:login")

#  Admin Interface.................................................................................................................................
class AdminDashBoardView(TemplateView):
    template_name = "AdminDashBoardPage.html"

    def get_context_data(self, **kwargs):
        performers = OnlineJudge.objects.order_by('score')
        reversed(performers)
        total = len(performers)
        try:
            performers = performers[:10]
        except:
            pass
        kwargs.update({'main_template':'FilterDataPage.html','performers':performers,'is_admin':True,'branch':"ALL","host":"ALL",'total':total,'count':10})
        return super().get_context_data(**kwargs)


class AdminStudentPerformanceDetailView(DetailView):
    model = OnlineJudge
    template_name = "AdminDashBoardPage.html"
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        kwargs.update({'main_template':'StudentOJAccountListPage.html','accounts':reversed(OnlineJudge.objects.filter(username=self.object.username)),'is_admin':True,'branch':'ALL','host':'ALL'})
        return super().get_context_data(**kwargs)


class AdminStudentsListView(ListView):
    model = UserModel
    template_name = "AdminDashBoardPage.html"
    context_object_name = 'students'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        kwargs.update({'main_template':'StudentsListPage.html','all_students':True,'is_admin':True})
        return super().get_context_data(**kwargs)

class AdminStudentProfileView(DetailView):
    model = UserModel
    template_name = "AdminDashBoard.html"
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        kwargs.update({'main_template':"StudentPersonalInfoPage.html",'is_admin': True})
        return super().get_context_data(**kwargs)

def DataFilterView(request):
    branch = request.POST['branch']
    host = request.POST['host']
    count = int(request.POST['count'])
    if branch!='ALL':
        if host!='ALL':
            s = OnlineJudge.objects.filter(usermodel__branch = branch,host=host)
        else:
            s = OnlineJudge.objects.filter(usermodel__branch = branch)
    else:
         if host!='ALL':
            s = OnlineJudge.objects.filter(host=host)
         else:
            s = OnlineJudge.objects.all()
    total = len(s)
    try:
        s = s[:count]
    except:
        count = len(s)

    cache.set('pagination',True)
    cache.set('objects',s)
    cache.set('limiter',count)
    cache.set('count',count)
    pages = total//count


    return render(request,'AdminDashBoardPage.html',{'main_template':'FilterDataPage.html','performers':s,'is_admin':True,'branch':branch,'host':host,'count':count,'total':total})



def StudentFilterView(request):
    branch = request.POST['branch']
    yop = request.POST['yop']
    count = int(request.POST['count'])
    if branch!='ALL':
        if yop!='ALL':
            s = UserModel.objects.filter(branch = branch,yop=yop)
        else:
            s = UserModel.objects.filter(branch = branch)
    else:
         if yop!='ALL':
            s = UserModel.objects.filter(yop=yop)
         else:
            s = UserModel.objects.filter()
    total = len(s)
    try:
        s = s[:count]
    except:
        count = len(s)
    return render(request,'AdminDashBoardPage.html',{'main_template':'StudentsListPage.html','students':s,'is_admin':True,'count':count,'total':total})


def AdminBlockAccountView(request,pk):
    account = OnlineJudge.objects.get(pk=pk)
    user = UserModel.objects.get(username=account.username)
    user.is_blocked = True
    user.save()
    return redirect('myapp:admin-performance-view',pk=account.pk)



def DownloadAsCSVFile(request,host,branch):
    if branch!='ALL':
        if host!='ALL':
            data = list(OnlineJudge.objects.filter(usermodel__branch=branch,host=host))
        else:
            data = list(OnlineJudge.objects.filter(usermodel__branch=branch))
    else:
        if host!='ALL':
            data = list(OnlineJudge.objects.filter(host=host))
        else:
            data = list(OnlineJudge.objects.all())
    df = pd.DataFrame(data)
    is_saved = False
    count = 0
    while not is_saved:
        try:
            fname = 'sheet' + str(count) +".csv"
            df.to_csv(fname)
            is_saved = True
        except:
            count += 1

    print('downloaded')
    return render(request,'AdminDashBoardPage.html',{'main_template':'FilterDataPage.html','performers':data,'is_admin':True,'host':host,'branch':branch})


def paginateFilterData(request):
    paginate = cache.get('pagination')
    if paginate:
        objects = cache.get('objects')
        limiter = cache.get('limiter')
        count = cache.get('count')
        total = len(objects)
        if count+limiter<total:
            objects = objects[count:count+limiter]
            count += limiter
            cache.set('count',count)
            return render(request,'AdminDashBoardPage.html',{'main_template':'FilterDataPage.html','performers':objects,'is_admin':True,'branch':'ALL','host':'ALL','count':count,'total':total})
        else:
            cache.set('pagination',False)
            cache.set('limiter',1)
            cache.set('count',0)
            objects = objects[count:]
            return render(request,'AdminDashBoardPage.html',{'main_template':'FilterDataPage.html','performers':objects,'is_admin':True,'branch':'ALL','host':'ALL','count':count,'total':total})
    return render(request,'AdminDashBoardPage.html',{'main_template':'FilterDataPage.html','performers':cache.get('objects'),'is_admin':True,'branch':'ALL','host':'ALL','count':len(cache.get('objects')),'total':len(cache.get('objects'))})





