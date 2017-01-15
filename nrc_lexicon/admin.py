from django.contrib import admin

# Register your models here.
from .models import Emotion, Word




class EmotionAdmin(admin.ModelAdmin):
	fieldsets = [(None, {'fields': ['emotions']}),]

	search_fields = ['emotion']



class WordAdmin(admin.ModelAdmin):
	fieldsets = [(None, {'fields': ['word']})]


	search_fields = ['word']




admin.site.register(Emotion, EmotionAdmin)

admin.site.register(Word, WordAdmin)
