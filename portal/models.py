from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    def __str__(self): return f"{self.user.username} Profile"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Item(models.Model):
    ITEM_TYPES = [('LOST','Lost'),('FOUND','Found')]
    STATUS_CHOICES = [('OPEN','Open'),('CLAIMED','Claimed'),('RESOLVED','Resolved')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_of_event = models.DateField()
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    contact_info = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse('item_detail', args=[self.pk])

class ClaimRequest(models.Model):
    CLAIM_STATUS = [('PENDING','Pending'),('APPROVED','Approved'),('REJECTED','Rejected')]
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims_made')
    message = models.TextField()
    proof_note = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=CLAIM_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('item','claimant')
        ordering = ['-created_at']
    def __str__(self): return f"{self.claimant.username} -> {self.item.title}"
