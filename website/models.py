from django.db import models
import uuid


class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	Age =  models.CharField(max_length=50)
	Apartmentnumber =  models.CharField(max_length=50)
	CNIC =  models.CharField(max_length=20)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")

class Resident(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    apartment_number = models.CharField(max_length=10, unique=True)
    cnic_number = models.CharField(max_length=15, unique=True, null=True)
    age=models.CharField(max_length=20,null=True)
    numberofpersons=models.CharField(max_length=25,null=True)
    entry_code = models.UUIDField(default=uuid.uuid4, editable=False)


class Visitor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=20, null=True, blank=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    visit_code = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.visit_code}"
    

class Guard(models.Model):
    badge_number = models.CharField(max_length=50, unique=True)
    shift_start_time = models.TimeField()
    shift_end_time = models.TimeField()

    def __str__(self):
        return self.badge_number