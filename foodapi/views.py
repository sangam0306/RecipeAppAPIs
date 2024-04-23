from rest_framework.response import Response
from authe.views import ModelAPIView
from foodapi.models import Tag, Receipe, Indegridents
from django.core.serializers import serialize


class TagView(ModelAPIView):
    def post(self, request):
        request_data = request.data
        tag_name = request_data["tagName"]

        if Tag.objects.filter(name=tag_name).exists():
            msg = "already exists"
        else:
            Tag.objects.create(name=tag_name)
            msg = "created successfully"

        response_data = {
            "msg": msg,
        }

        return Response(status=200, data=response_data)


class IngredientView(ModelAPIView):
    def post(self, request):
        request_data = request.data
        ingredient_name = request_data["ingredientName"]

        if Indegridents.objects.filter(name=ingredient_name).exists():
            msg = "already exists"
        else:
            Indegridents.objects.create(name=ingredient_name)
            msg = "created successfully"

        response_data = {
            "msg": msg,
        }

        return Response(status=200, data=response_data)


class RecipeView(ModelAPIView):
    def get(self, request):
        recipe_name = request.GET.get("recipeName")

        if Receipe.objects.filter(name=recipe_name).exists():
            recipe_obj = Receipe.objects.get(name=recipe_name)

            tags_objs = recipe_obj.tags.all()
            tag_json = serialize("json", tags_objs)

            ingredients_objs = recipe_obj.indegridents.all()
            ingredients_json = serialize("json", ingredients_objs)

            response_data = {
                "recipeName": recipe_name,
                "tags": tag_json,
                "ingredients": ingredients_json,
                "time": recipe_obj.time_minutes,
                "url": recipe_obj.video_urls,
                "price": recipe_obj.price,
                "userName": recipe_obj.user.username,
            }

            status = 200
        else:
            response_data = {
                "msg": "Receipe not found",
            }
            status = 404

        return Response(data=response_data, status=status)

    def post(self, request):
        request_data = request.data
        recipe_name = request_data["name"]

        if Receipe.objects.filter(name=recipe_name).exists():
            msg = f"recipe with name {recipe_name} already exists"
            status = 500
        else:

            recipe_obj = Receipe.objects.create(
                user=request.user,
                name=recipe_name,
                description=request_data["description"],
                video_urls=request_data["url"],
                time_minutes=request_data["time"],
                price=request_data["price"],
            )

            if "tags" in request_data:
                for tag in request_data["tags"]:
                    tag_obj = Tag.objects.get(name=tag)
                    recipe_obj.tags.set([tag_obj])

            if "ingredients" in request_data:
                for ingredient in request_data["ingredients"]:
                    ingredient_obj = Indegridents.objects.get(name=ingredient)
                    recipe_obj.indegridents.set([ingredient_obj])

            msg = f"successfully created recipe {recipe_name}"
            status = 200

        response_data = {"msg": msg}

        return Response(data=response_data, status=status)

    def delete(self, request):
        recipe_name = request.GET.get("recipeName")

        if Receipe.objects.filter(name=recipe_name).exists():
            recipe_obj = Receipe.objects.get(name=recipe_name)
            recipe_obj.delete()

            response_data = {"msg": f"successfully dleted recipe {recipe_name}"}

            status = 200
        else:
            response_data = {
                "msg": "Receipe not found",
            }
            status = 404

        return Response(data=response_data, status=status)


class AllRecipeView(ModelAPIView):
    def get(self, request):
        recipe_objs = Receipe.objects.all()

        response_data = []

        for recipe_obj in recipe_objs:
            tags_objs = recipe_obj.tags.all()
            tag_json = serialize("json", tags_objs)

            ingredients_objs = recipe_obj.indegridents.all()
            ingredients_json = serialize("json", ingredients_objs)

            data = {
                "recipeName": recipe_obj.name,
                "tags": tag_json,
                "ingredients": ingredients_json,
                "time": recipe_obj.time_minutes,
                "url": recipe_obj.video_urls,
                "price": recipe_obj.price,
                "userName": recipe_obj.user.username,
            }

            response_data.append(data)

        return Response(data=response_data, status=200)
