from django.views.generic.list import ListView

from projects.models import Project


class Home(ListView):
    model = Project
    template_name = 'index.html'

    def get_queryset(self):
        filter_value = self.request.GET.get('filter', 'All Needs')
        if filter_value == 'All Needs':
            context = Project.objects.all()
        else:
            context = Project.objects.filter(
                position__title__icontains=filter_value[0:3]
            )
        return context

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter')
        return context