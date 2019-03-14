# apps/admin/viewsets.py
# Python imports


# Django imports


# Third party apps imports
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

# Local imports
from .models import Admin
from .serializers import AdminSerializer


# Create your viewsets here.


class AdminViewSet(ModelViewSet):
    serializer_class = AdminSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny, ]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if hasattr(self.request.auth.user, 'admin'):
            admin = self.request.auth.user.admin
            if admin.superadmin:
                queryset = Admin.objects.exclude(pk=admin.pk)
                return queryset

    def destroy(self, request, *args, **kwargs):
        if hasattr(request.auth.user, 'admin'):
            admin = request.auth.user.admin
            if admin.superadmin:
                return super(AdminViewSet, self).destroy(request, *args, **kwargs)
            else:
                return Response({"error": "Needs to be a super administrator"})
        else:
            return Response({"error": "Needs to be a super administrator"})

    @action(detail=True, methods=['patch'])
    def changetosuperadmin(self, request, pk=None):
        admin = Admin.objects.get(pk=pk)
        if admin.superadmin:
            return Response({"Error": "Admin is already a super-admin"})
        else:
            admin.superadmin = True
            admin.save()
        return Response({"Message": "Changed to super-admin"})
