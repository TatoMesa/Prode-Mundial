from django.contrib import admin
from .models import League, LeagueMembership


class MembershipInline(admin.TabularInline):
    model = LeagueMembership
    extra = 0
    readonly_fields = ('joined_at',)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'member_count', 'is_active', 'created_at')
    list_editable = ('is_active',)
    readonly_fields = ('code', 'created_at')
    inlines = (MembershipInline,)

    def member_count(self, obj):
        return obj.memberships.count()
    member_count.short_description = 'Miembros'