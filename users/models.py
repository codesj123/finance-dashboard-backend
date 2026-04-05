from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  
  ROLE_CHOICES = [
    
    ('admin','Admin'),
    ('analyst','Analyst'),
    ('visitor','Visitor')
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default='visitor')
    def __str__(self):
      
      return f'{self.username} ({self.role})'
           
   def isAdmin(self):
     return self.role == self.ADMIN
   def isAnalyst(self):
     return self.role == self.ANALYST
   def isVisitor(self):
     return self.role == self.VISITOR