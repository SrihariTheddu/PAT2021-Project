# PAT2021-Project

#Introduction
This is an Web Application to track the performance of a student in competetive programming of particular institution
It tracks the performance of a a particular student on different platforms.And their supervisors can able to moniter the performance of student.

#Tools Used
In this application we use python Django Frame Work, In addition with traditional markup languages......
Backend  :-   Python Django Web Frame work
Frontend :-   HTML,CSS and JAVASCRIPT

#Layout
   Here is the Directory of our project
   >mysite
   __init__.py
   *settings.py
   *urls.py
   *asgi.py
   >myapp
   *__init__.py
   *admin.py
   *models.py
   *test.py
   *urls.py
   *views.py
   >static
   *designs
   *root
   >Templates
   Contains all web Templates
   >manage.py
   >db.sqlite3
   
 ##Installation
  
  ### Follow the steps to setup the projecct
  
  first of all, you need to check that django framework is installed on your machine
     
   use command :-  django-admin --version
   if you did not installed it then use command
   
   command :-  pip install django
   then you need to install pillow library to work with images in django
   command :- pip install pillow
   
   than go to project directory and check the project
   command:- python manage.py check
   
   if there are any error and warning than fix them
   
   Load your static files into static directory
   command:  python manage.py collectstatic
   
   Than apply all the migrations to database
   command :-   python manage.py makemigrations
   
   if there are any errors or warning than fix them
   
   Now use migrate command to make changes
   command:- python manage.py migrate
   
   Now create a super user key to access adminsite
   command:- python manage.py createsuperuser
   
   and follow the instructions to create super user
   
   Now create cache table by using command
   command:- python manage.py createcachetable
   
   **** Now you are all set ****
   now run your website by using
   command :- python manage.py runserever
   
   
 
 
 
 
 
 
 
 
 
 
 
 
 
 



