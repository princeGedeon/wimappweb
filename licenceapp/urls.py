from django.urls import path, include
from rest_framework.routers import DefaultRouter

from licenceapp.views import LicenceViewSet, AddLicenceKey, UploadLicencesForStudentsView, \
    UploadLicencesForTeachersView, UpdateLevelLicencesView, UserLicencesView, MatiereListView

router = DefaultRouter()

router.register(r'licences', LicenceViewSet)


urlpatterns = [
    path('add-licence/', AddLicenceKey.as_view(), name='add-licence'),

path('', include(router.urls)),

 path('upload-licences-students/', UploadLicencesForStudentsView.as_view(), name='upload-licences-students'),
    path('upload-licences-teachers/', UploadLicencesForTeachersView.as_view(), name='upload-licences-teachers'),
path('update-level-licences/', UpdateLevelLicencesView.as_view(), name='update-licences'),
    path('api/get_my_licences/', UserLicencesView.as_view(), name='user-licences'),
    path('list_all_matieres/', MatiereListView.as_view(), name='matiere-list'),

]