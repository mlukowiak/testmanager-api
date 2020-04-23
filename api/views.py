from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Scenario, Rating, Comment, ScenarioArea, ScenarioType, User, TestCase
from .serializers import ScenarioSerializer, RatingSerializer, CommentSerializer, ScenarioTypeSerializer, ScenarioAreaSerializer, TestCaseSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def add_testcase(self, request, pk=None):
        if 'testName' in request.data:
            testScenario = Scenario.objects.get(id=pk)
            testName = request.data['testName']
            testCondition = request.data['testCondition']
            testSteps = request.data['testSteps']
            testExpectedResult = request.data['testExpectedResult']
            testAuthor = request.user
            try:
                case = TestCase.objects.create(testAuthor=testAuthor,
                                               testScenario=testScenario,
                                               testName=testName,
                                               testCondition=testCondition,
                                               testSteps=testSteps,
                                               testExpectedResult=testExpectedResult)
                serializer = TestCaseSerializer(case, many=False)
                response = {'message': 'Dodano przypadek testowy!',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                raise Exception("Wystąpił błąd!")
        else:
            response = {'message': 'Nie podałeś nazwy przypadku testowego!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def rate_scenario(self, request, pk=None):
        if 'stars' in request.data:
            scenario = Scenario.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            try:
                rating = Rating.objects.get(user=user.id,
                                            scenario=scenario.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Zmieniono ocenę!', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user,
                                               scenario=scenario,
                                               stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Dodano ocenę!', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'Nie podałeś oceny!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def comment_scenario(self, request, pk=None):
        if 'commentText' in request.data:
            commentScenario = Scenario.objects.get(id=pk)
            commentText = request.data['commentText']
            commentAuthor = request.user
            try:
                comment = Comment.objects.create(commentAuthor=commentAuthor,
                                                 commentScenario=commentScenario,
                                                 commentText=commentText)
                serializer = CommentSerializer(comment, many=False)
                response = {'message': 'Dodano komentarz!',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                raise Exception("Wystąpił błąd!")
        else:
            response = {'message': 'Nie podałeś treści komentarza!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz tworzyć scenariuszy w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz edytować scenariuszy w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz usunąć scenariuszy w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class TestCaseViewSet(viewsets.ModelViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz tworzyć przypadków w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz edytować przypadków w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz usunąć przypadków w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RatingoViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz oceniać w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz edytować ocen w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz usunać ocen w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz komentować w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz edytować komentarzy w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz usunać komenatrzy w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class ScenarioAreaViewSet(viewsets.ModelViewSet):
    queryset = ScenarioArea.objects.all()
    serializer_class = ScenarioAreaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz stworzyć obszarów w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz edytować obszarów w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz utworzyć obszaró w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class ScenarioTypeViewSet(viewsets.ModelViewSet):
    queryset = ScenarioType.objects.all()
    serializer_class = ScenarioTypeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz stworzyć typu w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz edytować typu w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Nie możesz usunąć typu w ten sposób!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)