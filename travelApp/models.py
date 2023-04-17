from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def registerValidator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) == 0:
            errors['namereq'] = "Name is required"
        if len(postData['name']) <= 3:
            errors['namereq'] = "Name has 3 required characters"
        if len(postData['Uname']) == 0:
            errors['Unamereq'] = "User name is required"
        if len(postData['pw']) < 3:
            errors['pwreq'] = "Password needs to be at least 3 characters"
        if postData['pw'] != postData['cpw']:
            errors['cpwmatch'] = "Confirm Password Must Match"

        return errors 
    def loginValidator(self, postData):
        errors = {}
        UserMatch = User.objects.filter(Username = postData['username'])
        if len(postData['username']) == 0:
            errors['usernamereq'] = "username is required"
        elif len(UserMatch) == 0:
            errors['userNoMatch'] = "This user does not exist, register first"
        else:
            if UserMatch[0].Username != postData['username']:
                errors['usmatch']= "Incorrect Username"

        return errors

class VacationsManager(models.Manager):
    def vacationsValidator(self, postData):
        errors= {}
        if len(postData['des']) == 0:
            errors['desreq'] = "Destination is required"
        if len(postData['desc']) == 0:
            errors['descreq'] = "Description is required"
        if len(postData['leave']) == 0:
            errors['leavereq'] = "Leave Date is required"
        if len(postData['return']) == 0:
            errors['retreq'] = "Return Date is required"



        return errors 
    
class User(models.Model):
    Name = models.CharField(max_length=255)
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Vacations(models.Model):
    Name = models.CharField(max_length=255)
    TravelStart = models.CharField(max_length=255)
    TravelEnd = models.CharField(max_length=255)
    Plan = models.TextField()
    Traveler = models.ForeignKey(User, related_name= "PlacesToVisit", on_delete = models.CASCADE)
    PossibleTrips = models.ManyToManyField(User, related_name= "possible_places")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = VacationsManager()

