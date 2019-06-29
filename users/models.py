from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



GENDER_CHOICES = (
    ('m', 'male'),
    ('f', 'female'),
)

EDUCATION_CHOICES = (
    ('ug10', 'Under Grade 10'),
    ('gd10', 'Grade 10'),
    ('gd12', 'Grade 12'),
    ('ba', 'Bachelors'),
    ('ma', 'Masters'),
    ('mphl', 'M.Phil'),
    ('phd', 'Ph.D'),

)

FAMILY_CHOICES = (
    ('f', 'Father'),
    ('m', 'Mother'),
    ('gf', 'Grand Father'),
    ('gm', 'Gran Mother'),
    ('b', 'Brother'),
    ('si', 'Sister'),
    ('s', 'Son'),
    ('d', 'Daughter'),
    ('h', 'Husband'),
    ('w', 'Wife')

)

MARITAL_STATUS = (
    ('m', 'married'),
    ('u', 'unmarried'),
)


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    # GENDER_CHOICES = (
    #     ('m', 'male'),
    #     ('f', 'female')
    #     )
    # email = models.EmailField(unique=True)
    # birth_date = models.DateField(null=True, blank=True)
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    objects = CustomUserManager()


class ProfileManger(UserManager):
    pass

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    m_status = models.TextField(max_length=1, choices=MARITAL_STATUS, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    village = models.CharField(max_length=35, blank=True, null=True)
    State = models.CharField(max_length=25, blank=True, null=True)
    country =models.CharField(max_length=25, null= True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='gallery/profile_pic', null=True, default='static/images/empty_avatar.png')
    cnic = models.IntegerField(max_length=13, null=True, unique=True)

    objects = ProfileManger()

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class EducationManager(UserManager):
    pass


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    school = models.CharField(max_length=50)
    qualification = models.CharField(max_length=4, choices=EDUCATION_CHOICES)
    fieldOfStudy = models.CharField(max_length=50)
    dateFrom = models.DateField(auto_now=False, auto_now_add=False)
    dateTo = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    current = models.BooleanField(default=False)
    graduated = models.BooleanField(default=False)

    objects = EducationManager()

    def __str__(self):
        return self.profile.user.first_name


class FamilyInfoManager(UserManager):
    pass

class FamilyInfo(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    familychoice = models.CharField(max_length=2, choices=FAMILY_CHOICES)
    name = models.CharField(max_length=50)
    m_status = models.CharField(max_length=1, choices=MARITAL_STATUS)
    objects = FamilyInfoManager()

    def __str__(self):
        return self.profile.user.first_name


class Connection(models.Model):

    following = models.ManyToManyField(Profile, related_name='following')
    follower = models.ForeignKey(Profile, related_name='follower', null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    # def get_follows(self):
    #     return "\n".join([f.followings for f in self.followings.all()])


# Just handle profile ids in models, forget about user ids

    @classmethod
    def follow(cls, current_user, new_friend):
        current_user = Profile.objects.get(id=current_user)
        connection, created = cls.objects.get_or_create(
            follower=current_user
        )
        new_follow = Profile.objects.get(id=new_friend)
        new_follow = new_follow.id
        connection.following.add(new_follow)

    @classmethod
    def unfollow(cls, current_user, remove_friend):
        current_user = Profile.objects.get(id=current_user)
        connection, created = cls.objects.get_or_create(
            follower=current_user
        )
        remove_follow = Profile.objects.get(id=remove_friend)
        remove_follow = remove_follow.id
        connection.following.remove(remove_follow)



class Friend(models.Model):

    following = models.ForeignKey(Profile, related_name='i_follow', on_delete=models.CASCADE)
    follower = models.ForeignKey(Profile, related_name='my_follower', null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.following.user.first_name