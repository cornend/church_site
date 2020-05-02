from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin

from church_site.views import AdminListView, BaseCreateView, BaseUpdateView
from .forms import SpeakerCreateForm

from .models import Speaker


class SpeakersAdminListView(FormMixin, AdminListView):
    model = Speaker
    form_class = SpeakerCreateForm
    template_name = 'speakers/speakers-admin-list.html'
    context_object_name = 'speakers'
    page_title = 'Speakers | Admin List'
    current_page = 'manage'
    btn_add_href = reverse_lazy('speakers:speakers-admin-create')
    

class SpeakersAdminCreateView(BaseCreateView):
    model = Speaker
    template_name = 'speakers/speakers-admin-form.html'
    form_class = SpeakerCreateForm
    page_title = 'Speakers | Admin Create'
    current_page = 'manage'
    btn_back_href = reverse_lazy('speakers:speakers-admin-list')
    success_url = reverse_lazy('speakers:speakers-admin-list')


class SpeakerAdminUpdateView(BaseUpdateView):
    model = Speaker
    template_name = 'speakers/speakers-admin-form.html'
    form_class = SpeakerCreateForm
    page_title = 'Speakers | Admin Update'
    current_page = 'manage'
    btn_back_href = reverse_lazy('speakers:speakers-admin-list')
    success_url = reverse_lazy('speakers:speakers-admin-list')
