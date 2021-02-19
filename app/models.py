from django.db import models
from django.contrib.auth.models import User


class App(models.Model):
    appname = models.CharField(max_length=255)
    appIcon = models.ImageField(upload_to='app/images/icons')
    gitlink = models.TextField(null=True, blank=True)
    videolink = models.TextField(null=True, blank=True)
    playstorelink = models.TextField(null=True, blank=True)
    appstorelink = models.TextField(null=True, blank=True)
    weblink = models.TextField(null=True, blank=True)


    intro = models.CharField(max_length=255)
    likes = models.IntegerField(default=1)
    created = models.DateTimeField()
    start_id = models.IntegerField(default=-1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.appname

    def showInfo(self):
        return self.intro[:100]

    def get_yt_code(self):
        l = self.videolink.split('/')
        print(l)
        return l[-1]


class SnapAndDetail(models.Model):
    screenshot = models.ImageField(upload_to='app/images/appdata/snaps')
    header = models.CharField(max_length=255)
    info = models.TextField()
    prev_id = models.IntegerField(default=-1)
    next_id = models.IntegerField(default=-1)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return self.header[:20]

class TechStack(models.Model):
    icon =  models.ImageField(upload_to='app/images/techstack/icons')
    name = models.CharField(max_length=255)
    link = models.TextField(null=True, blank=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
