from django.shortcuts import render,HttpResponse,redirect
from django.http.response import JsonResponse
import requests
# Create your views here.
access_token = ""
def signIn(request):
    return render(request,"signin.html")

def checkLogin(request):
    if request.method =="POST":

        response = requests.post("http://127.0.0.1:8000/api/login/",data=request.POST)

        jsn = response.json()
        global access_token
        access_token = jsn["access"]
        page = request.GET.get("page")
        print("page---------_____>",page)
        if page==None:
            page=1
        response = requests.get(f"http://127.0.0.1:8000/api/upload?page={page}",headers={"Authorization":f"Bearer {jsn['access']}"})
        print(response.text)

        return render(request,"filelist.html",context={"list":response.json(),"page":range(1,response.json()["page"]+1),"currentPage":int(page),'startindex':5*(int(page)-1),'totalpage':response.json()["page"]})

def upload(request):

    if request.method == "POST":
        page=1
        print("im here",request.FILES['file'])
        response = requests.post("http://127.0.0.1:8000/api/upload/",files=request.FILES,headers={"Authorization":f"Bearer {access_token}"})

        response = requests.get("http://127.0.0.1:8000/api/upload?page=1",headers={"Authorization":f"Bearer {access_token}"})
        print(response.text)

        return render(request,"filelist.html",context={"list":response.json(),"page":range(1,response.json()["page"]+1),"currentPage":1,'startindex':5*(int(page)-1),'totalpage':response.json()["page"]})
    else:
        page = request.GET.get("page")
        print("page---------_____>",page)
        if page==None:
            page=1
        response = requests.get(f"http://127.0.0.1:8000/api/upload?page={page}",headers={"Authorization":f"Bearer {access_token}"})
        if response.status_code != 200:
            return render(request,"filelist.html",context={"code":0,"list":response.json()})  
        print(response.json()["page"])
        return render(request,"filelist.html",context={"list":response.json(),"page":range(1,response.json()["page"]+1),"currentPage":int(page),'startindex':5*(int(page)-1),'totalpage':response.json()["page"]})

def signUp(request):
    return render(request,"signup.html")

def saveData(request):
    if request.method == "POST":
        response = requests.post("http://127.0.0.1:8000/api/register/",data=request.POST)

    return render(request,"signin.html")

def logout(request):
    response = requests.get("http://127.0.0.1:8000/api/logout/",headers={"Authorization":f"Bearer {access_token}"})
    return render(request,"signin.html")

def deleteFile(request,id):
    response = requests.delete(f"http://127.0.0.1:8000/api/deletefile/{id}",headers={"Authorization":f"Bearer {access_token}"})
    print(response.text)
    return redirect('/upload/')