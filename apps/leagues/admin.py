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
        
        ('Sección 1 — Primera Ronda', {
            'fields': ('prizes_title', 'prize_1_name', 'prize_1_description', 'prize_1_image', 
                       'prize_2_name', 'prize_2_description', 'prize_2_image', 
                       'prize_3_name', 'prize_3_description', 'prize_3_image')
        }),
        
        ('Sección 2 — Partido de Argentina', {
            'fields': ('prizes_title2', 'prize_4_name', 'prize_4_description', 'prize_4_image', 
                       'prize_5_name', 'prize_5_description', 'prize_5_image', 
                       'prize_6_name', 'prize_6_description', 'prize_6_image')
        }),
        
        ('Sección 3 — Resultado Exacto', {
            'fields': ('prizes_title3', 'prize_7_name', 'prize_7_description', 'prize_7_image', 
                       'prize_8_name', 'prize_8_description', 'prize_8_image', 
                       'prize_9_name', 'prize_9_description', 'prize_9_image')
        }),
        
        ('Sección 4 — Mundial Completo', {
            'fields': ('prizes_title4', 'prize_10_name', 'prize_10_description', 'prize_10_image', 
                       'prize_11_name', 'prize_11_description', 'prize_11_image', 
                       'prize_12_name', 'prize_12_description', 'prize_12_image')
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