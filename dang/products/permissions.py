from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_seller & request.user.seller.able_to_post:
            return True
        return False

    # check whether the creator of object is the same as the user
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.created_by == request.user:
            return True
        return False
