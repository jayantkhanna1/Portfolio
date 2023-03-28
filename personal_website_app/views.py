from typing import List
from django.shortcuts import render,redirect
from .models import Accomplishments, Education, Job, Skills, Privatespace_users,Files,Static_website,Fullstack_website,Animations
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import mimetypes
from django.core.mail import send_mail
from passlib.hash import sha512_crypt as sha512
import os
from pathlib import Path
import datetime
from random import randrange
from django.http import HttpResponse
otp=0
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def index(request):
    try:
        edu_info=Education.objects.all()
        job_info=Job.objects.all()
        skill=Skills.objects.all()
        accomp=Accomplishments.objects.all()
        skill_list=list(skill)
        skill_list_1 = skill_list[:len(skill_list)//2]
        skill_list_2 = skill_list[len(skill_list)//2:]
        return render(request,'index.html',{'edu_info':edu_info,'job_info':job_info,'skill_1':skill_list_1,'skill_2':skill_list_2,'accomp':accomp})
    except:
        return render(request,'error.html')
def like(request):
    try:
        id=request.POST['text']
        acc=Accomplishments.objects.get(id=int((id)))
        likes=acc.likes+1
        acc.likes=likes
        acc.save()
        return redirect(request.META['HTTP_REFERER'])
    except:
        return render(request,'error.html')
def contact_email(request):
    try:
        name=request.POST["name"]
        email=request.POST["email"]
        subject=request.POST["subject"]
        message_temp=request.POST["message"]
        number=request.POST["number"]
        message="name: "+name+"\n number: "+number+"\n email: "+email+"\n subject: "+subject+"\n message: "+message_temp
        reciever=[os.environ.get('EMAIL')]
        send_mail(subject,message,os.environ.get('EMAIL'),reciever)
        messages.info(request,'MESSAGE SENT!')
        return redirect("index")
    except:
        return render(request,'error.html')
def privatespace_login(request):
    try:
        return render(request,'login.html')
    except:
        return render(request,'error.html')
def login(request):
    try:
        id=request.POST["id"]
        password=request.POST["pass"]
        password=sha512.hash(password, rounds=5000,salt=os.environ.get('SALT'))
        privateuser=Privatespace_users.objects.all()
        for x in privateuser:
            if( id==x.email and (password == x.password)):
                request.session['personal-website-id']= os.environ.get('SECRET_KEY_ALL_FILES')
                return redirect("privatespace")
            else:
                messages.info(request,'Wrong id or Password')
                return redirect("privatespace_login")
    except:
         return render(request,'error.html')
def forgotpass(request):
    try:
        otp=randrange(111111,999999)
        id=os.environ.get('EMAIL')
        send_mail("OTP","Your otp is= "+str(otp),os.environ.get('EMAIL'),[id])
        return render(request,'forgotpass.html',{'otp':otp})
    except:
        return render(request,'error.html')
def otp(request):
    try:
        return render(request,'changepass.html')
    except:
        return render(request,'error.html')
def changepass(request):
    #try:
        newpass=request.POST['password']
        newpasshash=sha512.hash(newpass, rounds=5000,salt=os.environ.get('SALT'))
        privateuser=Privatespace_users.objects.all()
        for x in privateuser:
            x.password=newpasshash
            x.save()
            return redirect("privatespace_login")
    #except:
     #   return render(request,'error.html')
def password_find(request):
    try:
        now=datetime.datetime.now()
        current_year=now.year
        lst=[]
        for x in range(1940, (current_year+1)):
            lst.append(x)
        return render(request,'cyber.html',{'years':lst})
    except:
        return render(request,'error.html')
def privatespace(request):
    try:
        data=request.session.get('personal-website-id',False)
        if(data==os.environ.get('SECRET_KEY_ALL_FILES')):
            dir=Files.objects.all()
            return render(request,'private.html',{'dir':dir})
        else:
            return redirect("privatespace_login")
    except:
        return render(request,'error.html')
def addfile(request):
    try:
        for file in request.FILES.getlist('file-upload'):
            dir=Files.objects.all()
            flag=0
            if(len(dir)!=0):
                for x in dir:
                    if(file.name==x.filename):
                        list(messages.get_messages(request))
                        messages.info(request,'File/s ALready Present')
                        flag=1
                if (flag==0) :
                    file_name = FileSystemStorage().save("files/"+file.name, file)
                    team_image = FileSystemStorage().url(file_name)
                    team_image = file.name
                    Files.objects.create(path='files/'+team_image,filename=team_image)
                flag=0
            else:
                file_name = FileSystemStorage().save("files/"+file.name, file)
                team_image = FileSystemStorage().url(file_name)
                team_image = file.name
                Files.objects.create(path='files/'+team_image,filename=team_image)
        return redirect('privatespace')
    except:
        return render(request,'error.html')
def editfile(request):
    try:
        newname=request.POST['newname']
        oldname=request.POST['oldname']
        if '.' in newname:
            pos=newname.rfind('.')
            newname=newname[0:pos]
        pos2=oldname.rfind('.')
        temp=oldname[pos2:]
        newname=newname+temp
        file=Files.objects.get(filename=oldname)
        os.rename('./media/'+str(file.path),'./media/files/'+newname)
        file.filename=newname
        file.path='files/'+newname
        file.save()
        return redirect('privatespace')
    except:
        return render(request,'error.html')
def deletefile(request):
    try:
        file=request.POST['filename']
        os.remove('./media/files/'+file)
        Files.objects.get(filename=file).delete()
        return redirect('privatespace')
    except:
        return render(request,'error.html')
def delete_all_files(request):
    try:
        files=Files.objects.all()
        for x in files:
            os.remove('./media/files/'+x.filename)
            x.delete()
        return redirect('privatespace')
    except:
        return render(request,'error.html')

def addeducation(request):
    try:
        name=request.POST['name']
        yearfrom=request.POST['yearfrom']
        yearto=request.POST['yearto']
        pergot=request.POST['pergot']
        pertot=request.POST['pertot']
        comment=request.POST['comment']
        edu=Education.objects.all()
        for x in edu:
            if x.name==name:
                messages.info(request,'Education already Present')
                return redirect('privatespace')
        else:
            Education.objects.create(name=name,year_from=yearfrom,year_too=yearto,per_got=pergot,per_total=pertot,comment=comment)
            return redirect('privatespace')
    except:
        return render(request,'error.html')
def editeducation(request):
    try:
        edu=Education.objects.all()
        return render(request,'editeducation.html',{'edu':edu})
    except:
        return render(request,'error.html')
def editeducationdata(request):
    try:
        id=request.POST['eduid']
        name=request.POST['name']
        yearfrom=request.POST['yearfrom']
        yearto=request.POST['yearto']
        pergot=request.POST['pergot']
        pertot=request.POST['pertot']
        comment=request.POST['comment']
        edu=Education.objects.get(id=id)
        edu.name=name
        edu.year_from=yearfrom
        edu.year_too=yearto
        edu.per_got=pergot
        edu.per_total=pertot
        edu.comment=comment
        edu.save()
        return redirect('editeducation')
    except:
        return render(request,'error.html')
def deleducationdata(request):
    try:
        id=request.POST['id']
        Education.objects.get(name=id).delete()
        return redirect('editeducation')
    except:
        return render(request,'error.html')
def addjob(request):
    try:
        name=request.POST['name']
        yearfrom=request.POST['yearfrom']
        yearto=request.POST['yearto']
        place=request.POST['place']
        comment=request.POST['comment']
        job=Job.objects.all()
        for x in job:
            if x.name==name:
                messages.info(request,'Job already Present')
                return redirect('privatespace')
        else:
            Job.objects.create(name=name,year_from=yearfrom,year_too=yearto,place=place,comment=comment)
            return redirect('privatespace')
    except:
        return render(request,'error.html')
def editjobpage(request):
    try:
        job=Job.objects.all()
        return render(request,'editjob.html',{'job':job})
    except:
        return render(request,'error.html')
def deljobdata(request):
    try:
        id=request.POST['id']
        Job.objects.get(name=id).delete()
        return redirect('editjobpage')
    except:
        return render(request,'error.html')
def editjobdata(request):
    try:
        id=request.POST['eduid']
        name=request.POST['name']
        yearfrom=request.POST['yearfrom']
        yearto=request.POST['yearto']
        place=request.POST['place']
        comment=request.POST['comment']
        job=Job.objects.get(id=id)
        job.name=name
        job.year_from=yearfrom
        job.year_too=yearto
        job.place=place
        job.comment=comment
        job.save()
        return redirect('editjobpage')
    except:
        return render(request,'error.html')
def addskill(request):
    try:
        name=request.POST['name']
        per=request.POST['per']
        skill=Skills.objects.all()
        for x in skill:
            if x.name==name:
                messages.info(request,'Skill already Present')
                return redirect('privatespace')
        else:
            Skills.objects.create(name=name,per=per)
            return redirect('privatespace')
    except:
        return render(request,'error.html')
def editskillpage(request):
    try:
        skill=Skills.objects.all()
        return render(request,'editskill.html',{'skill':skill})
    except:
        return render(request,'error.html')
def delskilldata(request):
    try:
        id=request.POST['id']
        Skills.objects.get(name=id).delete()
        return redirect('editskillpage')
    except:
        return render(request,'error.html')
def editskilldata(request):
    try:
        id=request.POST['skillid']
        name=request.POST['name']
        per=request.POST['per']
        skill=Skills.objects.get(id=id)
        skill.name=name
        skill.per=per
        skill.save()
        return redirect('editskillpage')
    except:
        return render(request,'error.html')
def addaccomp(request):
    try:
        name=request.POST['accomp-name']
        message=request.POST['message']
        url=request.POST['url']
        img=request.FILES['accomp-img']
        likes=int(10)
        accomp=Accomplishments.objects.all()
        for x in accomp:
            if x.name==name:
                messages.info(request,'Accomplishment already Present')
                return redirect('privatespace')
        else:
            file_name = FileSystemStorage().save("pics/accomplishments/"+img.name, img)
            team_image = FileSystemStorage().url(file_name)
            team_image='pics/accomplishments/'+img.name
            Accomplishments.objects.create(name=name,message=message,img=team_image,url=url,likes=likes)
            return redirect('privatespace')
    except:
        return render(request,'error.html')
def editaccomppage(request):
    try:
        accomp=Accomplishments.objects.all()
        return render(request,'editaccomppage.html',{'accomp':accomp})
    except:
        return render(request,'error.html')
def delaccompdata(request):
    try:
        id=request.POST['id']
        accomp=Accomplishments.objects.get(name=id)
        os.remove('./media/'+str(accomp.img))
        Accomplishments.objects.get(name=id).delete()
        return redirect('editaccomppage')
    except:
        return render(request,'error.html')
def editaccompdata(request):
    try:
        id=request.POST['accompid']
        name=request.POST['accomp-name']
        message=request.POST['message']
        url=request.POST['url']
        accomp=Accomplishments.objects.get(id=id)
        accomp.name=name
        accomp.message=message
        accomp.url=url
        accomp.save()
        return redirect('editaccomppage')
    except:
        return render(request,'error.html')
def websitepage(request):
    try:
        static=Static_website.objects.all()
        anim=Animations.objects.all()
        dynamic=Fullstack_website.objects.all()
        return render(request,'websites.html',{'static':static,'anim':anim,'dyno':dynamic})
    except:
        return render(request,'error.html')
def addstatic(request):
    try:
        name=request.POST['static-name']
        desc=request.POST['static-desc']
        url=request.POST['static-url']
        startdate=request.POST['static-start']
        enddate=request.POST['static-end']
        img=request.FILES['static-img']
        likes=int(10)
        accomp=Static_website.objects.all()
        for x in accomp:
            if x.name==name:
                messages.info(request,'Website already Present')
                return redirect('websitepage')
        else:
            file_name = FileSystemStorage().save("pics/static_website/"+img.name, img)
            team_image = FileSystemStorage().url(file_name)
            team_image='pics/static_website/'+img.name
            Static_website.objects.create(name=name,desc=desc,img=team_image,url=url,startdate=startdate,enddate=enddate,likes=likes,sheetname='static')
            return redirect('websitepage')
    except:
        return render(request,'error.html')
def editstatic(request):
    try:
        id=request.POST['static-id']
        name=request.POST['static-name']
        desc=request.POST['static-desc']
        url=request.POST['static-url']
        startdate=request.POST['static-start']
        enddate=request.POST['static-end']
        dyno=Static_website.objects.all()
        for x in dyno:
            if x.name==name:
                messages.info(request,'Name Can Not Be Same ')
                return redirect('websitepage')
        static=Static_website.objects.get(id=id)
        static.name=name
        static.desc=desc
        static.startdate=startdate
        static.enddate=enddate
        static.url=url
        static.save()
        return redirect('websitepage')
    except:
        return render(request,'error.html')
def delstatic(request):
    try:
        name=request.POST['name']
        static=Static_website.objects.get(name=name)
        os.remove('./media/'+str(static.img))
        Static_website.objects.get(name=name).delete()
        return redirect('websitepage')
    except:
        return render(request,'error.html')
def addanim(request):
    try:
        name=request.POST['name']
        desc=request.POST['desc']
        url=request.POST['url']
        startdate=request.POST['start']
        enddate=request.POST['end']
        img=request.FILES['img']
        likes=int(10)
        accomp=Animations.objects.all()
        for x in accomp:
            if x.name==name:
                messages.info(request,'Website already Present')
                return redirect('websitepage')
        else:
            file_name = FileSystemStorage().save("pics/animations/"+img.name, img)
            team_image = FileSystemStorage().url(file_name)
            team_image='pics/animations/'+img.name
            Animations.objects.create(sheetname='anim',name=name,desc=desc,img=team_image,url=url,startdate=startdate,enddate=enddate,likes=likes)
            return redirect('websitepage')
    except:
        return render(request,'error.html')
def editanim(request):
    try:
        id=request.POST['id']
        name=request.POST['name']
        desc=request.POST['desc']
        url=request.POST['url']
        startdate=request.POST['start']
        enddate=request.POST['end']
        dyno=Animations.objects.all()
        for x in dyno:
            if x.name==name:
                messages.info(request,'Name Can Not Be Same ')
                return redirect('websitepage')
        anim=Animations.objects.get(id=id)
        anim.name=name
        anim.desc=desc
        anim.startdate=startdate
        anim.enddate=enddate
        anim.url=url
        anim.save()
        return redirect('websitepage')
    except:
        return render(request,'error.html')
def delanim(request):
    try:
        name=request.POST['name']
        anim=Animations.objects.get(name=name)
        os.remove('./media/'+str(anim.img))
        Animations.objects.get(name=name).delete()
        return redirect('websitepage')
    except:
        return render(request,'error.html')
def adddyno(request):
    try:
        name=request.POST['name']
        desc=request.POST['desc']
        url=request.POST['url']
        startdate=request.POST['start']
        enddate=request.POST['end']
        img=request.FILES['img']
        likes=int(10)
        dyno=Fullstack_website.objects.all()
        for x in dyno:
            if x.name==name:
                messages.info(request,'Website already Present')
                return redirect('websitepage')
        else:
            file_name = FileSystemStorage().save("pics/dynamic/"+img.name, img)
            team_image = FileSystemStorage().url(file_name)
            team_image='pics/dynamic/'+img.name
            Fullstack_website.objects.create(sheetname='dyno',name=name,desc=desc,img=team_image,url=url,startdate=startdate,enddate=enddate,likes=likes)
            return redirect('websitepage')
    except:
        return render(request,'error.html')
def editdyno(request):
    try:
        id=request.POST['id']
        name=request.POST['name']
        desc=request.POST['desc']
        url=request.POST['url']
        startdate=request.POST['start']
        enddate=request.POST['end']
        dyno=Fullstack_website.objects.all()
        for x in dyno:
            if x.name==name:
                messages.info(request,'Name Can Not Be Same ')
                return redirect('websitepage')
        anim=Fullstack_website.objects.get(id=id)
        anim.name=name
        anim.desc=desc
        anim.startdate=startdate
        anim.enddate=enddate
        anim.url=url
        anim.save()
        return redirect('websitepage')
    except:
        return render(request,'error.html')
def deldyno(request):
    try:
        name=request.POST['name']
        anim=Fullstack_website.objects.get(name=name)
        os.remove('./media/'+str(anim.img))
        Fullstack_website.objects.get(name=name).delete()
        return redirect('websitepage')
    except:
        return render(request,'error.html')
def showanim(request):
    try:
        anim=Animations.objects.all()
        return render(request,'frontendwebsite.html',{'data':anim})
    except:
        return render(request,'error.html')
def showstatic(request):
    try:
        static=Static_website.objects.all()
        return render(request,'frontendwebsite.html',{'data':static})
    except:
        return render(request,'error.html')
def showdyno(request):
    try:
        dyno=Fullstack_website.objects.all()
        return render(request,'frontendwebsite.html',{'data':dyno})
    except:
        return render(request,'error.html')
def likeanim(request):
    try:
        id=request.POST['id']
        anim=Animations.objects.get(id=id)
        likes=anim.likes+1
        anim.likes=likes
        anim.save()
        return redirect('showanim')
    except:
        return render(request,'error.html')
def likedyno(request):
    try:
        id=request.POST['id']
        anim=Fullstack_website.objects.get(id=id)
        likes=anim.likes+1
        anim.likes=likes
        anim.save()
        return redirect('showdyno')
    except:
        return render(request,'error.html')
def likestatic(request):
    try:
        id=request.POST['id']
        anim=Static_website.objects.get(id=id)
        likes=anim.likes+1
        anim.likes=likes
        anim.save()
        return redirect('showstatic')
    except:
        return render(request,'error.html')










def findpass(request):
    try:
        fname=request.POST['fname']
        lname=request.POST['lname']
        date=request.POST['date']
        month=request.POST['month']
        year=request.POST['year']
        age=str(2021-int(year))
        passwords=[]
        comp1=date+month+year
        comp2=date+year+month
        comp3=month+date+year
        comp4=month+year+date
        comp5=year+month+date
        comp6=year+date+month
        comp7=age+comp1
        comp8=comp1+age
        comp9=age+comp2
        comp10=comp2+age
        comp11=age+comp3
        comp12=comp3+age
        comp13=age+comp4
        comp14=comp4+age
        comp15=age+comp5
        comp16=comp5+age
        comp17=age+comp6
        comp18=comp6+age
        
        #just name
        passwords.append(fname)
        passwords.append(lname)
        passwords.append(fname.capitalize())
        passwords.append(lname.capitalize())
        passwords.append(fname+lname)
        passwords.append(fname.capitalize()+lname.capitalize())
        passwords.append(lname.capitalize()+fname.capitalize())
        passwords.append(lname.capitalize()+fname)
        passwords.append(lname+fname.capitalize())
        passwords.append(fname.capitalize()+lname)
        passwords.append(fname+lname.capitalize())
        passwords.append(fname.capitalize()+fname.capitalize())
        passwords.append(fname+fname.capitalize())
        passwords.append(fname.capitalize()+fname)
        passwords.append(lname.capitalize()+lname.capitalize())
        passwords.append(lname+lname.capitalize())
        passwords.append(lname.capitalize()+lname)

        #with year
        passwords.append(fname+year)
        passwords.append(lname+year)
        passwords.append(fname.capitalize()+year)
        passwords.append(lname.capitalize()+year)
        passwords.append(fname+lname+year)
        passwords.append(fname.capitalize()+lname.capitalize()+year)
        passwords.append(lname.capitalize()+fname.capitalize()+year)
        passwords.append(lname.capitalize()+fname+year)
        passwords.append(lname+fname.capitalize()+year)
        passwords.append(fname.capitalize()+lname+year)
        passwords.append(fname+lname.capitalize()+year)
        passwords.append(fname.capitalize()+fname.capitalize()+year)
        passwords.append(fname+fname.capitalize()+year)
        passwords.append(fname.capitalize()+fname+year)
        passwords.append(lname.capitalize()+lname.capitalize()+year)
        passwords.append(lname+lname.capitalize()+year)
        passwords.append(lname.capitalize()+lname+year)
        passwords.append(year+fname)
        passwords.append(year+lname)
        passwords.append(year+fname.capitalize())
        passwords.append(year+lname.capitalize())
        passwords.append(year+fname+lname)
        passwords.append(year+fname.capitalize()+lname.capitalize())
        passwords.append(year+lname.capitalize()+fname.capitalize())
        passwords.append(year+lname.capitalize()+fname)
        passwords.append(year+lname+fname.capitalize())
        passwords.append(year+fname.capitalize()+lname)
        passwords.append(year+fname+lname.capitalize())
        passwords.append(year+fname.capitalize()+fname.capitalize())
        passwords.append(year+fname+fname.capitalize())
        passwords.append(year+fname.capitalize()+fname)
        passwords.append(year+lname.capitalize()+lname.capitalize())
        passwords.append(year+lname+lname.capitalize())
        passwords.append(year+lname.capitalize()+lname)
        passwords.append(fname+year+lname)
        passwords.append(fname.capitalize()+year+lname.capitalize())
        passwords.append(lname.capitalize()+year+fname.capitalize())
        passwords.append(lname.capitalize()+year+fname)
        passwords.append(lname+year+fname.capitalize())
        passwords.append(fname.capitalize()+year+lname)
        passwords.append(fname+year+lname.capitalize())
        passwords.append(fname.capitalize()+year+fname.capitalize())
        passwords.append(fname+year+fname.capitalize())
        passwords.append(fname.capitalize()+year+fname)
        passwords.append(lname.capitalize()+year+lname.capitalize())
        passwords.append(lname+year+lname.capitalize())
        passwords.append(lname.capitalize()+year+lname)

        #with age
        passwords.append(fname+age)
        passwords.append(lname+age)
        passwords.append(fname.capitalize()+age)
        passwords.append(lname.capitalize()+age)
        passwords.append(fname+lname+age)
        passwords.append(fname.capitalize()+lname.capitalize()+age)
        passwords.append(lname.capitalize()+fname.capitalize()+age)
        passwords.append(lname.capitalize()+fname+age)
        passwords.append(lname+fname.capitalize()+age)
        passwords.append(fname.capitalize()+lname+age)
        passwords.append(fname+lname.capitalize()+age)
        passwords.append(fname.capitalize()+fname.capitalize()+age)
        passwords.append(fname+fname.capitalize()+age)
        passwords.append(fname.capitalize()+fname+age)
        passwords.append(lname.capitalize()+lname.capitalize()+age)
        passwords.append(lname+lname.capitalize()+age)
        passwords.append(lname.capitalize()+lname+age)
        passwords.append(age+fname)
        passwords.append(age+lname)
        passwords.append(age+fname.capitalize())
        passwords.append(age+lname.capitalize())
        passwords.append(age+fname+lname)
        passwords.append(age+fname.capitalize()+lname.capitalize())
        passwords.append(age+lname.capitalize()+fname.capitalize())
        passwords.append(age+lname.capitalize()+fname)
        passwords.append(age+lname+fname.capitalize())
        passwords.append(age+fname.capitalize()+lname)
        passwords.append(age+fname+lname.capitalize())
        passwords.append(age+fname.capitalize()+fname.capitalize())
        passwords.append(age+fname+fname.capitalize())
        passwords.append(age+fname.capitalize()+fname)
        passwords.append(age+lname.capitalize()+lname.capitalize())
        passwords.append(age+lname+lname.capitalize())
        passwords.append(age+lname.capitalize()+lname)
        passwords.append(fname+age+lname)
        passwords.append(fname.capitalize()+age+lname.capitalize())
        passwords.append(lname.capitalize()+age+fname.capitalize())
        passwords.append(lname.capitalize()+age+fname)
        passwords.append(lname+age+fname.capitalize())
        passwords.append(fname.capitalize()+age+lname)
        passwords.append(fname+age+lname.capitalize())
        passwords.append(fname.capitalize()+age+fname.capitalize())
        passwords.append(fname+age+fname.capitalize())
        passwords.append(fname.capitalize()+age+fname)
        passwords.append(lname.capitalize()+age+lname.capitalize())
        passwords.append(lname+age+lname.capitalize())
        passwords.append(lname.capitalize()+age+lname)

        #with date
        passwords.append(fname+date)
        passwords.append(lname+date)
        passwords.append(fname.capitalize()+date)
        passwords.append(lname.capitalize()+date)
        passwords.append(fname+lname+date)
        passwords.append(fname.capitalize()+lname.capitalize()+date)
        passwords.append(lname.capitalize()+fname.capitalize()+date)
        passwords.append(lname.capitalize()+fname+date)
        passwords.append(lname+fname.capitalize()+date)
        passwords.append(fname.capitalize()+lname+date)
        passwords.append(fname+lname.capitalize()+date)
        passwords.append(fname.capitalize()+fname.capitalize()+date)
        passwords.append(fname+fname.capitalize()+date)
        passwords.append(fname.capitalize()+fname+date)
        passwords.append(lname.capitalize()+lname.capitalize()+date)
        passwords.append(lname+lname.capitalize()+date)
        passwords.append(lname.capitalize()+lname+date)
        passwords.append(date+fname)
        passwords.append(date+lname)
        passwords.append(date+fname.capitalize())
        passwords.append(date+lname.capitalize())
        passwords.append(date+fname+lname)
        passwords.append(date+fname.capitalize()+lname.capitalize())
        passwords.append(date+lname.capitalize()+fname.capitalize())
        passwords.append(date+lname.capitalize()+fname)
        passwords.append(date+lname+fname.capitalize())
        passwords.append(date+fname.capitalize()+lname)
        passwords.append(date+fname+lname.capitalize())
        passwords.append(date+fname.capitalize()+fname.capitalize())
        passwords.append(date+fname+fname.capitalize())
        passwords.append(date+fname.capitalize()+fname)
        passwords.append(date+lname.capitalize()+lname.capitalize())
        passwords.append(date+lname+lname.capitalize())
        passwords.append(date+lname.capitalize()+lname)
        passwords.append(fname+date+lname)
        passwords.append(fname.capitalize()+date+lname.capitalize())
        passwords.append(lname.capitalize()+date+fname.capitalize())
        passwords.append(lname.capitalize()+date+fname)
        passwords.append(lname+date+fname.capitalize())
        passwords.append(fname.capitalize()+date+lname)
        passwords.append(fname+date+lname.capitalize())
        passwords.append(fname.capitalize()+date+fname.capitalize())
        passwords.append(fname+date+fname.capitalize())
        passwords.append(fname.capitalize()+date+fname)
        passwords.append(lname.capitalize()+date+lname.capitalize())
        passwords.append(lname+date+lname.capitalize())
        passwords.append(lname.capitalize()+date+lname)

        #with month
        passwords.append(fname+month)
        passwords.append(lname+month)
        passwords.append(fname.capitalize()+month)
        passwords.append(lname.capitalize()+month)
        passwords.append(fname+lname+month)
        passwords.append(fname.capitalize()+lname.capitalize()+month)
        passwords.append(lname.capitalize()+fname.capitalize()+month)
        passwords.append(lname.capitalize()+fname+month)
        passwords.append(lname+fname.capitalize()+month)
        passwords.append(fname.capitalize()+lname+month)
        passwords.append(fname+lname.capitalize()+month)
        passwords.append(fname.capitalize()+fname.capitalize()+month)
        passwords.append(fname+fname.capitalize()+month)
        passwords.append(fname.capitalize()+fname+month)
        passwords.append(lname.capitalize()+lname.capitalize()+month)
        passwords.append(lname+lname.capitalize()+month)
        passwords.append(lname.capitalize()+lname+month)
        passwords.append(month+fname)
        passwords.append(month+lname)
        passwords.append(month+fname.capitalize())
        passwords.append(month+lname.capitalize())
        passwords.append(month+fname+lname)
        passwords.append(month+fname.capitalize()+lname.capitalize())
        passwords.append(month+lname.capitalize()+fname.capitalize())
        passwords.append(month+lname.capitalize()+fname)
        passwords.append(month+lname+fname.capitalize())
        passwords.append(month+fname.capitalize()+lname)
        passwords.append(month+fname+lname.capitalize())
        passwords.append(month+fname.capitalize()+fname.capitalize())
        passwords.append(month+fname+fname.capitalize())
        passwords.append(month+fname.capitalize()+fname)
        passwords.append(month+lname.capitalize()+lname.capitalize())
        passwords.append(month+lname+lname.capitalize())
        passwords.append(month+lname.capitalize()+lname)
        passwords.append(fname+month+lname)
        passwords.append(fname.capitalize()+month+lname.capitalize())
        passwords.append(lname.capitalize()+month+fname.capitalize())
        passwords.append(lname.capitalize()+month+fname)
        passwords.append(lname+month+fname.capitalize())
        passwords.append(fname.capitalize()+month+lname)
        passwords.append(fname+month+lname.capitalize())
        passwords.append(fname.capitalize()+month+fname.capitalize())
        passwords.append(fname+month+fname.capitalize())
        passwords.append(fname.capitalize()+month+fname)
        passwords.append(lname.capitalize()+month+lname.capitalize())
        passwords.append(lname+month+lname.capitalize())
        passwords.append(lname.capitalize()+month+lname)

        #comp1
        passwords.append(fname+comp1)
        passwords.append(lname+comp1)
        passwords.append(fname.capitalize()+comp1)
        passwords.append(lname.capitalize()+comp1)
        passwords.append(fname+lname+comp1)
        passwords.append(fname.capitalize()+lname.capitalize()+comp1)
        passwords.append(lname.capitalize()+fname.capitalize()+comp1)
        passwords.append(lname.capitalize()+fname+comp1)
        passwords.append(lname+fname.capitalize()+comp1)
        passwords.append(fname.capitalize()+lname+comp1)
        passwords.append(fname+lname.capitalize()+comp1)
        passwords.append(fname.capitalize()+fname.capitalize()+comp1)
        passwords.append(fname+fname.capitalize()+comp1)
        passwords.append(fname.capitalize()+fname+comp1)
        passwords.append(lname.capitalize()+lname.capitalize()+comp1)
        passwords.append(lname+lname.capitalize()+comp1)
        passwords.append(lname.capitalize()+lname+comp1)
        passwords.append(comp1+fname)
        passwords.append(comp1+lname)
        passwords.append(comp1+fname.capitalize())
        passwords.append(comp1+lname.capitalize())
        passwords.append(comp1+fname+lname)
        passwords.append(comp1+fname.capitalize()+lname.capitalize())
        passwords.append(comp1+lname.capitalize()+fname.capitalize())
        passwords.append(comp1+lname.capitalize()+fname)
        passwords.append(comp1+lname+fname.capitalize())
        passwords.append(comp1+fname.capitalize()+lname)
        passwords.append(comp1+fname+lname.capitalize())
        passwords.append(comp1+fname.capitalize()+fname.capitalize())
        passwords.append(comp1+fname+fname.capitalize())
        passwords.append(comp1+fname.capitalize()+fname)
        passwords.append(comp1+lname.capitalize()+lname.capitalize())
        passwords.append(comp1+lname+lname.capitalize())
        passwords.append(comp1+lname.capitalize()+lname)
        passwords.append(fname+comp1+lname)
        passwords.append(fname.capitalize()+comp1+lname.capitalize())
        passwords.append(lname.capitalize()+comp1+fname.capitalize())
        passwords.append(lname.capitalize()+comp1+fname)
        passwords.append(lname+comp1+fname.capitalize())
        passwords.append(fname.capitalize()+comp1+lname)
        passwords.append(fname+comp1+lname.capitalize())
        passwords.append(fname.capitalize()+comp1+fname.capitalize())
        passwords.append(fname+comp1+fname.capitalize())
        passwords.append(fname.capitalize()+comp1+fname)
        passwords.append(lname.capitalize()+comp1+lname.capitalize())
        passwords.append(lname+comp1+lname.capitalize())
        passwords.append(lname.capitalize()+comp1+lname)

        #comp2
        passwords.append(fname+comp2)
        passwords.append(lname+comp2)
        passwords.append(fname.capitalize()+comp2)
        passwords.append(lname.capitalize()+comp2)
        passwords.append(fname+lname+comp2)
        passwords.append(fname.capitalize()+lname.capitalize()+comp2)
        passwords.append(lname.capitalize()+fname.capitalize()+comp2)
        passwords.append(lname.capitalize()+fname+comp2)
        passwords.append(lname+fname.capitalize()+comp2)
        passwords.append(fname.capitalize()+lname+comp2)
        passwords.append(fname+lname.capitalize()+comp2)
        passwords.append(fname.capitalize()+fname.capitalize()+comp2)
        passwords.append(fname+fname.capitalize()+comp2)
        passwords.append(fname.capitalize()+fname+comp2)
        passwords.append(lname.capitalize()+lname.capitalize()+comp2)
        passwords.append(lname+lname.capitalize()+comp2)
        passwords.append(lname.capitalize()+lname+comp2)
        passwords.append(comp2+fname)
        passwords.append(comp2+lname)
        passwords.append(comp2+fname.capitalize())
        passwords.append(comp2+lname.capitalize())
        passwords.append(comp2+fname+lname)
        passwords.append(comp2+fname.capitalize()+lname.capitalize())
        passwords.append(comp2+lname.capitalize()+fname.capitalize())
        passwords.append(comp2+lname.capitalize()+fname)
        passwords.append(comp2+lname+fname.capitalize())
        passwords.append(comp2+fname.capitalize()+lname)
        passwords.append(comp2+fname+lname.capitalize())
        passwords.append(comp2+fname.capitalize()+fname.capitalize())
        passwords.append(comp2+fname+fname.capitalize())
        passwords.append(comp2+fname.capitalize()+fname)
        passwords.append(comp2+lname.capitalize()+lname.capitalize())
        passwords.append(comp2+lname+lname.capitalize())
        passwords.append(comp2+lname.capitalize()+lname)
        passwords.append(fname+comp2+lname)
        passwords.append(fname.capitalize()+comp2+lname.capitalize())
        passwords.append(lname.capitalize()+comp2+fname.capitalize())
        passwords.append(lname.capitalize()+comp2+fname)
        passwords.append(lname+comp2+fname.capitalize())
        passwords.append(fname.capitalize()+comp2+lname)
        passwords.append(fname+comp2+lname.capitalize())
        passwords.append(fname.capitalize()+comp2+fname.capitalize())
        passwords.append(fname+comp2+fname.capitalize())
        passwords.append(fname.capitalize()+comp2+fname)
        passwords.append(lname.capitalize()+comp2+lname.capitalize())
        passwords.append(lname+comp2+lname.capitalize())
        passwords.append(lname.capitalize()+comp2+lname)

        #comp3
        passwords.append(fname+comp3)
        passwords.append(lname+comp3)
        passwords.append(fname.capitalize()+comp3)
        passwords.append(lname.capitalize()+comp3)
        passwords.append(fname+lname+comp3)
        passwords.append(fname.capitalize()+lname.capitalize()+comp3)
        passwords.append(lname.capitalize()+fname.capitalize()+comp3)
        passwords.append(lname.capitalize()+fname+comp3)
        passwords.append(lname+fname.capitalize()+comp3)
        passwords.append(fname.capitalize()+lname+comp3)
        passwords.append(fname+lname.capitalize()+comp3)
        passwords.append(fname.capitalize()+fname.capitalize()+comp3)
        passwords.append(fname+fname.capitalize()+comp3)
        passwords.append(fname.capitalize()+fname+comp3)
        passwords.append(lname.capitalize()+lname.capitalize()+comp3)
        passwords.append(lname+lname.capitalize()+comp3)
        passwords.append(lname.capitalize()+lname+comp3)
        passwords.append(comp3+fname)
        passwords.append(comp3+lname)
        passwords.append(comp3+fname.capitalize())
        passwords.append(comp3+lname.capitalize())
        passwords.append(comp3+fname+lname)
        passwords.append(comp3+fname.capitalize()+lname.capitalize())
        passwords.append(comp3+lname.capitalize()+fname.capitalize())
        passwords.append(comp3+lname.capitalize()+fname)
        passwords.append(comp3+lname+fname.capitalize())
        passwords.append(comp3+fname.capitalize()+lname)
        passwords.append(comp3+fname+lname.capitalize())
        passwords.append(comp3+fname.capitalize()+fname.capitalize())
        passwords.append(comp3+fname+fname.capitalize())
        passwords.append(comp3+fname.capitalize()+fname)
        passwords.append(comp3+lname.capitalize()+lname.capitalize())
        passwords.append(comp3+lname+lname.capitalize())
        passwords.append(comp3+lname.capitalize()+lname)
        passwords.append(fname+comp3+lname)
        passwords.append(fname.capitalize()+comp3+lname.capitalize())
        passwords.append(lname.capitalize()+comp3+fname.capitalize())
        passwords.append(lname.capitalize()+comp3+fname)
        passwords.append(lname+comp3+fname.capitalize())
        passwords.append(fname.capitalize()+comp3+lname)
        passwords.append(fname+comp3+lname.capitalize())
        passwords.append(fname.capitalize()+comp3+fname.capitalize())
        passwords.append(fname+comp3+fname.capitalize())
        passwords.append(fname.capitalize()+comp3+fname)
        passwords.append(lname.capitalize()+comp3+lname.capitalize())
        passwords.append(lname+comp3+lname.capitalize())
        passwords.append(lname.capitalize()+comp3+lname)

        #comp4
        passwords.append(fname+comp4)
        passwords.append(lname+comp4)
        passwords.append(fname.capitalize()+comp4)
        passwords.append(lname.capitalize()+comp4)
        passwords.append(fname+lname+comp4)
        passwords.append(fname.capitalize()+lname.capitalize()+comp4)
        passwords.append(lname.capitalize()+fname.capitalize()+comp4)
        passwords.append(lname.capitalize()+fname+comp4)
        passwords.append(lname+fname.capitalize()+comp4)
        passwords.append(fname.capitalize()+lname+comp4)
        passwords.append(fname+lname.capitalize()+comp4)
        passwords.append(fname.capitalize()+fname.capitalize()+comp4)
        passwords.append(fname+fname.capitalize()+comp4)
        passwords.append(fname.capitalize()+fname+comp4)
        passwords.append(lname.capitalize()+lname.capitalize()+comp4)
        passwords.append(lname+lname.capitalize()+comp4)
        passwords.append(lname.capitalize()+lname+comp4)
        passwords.append(comp4+fname)
        passwords.append(comp4+lname)
        passwords.append(comp4+fname.capitalize())
        passwords.append(comp4+lname.capitalize())
        passwords.append(comp4+fname+lname)
        passwords.append(comp4+fname.capitalize()+lname.capitalize())
        passwords.append(comp4+lname.capitalize()+fname.capitalize())
        passwords.append(comp4+lname.capitalize()+fname)
        passwords.append(comp4+lname+fname.capitalize())
        passwords.append(comp4+fname.capitalize()+lname)
        passwords.append(comp4+fname+lname.capitalize())
        passwords.append(comp4+fname.capitalize()+fname.capitalize())
        passwords.append(comp4+fname+fname.capitalize())
        passwords.append(comp4+fname.capitalize()+fname)
        passwords.append(comp4+lname.capitalize()+lname.capitalize())
        passwords.append(comp4+lname+lname.capitalize())
        passwords.append(comp4+lname.capitalize()+lname)
        passwords.append(fname+comp4+lname)
        passwords.append(fname.capitalize()+comp4+lname.capitalize())
        passwords.append(lname.capitalize()+comp4+fname.capitalize())
        passwords.append(lname.capitalize()+comp4+fname)
        passwords.append(lname+comp4+fname.capitalize())
        passwords.append(fname.capitalize()+comp4+lname)
        passwords.append(fname+comp4+lname.capitalize())
        passwords.append(fname.capitalize()+comp4+fname.capitalize())
        passwords.append(fname+comp4+fname.capitalize())
        passwords.append(fname.capitalize()+comp4+fname)
        passwords.append(lname.capitalize()+comp4+lname.capitalize())
        passwords.append(lname+comp4+lname.capitalize())
        passwords.append(lname.capitalize()+comp4+lname)

        #comp5
        passwords.append(fname+comp5)
        passwords.append(lname+comp5)
        passwords.append(fname.capitalize()+comp5)
        passwords.append(lname.capitalize()+comp5)
        passwords.append(fname+lname+comp5)
        passwords.append(fname.capitalize()+lname.capitalize()+comp5)
        passwords.append(lname.capitalize()+fname.capitalize()+comp5)
        passwords.append(lname.capitalize()+fname+comp5)
        passwords.append(lname+fname.capitalize()+comp5)
        passwords.append(fname.capitalize()+lname+comp5)
        passwords.append(fname+lname.capitalize()+comp5)
        passwords.append(fname.capitalize()+fname.capitalize()+comp5)
        passwords.append(fname+fname.capitalize()+comp5)
        passwords.append(fname.capitalize()+fname+comp5)
        passwords.append(lname.capitalize()+lname.capitalize()+comp5)
        passwords.append(lname+lname.capitalize()+comp5)
        passwords.append(lname.capitalize()+lname+comp5)
        passwords.append(comp5+fname)
        passwords.append(comp5+lname)
        passwords.append(comp5+fname.capitalize())
        passwords.append(comp5+lname.capitalize())
        passwords.append(comp5+fname+lname)
        passwords.append(comp5+fname.capitalize()+lname.capitalize())
        passwords.append(comp5+lname.capitalize()+fname.capitalize())
        passwords.append(comp5+lname.capitalize()+fname)
        passwords.append(comp5+lname+fname.capitalize())
        passwords.append(comp5+fname.capitalize()+lname)
        passwords.append(comp5+fname+lname.capitalize())
        passwords.append(comp5+fname.capitalize()+fname.capitalize())
        passwords.append(comp5+fname+fname.capitalize())
        passwords.append(comp5+fname.capitalize()+fname)
        passwords.append(comp5+lname.capitalize()+lname.capitalize())
        passwords.append(comp5+lname+lname.capitalize())
        passwords.append(comp5+lname.capitalize()+lname)
        passwords.append(fname+comp5+lname)
        passwords.append(fname.capitalize()+comp5+lname.capitalize())
        passwords.append(lname.capitalize()+comp5+fname.capitalize())
        passwords.append(lname.capitalize()+comp5+fname)
        passwords.append(lname+comp5+fname.capitalize())
        passwords.append(fname.capitalize()+comp5+lname)
        passwords.append(fname+comp5+lname.capitalize())
        passwords.append(fname.capitalize()+comp5+fname.capitalize())
        passwords.append(fname+comp5+fname.capitalize())
        passwords.append(fname.capitalize()+comp5+fname)
        passwords.append(lname.capitalize()+comp5+lname.capitalize())
        passwords.append(lname+comp5+lname.capitalize())
        passwords.append(lname.capitalize()+comp5+lname)

        #comp6
        passwords.append(fname+comp6)
        passwords.append(lname+comp6)
        passwords.append(fname.capitalize()+comp6)
        passwords.append(lname.capitalize()+comp6)
        passwords.append(fname+lname+comp6)
        passwords.append(fname.capitalize()+lname.capitalize()+comp6)
        passwords.append(lname.capitalize()+fname.capitalize()+comp6)
        passwords.append(lname.capitalize()+fname+comp6)
        passwords.append(lname+fname.capitalize()+comp6)
        passwords.append(fname.capitalize()+lname+comp6)
        passwords.append(fname+lname.capitalize()+comp6)
        passwords.append(fname.capitalize()+fname.capitalize()+comp6)
        passwords.append(fname+fname.capitalize()+comp6)
        passwords.append(fname.capitalize()+fname+comp6)
        passwords.append(lname.capitalize()+lname.capitalize()+comp6)
        passwords.append(lname+lname.capitalize()+comp6)
        passwords.append(lname.capitalize()+lname+comp6)
        passwords.append(comp6+fname)
        passwords.append(comp6+lname)
        passwords.append(comp6+fname.capitalize())
        passwords.append(comp6+lname.capitalize())
        passwords.append(comp6+fname+lname)
        passwords.append(comp6+fname.capitalize()+lname.capitalize())
        passwords.append(comp6+lname.capitalize()+fname.capitalize())
        passwords.append(comp6+lname.capitalize()+fname)
        passwords.append(comp6+lname+fname.capitalize())
        passwords.append(comp6+fname.capitalize()+lname)
        passwords.append(comp6+fname+lname.capitalize())
        passwords.append(comp6+fname.capitalize()+fname.capitalize())
        passwords.append(comp6+fname+fname.capitalize())
        passwords.append(comp6+fname.capitalize()+fname)
        passwords.append(comp6+lname.capitalize()+lname.capitalize())
        passwords.append(comp6+lname+lname.capitalize())
        passwords.append(comp6+lname.capitalize()+lname)
        passwords.append(fname+comp6+lname)
        passwords.append(fname.capitalize()+comp6+lname.capitalize())
        passwords.append(lname.capitalize()+comp6+fname.capitalize())
        passwords.append(lname.capitalize()+comp6+fname)
        passwords.append(lname+comp6+fname.capitalize())
        passwords.append(fname.capitalize()+comp6+lname)
        passwords.append(fname+comp6+lname.capitalize())
        passwords.append(fname.capitalize()+comp6+fname.capitalize())
        passwords.append(fname+comp6+fname.capitalize())
        passwords.append(fname.capitalize()+comp6+fname)
        passwords.append(lname.capitalize()+comp6+lname.capitalize())
        passwords.append(lname+comp6+lname.capitalize())
        passwords.append(lname.capitalize()+comp6+lname)

        #comp7
        passwords.append(fname+comp7)
        passwords.append(lname+comp7)
        passwords.append(fname.capitalize()+comp7)
        passwords.append(lname.capitalize()+comp7)
        passwords.append(fname+lname+comp7)
        passwords.append(fname.capitalize()+lname.capitalize()+comp7)
        passwords.append(lname.capitalize()+fname.capitalize()+comp7)
        passwords.append(lname.capitalize()+fname+comp7)
        passwords.append(lname+fname.capitalize()+comp7)
        passwords.append(fname.capitalize()+lname+comp7)
        passwords.append(fname+lname.capitalize()+comp7)
        passwords.append(fname.capitalize()+fname.capitalize()+comp7)
        passwords.append(fname+fname.capitalize()+comp7)
        passwords.append(fname.capitalize()+fname+comp7)
        passwords.append(lname.capitalize()+lname.capitalize()+comp7)
        passwords.append(lname+lname.capitalize()+comp7)
        passwords.append(lname.capitalize()+lname+comp7)
        passwords.append(comp7+fname)
        passwords.append(comp7+lname)
        passwords.append(comp7+fname.capitalize())
        passwords.append(comp7+lname.capitalize())
        passwords.append(comp7+fname+lname)
        passwords.append(comp7+fname.capitalize()+lname.capitalize())
        passwords.append(comp7+lname.capitalize()+fname.capitalize())
        passwords.append(comp7+lname.capitalize()+fname)
        passwords.append(comp7+lname+fname.capitalize())
        passwords.append(comp7+fname.capitalize()+lname)
        passwords.append(comp7+fname+lname.capitalize())
        passwords.append(comp7+fname.capitalize()+fname.capitalize())
        passwords.append(comp7+fname+fname.capitalize())
        passwords.append(comp7+fname.capitalize()+fname)
        passwords.append(comp7+lname.capitalize()+lname.capitalize())
        passwords.append(comp7+lname+lname.capitalize())
        passwords.append(comp7+lname.capitalize()+lname)
        passwords.append(fname+comp7+lname)
        passwords.append(fname.capitalize()+comp7+lname.capitalize())
        passwords.append(lname.capitalize()+comp7+fname.capitalize())
        passwords.append(lname.capitalize()+comp7+fname)
        passwords.append(lname+comp7+fname.capitalize())
        passwords.append(fname.capitalize()+comp7+lname)
        passwords.append(fname+comp7+lname.capitalize())
        passwords.append(fname.capitalize()+comp7+fname.capitalize())
        passwords.append(fname+comp7+fname.capitalize())
        passwords.append(fname.capitalize()+comp7+fname)
        passwords.append(lname.capitalize()+comp7+lname.capitalize())
        passwords.append(lname+comp7+lname.capitalize())
        passwords.append(lname.capitalize()+comp7+lname)

        #comp8
        passwords.append(fname+comp8)
        passwords.append(lname+comp8)
        passwords.append(fname.capitalize()+comp8)
        passwords.append(lname.capitalize()+comp8)
        passwords.append(fname+lname+comp8)
        passwords.append(fname.capitalize()+lname.capitalize()+comp8)
        passwords.append(lname.capitalize()+fname.capitalize()+comp8)
        passwords.append(lname.capitalize()+fname+comp8)
        passwords.append(lname+fname.capitalize()+comp8)
        passwords.append(fname.capitalize()+lname+comp8)
        passwords.append(fname+lname.capitalize()+comp8)
        passwords.append(fname.capitalize()+fname.capitalize()+comp8)
        passwords.append(fname+fname.capitalize()+comp8)
        passwords.append(fname.capitalize()+fname+comp8)
        passwords.append(lname.capitalize()+lname.capitalize()+comp8)
        passwords.append(lname+lname.capitalize()+comp8)
        passwords.append(lname.capitalize()+lname+comp8)
        passwords.append(comp8+fname)
        passwords.append(comp8+lname)
        passwords.append(comp8+fname.capitalize())
        passwords.append(comp8+lname.capitalize())
        passwords.append(comp8+fname+lname)
        passwords.append(comp8+fname.capitalize()+lname.capitalize())
        passwords.append(comp8+lname.capitalize()+fname.capitalize())
        passwords.append(comp8+lname.capitalize()+fname)
        passwords.append(comp8+lname+fname.capitalize())
        passwords.append(comp8+fname.capitalize()+lname)
        passwords.append(comp8+fname+lname.capitalize())
        passwords.append(comp8+fname.capitalize()+fname.capitalize())
        passwords.append(comp8+fname+fname.capitalize())
        passwords.append(comp8+fname.capitalize()+fname)
        passwords.append(comp8+lname.capitalize()+lname.capitalize())
        passwords.append(comp8+lname+lname.capitalize())
        passwords.append(comp8+lname.capitalize()+lname)
        passwords.append(fname+comp8+lname)
        passwords.append(fname.capitalize()+comp8+lname.capitalize())
        passwords.append(lname.capitalize()+comp8+fname.capitalize())
        passwords.append(lname.capitalize()+comp8+fname)
        passwords.append(lname+comp8+fname.capitalize())
        passwords.append(fname.capitalize()+comp8+lname)
        passwords.append(fname+comp8+lname.capitalize())
        passwords.append(fname.capitalize()+comp8+fname.capitalize())
        passwords.append(fname+comp8+fname.capitalize())
        passwords.append(fname.capitalize()+comp8+fname)
        passwords.append(lname.capitalize()+comp8+lname.capitalize())
        passwords.append(lname+comp8+lname.capitalize())
        passwords.append(lname.capitalize()+comp8+lname)

        #comp9
        passwords.append(fname+comp9)
        passwords.append(lname+comp9)
        passwords.append(fname.capitalize()+comp9)
        passwords.append(lname.capitalize()+comp9)
        passwords.append(fname+lname+comp9)
        passwords.append(fname.capitalize()+lname.capitalize()+comp9)
        passwords.append(lname.capitalize()+fname.capitalize()+comp9)
        passwords.append(lname.capitalize()+fname+comp9)
        passwords.append(lname+fname.capitalize()+comp9)
        passwords.append(fname.capitalize()+lname+comp9)
        passwords.append(fname+lname.capitalize()+comp9)
        passwords.append(fname.capitalize()+fname.capitalize()+comp9)
        passwords.append(fname+fname.capitalize()+comp9)
        passwords.append(fname.capitalize()+fname+comp9)
        passwords.append(lname.capitalize()+lname.capitalize()+comp9)
        passwords.append(lname+lname.capitalize()+comp9)
        passwords.append(lname.capitalize()+lname+comp9)
        passwords.append(comp9+fname)
        passwords.append(comp9+lname)
        passwords.append(comp9+fname.capitalize())
        passwords.append(comp9+lname.capitalize())
        passwords.append(comp9+fname+lname)
        passwords.append(comp9+fname.capitalize()+lname.capitalize())
        passwords.append(comp9+lname.capitalize()+fname.capitalize())
        passwords.append(comp9+lname.capitalize()+fname)
        passwords.append(comp9+lname+fname.capitalize())
        passwords.append(comp9+fname.capitalize()+lname)
        passwords.append(comp9+fname+lname.capitalize())
        passwords.append(comp9+fname.capitalize()+fname.capitalize())
        passwords.append(comp9+fname+fname.capitalize())
        passwords.append(comp9+fname.capitalize()+fname)
        passwords.append(comp9+lname.capitalize()+lname.capitalize())
        passwords.append(comp9+lname+lname.capitalize())
        passwords.append(comp9+lname.capitalize()+lname)
        passwords.append(fname+comp9+lname)
        passwords.append(fname.capitalize()+comp9+lname.capitalize())
        passwords.append(lname.capitalize()+comp9+fname.capitalize())
        passwords.append(lname.capitalize()+comp9+fname)
        passwords.append(lname+comp9+fname.capitalize())
        passwords.append(fname.capitalize()+comp9+lname)
        passwords.append(fname+comp9+lname.capitalize())
        passwords.append(fname.capitalize()+comp9+fname.capitalize())
        passwords.append(fname+comp9+fname.capitalize())
        passwords.append(fname.capitalize()+comp9+fname)
        passwords.append(lname.capitalize()+comp9+lname.capitalize())
        passwords.append(lname+comp9+lname.capitalize())
        passwords.append(lname.capitalize()+comp9+lname)

        #comp10
        passwords.append(fname+comp10)
        passwords.append(lname+comp10)
        passwords.append(fname.capitalize()+comp10)
        passwords.append(lname.capitalize()+comp10)
        passwords.append(fname+lname+comp10)
        passwords.append(fname.capitalize()+lname.capitalize()+comp10)
        passwords.append(lname.capitalize()+fname.capitalize()+comp10)
        passwords.append(lname.capitalize()+fname+comp10)
        passwords.append(lname+fname.capitalize()+comp10)
        passwords.append(fname.capitalize()+lname+comp10)
        passwords.append(fname+lname.capitalize()+comp10)
        passwords.append(fname.capitalize()+fname.capitalize()+comp10)
        passwords.append(fname+fname.capitalize()+comp10)
        passwords.append(fname.capitalize()+fname+comp10)
        passwords.append(lname.capitalize()+lname.capitalize()+comp10)
        passwords.append(lname+lname.capitalize()+comp10)
        passwords.append(lname.capitalize()+lname+comp10)
        passwords.append(comp10+fname)
        passwords.append(comp10+lname)
        passwords.append(comp10+fname.capitalize())
        passwords.append(comp10+lname.capitalize())
        passwords.append(comp10+fname+lname)
        passwords.append(comp10+fname.capitalize()+lname.capitalize())
        passwords.append(comp10+lname.capitalize()+fname.capitalize())
        passwords.append(comp10+lname.capitalize()+fname)
        passwords.append(comp10+lname+fname.capitalize())
        passwords.append(comp10+fname.capitalize()+lname)
        passwords.append(comp10+fname+lname.capitalize())
        passwords.append(comp10+fname.capitalize()+fname.capitalize())
        passwords.append(comp10+fname+fname.capitalize())
        passwords.append(comp10+fname.capitalize()+fname)
        passwords.append(comp10+lname.capitalize()+lname.capitalize())
        passwords.append(comp10+lname+lname.capitalize())
        passwords.append(comp10+lname.capitalize()+lname)
        passwords.append(fname+comp10+lname)
        passwords.append(fname.capitalize()+comp10+lname.capitalize())
        passwords.append(lname.capitalize()+comp10+fname.capitalize())
        passwords.append(lname.capitalize()+comp10+fname)
        passwords.append(lname+comp10+fname.capitalize())
        passwords.append(fname.capitalize()+comp10+lname)
        passwords.append(fname+comp10+lname.capitalize())
        passwords.append(fname.capitalize()+comp10+fname.capitalize())
        passwords.append(fname+comp10+fname.capitalize())
        passwords.append(fname.capitalize()+comp10+fname)
        passwords.append(lname.capitalize()+comp10+lname.capitalize())
        passwords.append(lname+comp10+lname.capitalize())
        passwords.append(lname.capitalize()+comp10+lname)

        #comp11
        passwords.append(fname+comp11)
        passwords.append(lname+comp11)
        passwords.append(fname.capitalize()+comp11)
        passwords.append(lname.capitalize()+comp11)
        passwords.append(fname+lname+comp11)
        passwords.append(fname.capitalize()+lname.capitalize()+comp11)
        passwords.append(lname.capitalize()+fname.capitalize()+comp11)
        passwords.append(lname.capitalize()+fname+comp11)
        passwords.append(lname+fname.capitalize()+comp11)
        passwords.append(fname.capitalize()+lname+comp11)
        passwords.append(fname+lname.capitalize()+comp11)
        passwords.append(fname.capitalize()+fname.capitalize()+comp11)
        passwords.append(fname+fname.capitalize()+comp11)
        passwords.append(fname.capitalize()+fname+comp11)
        passwords.append(lname.capitalize()+lname.capitalize()+comp11)
        passwords.append(lname+lname.capitalize()+comp11)
        passwords.append(lname.capitalize()+lname+comp11)
        passwords.append(comp11+fname)
        passwords.append(comp11+lname)
        passwords.append(comp11+fname.capitalize())
        passwords.append(comp11+lname.capitalize())
        passwords.append(comp11+fname+lname)
        passwords.append(comp11+fname.capitalize()+lname.capitalize())
        passwords.append(comp11+lname.capitalize()+fname.capitalize())
        passwords.append(comp11+lname.capitalize()+fname)
        passwords.append(comp11+lname+fname.capitalize())
        passwords.append(comp11+fname.capitalize()+lname)
        passwords.append(comp11+fname+lname.capitalize())
        passwords.append(comp11+fname.capitalize()+fname.capitalize())
        passwords.append(comp11+fname+fname.capitalize())
        passwords.append(comp11+fname.capitalize()+fname)
        passwords.append(comp11+lname.capitalize()+lname.capitalize())
        passwords.append(comp11+lname+lname.capitalize())
        passwords.append(comp11+lname.capitalize()+lname)
        passwords.append(fname+comp11+lname)
        passwords.append(fname.capitalize()+comp11+lname.capitalize())
        passwords.append(lname.capitalize()+comp11+fname.capitalize())
        passwords.append(lname.capitalize()+comp11+fname)
        passwords.append(lname+comp11+fname.capitalize())
        passwords.append(fname.capitalize()+comp11+lname)
        passwords.append(fname+comp11+lname.capitalize())
        passwords.append(fname.capitalize()+comp11+fname.capitalize())
        passwords.append(fname+comp11+fname.capitalize())
        passwords.append(fname.capitalize()+comp11+fname)
        passwords.append(lname.capitalize()+comp11+lname.capitalize())
        passwords.append(lname+comp11+lname.capitalize())
        passwords.append(lname.capitalize()+comp11+lname)

        #comp12
        passwords.append(fname+comp12)
        passwords.append(lname+comp12)
        passwords.append(fname.capitalize()+comp12)
        passwords.append(lname.capitalize()+comp12)
        passwords.append(fname+lname+comp12)
        passwords.append(fname.capitalize()+lname.capitalize()+comp12)
        passwords.append(lname.capitalize()+fname.capitalize()+comp12)
        passwords.append(lname.capitalize()+fname+comp12)
        passwords.append(lname+fname.capitalize()+comp12)
        passwords.append(fname.capitalize()+lname+comp12)
        passwords.append(fname+lname.capitalize()+comp12)
        passwords.append(fname.capitalize()+fname.capitalize()+comp12)
        passwords.append(fname+fname.capitalize()+comp12)
        passwords.append(fname.capitalize()+fname+comp12)
        passwords.append(lname.capitalize()+lname.capitalize()+comp12)
        passwords.append(lname+lname.capitalize()+comp12)
        passwords.append(lname.capitalize()+lname+comp12)
        passwords.append(comp12+fname)
        passwords.append(comp12+lname)
        passwords.append(comp12+fname.capitalize())
        passwords.append(comp12+lname.capitalize())
        passwords.append(comp12+fname+lname)
        passwords.append(comp12+fname.capitalize()+lname.capitalize())
        passwords.append(comp12+lname.capitalize()+fname.capitalize())
        passwords.append(comp12+lname.capitalize()+fname)
        passwords.append(comp12+lname+fname.capitalize())
        passwords.append(comp12+fname.capitalize()+lname)
        passwords.append(comp12+fname+lname.capitalize())
        passwords.append(comp12+fname.capitalize()+fname.capitalize())
        passwords.append(comp12+fname+fname.capitalize())
        passwords.append(comp12+fname.capitalize()+fname)
        passwords.append(comp12+lname.capitalize()+lname.capitalize())
        passwords.append(comp12+lname+lname.capitalize())
        passwords.append(comp12+lname.capitalize()+lname)
        passwords.append(fname+comp12+lname)
        passwords.append(fname.capitalize()+comp12+lname.capitalize())
        passwords.append(lname.capitalize()+comp12+fname.capitalize())
        passwords.append(lname.capitalize()+comp12+fname)
        passwords.append(lname+comp12+fname.capitalize())
        passwords.append(fname.capitalize()+comp12+lname)
        passwords.append(fname+comp12+lname.capitalize())
        passwords.append(fname.capitalize()+comp12+fname.capitalize())
        passwords.append(fname+comp12+fname.capitalize())
        passwords.append(fname.capitalize()+comp12+fname)
        passwords.append(lname.capitalize()+comp12+lname.capitalize())
        passwords.append(lname+comp12+lname.capitalize())
        passwords.append(lname.capitalize()+comp12+lname)

        #comp13
        passwords.append(fname+comp13)
        passwords.append(lname+comp13)
        passwords.append(fname.capitalize()+comp13)
        passwords.append(lname.capitalize()+comp13)
        passwords.append(fname+lname+comp13)
        passwords.append(fname.capitalize()+lname.capitalize()+comp13)
        passwords.append(lname.capitalize()+fname.capitalize()+comp13)
        passwords.append(lname.capitalize()+fname+comp13)
        passwords.append(lname+fname.capitalize()+comp13)
        passwords.append(fname.capitalize()+lname+comp13)
        passwords.append(fname+lname.capitalize()+comp13)
        passwords.append(fname.capitalize()+fname.capitalize()+comp13)
        passwords.append(fname+fname.capitalize()+comp13)
        passwords.append(fname.capitalize()+fname+comp13)
        passwords.append(lname.capitalize()+lname.capitalize()+comp13)
        passwords.append(lname+lname.capitalize()+comp13)
        passwords.append(lname.capitalize()+lname+comp13)
        passwords.append(comp13+fname)
        passwords.append(comp13+lname)
        passwords.append(comp13+fname.capitalize())
        passwords.append(comp13+lname.capitalize())
        passwords.append(comp13+fname+lname)
        passwords.append(comp13+fname.capitalize()+lname.capitalize())
        passwords.append(comp13+lname.capitalize()+fname.capitalize())
        passwords.append(comp13+lname.capitalize()+fname)
        passwords.append(comp13+lname+fname.capitalize())
        passwords.append(comp13+fname.capitalize()+lname)
        passwords.append(comp13+fname+lname.capitalize())
        passwords.append(comp13+fname.capitalize()+fname.capitalize())
        passwords.append(comp13+fname+fname.capitalize())
        passwords.append(comp13+fname.capitalize()+fname)
        passwords.append(comp13+lname.capitalize()+lname.capitalize())
        passwords.append(comp13+lname+lname.capitalize())
        passwords.append(comp13+lname.capitalize()+lname)
        passwords.append(fname+comp13+lname)
        passwords.append(fname.capitalize()+comp13+lname.capitalize())
        passwords.append(lname.capitalize()+comp13+fname.capitalize())
        passwords.append(lname.capitalize()+comp13+fname)
        passwords.append(lname+comp13+fname.capitalize())
        passwords.append(fname.capitalize()+comp13+lname)
        passwords.append(fname+comp13+lname.capitalize())
        passwords.append(fname.capitalize()+comp13+fname.capitalize())
        passwords.append(fname+comp13+fname.capitalize())
        passwords.append(fname.capitalize()+comp13+fname)
        passwords.append(lname.capitalize()+comp13+lname.capitalize())
        passwords.append(lname+comp13+lname.capitalize())
        passwords.append(lname.capitalize()+comp13+lname)

        #comp14
        passwords.append(fname+comp14)
        passwords.append(lname+comp14)
        passwords.append(fname.capitalize()+comp14)
        passwords.append(lname.capitalize()+comp14)
        passwords.append(fname+lname+comp14)
        passwords.append(fname.capitalize()+lname.capitalize()+comp14)
        passwords.append(lname.capitalize()+fname.capitalize()+comp14)
        passwords.append(lname.capitalize()+fname+comp14)
        passwords.append(lname+fname.capitalize()+comp14)
        passwords.append(fname.capitalize()+lname+comp14)
        passwords.append(fname+lname.capitalize()+comp14)
        passwords.append(fname.capitalize()+fname.capitalize()+comp14)
        passwords.append(fname+fname.capitalize()+comp14)
        passwords.append(fname.capitalize()+fname+comp14)
        passwords.append(lname.capitalize()+lname.capitalize()+comp14)
        passwords.append(lname+lname.capitalize()+comp14)
        passwords.append(lname.capitalize()+lname+comp14)
        passwords.append(comp14+fname)
        passwords.append(comp14+lname)
        passwords.append(comp14+fname.capitalize())
        passwords.append(comp14+lname.capitalize())
        passwords.append(comp14+fname+lname)
        passwords.append(comp14+fname.capitalize()+lname.capitalize())
        passwords.append(comp14+lname.capitalize()+fname.capitalize())
        passwords.append(comp14+lname.capitalize()+fname)
        passwords.append(comp14+lname+fname.capitalize())
        passwords.append(comp14+fname.capitalize()+lname)
        passwords.append(comp14+fname+lname.capitalize())
        passwords.append(comp14+fname.capitalize()+fname.capitalize())
        passwords.append(comp14+fname+fname.capitalize())
        passwords.append(comp14+fname.capitalize()+fname)
        passwords.append(comp14+lname.capitalize()+lname.capitalize())
        passwords.append(comp14+lname+lname.capitalize())
        passwords.append(comp14+lname.capitalize()+lname)
        passwords.append(fname+comp14+lname)
        passwords.append(fname.capitalize()+comp14+lname.capitalize())
        passwords.append(lname.capitalize()+comp14+fname.capitalize())
        passwords.append(lname.capitalize()+comp14+fname)
        passwords.append(lname+comp14+fname.capitalize())
        passwords.append(fname.capitalize()+comp14+lname)
        passwords.append(fname+comp14+lname.capitalize())
        passwords.append(fname.capitalize()+comp14+fname.capitalize())
        passwords.append(fname+comp14+fname.capitalize())
        passwords.append(fname.capitalize()+comp14+fname)
        passwords.append(lname.capitalize()+comp14+lname.capitalize())
        passwords.append(lname+comp14+lname.capitalize())
        passwords.append(lname.capitalize()+comp14+lname)

        #comp15
        passwords.append(fname+comp15)
        passwords.append(lname+comp15)
        passwords.append(fname.capitalize()+comp15)
        passwords.append(lname.capitalize()+comp15)
        passwords.append(fname+lname+comp15)
        passwords.append(fname.capitalize()+lname.capitalize()+comp15)
        passwords.append(lname.capitalize()+fname.capitalize()+comp15)
        passwords.append(lname.capitalize()+fname+comp15)
        passwords.append(lname+fname.capitalize()+comp15)
        passwords.append(fname.capitalize()+lname+comp15)
        passwords.append(fname+lname.capitalize()+comp15)
        passwords.append(fname.capitalize()+fname.capitalize()+comp15)
        passwords.append(fname+fname.capitalize()+comp15)
        passwords.append(fname.capitalize()+fname+comp15)
        passwords.append(lname.capitalize()+lname.capitalize()+comp15)
        passwords.append(lname+lname.capitalize()+comp15)
        passwords.append(lname.capitalize()+lname+comp15)
        passwords.append(comp15+fname)
        passwords.append(comp15+lname)
        passwords.append(comp15+fname.capitalize())
        passwords.append(comp15+lname.capitalize())
        passwords.append(comp15+fname+lname)
        passwords.append(comp15+fname.capitalize()+lname.capitalize())
        passwords.append(comp15+lname.capitalize()+fname.capitalize())
        passwords.append(comp15+lname.capitalize()+fname)
        passwords.append(comp15+lname+fname.capitalize())
        passwords.append(comp15+fname.capitalize()+lname)
        passwords.append(comp15+fname+lname.capitalize())
        passwords.append(comp15+fname.capitalize()+fname.capitalize())
        passwords.append(comp15+fname+fname.capitalize())
        passwords.append(comp15+fname.capitalize()+fname)
        passwords.append(comp15+lname.capitalize()+lname.capitalize())
        passwords.append(comp15+lname+lname.capitalize())
        passwords.append(comp15+lname.capitalize()+lname)
        passwords.append(fname+comp15+lname)
        passwords.append(fname.capitalize()+comp15+lname.capitalize())
        passwords.append(lname.capitalize()+comp15+fname.capitalize())
        passwords.append(lname.capitalize()+comp15+fname)
        passwords.append(lname+comp15+fname.capitalize())
        passwords.append(fname.capitalize()+comp15+lname)
        passwords.append(fname+comp15+lname.capitalize())
        passwords.append(fname.capitalize()+comp15+fname.capitalize())
        passwords.append(fname+comp15+fname.capitalize())
        passwords.append(fname.capitalize()+comp15+fname)
        passwords.append(lname.capitalize()+comp15+lname.capitalize())
        passwords.append(lname+comp15+lname.capitalize())
        passwords.append(lname.capitalize()+comp15+lname)

        #comp16
        passwords.append(fname+comp16)
        passwords.append(lname+comp16)
        passwords.append(fname.capitalize()+comp16)
        passwords.append(lname.capitalize()+comp16)
        passwords.append(fname+lname+comp16)
        passwords.append(fname.capitalize()+lname.capitalize()+comp16)
        passwords.append(lname.capitalize()+fname.capitalize()+comp16)
        passwords.append(lname.capitalize()+fname+comp16)
        passwords.append(lname+fname.capitalize()+comp16)
        passwords.append(fname.capitalize()+lname+comp16)
        passwords.append(fname+lname.capitalize()+comp16)
        passwords.append(fname.capitalize()+fname.capitalize()+comp16)
        passwords.append(fname+fname.capitalize()+comp16)
        passwords.append(fname.capitalize()+fname+comp16)
        passwords.append(lname.capitalize()+lname.capitalize()+comp16)
        passwords.append(lname+lname.capitalize()+comp16)
        passwords.append(lname.capitalize()+lname+comp16)
        passwords.append(comp16+fname)
        passwords.append(comp16+lname)
        passwords.append(comp16+fname.capitalize())
        passwords.append(comp16+lname.capitalize())
        passwords.append(comp16+fname+lname)
        passwords.append(comp16+fname.capitalize()+lname.capitalize())
        passwords.append(comp16+lname.capitalize()+fname.capitalize())
        passwords.append(comp16+lname.capitalize()+fname)
        passwords.append(comp16+lname+fname.capitalize())
        passwords.append(comp16+fname.capitalize()+lname)
        passwords.append(comp16+fname+lname.capitalize())
        passwords.append(comp16+fname.capitalize()+fname.capitalize())
        passwords.append(comp16+fname+fname.capitalize())
        passwords.append(comp16+fname.capitalize()+fname)
        passwords.append(comp16+lname.capitalize()+lname.capitalize())
        passwords.append(comp16+lname+lname.capitalize())
        passwords.append(comp16+lname.capitalize()+lname)
        passwords.append(fname+comp16+lname)
        passwords.append(fname.capitalize()+comp16+lname.capitalize())
        passwords.append(lname.capitalize()+comp16+fname.capitalize())
        passwords.append(lname.capitalize()+comp16+fname)
        passwords.append(lname+comp16+fname.capitalize())
        passwords.append(fname.capitalize()+comp16+lname)
        passwords.append(fname+comp16+lname.capitalize())
        passwords.append(fname.capitalize()+comp16+fname.capitalize())
        passwords.append(fname+comp16+fname.capitalize())
        passwords.append(fname.capitalize()+comp16+fname)
        passwords.append(lname.capitalize()+comp16+lname.capitalize())
        passwords.append(lname+comp16+lname.capitalize())
        passwords.append(lname.capitalize()+comp16+lname)

        #comp17
        passwords.append(fname+comp17)
        passwords.append(lname+comp17)
        passwords.append(fname.capitalize()+comp17)
        passwords.append(lname.capitalize()+comp17)
        passwords.append(fname+lname+comp17)
        passwords.append(fname.capitalize()+lname.capitalize()+comp17)
        passwords.append(lname.capitalize()+fname.capitalize()+comp17)
        passwords.append(lname.capitalize()+fname+comp17)
        passwords.append(lname+fname.capitalize()+comp17)
        passwords.append(fname.capitalize()+lname+comp17)
        passwords.append(fname+lname.capitalize()+comp17)
        passwords.append(fname.capitalize()+fname.capitalize()+comp17)
        passwords.append(fname+fname.capitalize()+comp17)
        passwords.append(fname.capitalize()+fname+comp17)
        passwords.append(lname.capitalize()+lname.capitalize()+comp17)
        passwords.append(lname+lname.capitalize()+comp17)
        passwords.append(lname.capitalize()+lname+comp17)
        passwords.append(comp17+fname)
        passwords.append(comp17+lname)
        passwords.append(comp17+fname.capitalize())
        passwords.append(comp17+lname.capitalize())
        passwords.append(comp17+fname+lname)
        passwords.append(comp17+fname.capitalize()+lname.capitalize())
        passwords.append(comp17+lname.capitalize()+fname.capitalize())
        passwords.append(comp17+lname.capitalize()+fname)
        passwords.append(comp17+lname+fname.capitalize())
        passwords.append(comp17+fname.capitalize()+lname)
        passwords.append(comp17+fname+lname.capitalize())
        passwords.append(comp17+fname.capitalize()+fname.capitalize())
        passwords.append(comp17+fname+fname.capitalize())
        passwords.append(comp17+fname.capitalize()+fname)
        passwords.append(comp17+lname.capitalize()+lname.capitalize())
        passwords.append(comp17+lname+lname.capitalize())
        passwords.append(comp17+lname.capitalize()+lname)
        passwords.append(fname+comp17+lname)
        passwords.append(fname.capitalize()+comp17+lname.capitalize())
        passwords.append(lname.capitalize()+comp17+fname.capitalize())
        passwords.append(lname.capitalize()+comp17+fname)
        passwords.append(lname+comp17+fname.capitalize())
        passwords.append(fname.capitalize()+comp17+lname)
        passwords.append(fname+comp17+lname.capitalize())
        passwords.append(fname.capitalize()+comp17+fname.capitalize())
        passwords.append(fname+comp17+fname.capitalize())
        passwords.append(fname.capitalize()+comp17+fname)
        passwords.append(lname.capitalize()+comp17+lname.capitalize())
        passwords.append(lname+comp17+lname.capitalize())
        passwords.append(lname.capitalize()+comp17+lname)

        #comp18
        passwords.append(fname+comp18)
        passwords.append(lname+comp18)
        passwords.append(fname.capitalize()+comp18)
        passwords.append(lname.capitalize()+comp18)
        passwords.append(fname+lname+comp18)
        passwords.append(fname.capitalize()+lname.capitalize()+comp18)
        passwords.append(lname.capitalize()+fname.capitalize()+comp18)
        passwords.append(lname.capitalize()+fname+comp18)
        passwords.append(lname+fname.capitalize()+comp18)
        passwords.append(fname.capitalize()+lname+comp18)
        passwords.append(fname+lname.capitalize()+comp18)
        passwords.append(fname.capitalize()+fname.capitalize()+comp18)
        passwords.append(fname+fname.capitalize()+comp18)
        passwords.append(fname.capitalize()+fname+comp18)
        passwords.append(lname.capitalize()+lname.capitalize()+comp18)
        passwords.append(lname+lname.capitalize()+comp18)
        passwords.append(lname.capitalize()+lname+comp18)
        passwords.append(comp18+fname)
        passwords.append(comp18+lname)
        passwords.append(comp18+fname.capitalize())
        passwords.append(comp18+lname.capitalize())
        passwords.append(comp18+fname+lname)
        passwords.append(comp18+fname.capitalize()+lname.capitalize())
        passwords.append(comp18+lname.capitalize()+fname.capitalize())
        passwords.append(comp18+lname.capitalize()+fname)
        passwords.append(comp18+lname+fname.capitalize())
        passwords.append(comp18+fname.capitalize()+lname)
        passwords.append(comp18+fname+lname.capitalize())
        passwords.append(comp18+fname.capitalize()+fname.capitalize())
        passwords.append(comp18+fname+fname.capitalize())
        passwords.append(comp18+fname.capitalize()+fname)
        passwords.append(comp18+lname.capitalize()+lname.capitalize())
        passwords.append(comp18+lname+lname.capitalize())
        passwords.append(comp18+lname.capitalize()+lname)
        passwords.append(fname+comp18+lname)
        passwords.append(fname.capitalize()+comp18+lname.capitalize())
        passwords.append(lname.capitalize()+comp18+fname.capitalize())
        passwords.append(lname.capitalize()+comp18+fname)
        passwords.append(lname+comp18+fname.capitalize())
        passwords.append(fname.capitalize()+comp18+lname)
        passwords.append(fname+comp18+lname.capitalize())
        passwords.append(fname.capitalize()+comp18+fname.capitalize())
        passwords.append(fname+comp18+fname.capitalize())
        passwords.append(fname.capitalize()+comp18+fname)
        passwords.append(lname.capitalize()+comp18+lname.capitalize())
        passwords.append(lname+comp18+lname.capitalize())
        passwords.append(lname.capitalize()+comp18+lname)

        leni=len(passwords)
        #special characters
        for y in range(leni):
            for x in range(33,48):
                for z in range(len(passwords[y])):
                    string=passwords[y]
                    passwords.append(string[:z]+str(chr(x))+string[z:])
                passwords.append(passwords[y]+str(chr(x)))

        for y in range(leni):
            for x in range(58,65):
                for z in range(len(passwords[y])):
                    string=passwords[y]
                    passwords.append(string[:z]+str(chr(x))+string[z:])
                passwords.append(passwords[y]+str(chr(x)))

        for y in range(leni):
            for x in range(91,97):
                for z in range(len(passwords[y])):
                    string=passwords[y]
                    passwords.append(string[:z]+str(chr(x))+string[z:])
                passwords.append(passwords[y]+str(chr(x)))

        for y in range(leni):
            for x in range(123,127):
                for z in range(len(passwords[y])):
                    string=passwords[y]
                    passwords.append(string[:z]+str(chr(x))+string[z:])
                passwords.append(passwords[y]+str(chr(x)))

        textfile = open("personal_website_app/static/passwords/passwords.txt", "w")
        for element in passwords:
            textfile.write(element + "\n")
        textfile.close()
        fl_path = 'personal_website_app/static/passwords/passwords.txt'
        filename = 'passwords.txt'
        fl = open(fl_path, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename 
        return response
    except:
        return render(request,'error.html')