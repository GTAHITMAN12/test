from rest_framework import serializers
from apis.models import   Classes, Personnel, Schools, StudentSubjectsScore, Subjects
class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnel 
        fields = '__all__'
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['title',]
class StudentScoreSerializer(serializers.ModelSerializer):
    student=PersonalSerializer(many=False ,read_only=True)
    subject=SubjectSerializer(many=True ,read_only=True)
    class Meta:
        model = StudentSubjectsScore
        fields = ['id','student', 'credit', 'subject', 'score']
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schools
        fields = ['title',] 

class ClassesSerializer(serializers.ModelSerializer):
    school=SchoolSerializer(many=False ,read_only=True)
    class Meta:
        model = Classes
        fields = ['school',] 
 
class StudentSerializer(serializers.ModelSerializer):
    school_class=ClassesSerializer(many=False ,read_only=True)
    class Meta:
        model = Personnel
        fields = ['id','first_name','last_name','school_class'] 
 
class SubjectScoreSerializer(serializers.ModelSerializer):
    student=PersonalSerializer(many=False ,read_only=True)
    subjects=SubjectSerializer(many=False ,read_only=True)
    class Meta:
        model = StudentSubjectsScore
        fields = '__all__'

class SchoolnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schools
        fields = ['title',] 
class SchoolidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schools
        fields = ['id',] 
class ClassesidSerializer(serializers.ModelSerializer):
    school=SchoolSerializer(many=False ,read_only=True)
    class Meta:
        model = Classes
        fields = ['id','school'] 