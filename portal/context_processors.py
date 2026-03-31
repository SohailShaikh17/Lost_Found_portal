from .models import Item
def portal_stats(request):
    return {
        'site_total_lost': Item.objects.filter(item_type='LOST').count(),
        'site_total_found': Item.objects.filter(item_type='FOUND').count(),
        'site_total_claimed': Item.objects.filter(status__in=['CLAIMED','RESOLVED']).count(),
    }
