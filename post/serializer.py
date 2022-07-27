from rest_framework import serializers

from post.models import Comment, HashTag, Post

class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

class GetSerializer(serializers.ModelSerializer):
    hash_tags = HashTagSerializer(many=True, read_only=True)
    user_name = serializers.StringRelatedField(source='user.email')
    class Meta:
        model = Post
        fields = ['id', 'user_name','title', 'context', 'hash_tags']

class PostSerializer(serializers.ModelSerializer):
    hash_tags = HashTagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'context', 'user', 'hash_tags']
        read_only_fields = ['hash_tags']

    def create(self, validated_data):
        hash_tags = self.context['hash_tags'].split(',')
        post = Post.objects.create(**validated_data)
        hts = []
        
        for hash_tag in hash_tags:

            if ht := HashTag.objects.filter(name=hash_tag[1:]).first():
                pass
            else:
                ht = HashTag.objects.create(name=hash_tag[1:])
            hts.append(ht)
        
        post.hash_tags.set(hts)
        return post

class PatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'context']

class DetailSerializer(serializers.ModelSerializer):
    email = serializers.StringRelatedField(source='user.email')
    like = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = ['id', 'email','title', 'context', 'like', 'views', 'comments']


    def get_like(self, obj):
        return len(obj.likes.all())

class HashTagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HashTag
        fields = ['name']
    