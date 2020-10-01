from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from .models import Movie, Rating
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import MovieSerializer, RatingSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer


# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
  queryset = Movie.objects.all()
  serializer_class = MovieSerializer
  authentication_classes = (TokenAuthentication, )
  @action(detail=True, methods=["POST"])
  def rate_movie(self, request, pk=None):
    if 'stars' in  request.data:
      movie = Movie.objects.get(id=pk)
      stars = request.data['stars']
      user = request.user

      try:
        rating = Rating.objects.get(user=user.id, movie=movie.id)
        rating.stars = stars
        rating.save()
        serializer = RatingSerializer(rating, many=False)
        response = {
        "me sage": "it's working",
        "result" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
      except:
        rating = Rating.objects.create(user=user, movie=movie, stars=stars)
        serializer = RatingSerializer(rating, many=False)
        response = {
        "me sage": "it's working create",
        "result" : serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


     
    else:
      response = {
        "message": "PROVIDE STARS"
      } 
      return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
  queryset = Rating.objects.all()
  serializer_class = RatingSerializer
  authentication_classes = (TokenAuthentication, )