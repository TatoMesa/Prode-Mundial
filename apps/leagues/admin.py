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

    fieldsets = (
        ('Datos básicos', {
            'fields': ('name', 'code', 'is_active', 'logo'),
        }),
        ('🥇 Premio 1', {
            'classes': ('collapse',),
            'fields': ('prize_1_name', 'prize_1_description', 'prize_1_image'),
        }),
        ('🥈 Premio 2', {
            'classes': ('collapse',),
            'fields': ('prize_2_name', 'prize_2_description', 'prize_2_image'),
        }),
        ('🥉 Premio 3', {
            'classes': ('collapse',),
            'fields': ('prize_3_name', 'prize_3_description', 'prize_3_image'),
        }),
        ('🏅 Premio 4', {
            'classes': ('collapse',),
            'fields': ('prize_4_name', 'prize_4_description', 'prize_4_image'),
        }),
        ('📣 Sección de marketing', {
            'classes': ('collapse',),
            'fields': (
                'marketing_title', 'marketing_text', 'marketing_image',
                'marketing_link_text', 'marketing_link_url',
            ),
        }),
    )

    def member_count(self, obj):
        return obj.memberships.count()
    member_count.short_description = 'Miembros'