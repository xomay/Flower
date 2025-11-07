from django.contrib.auth.models import Group
from rest_framework import permissions

def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None

def get_groups(user):
    return list(Group.objects.filter(user = user).values_list('name', flat=True))

def get_groups(poste):
    return list(Group.objects.filter(poste = poste).values_list('name', flat=True))

class HasGroupPermission(permissions.BasePermission):
    """
    Ensure user is in required groups.
    """

    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.
        required_groups_mapping = getattr(view, "required_groups", {})

        # Determine the required groups for this particular request method.
        required_groups = required_groups_mapping.get(request.method, [])

        # Return True if the user has all the required groups or is staff.
        return all([is_in_group(request.user, group_name) for group_name in required_groups])

class HasAnyGroupPermission(permissions.BasePermission):
    """
    Autorise l’accès si l’utilisateur a au moins un des rôles requis.
    """

    def has_permission(self, request, view):
        required_groups_mapping = getattr(view, "required_groups", {})
        required_groups = required_groups_mapping.get(request.method, [])

        # Si aucune restriction n’est définie pour cette méthode → accès autorisé
        if not required_groups:
            return True

        # Si l’utilisateur est staff, il passe toujours
        if request.user and request.user.is_staff:
            return True

        # Autoriser si l'utilisateur a AU MOINS un des groupes
        return any(is_in_group(request.user, group_name) for group_name in required_groups)

from flower_app.models.Etude import Etude
from flower_app.models.People.Realisateur import Realisateur

class HasReaPermissionToSeeEtude(permissions.BasePermission):
    def has_permission(self, request, view):
        pk_url = request.parser_context['kwargs']['pk']
        etude_instance = Etude.objects.get(pk=pk_url)
        try:
            Realisateur.objects.get(user=request.user).mission_set.get(project=etude_instance)
            return True
        except:
            return False