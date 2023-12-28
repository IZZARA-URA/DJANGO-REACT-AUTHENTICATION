from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser): 
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    
    def profile(self): 
        profile = Profile.objects.get(user=self)
        
    def __str__(self):
        return self.username 
    
class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    full_name = models.CharField(max_length=300)
    bio = models.CharField(max_length=300)
    image = models.ImageField(upload_to="user_image", default="default.jpg")
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs): 
        if self.full_name == "" or self.full_name == None: 
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)
    

def create_user_profile(sender, instance, created, **kwargs): 
    if created: 
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs): 
    instance.profile.save()
    
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
    
    
class ChatMessage(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reciever")
    
    message = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Mete: 
        odering = ['date']
        verbose_name_plural = 'Message'
        
    def __str__(self):
        return f"{self.sender} - {self.reciever}"
    
    @property
    def sender_profile(self):
        sender_profile = Profile.objects.get(user=self.sender)
        return sender_profile
    
    @property 
    def reciever_profile(self): 
        receiver_profile = Profile.objects.get(user=self.reciever)
        return receiver_profile
    
    

    