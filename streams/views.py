from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View

from church_site.views import AdminListView, BaseListView, BaseDetailView, BaseCreateView, BaseUpdateView
from churches.models import Church
from .forms import StreamCreateForm

from .models import Stream


class StreamsListView(BaseListView):
    page_title = 'Live'
    current_page = 'live'
    model = Stream
    template_name = 'streams/streams-list.html'
    context_object_name = 'streams'

    def get_queryset(self):
        if self.kwargs.get('church'):
            return self.model.objects.filter(event__end__gt=timezone.now(),
                                             event__church__name=self.kwargs.get('church').replace('-', ' '))
        return Stream.objects.filter(event__end__gt=timezone.now())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['churches'] = Church.objects.all()
        context['current_church'] = self.kwargs.get('church') if self.kwargs.get('church') else None
        return context


class LiveAudioView(BaseDetailView):
    # page_title = 'Page Title'
    current_page = 'live'
    model = Stream
    template_name = 'streams/live-audio.html'
    context_object_name = 'stream'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Live Audio - {self.object.title}'
        return context


class LiveVideoView(BaseDetailView):
    page_title = 'Page Title'
    current_page = 'live'
    model = Stream
    template_name = 'streams/live-video.html'
    context_object_name = 'stream'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Live Video - {self.object.title}'
        return context


class StreamsAdminListView(PermissionRequiredMixin, AdminListView):
    permission_required = 'streams.view_stream'
    model = Stream
    context_object_name = 'streams'
    template_name = 'streams/streams-admin-list.html'
    page_title = 'Streams - Admin'
    current_page = 'manage'
    btn_add_href = reverse_lazy('streams:streams-admin-create')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.member_streams(self.request.user)
        return queryset


class StreamsAdminCreateView(PermissionRequiredMixin, BaseCreateView):
    permission_required = 'streams.add_stream'
    model = Stream
    template_name = 'admin-form-view.html'
    form_class = StreamCreateForm
    success_url = reverse_lazy('streams:streams-admin-list')
    page_title = 'New Stream - Admin'
    current_page = 'manage'
    btn_back_href = reverse_lazy('streams:streams-admin-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class StreamAdminUpdateView(PermissionRequiredMixin, BaseUpdateView):
    permission_required = 'streams.change_stream'
    model = Stream
    template_name = 'admin-form-view.html'
    form_class = StreamCreateForm
    success_url = reverse_lazy('streams:streams-admin-list')
    page_title = 'Update Stream - Admin'
    current_page = 'manage'
    btn_back_href = reverse_lazy('streams:streams-admin-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class StreamAdminLiveUpdateView(PermissionRequiredMixin, View):
    permission_required = 'streams.change_stream'

    # This will change the live status of the live stream
    def get(self, request, pk=None):
        stream = Stream.objects.filter(id=pk).first()
        if stream:
            stream.live = not stream.live
            stream.save()
        return redirect('streams:streams-admin-list')