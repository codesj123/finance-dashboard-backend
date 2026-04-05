from django.shortcuts import render
from django.db.models import Q
from django.conf import settings
from django.db.model.functions import TruncMonth
from django.db.models.functions import TruncMonth
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import *
from .serializers import *
from .pagination import *

class TransactionListView(APIView):
  def get_permissions(self):
    if self.request.method == 'GET':
      return isVisitor()
    return isAdmin()
    
  def get(self,request):
    transaction = Transaction.objects.filter(is_deleted = False)
    
    t_type = request.query_params.get('transaction_type')
    category = request.query_params.get('category')
    date_from = request.query_params.get('from')
    date_to = request.query_params.get('to')
   
   if (t_type in ['income','expense']):
     transaction = transaction.filter(transaction_type=t_type)
   if category:
     transaction = transaction.filter(category= category)
   if date_from:
     transaction = transaction.filter(date_gte=date_from)
   if date_to:
     transaction = transaction.filter(date_lte=date_to)
   
   pagination= TransactionPagination()
   page = pagination.paginate_queryset(transaction,request)
    serializer = (TransactionSerializer(page,many=True,))
    return pagination.get_paginated_response(serializer.data)
    
  def post(self,request):
    serializer = TransactionSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save(created_by = request.user)
       return Response(serializer.data)
    return Response(serializer.error, ststus =400)
  
  
class TransactionDetailView(APIView):
  def get_permissions(self):
    if self.request.method == "GET":
      return isVisitor()
    return isAdmin()
    
  def get_object(self,pk):
    try:
      return Transaction.objects.get(pk=pk,is_deleted=False)
    except Transaction.DoesNotExist:
      return None
    
  def get(self,request,pk):
    t = self.get_object(pk)
    if not t:
      return Response({'error': 'transaction not found'},status=404)
    return Response(TransactionSerializer(t).data)
  def put(self,request,pk):
    t = self.get_object(pk)
    if not t:
      return Response({'error': 'transaction not found'},status=404)
    serializer = (TransactionSerializer(t,data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors,status=400)  
   
  def delete(self,request,pk):
    t = Transaction.objects.get(pk=pk, is_deleted = False )
    t.is_deleted = True
    t.save()
    return Response({'message' : 'Deleted'},status=204)
  
class AnalystDetailView(APIView):
      t = Transaction.objects.filter(pk=pk, is_deleted = False )
      totals = t.aggregate(
        total_income = Sum('amount',filter=Q(transaction_type=Transaction.INCOME))
        total_expense = Sum('amount',filter=Q(transaction_type=Transaction.EXPENSE))
        )
        
        total_income=totals['total_income'] or 0
        total_expense=totals['total_expense'] or 0
        
        by_categories = (
          t.values('category')
          .annotate(total=Sum('amount'))
          .order_by('-total')
        )
        
        recent=t.order_by('-date')[:5]
        
        return Response({
          'total_income' : str('total_income'),
          'total_expense' : str('total_expense'),
          'net_balance' :str(total_income- total_expense),
          'by_category' :list(by_category),
          'recent_activity': TransactionSerializer(recent,many=True).data
          
        })
        
class AnalyticsDetailView(APIView):
  t = Transaction.objects.filter( is_deleted = False )
  
  monthly = {
    t.annotate(month=TruncMonth('date'))
    .values('month','type')
    .annotate(total=Sum('amount'))
    .order_by('month')
  }
  
  return Response({'monthly_trends' : list(monthly)})