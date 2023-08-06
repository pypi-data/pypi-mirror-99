from rest_framework import permissions


class LocalhostPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        return ip_addr in ['127.0.0.1', '::1']
