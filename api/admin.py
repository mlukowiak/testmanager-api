from django.contrib import admin
from .models import Scenario, ScenarioArea, ScenarioType, Comment, Rating, TestCase

admin.site.register(Scenario)
admin.site.register(ScenarioArea)
admin.site.register(ScenarioType)
admin.site.register(Comment)
admin.site.register(TestCase)
admin.site.register(Rating)
