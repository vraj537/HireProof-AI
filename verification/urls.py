from django.urls import path
from . import views
urlpatterns=[path("",views.dashboard,name="dashboard"),path("candidates/",views.candidates,name="candidates"),path("candidate/new/",views.candidate_new,name="candidate_new"),path("candidate/<int:pk>/",views.candidate_detail,name="candidate_detail"),path("candidate/<int:pk>/analyze/",views.analyze,name="analyze"),path("candidate/<int:pk>/evidence/",views.add_evidence,name="add_evidence"),path("candidate/<int:pk>/resume/",views.candidate_resume,name="candidate_resume")]
