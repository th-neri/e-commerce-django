from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # anyone can access the endpoint as long as the method(GET in this case) is in SAFE_METHODS
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff) # if request user is set and if the user is staff then return true

# can't have access to GET unless relevant model permission unlike DjangoModelPermissions that the user is able to retrieve customers
class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']