from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
# from views import TemplateView
from data import utils
from ui import views
from ui.views import userrating
from ui.views import NewsDetailView,Createnews
# from ui.views import beautifulsoup


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', views.userProfile, name='userProfile'),
    url(r'^trainer/(?P<trainer_id>[0-9]+)$', views.trainer, name='trainer'),
    # url(r'^wholenewss/(?P<news_id>[0-9]+)$', views.wholenews, name='wholenews'),
    url(r'^news/(?P<pk>\d+)/$', NewsDetailView.as_view(), name='NewsDetailView'),
    url(r'^training/$', views.training, name='training'),
    url(r'^get_traning_locations/$', views.get_traning_locations, name='get_traning_locations'),
    url(r'^trainerZaAjaks/(?P<trainer_id>[0-9]+)$', views.trainerZaAjaks, name='trainerZaAjaks'),
    url(r'^selectefdTraining/(?P<training_id>[0-9]+)/(?P<RegUser_id>[0-9]+)/$', views.selectedTraining, name='selectedTraining'),
    url(r'^userProfile/$', views.userProfile, name='userProfile'),
    url(r'^userrating/(?P<trainer_id>[0-9]+)/$', userrating.as_view(), name='userrating'),
    url(r'^a/(?P<trainer_id>[0-9]+)/$', userrating.as_view(), name='a'),
    url(r'^userProfilechannges/$', views.userProfilechannges, name='userProfilechannges'),
    url(r'^trainerProfilechannges/$', views.trainerProfilechannges, name='trainerProfilechannges'),
    url(r'^trainingStats/(?P<training_id>[0-9]+)/$', views.trainingStats, name='trainingStats'),
    url(r'^zakazaniTrening/(?P<training_id>[0-9]+)/$', views.zakazaniTrening, name='zakazaniTrening'),
    url(r'^newTrainingForm/$', views.newTrainingForm, name='newTrainingForm'),
    url(r'^proveraKoJeBioNaTreningu/$', views.proveraKoJeBioNaTreningu, name='proveraKoJeBioNaTreningu'),
    url(r'^uplate/$', views.uplate, name='uplate'),
    url(r'^treningform/$', views.newTrainingForm, name='newTrainingForm'),
    url(r'^odjava/(?P<training_id>[0-9]+)/$', views.odjava, name='odjava'),
    url(r'^PravljenjeVesti/$', Createnews.as_view(), name='Createnews'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






