from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin
from djangoldp_community.models import Community, CommunityMember, CommunityCircle,\
    CommunityProject, CommunityJobOffer, CommunityProfile, CommunityAddress


class EmptyAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class MemberInline(admin.TabularInline):
    model = CommunityMember
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class CircleInline(admin.TabularInline):
    model = CommunityCircle
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class ProjectInline(admin.TabularInline):
    model = CommunityProject
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class JobOfferInline(admin.TabularInline):
    model = CommunityJobOffer
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class ProfileInline(admin.StackedInline):
    model = CommunityProfile
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class AddressInline(admin.TabularInline):
    model = CommunityAddress
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class CommunityAdmin(DjangoLDPAdmin):
    exclude = ('slug', 'is_backlink', 'allow_create_backlink')
    inlines = [ProfileInline, AddressInline, MemberInline, CircleInline, ProjectInline, JobOfferInline]
    search_fields = ['urlid', 'name', 'members__user__urlid']
    ordering = ['urlid']


admin.site.register(Community, CommunityAdmin)
admin.site.register(CommunityMember, EmptyAdmin)
admin.site.register(CommunityCircle, EmptyAdmin)
admin.site.register(CommunityProject, EmptyAdmin)
admin.site.register(CommunityJobOffer, EmptyAdmin)
admin.site.register(CommunityProfile, EmptyAdmin)
admin.site.register(CommunityAddress, EmptyAdmin)
