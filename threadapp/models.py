from django.db import models

from accountapp.models import Company


class Thread(models.Model):
    thread_cd = models.CharField(max_length=50, unique=True)
    thread_nm = models.CharField(max_length=200, null=False)
    content = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='thread/', null=True)
    owner = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='company', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.thread_cd} - {self.thread_nm}"
