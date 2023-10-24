from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category

class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content','post_photo','photo', 'cat','husband','tags']
    #exclude = ['tags', 'is_published']
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ['tags']
    #filter_vertical = ['tags']

    list_display = ('id','post_photo', 'title', 'time_create', 'is_published','cat')
    list_display_links = ('id','title',)
    ordering = ['time_create','title']
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published','set_draft']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [MarriedFilter,'cat__name', 'is_published']
    save_on_top = True

    @admin.display(description="Изображение")
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Без фото"

    @admin.display(description="Краткое описание",ordering='content')
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов."

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count=queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')





#admin.site.register(Women,WomenAdmin)

# Register your models here.
