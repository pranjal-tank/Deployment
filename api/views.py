from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse
from django.conf import settings
import subprocess
import os
import requests
from api.serializers import FileSerializer
from rest_framework.decorators import api_view
import docker
import json

user_name=None

def handle_uploaded_file(f):
    global user_name
    fs=FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'temp'))
    for file in f:
        fs.save(file.name,file)


class FileUploadViewSet(viewsets.ViewSet):
    def create(self, request):
        docker_client=docker.from_env()
        serializer_class = FileSerializer(data=request.data)
        if 'file' not in request.FILES or not serializer_class.is_valid():
            return Response({'message':'Deploy Failed'},status=status.HTTP_400_BAD_REQUEST)
        else:
            handle_uploaded_file(request.FILES.getlist('file'))  
            # container=docker_client.containers.run("python3.10","sleep infinity",detach=True)  
            # uploaded_files=os.path.join(settings.MEDIA_ROOT,user_name)
            # for file in request.FILES.getlist('file'):
            #     file_path=uploaded_files+"\\"+file.name
            #     subprocess.run(["docker","cp",file_path,container.name+":/"+file.name])
            # transaction_data={
            #     'container_id':container.id+".json",
            #     "transaction":[]
            # }
            # transaction_json_path=os.path.join(settings.BASE_DIR,"transactions_json",container.id+".json")
            # transaction_json=open(transaction_json_path,"w")
            # transaction_json.write(json.dumps(transaction_data))
            # transaction_json.close()
            # subprocess.run(["docker","cp",transaction_json_path,container.name+":/transactions.json"])
            # pnl_data={
            #     'container_id':container.id+".json",
            #     "pnl":[]
            # }
            # pnl_json_path=os.path.join(settings.BASE_DIR,"pnl_json",container.id+".json")
            # pnl_json=open(pnl_json_path,"w")
            # pnl_json.write(json.dumps(pnl_data))
            # pnl_json.close()
            # container.exec_run("pip install -r requirements.txt")
            return Response({'message':'Deploy Successfull!'},status=status.HTTP_201_CREATED)

@api_view(['POST'])
def upload_files(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return Response({'message':'Deploy Failed'},status=status.HTTP_400_BAD_REQUEST)
        else:
            handle_uploaded_file(request.FILES.getlist('file'))  
            return Response({'message':'Deploy Successfull!'},status=status.HTTP_201_CREATED)



@api_view(['POST'])
def user_auth(request):
    if request.method == 'POST':
        if request.data['username'] and request.data['password']:
            username=request.data['username']
            password=request.data['password']
            user=authenticate(username=username,password=password)
            # if user is not None:
            #     global user_name
            #     user_name=username
            #     return Response({'message':'Authentication successfull....'},status=status.HTTP_201_CREATED)
            # else:
            #     return Response({'message':'Authentication Failed!'},status=status.HTTP_400_BAD_REQUEST)
            if username=='pranjal' and password=='12345':
                return Response({'message':'Authentication Successfull!'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'username or password field missing'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def strategy_transaction(request):
    if request.method == 'POST':
        if request.data:
            data=dict(request.data)
            json_file_path=os.path.join(settings.BASE_DIR,"transactions_json",request.data['container_id'])
            json_file=open(json_file_path,"w")
            json_file.write(json.dumps(data))
            json_file.close()
            return Response({'message':'hii!'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'bye!'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def strategy_pnl(request):
    if request.method == 'POST':
        if request.data:
            data=dict(request.data)
            json_file_path=os.path.join(settings.BASE_DIR,"pnl_json",request.data['container_id'])
            json_file=open(json_file_path,"w")
            json_file.write(json.dumps(data))
            json_file.close()
            return Response({'message':'hii!'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'bye!'},status=status.HTTP_400_BAD_REQUEST)










