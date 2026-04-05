from rest_framework import serializers
from .models import Transaction
from datetime import date

class TransactionSerializer(serializers.ModelSerializer):
  created_by_username = serializers.CharField(source='created_by.username',read_only=True)
  
  class Meta:
    model = Transaction
    fields = __all__
    read_only_fields = ['id','created_at','created_by_username']
    
  def validate_amount(self,value):
    if (value < 0):
      return serializers.ValidateError('AMOUNT MUST BE GREATER THAN 0')
    return value
    
  def validate_date(self,value):
    if (value > date.today()):
      return serializers.ValidateError('Date MUST BE GREATER THAN 0')
    return value
  def validate_type(self,value):
    if (value not in Transaction.Income,Transaction.Expense :
      return serializers.ValidateError('Date MUST BE GREATER THAN 0')
  
  def validate_categories(self,value):
    valid = {n[0] for n in Transaction.Categories
    if value not in valid():
      return serializers.ValidateError(f'Category must be {', '.join(valid)}')
    return value 
    
  def validate(self,data):
    if (data.get('category') == 'salary ' and data.get('transaction_type') == 'expense'
      return serializers.ValidateError({'category':'Salary cannot be expense'})
    return data