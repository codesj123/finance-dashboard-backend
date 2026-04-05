from rest_framework.permissions import BasePermission
from . import models
class isAdmin(BasePermission):
  def has_permission(self, request, view):
    return (request.user.is_authenticated and request.user.role == 'admin')
    
class isAnalyst(BasePermission):
  def has_permission(self, request, view):
    return (request.user.is_authenticated and request.user.role in ['analyst','admin'])
    
class isVisitor(BasePermission):
  def has_permission(self, request, view):
    return (request.user.is_authenticated)