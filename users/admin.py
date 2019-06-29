from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, FamilyInfo, Education, Profile, Connection, Friend


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['id', 'username', 'first_name', 'last_name']

class FamilyInfoAdmin(admin.ModelAdmin):
    model = FamilyInfo
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

class EducationAdmin(admin.ModelAdmin):
    model = Education
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['id', 'user']

    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

class ConnectionAdmin(admin.ModelAdmin):
    model = Connection
    list_display = ['follower', 'created_date', 'show_following']

    def show_following(self, obj):
        return ", ".join([
            following.user.username for following in obj.following.all()
        ])

class FriendAdmin(admin.ModelAdmin):
    model = Friend
    list_display = ['follower', 'following', 'created_date']





admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(FamilyInfo, FamilyInfoAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Friend, FriendAdmin)
