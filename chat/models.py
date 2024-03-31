from django.db import models
from user.models import BaseUser

class ChatMessage(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="user",null=True)
    sender = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="receiver")

    image = models.ImageField(upload_to='message_images', null=True, blank=True)
    message = models.TextField(max_length=1000, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =  ['date']
        verbose_name_plural = 'Message'

    def __str__(self):
        return f"{self.id} - {self.sender} - {self.receiver}"