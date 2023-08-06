from djangoldp.permissions import LDPPermissions
from django.urls import resolve
from djangoldp.utils import is_authenticated_user
from djangoldp_project.permissions import ProjectPermissions
from djangoldp_circle.permissions import CirclePermissions


class CommunityPermissions(LDPPermissions):

    filter_backends = []

    def _get_community_from_obj(self, obj):
        from djangoldp_community.models import Community
        if isinstance(obj, Community):
            return obj

        if not hasattr(obj, 'community') or not isinstance(obj.community, Community):
            raise KeyError('Object ' + str(obj) + ' must have a ForeignKey "community" to model Community to use CommunityPermissions')

        return obj.community

    def get_object_permissions(self, request, view, obj):
        from djangoldp_community.models import Community, CommunityMember

        perms = set(super().get_object_permissions(request, view, obj))
        allow_continue = True
        if hasattr(obj, 'project'):
            if not obj.project.members.filter(user=request.user).exists() or obj.project.status != "Public":
                allow_continue = False
        elif hasattr(obj, 'circle'):
            if not obj.circle.members.filter(user=request.user).exists() or obj.circle.status != "Public":
                allow_continue = False

        if allow_continue:
            perms = perms.union({'view'})

            community = self._get_community_from_obj(obj)

            if is_authenticated_user(request.user) and community.members.filter(user=request.user).exists():
                # Any member can add a job offer, circle or project to the community
                if not isinstance(obj, Community) and not isinstance(obj, CommunityMember):
                    perms = perms.union({'add'})

                member = community.members.get(user=request.user)
                if member.is_admin:
                    # Admins can add members
                    perms = perms.union({'add', 'change'})

                    if isinstance(obj, CommunityMember):
                        if (obj.user == request.user and community.members.filter(is_admin=True).count() > 1) \
                                or not obj.is_admin:
                            # Admins can't delete community or other admins, but have super-powers on everything else
                            # I can't delete myself if I am the last member
                            perms = perms.union({'delete'})
                    elif not isinstance(obj, Community):
                        perms = perms.union({'delete'})
                elif isinstance(obj, CommunityMember) and obj.user == request.user:
                    perms = perms.union({'delete'})

        return perms


class CommunityCirclePermissions(CirclePermissions):
    filter_backends = []

    def get_object_permissions(self, request, view, obj):
        obj = obj.circle
        return set(super().get_object_permissions(request, view, obj))

    def get_container_permissions(self, request, view, obj=None):
        perms = super().get_container_permissions(request, view, obj, True)
        if obj is None:
            from djangoldp_community.models import Community
            resolved = resolve(request.path_info)
            if hasattr(resolved.kwargs, 'slug'):
                community = Community.objects.get(slug=resolved.kwargs['slug'])
                if community.members.filter(user=request.user).exists():
                    perms = perms.union({'add'})
        return perms


class CommunityProjectPermissions(ProjectPermissions):
    filter_backends = []

    def get_object_permissions(self, request, view, obj):
        obj = obj.project
        return set(super().get_object_permissions(request, view, obj))

    def get_container_permissions(self, request, view, obj=None):
        perms = super().get_container_permissions(request, view, obj, True)
        if obj is None:
            from djangoldp_community.models import Community
            resolved = resolve(request.path_info)
            if hasattr(resolved.kwargs, 'slug'):
                community = Community.objects.get(slug=resolved.kwargs['slug'])
                if community.members.filter(user=request.user).exists():
                    perms = perms.union({'add'})
        else:
            return self.get_object_permissions(request, view, obj)
        return perms


class CommunityJobPermissions(LDPPermissions):
    filter_backends = []

    def get_object_permissions(self, request, view, obj):
        obj = obj.joboffer
        return set(super().get_object_permissions(request, view, obj))

    def get_container_permissions(self, request, view, obj=None):
        perms = super().get_container_permissions(request, view, obj)
        if obj is None:
            from djangoldp_community.models import Community
            resolved = resolve(request.path_info)
            if hasattr(resolved.kwargs, 'slug'):
                community = Community.objects.get(slug=resolved.kwargs['slug'])
                if community.members.filter(user=request.user).exists():
                    perms = perms.union({'add'})
        else:
            return self.get_object_permissions(request, view, obj)
        return perms


class CommunityMembersPermissions(CommunityPermissions):
    filter_backends = []

    def get_container_permissions(self, request, view, obj=None):
        perms = set({'view'})
        if obj is None:
            from djangoldp_community.models import Community
            resolved = resolve(request.path_info)
            if hasattr(resolved.kwargs, 'slug'):
                community = Community.objects.get(slug=resolved.kwargs['slug'])
                if community.members.filter(user=request.user).exists():
                    if community.members.get(user=request.user).is_admin:
                        perms = perms.union({'add'})
        else:
            return self.get_object_permissions(request, view, obj)
        return perms
