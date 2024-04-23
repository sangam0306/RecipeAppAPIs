from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from authe.models import Profile


class ModelAPIView(APIView):
    permission_classes = [IsAuthenticated]


class RegisterView(APIView):
    def post(self, request):
        request_data = request.data

        user_name = request_data["userName"]
        password = request_data["passward"]
        email = request_data["email"]
        name = request_data["name"]
        description = request_data["description"]

        user_obj = User.objects.create(
            username=user_name, password=password, email=email
        )

        profile_obj = Profile.objects.create(
            user=user_obj,
            name=name,
            description=description,
        )

        response_data = {"msg": "Register successfully", "UserId": user_obj.pk, "ProfileId": profile_obj.pk}
        status = 200
        return Response(data=response_data, status=status)


class LoginView(APIView):
    def get(self, request):
        user_name = request.GET.get("userName")
        password = request.GET.get("passward")

        print(user_name, password)

        if User.objects.filter(username=user_name, password=password).count() == 1:
            user_obj = User.objects.get(username=user_name, password=password)

            refresh_token = RefreshToken.for_user(user_obj)

            response_data = {
                "email": user_obj.email,
                "userName": user_obj.username,
                "accessToken": str(refresh_token.access_token),
                "refreshToken": str(refresh_token),
            }
            status = 200
        else:
            response_data = {"msg": "User does not exist"}
            status = 404

        return Response(data=response_data, status=status)


class ProfileView(ModelAPIView):
    def get(self, request):
        name = request.GET.get('name')

        if Profile.objects.filter(name=name).count() == 1:
            profile_obj = Profile.objects.get(name=name)

            response_data = {
                "name": profile_obj.name,
                "description": profile_obj.description,
                "user": profile_obj.user.username
            }

            status = 200
        else:
            response_data = {
                "msg": f"Profile not found for name {name}"
            }
            status = 400

        return Response(data=response_data, status=status)

    def put(self, request):
        request_data = request.data
        name = request_data['name']

        if Profile.objects.filter(name=name).count() == 1:
            profile_obj = Profile.objects.get(name=name)

            profile_obj.description = request_data["description"]
            profile_obj.photo = request_data["photo"]
            profile_obj.save()

            response_data = {"msg": "Profile updated successfully"}
            status = 200
        else:
            response_data = {
                "msg": f"Profile not found for name {name}"
            }
            status = 400

        return Response(data=response_data, status=status)

    def delete(self, request):
        name = request.GET.get('name')

        if Profile.objects.filter(name=name).count() == 1:
            profile_obj = Profile.objects.get(name=name)
            profile_obj.delete()

            response_data = {
                "msg": "Profile deleted successfully."
            }

            status = 200
        else:
            response_data = {
                "msg": f"Profile not found for name {name}"
            }
            status = 400

        return Response(data=response_data, status=status)
