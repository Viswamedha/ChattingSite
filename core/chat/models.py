from django.db import models
from django.urls import reverse
from main.models import User
from django.template.defaultfilters import slugify
import uuid, pytz

# Create your models here.
class Room(models.Model):

    tag = models.UUIDField(verbose_name = 'Tag', default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 64, unique = True)
    slug = models.SlugField(null = False, unique = True, blank = True)
    description = models.TextField(default = '')
    private = models.BooleanField(default = False)
    allowed = models.ManyToManyField(User, related_name = 'private_rooms', blank = True)
    maximum = models.IntegerField(default = 100)

    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse('room_view', args=[self.slug,])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Message(models.Model):

    tag = models.UUIDField(verbose_name = 'Tag', default = uuid.uuid4, editable = False)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    sent = models.DateTimeField(auto_now_add = True)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    visible = models.BooleanField(default = True)
    content = models.CharField(max_length = 5000)

    @property
    def created(self):
        local = pytz.timezone('Europe/London')
        r = self.sent.astimezone(local)
        return r.strftime('%b %d, %Y %H:%M:%S')

    class Meta:
        ordering = ('sent',)