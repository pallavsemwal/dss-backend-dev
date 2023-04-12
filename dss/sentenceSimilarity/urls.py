from django.urls import path

from . import views

urlpatterns = [ 
    path('similarSentence',views.similarSentence),
    path('addLesson',views.addLesson),
    path('lessonLearnt',views.lessonLearnt),
    path('updateCount',views.updateCount),
    path('cosineSimilarityMat',views.cosineSimilarityMat),
]