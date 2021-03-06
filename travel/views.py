from .models import Trip, Event, Principal
from .forms import TripForm, EventForm, PrincipalForm
from django.views.generic import ListView, DetailView, TemplateView
from django.template.loader import get_template
from django.shortcuts import render, redirect
from .serializers import TripSerializer, EventSerializer
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from dal import autocomplete
from cities_light.models import Country, City
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
class LoginRequiredView(LoginRequiredMixin):
    login_url = '/accounts/login/'

class HomeView(TemplateView):
    template_name = 'travel/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

class TripDetail(LoginRequiredView, DetailView):
    queryset = Trip.objects.all()

    def get_object(self):
        object = super(TripDetail, self).get_object()
        return object

class TripList(LoginRequiredView, ListView):
	model = Trip

@login_required(login_url='/accounts/login/')
def trip_new(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.save()
            form.save_m2m()
            messages.success(request, 'A new itinerary was successfully created.')
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripForm()
    return render(request, 'travel/trip_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def trip_edit(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == "POST":
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.save()
            form.save_m2m()
            messages.success(request, 'The itinerary was successfully updated.')
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripForm(instance=trip)
    return render(request, 'travel/trip_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == "POST":
        trip.delete()
        messages.success(request, 'The itinerary was successfully deleted.')
        return redirect('trip_list')
    return render(request, 'travel/trip_confirm_delete.html', {'trip': trip})

class EventList(LoginRequiredView, ListView):
    model = Event

class EventDetail(LoginRequiredView, DetailView):
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['trips'] = Trip.objects.filter(events__id = self.object.id)
        return context

@login_required(login_url='/accounts/login/')
def event_new(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.cities_light_country = event.cities_light_city.country
            event.save()
            form.save_m2m()
            messages.success(request, 'A new event was successfully created.')
            return redirect('trip_new')
    else:
        form = EventForm()
    return render(request, 'travel/event_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            form.save_m2m()
            messages.success(request, 'The event was successfully updated.')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'travel/event_form.html', {'form': form})

class PrincipalList(LoginRequiredView, ListView):
    model = Principal

class PrincipalDetail(LoginRequiredView, DetailView):
    queryset = Principal.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PrincipalDetail, self).get_context_data(**kwargs)
        context['trips'] = Trip.objects.filter(principal__id = self.object.id)
        return context

@login_required(login_url='/accounts/login/')
def principal_new(request):
    if request.method == "POST":
        form = PrincipalForm(request.POST)
        if form.is_valid():
            principal = form.save(commit=False)
            principal.save()
            form.save_m2m()
            messages.success(request, 'A new principal record was successfully created.')
            return redirect('trip_new')
    else:
        form = PrincipalForm()
    return render(request, 'travel/principal_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def principal_edit(request, pk):
    principal = get_object_or_404(Principal, pk=pk)
    if request.method == "POST":
        form = PrincipalForm(request.POST, instance=principal)
        if form.is_valid():
            principal = form.save(commit=False)
            principal.save()
            form.save_m2m()
            messages.success(request, 'The principal record was successfully updated.')
            return redirect('principal_detail', pk=principal.pk)
    else:
        form = PrincipalForm(instance=principal)
    return render(request, 'travel/principal_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def dashboard_view(request):
    return render(request, 'travel/dashboard.html')

class TripViewSet(LoginRequiredView, viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

class EventViewSet(LoginRequiredView, viewsets.ModelViewSet):
    queryset = Event.objects.all();
    serializer_class = EventSerializer

class CityAutocomplete(LoginRequiredView, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return City.objects.none()

        qs = City.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
