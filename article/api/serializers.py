from .models import Article, Author
from rest_framework import serializers
import uuid as uuid_

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('author_uuid', )

class ArticleSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many = True)

    class Meta:
        model = Article
        fields = '__all__'

    '''
    def get_authors(self, instance: Article) -> list:
        return list(
            instance.authors.values_list(
                'author_uuid',
                flat = True
            )
        )
    '''

    def create(self, validated_data: dict) -> Article:
        author_data = validated_data.pop('authors')

        article_ = Article.objects.create(**validated_data)

        article_.save()

        for author_item in author_data:
            author_ = Author.objects.get_or_create(author_uuid = author_item.get('author_uuid'))[0]
            article_.authors.add(author_)

        return article_

    def update(self, instance: Article, validated_data: dict) -> Article:
        authors_data = validated_data.pop('authors')

        authors_ = instance.authors

        instance.title = validated_data.get('title', instance.title)
        instance.published = validated_data.get('published', instance.published)
        instance.journal = validated_data.get('journal', instance.journal)

        if len(authors_data):
            instance.authors.clear()

            for a_item in authors_data:
                author_, created = Author.objects.get_or_create(author_uuid = a_item.get('author_uuid'))
                instance.authors.add(author_)

        instance.save()

        return instance