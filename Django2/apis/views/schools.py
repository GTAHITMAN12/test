
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.models import SchoolStructure, Schools, Classes, Personnel, Subjects, StudentSubjectsScore
from apis.serializer import  ClassesSerializer, ClassesidSerializer, PersonalSerializer, SchoolSerializer, SchoolidSerializer, SchoolnameSerializer, StudentScoreSerializer, StudentSerializer, SubjectScoreSerializer, SubjectSerializer
from apis.util.calculategrade import calculate_gpa, calculate_grade
from apis.util.role import role


class StudentSubjectsScoreAPIView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        """
        [Backend API and Data Validations Skill Test]

        description: create API Endpoint for insert score data of each student by following rules.

        rules:      - Score must be number, equal or greater than 0 and equal or less than 100.
                    - Credit must be integer, greater than 0 and equal or less than 3.
                    - Payload data must be contained `first_name`, `last_name`, `subject_title` and `score`.
                        - `first_name` in payload must be string (if not return bad request status).
                        - `last_name` in payload must be string (if not return bad request status).
                        - `subject_title` in payload must be string (if not return bad request status).
                        - `score` in payload must be number (if not return bad request status).

                    - Student's score of each subject must be unique (it's mean 1 student only have 1 row of score
                            of each subject).
                    - If student's score of each subject already existed, It will update new score
                            (Don't created it).
                    - If Update, Credit must not be changed.
                    - If Data Payload not complete return clearly message with bad request status.
                    - If Subject's Name or Student's Name not found in Database return clearly message with bad request status.
                    - If Success return student's details, subject's title, credit and score context with created status.

        remark:     - `score` is subject's score of each student.
                    - `credit` is subject's credit.
                    - student's first name, lastname and subject's title can find in DATABASE (you can create more
                            for test add new score).

        """

        subjects_context = [{"id": 1, "title": "Math"}, {"id": 2, "title": "Physics"}, {"id": 3, "title": "Chemistry"},
                            {"id": 4, "title": "Algorithm"}, {"id": 5, "title": "Coding"}]

        credits_context = [{"id": 6, "credit": 1, "subject_id_list_that_using_this_credit": [3]},
                           {"id": 7, "credit": 2, "subject_id_list_that_using_this_credit": [2, 4]},
                           {"id": 9, "credit": 3, "subject_id_list_that_using_this_credit": [1, 5]}]

        credits_mapping = [{"subject_id": 1, "credit_id": 9}, {"subject_id": 2, "credit_id": 7},
                           {"subject_id": 3, "credit_id": 6}, {"subject_id": 4, "credit_id": 7},
                           {"subject_id": 5, "credit_id": 9}]
        
        students_first_name = request.data.get("first_name", None)
        students_last_name = request.data.get("last_name", None)
        subjects_title = request.data.get("subjects", None)
        score = request.data.get("score", None)
        data=request.data
        subid=[subid["id"] for subid in subjects_context if subid["title"] == str(data['subjects'])][0]
        credits=[credits["credit"] for credits in credits_context if   subid in credits["subject_id_list_that_using_this_credit"]][0]
        data['credit']=credits 
        #print(credits)
        #print(context)
        #print(students_first_name,students_last_name,subjects_title,score)
        #credit, id, score, student, student_id, subjects, subjects_id
        serializer = StudentScoreSerializer(data=request.data)
        if not serializer.is_valid() and score > 0 and score <= 100 and credits > 0 and credits <= 3  :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        try:
            student = Personnel.objects.get(first_name=students_first_name, last_name=students_last_name)
            subject = Subjects.objects.get(title=subjects_title)
        except  student.DoesNotExist and subject.DoesNotExist :
            return Response("Student or Subject not found", status=status.HTTP_400_BAD_REQUEST)
 
        
         
        
        data = serializer.validated_data
        """print("serializer.validated_data",data)
        print("subject",subject.__dict__)
        print("student",student.__dict__)"""
            

        try:
            oldscore = StudentSubjectsScore.objects.get(student=student, subjects=subject)
            oldscore.score = score
            print(oldscore.__dict__)
            oldscore.save( )
            serializer = StudentScoreSerializer(oldscore)
            return Response((serializer.data,SubjectSerializer(subject).data), status=status.HTTP_200_OK)
        except StudentSubjectsScore.DoesNotExist:
            new_score=StudentSubjectsScore.objects.create(student=student, subjects=subject, score=score , credit=data['credit'])
            print(new_score.__dict__)
            new_score.save()
            serializer = StudentScoreSerializer(new_score)
            return Response((serializer.data,SubjectSerializer(subject).data), status=status.HTTP_201_CREATED)
         
        


class StudentSubjectsScoreDetailsAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Backend API and Data Calculation Skill Test]

        description: get student details, subject's details, subject's credit, their score of each subject,
                    their grade of each subject and their grade point average by student's ID.

        pattern:     Data pattern in 'context_data' variable below.

        remark:     - `grade` will be A  if 80 <= score <= 100
                                      B+ if 75 <= score < 80
                                      B  if 70 <= score < 75
                                      C+ if 65 <= score < 70
                                      C  if 60 <= score < 65
                                      D+ if 55 <= score < 60
                                      D  if 50 <= score < 55
                                      F  if score < 50

        """

        student_id = kwargs.get("id", None)
        student= Personnel.objects.get(id=student_id)
        subject= Subjects.objects.get(id=student_id)
        serializer=StudentSerializer(student)
        student_data=serializer.data
        student_name=" ".join([student_data['first_name'],student_data['last_name']])
        school_name=serializer.data['school_class']['school']['title']
        print(school_name)
        print(
            student_id,
            student_name,
            school_name,
        )
        subjectjson=[]
        grade=0
        try:
            subject = StudentSubjectsScore.objects.filter(student=student)
            serializer=SubjectScoreSerializer(subject,many=True)
 
        except StudentSubjectsScore.DoesNotExist:
            subjectjson=[]  
            gpa=0
        gradelist=[]
        creditslist=[]
        if subject is not None:
            for item in serializer.data :
                #print(item)
                grade=calculate_grade(item['score'])
                subjectdetail={
                    "subject":item['subjects']['title'],
                    "credit":item['credit'],
                    "score":item['score'],
                    "grade":grade,
                }
                gradelist.append(grade)
                creditslist.append(item['credit'])
                subjectjson.append(subjectdetail)
        gpa=calculate_gpa(gradelist,creditslist)
        print(subjectjson)
        example_context_data = {
            "student":
                {
                    "id":student_id,
                    "full_name":student_name,
                    "school":school_name,
                },

            "subject_detail": subjectjson ,
            "grade_point_average": gpa,
        }

        return Response(example_context_data, status=status.HTTP_200_OK)


class PersonnelDetailsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        [Basic Skill and Observational Skill Test]

        description: get personnel details by school's name.

        data pattern:  {order}. school: {school's title}, role: {personnel type in string}, class: {class's order}, name: {first name} {last name}.

        result pattern : in `data_pattern` variable below.

        example:    1. school: Rose Garden School, role: Head of the room, class: 1, name: Reed Richards.
                    2. school: Rose Garden School, role: Student, class: 1, name: Blackagar Boltagon.

        rules:      - Personnel's name and School's title must be capitalize.
                    - Personnel's details order must be ordered by their role, their class order and their name.

        """
        school_title = kwargs.get("school_title", None)

        if not school_title:
            return Response("Please provide a school title.", status=status.HTTP_400_BAD_REQUEST)
        schoolobj=Schools.objects.get(title=school_title)
        school_id=ClassesidSerializer(schoolobj)
        print(school_id.data)
        
        personnel = Personnel.objects.filter(school_class__school__id=school_id.data['id']).order_by('personnel_type', 'school_class__class_order', 'first_name') 
        
        your_result = []
        for idx, person in enumerate(personnel, start=1):
            data_pattern = f"{idx}. school: {school_title}, role: {role(person.personnel_type)}, class: {person.school_class_id}, name: {' '.join([person.first_name,person.last_name])}."
            your_result.append(data_pattern)

        return Response(your_result, status=status.HTTP_200_OK)
        """school_title = kwargs.get("school_title", None)

        your_result = []

        return Response(your_result, status=status.HTTP_400_BAD_REQUEST)"""


class SchoolHierarchyAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Logical Test]

        description: get personnel list in hierarchy order by school's title, class and personnel's name.

        pattern: in `data_pattern` variable below.

        """

        data_pattern = []
        schoolset={}
        teacherset={}
        studentlist=[]
        school = Schools.objects.all().values()
        for i in school:
            school_name=i['title']
            schoolset["school"]=school_name
            print(school_name)
            schoolobj=Schools.objects.get(title=school_name)
            school_id=SchoolidSerializer(schoolobj)
            classobj=Classes.objects.filter(school=school_id.data['id'])
            class_id=ClassesidSerializer(classobj,many=True)
            #print(class_id.data)
            for  j in class_id.data:
                class_name=j['id']
                print(class_name)
                teacherdetail=''
                for person in Personnel.objects.filter(school_class_id__id=class_name).order_by('school_class_id','personnel_type'):
                    if(role(person.personnel_type)=="Teacher"):
                        teacherdetail=role(person.personnel_type)+':'+' '.join([person.first_name,person.last_name])
                    else:
                        studentlist.append({
                            #"school": school_name,
                            #"class": person.school_class_id,
                            role(person.personnel_type):' '.join([person.first_name,person.last_name])
                        })
                teacherset[f"{teacherdetail}"]=studentlist
                studentlist=[]
                schoolset[f"class {class_name}"]=teacherset
                teacherset={}
                
            data_pattern.append(schoolset)
            schoolset={}    
        #print(schoolset)
        # Sort the flattened data by school, class, and name
        #sorted_data = sorted(flattened_data, key=lambda x: (x["school"], x["class"], x["name"]))
        return Response(data_pattern, status=status.HTTP_200_OK) 

class SchoolStructureAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Logical Test]

        description: get School's structure list in hierarchy.

        pattern: in `data_pattern` variable below.

        """
        Head=[]
        lv1=[]
        lv2=[]
        set1={}
        set2={}
        temp=0
        struct=SchoolStructure.objects.all().values()
        for i in struct:
            if(i['parent_id']==None):
                set2['title']=i['title']
                temp=i['id']
                for j in struct:
                    if(j['parent_id']==temp):
                        set1['title']=j['title']
                        temp=j['id']
                        for k in struct:
                            if(k['parent_id']==temp):
                                lv2.append({"title":k['title']})
                        set1['sub']=lv2
                        lv1.append(set1)
                        temp=i['id']
                        set1={}
                        lv2=[]
                set2['sub']=lv1
                Head.append(set2)
                set2={}
            lv1=[]
        your_result = Head

        return Response(your_result, status=status.HTTP_200_OK)
