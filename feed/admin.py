from django.contrib import admin
from .models import *
from django.http import HttpResponse
import csv, io

# Register your models here.
admin.site.register(User)
admin.site.register(RealUser)
admin.site.register(Post)
admin.site.register(CommentPost)
admin.site.register(ParentPost)


# PostInteractionTracker Admin Custom Features
def export_results(modeladmin, request, queryset):
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(["Action Timestamp (UTC)", "User Display Name", "Username", "User Action", "User Action Content",
                     "Post ID", "Post Create Date (UTC)", "Post Author ID", "Post Author Name", "Post Text"])

    for entry in queryset:
        writer.writerow([
            entry.timestamp,
            entry.user.name,
            entry.user.user_name,
            entry.action,
            entry.content,
            entry.post_id,
            entry.post.create_date,
            entry.post.author.id,
            entry.post.author.name,
            entry.post.text
        ])

    return HttpResponse(output.getvalue(), content_type="text/plain")


export_results.short_description = "Export selected trackers"


class PostInteractionTrackerAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'post']
    ordering = ['-timestamp']
    actions = [export_results]


admin.site.register(PostInteractionTracker, PostInteractionTrackerAdmin)