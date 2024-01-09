from .serializers import *
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import pagination
from rest_framework.permissions import IsAuthenticated
# Create your views here.
#======================================================================== Admin Panel API ======================================================================

#================================================ User Company LIST(POST)
class AdminAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUersSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        try:
            user=request.user
            if user:
                user_obj = User.objects.all()
                serializer = AdminUersSerializer(user_obj,many=True)
                return Response({'status':status.HTTP_201_CREATED,'message': 'Company fetched Successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
                # else:
                #     return Response({'status':status.HTTP_200_OK,'message': '', 'data': ""}, status=status.HTTP_200_OK)
            else:
                return Response({'status':status.HTTP_400_BAD_REQUEST,'message': 'User not found.', 'data': ""}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, page=None,*args, **kwargs):
        try:
            data=request.data
            draw=request.POST.get("draw")
            if request.user.is_superuser==True:
                instance=self.get_queryset()
                recordsTotal=instance.count()
                page = data['start']//data['length']+1
                if data['length']!='':
                    pagination.PageNumberPagination.page_size = data['length']
                else:
                    data['page_size']=10
                    pagination.PageNumberPagination.page_size = 10
                #Sorting for 0,1,2,3,4
                if data['order']:
                    order_by=data['order'][0]['column']
                    if data['order'][0]['dir']!="asc":
                        #"decending ordering"
                        if data['order'][0]['column']==0:
                            instance = instance.order_by("-id")
                        elif data['order'][0]['column']==1:
                            instance = instance.order_by("-email")
                        elif data['order'][0]['column']==2 or data['order'][0]['column']==3 or data['order'][0]['column']==4:
                            instance = instance.order_by("-"+data['columns'][order_by]["data"])
                    else:
                        #"Acending ordering"
                        if data['order'][0]['column']==0:
                            instance = instance.order_by("id")
                        elif data['order'][0]['column']==1:
                            instance = instance.order_by("email")
                        elif data['order'][0]['column']==2 or data['order'][0]['column']==3 or data['order'][0]['column']==4:
                            instance = instance.order_by(data['columns'][order_by]["data"])

                if instance is not None:
                    serializer = AdminUersSerializer(instance, many=True)
                    result=serializer.data
                    #Sorting for 5 TO LAST
                    if data['order'][0]['column']!=0 or data['order'][0]['column']!=1 or data['order'][0]['column']!=2 or data['order'][0]['column']!=3 or data['order'][0]['column']!=4:
                        if data['order'][0]['dir']!="asc":
                            result = sorted(result, key=lambda x: x[data['columns'][order_by]["data"]], reverse=True)
                        elif data['order'][0]['dir']=="asc":
                            result = sorted(result, key=lambda x: x[data['columns'][order_by]["data"]], reverse=False)
                    #Searching
                    if data['search']['value']!='':
                        result=[i for i in result for key ,value in i.items() if str(data['search']['value']).strip() in str(value)]
                        result = [i for n, i in enumerate(result) if i not in result[n + 1:]]
                        recordFil=len(result)
                    else:
                        recordFil=len(result)
                    result=result[data['minNumber']-1:data['maxNumber']]
                    data={
                        "data":result,
                        "draw":page,
                        "recordsFiltered":recordFil,
                        "recordsTotal":recordsTotal,
                        "page_size":data['length'],
                    }
                    return Response({'message': status.HTTP_200_OK, 'message': 'Successfully fetch users.','data': data}, status=status.HTTP_200_OK)
            else:
                return Response({'status':status.HTTP_400_BAD_REQUEST,'message': 'Admin Account Needed..!', 'data': ""}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.partial_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.destroy(self, request, *args, **kwargs)

# ======================================================= User Chatlog LIST(POST)
class AdminChatlogAPI(viewsets.ModelViewSet):
    serializer_class = AdminChatLogSerializer
    queryset = chat_log.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, page=None,*args, **kwargs):
        try:
            data=request.data            
            draw=request.POST.get("draw")
            if request.user.is_superuser==True:
                instance=self.get_queryset()
                recordsTotal=instance.count()
                page = data['start']//data['length']+1                
                if data['length']!='':
                    pagination.PageNumberPagination.page_size = data['length']
                else:
                    data['page_size']=10                    
                    pagination.PageNumberPagination.page_size = 10                
                if data['order']:
                    order_by=data['order'][0]['column']
                    if data['order'][0]['dir']!="asc":
                        instance = instance.order_by("-"+data['columns'][order_by]["data"])
                    else:
                        instance = instance.order_by(data['columns'][order_by]["data"])

                serializer = AdminChatLogSerializer(instance, many=True)
                result=serializer.data
                if data['search']['value']!='':
                    result=[i for i in result for key ,value in i.items() if data['search']['value'] in str(value)]        
                    result = [i for n, i in enumerate(result) if i not in result[n + 1:]]
                    recordFil=len(result)
                else:
                    recordFil=len(result)
                result=result[data['minNumber']-1:data['maxNumber']]
                data={
                    "data":result,
                    "draw":page,
                    "recordsFiltered":recordFil,
                    "recordsTotal":recordsTotal,
                    "page_size":data['length'],
                }
                    # user_data=self.get_paginated_response(data)                    # return user_data                    
                return Response({'message': status.HTTP_200_OK, 'data': data}, status=status.HTTP_200_OK)
            else:
                return Response({'status':status.HTTP_400_BAD_REQUEST,'message': 'Admin Account Needed..!', 'data': ""}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AdminChatLogSerializer(queryset, many=True)
        return Response({'message': status.HTTP_200_OK, 'data': serializer.data}, status=status.HTTP_200_OK)

#======================================================== Admin DashBoard
class AdminDashboardAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request, format=None):
        count_user = User.objects.all().count()
        count_company = create_company.objects.count()
        count_chat = chat_log.objects.count()
        content = {'Total_user': count_user,'Total_company': count_company,'Total_chat':count_chat}
        return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':content},status=status.HTTP_200_OK)

#======================================================== Admin Mail Config
class AdminMailConfig(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request): 
        user=request.user
        if user.is_superuser: 
            instance=template_config.objects.all()
            seri=AdminMailConfigSerializer(instance,many=True)
            return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':seri.data},status=status.HTTP_200_OK) 
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Admin Account Needed..!','data':""},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request): 
        data = request.data
        user=request.user
        if user.is_superuser: 
            if template_config.objects.filter(template=data['template']).exists():
                instance=template_config.objects.get(template=data['template'])
                seri=AdminMailConfigSerializer(instance,data=data,partial=True)
                if seri.is_valid():
                    seri.save()
                    return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':seri.data},status=status.HTTP_200_OK) 
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Error','data':seri.errors},status=status.HTTP_400_BAD_REQUEST)
            else: 
                seri=AdminMailConfigSerializer(data=data,partial=True) 
                if seri.is_valid():
                    seri.save()
                    return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':seri.data},status=status.HTTP_200_OK) 
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Error','data':seri.errors},status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message': 'Admin Account Needed..!', 'data': ""}, status=status.HTTP_400_BAD_REQUEST)
