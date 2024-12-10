from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Topic, Material, Quiz, Question, UserResult, UserAnswer

# Register your models here.

admin.site.register(Topic)

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'is_approved', 'uploaded_by','topic')
    list_filter = ('is_approved', 'material_type', 'topic', 'uploaded_by')
    actions = ['approved_materials']

    def approve_materials(self, request, queryset):
        queryset.update(is_approved=True)
        self.massage(request, "Material is approved")

    def get_queryset(self, request):
        queryset = super(). get_queryset(request)

        if request.user.is_superuser: # shows the material to the admin
            return queryset

        # what the user can see? Only approved material
        return queryset.filter(is_approved= False)
    
admin.site.register(Material,MaterialAdmin)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(UserResult)
admin.site.register(UserAnswer)