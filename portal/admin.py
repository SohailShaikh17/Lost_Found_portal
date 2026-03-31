from django.contrib import admin
from .models import Profile, Category, Item, ClaimRequest

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','department','phone_number')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title','item_type','category','location','status','user','created_at')
    list_filter = ('item_type','status','category')
    search_fields = ('title','description','location')

@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('item','claimant','status','created_at')
    list_filter = ('status',)
