from datetime import date

from .models import Task, Tag, Comment
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    class Meta:
        model = Task
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
