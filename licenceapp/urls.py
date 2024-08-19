from django.urls import path, include
from rest_framework.routers import DefaultRouter

from licenceapp.views import LicenceViewSet, AddLicenceKey, UploadLicencesForStudentsView, \
    UploadLicencesForTeachersView, UpdateLevelLicencesView, UserLicencesView,  MatiereListCreateView, \
    MatiereDetailView, ClasseListCreateView, ClasseDetailView, NiveauListCreateView, NiveauDetailView

router = DefaultRouter()

router.register(r'licences', LicenceViewSet)


urlpatterns = [
    path('add-licence/', AddLicenceKey.as_view(), name='add-licence'),

path('', include(router.urls)),

 path('upload-licences-students/', UploadLicencesForStudentsView.as_view(), name='upload-licences-students'),
    path('upload-licences-teachers/', UploadLicencesForTeachersView.as_view(), name='upload-licences-teachers'),
path('update-level-licences/', UpdateLevelLicencesView.as_view(), name='update-licences'),
    path('api/get_my_licences/', UserLicencesView.as_view(), name='user-licences'),
    path('matieres/', MatiereListCreateView.as_view(), name='matiere-list-create'),
    path('matieres/<int:pk>/', MatiereDetailView.as_view(), name='matiere-detail'),

    path('classes/', ClasseListCreateView.as_view(), name='classe-list-create'),
    path('classes/<int:pk>/', ClasseDetailView.as_view(), name='classe-detail'),

    path('niveaux/', NiveauListCreateView.as_view(), name='niveau-list-create'),
    path('niveaux/<int:pk>/', NiveauDetailView.as_view(), name='niveau-detail'),


]