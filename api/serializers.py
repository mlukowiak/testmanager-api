from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Scenario, Rating, Comment, ScenarioType, ScenarioArea, TestCase
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'

class ScenarioSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    cases = TestCaseSerializer(many=True)
    class Meta:
        model = Scenario
        fields = ('id',
                  'scenarioTitle',
                  'scenarioAuthor',
                  'scenarioArea',
                  'scenarioDate',
                  'scenarioDescription',
                  'scenarioType',
                  'scenarioInitial',
                  'scenarioFinal',
                  'cases_number',
                  'cases',
                  'ratings_number',
                  'avg_ratings',
                  'comments_number',
                  'comments')

    def all_cases(self, validated_data):
        cases_data = validated_data.pop('cases')
        scenario = Scenario.objects.create(**validated_data)
        for case_data in cases_data:
            TestCase.objects.create(scenario=scenario, **case_data)
        return scenario

    def all_comments(self, validated_data):
        comments_data = validated_data.pop('comments')
        scenario = Scenario.objects.create(**validated_data)
        for comment_data in comments_data:
            Comment.objects.create(scenario=scenario, **comment_data)
        return scenario

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class ScenarioTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioType
        fields = '__all__'

class ScenarioAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioArea
        fields = '__all__'