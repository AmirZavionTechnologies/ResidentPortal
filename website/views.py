from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record, Resident, Visitor, Guard, Vehicle
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import ResidentSerializer, VisitorSerializer, GuardSerializer, VehicleSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView




def home(request):
	records = Record.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})



def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})



def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
	


####Token Authentication ####
@api_view(['POST'])
def login_api(request):
    serializer=AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user=serializer.validated_data['user']
    created, token=AuthToken.objects.create(user)
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_info': {
        'id':user.id,
        'username':user.username,
        'email':user.email
        },
    'token':token
    })

@api_view(['GET'])
def get_user_data(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'user_info': {
            'id':user.id,
            'username':user.username,
            'email':user.email
            },
        })
    return Response({'error':'not authenticated'},status=400)

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resident = serializer.save()

        # Set the current user as the resident
        resident.user = request.user
        resident.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        # Return an empty queryset to prevent listing
        return Resident.objects.none()
	
class VehicleViewSet(viewsets.ModelViewSet):
    queryset=Vehicle.objects.all()
    serializer_class=VehicleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle = serializer.save()

        # Set the current user as the resident
        vehicle.user = request.user
        vehicle.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        # Return an empty queryset to prevent listing
        return Vehicle.objects.none()
	

class VisitorViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    
class GuardViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Guard.objects.all()
    serializer_class = GuardSerializer

class ResidentByEntryCode(APIView):

    def get(self, request, entry_code):
        residents = Resident.objects.filter(entry_code=entry_code)
        if not residents.exists():
            return Response({"message": "No residents found for the provided apartment number."})
        
        serializer = ResidentSerializer(residents, many=True)
        return Response(serializer.data)
	
class GuardSearchResidentByEntryCode(APIView):

    def get(self, request, entry_code):
        try:
            resident = Resident.objects.get(entry_code=entry_code)
            serializer = ResidentSerializer(resident)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Resident.DoesNotExist:
            return Response({'message': 'Resident not found'}, status=status.HTTP_404_NOT_FOUND)