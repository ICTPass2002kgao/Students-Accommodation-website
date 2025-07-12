# from rest_framework import serializers
# from .models import Accommodation, Student, Application


# class LandlordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Accommodation
#         fields = [
#             "id",
#             "accommodation_name",
#             "address",
#             "email",
#             "images",
#             "description",
#             "price",
#             "offered_amenities",  # Fixed typo
#             "accommodated_universities",
#             "logo",
#         ]


# class ApplicationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Application
#         fields = [
#             "id",
#             "student",
#             "landlord",
#             "status",
#             "applied_at",
#         ]


# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = "__all__"
