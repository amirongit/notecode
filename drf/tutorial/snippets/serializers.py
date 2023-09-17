from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

# The fields that get serialized or deserialized can be defined in the body
# of the serializer; also the fields can have validation flags to be used for
# creating and updating instances. there are flags to control the way which in
# fields are displayed in different situations, too.


class ExplicitSnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True,
                                  max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES,
                                       default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        '''
        Create and return a new `Snippet` instance, given the validated data.
        '''
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''
        Update and return an existing `Snippet` instance, given the validated
        data.
        '''
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


# ModelSerializer classes are a shortcut for creating serializers for models.
# reverse attributes aren't included by default in model serializers, and need
# to be defined explicitly.


class NonHyperSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'owner', 'title', 'code', 'linenos', 'language',
                  'style']

    owner = serializers.ReadOnlyField(source='owner.username')


class NonHyperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all()
    )


# HyperlinkedModelSerializer doesn't include the id field by default. it
# includes a url field using HyperlinkedIdentityField, and represents
# relationships using HyperlinkedRelatedField instead of primary keys.
# The url field of HyperlinkedModelSerializer point to a view called
# {mode_name}-detail by default.


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner', 'title', 'code',
                  'linenos', 'language', 'style']

    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight', format='html'
    )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']

    snippets = serializers.HyperlinkedRelatedField(many=True,
                                                   view_name='snippet-detail',
                                                   read_only=True)
