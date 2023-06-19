from django.contrib import admin
from postApp.models import Author, Post, BlockedUser, Comment, Interest, Skill, File


# Register your models here.


class AuthorAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (request.user == obj.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (request.user == obj.user):
            return True
        return False

    def has_view_permission(self, request, obj=None):
        return True


admin.site.register(Author,AuthorAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author",)
    search_fields = ("title","content",)
    list_filter = ("createdOn",)


    def has_add_permission(self, request):
        return True


    def has_change_permission(self, request, obj=None):
        #if request.user.is_superuser:
            #return True
        if obj and (obj.author.user == request.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and (obj.author.user == request.user):
            return True
        return False


    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and not BlockedUser.objects.filter(blocked_user__user=request.user,
                                                  blocking_user__user=obj.author.user).exists():
            return True
        return False


admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("content","createdOn")
    #Корисник може да додаде коментар само на пост кој е видлив за него, па затоа нема потреба од проверка
    #во оваа метода дали корисникот е блокиран од страна на авторот на постот
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author.user == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author.user == request.user:
            return True
        if obj and obj.post.author.user == request.user:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and not BlockedUser.objects.filter(blocked_user__user=request.user,
                                                  blocking_user__user=obj.post.author.user).exists():
            return True
        return False

admin.site.register(Comment,CommentAdmin)


class BlockedUserAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and obj.blocking_user.user == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and obj.blocking_user.user == request.user:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        return True

admin.site.register(BlockedUser,BlockedUserAdmin)

class InterestAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author.user == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author.user == request.user:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        return True

admin.site.register(Interest,InterestAdmin)

class SkillAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author.user == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author.user == request.user:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        return True

admin.site.register(Skill,SkillAdmin)

class FileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
       if request.user.is_superuser:
           return True
       if obj and obj.post.author.user == request.user:
           return True
       return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.post.author.user == request.user:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and not BlockedUser.objects.filter(blocked_user__user=request.user,
                                                  blocking_user__user=obj.post.author.user).exists():
            return True
        return False

admin.site.register(File,FileAdmin)
