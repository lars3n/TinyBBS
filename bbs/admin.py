from django.contrib import admin
from bbs.models import *

class BBS_admin(admin.ModelAdmin):
    list_display = ("bbs_title", "bbs_summary", "bbs_author", "signature",
        "view_count", "created_at", "updated_at")
    list_filter = ("created_at", )
    search_fields = ("bbs_title", "bbs_author__user__username",)

    def signature(self, obj):
        return obj.bbs_author.signature
    signature.short_description = "qianming"

admin.site.register(BBS, BBS_admin)
admin.site.register(Category)
admin.site.register(BBS_user)
admin.site.register(Comments)
admin.site.register(CateClass)