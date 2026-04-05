from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser

class TransactionModel(models.Model):

  Categories = [('salary', 'Salary'),('investment', 'Investment'),('rent', 'Rent'),('utilities','Utilitis'),('food','Food'),('transport','Transport'),('other','Other')]
  amount = models.DecimalField(max_digits=12, decimal_places=2)
  transaction_type = models.CharField(max_length=10, choices=[('income'),('expenses')])
  description = models.TextField()
  date = models.DateField()
  category = models.CharField(max_length=20, choices=Categories)
  created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    related_name='transactions'
  )
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now=True)
  is_deleted = models.BooleanField(default=False)
  
  class Meta:
    ordering=['-date']
  
  
  def __str__(self):
    return f'{self.transaction_type} | {self.amount} | {self.category}'
    