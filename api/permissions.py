from rest_framework.permissions import BasePermission
from .models import Content


class IsAdminOrAuthor(BasePermission):
  def has_object_permission(self, request, view, obj):
    if isinstance(obj,Content):
      return request.user.is_admin or (obj.owner == request.user)
   