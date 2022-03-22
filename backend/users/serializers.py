from recipes.models import Recipe
from rest_framework import serializers
from .models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели пользователя.
    Для операций создания и редактирования пользователя.
    """

    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    def get_is_subscribed(self, author):
        """
        Метод возвращает, подписан ли текущий пользователь на author.
        """
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            return author.follower.filter(user=current_user).exists()
        return False

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',)
        model = User

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AccessTokenSerializer(serializers.Serializer):
    """
    Сериализатор для получения токена.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Сериализатор изменения пароля.
    """
    model = User

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class FollowRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели рецептов для подписок.
    """

    class Meta:
        model = Recipe

        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для класса Follow.
    """

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    recipes = FollowRecipeSerializer(source='author.recipes',
                                     read_only=True,
                                     many=True)

    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',)

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()
