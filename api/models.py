from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class ScenarioType(models.Model):
    scenarioTypeName = models.CharField(max_length=256)

    def __str__(self):
        return self.scenarioTypeName

class ScenarioArea(models.Model):
    scenarioAreaName = models.CharField(max_length=256)

    def __str__(self):
        return self.scenarioAreaName

class Scenario(models.Model):
    scenarioTitle = models.CharField(max_length=256)
    scenarioAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    scenarioArea = models.ForeignKey(ScenarioArea, on_delete=models.CASCADE)
    scenarioDate = models.DateTimeField(default=timezone.now)
    scenarioDescription = models.TextField()
    scenarioType = models.ForeignKey(ScenarioType, on_delete=models.CASCADE)
    scenarioInitial = models.TextField(null=True, blank=True)
    scenarioFinal = models.TextField(null=True, blank=True)

    def cases_number(self):
        cases = TestCase.objects.filter(testScenario=self)
        return len(cases)

    def ratings_number(self):
        ratings = Rating.objects.filter(scenario=self)
        return len(ratings)

    def avg_ratings(self):
        sum = 0
        ratings = Rating.objects.filter(scenario=self)
        for rating in ratings:
            sum += rating.stars
        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0

    def comments_number(self):
        comments = Comment.objects.filter(commentScenario=self)
        return len(comments)

    def __str__(self):
        return self.scenarioTitle

class Comment(models.Model):
    commentText = models.CharField(max_length=256)
    commentScenario = models.ForeignKey(Scenario, related_name='comments', on_delete=models.CASCADE)
    commentAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    commentDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.commentText) + " - " + str(self.commentAuthor) + " (" + str(self.commentScenario) + ")"

class Rating(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'scenario'),)
        index_together = (('user', 'scenario'),)

    def __str__(self):
        return str(self.scenario) + " - " + str(self.user) + " (" + str(self.stars) + ")"

class TestCase(models.Model):
    testName = models.CharField(max_length=256)
    testCondition = models.TextField(null=True, blank=True)
    testSteps = models.TextField(null=True, blank=True)
    testExpectedResult = models.TextField(null=True, blank=True)
    testScenario = models.ForeignKey(Scenario, related_name='cases', on_delete=models.CASCADE)
    testAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    testDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.testName) + " (" + str(self.testScenario) + ")"
