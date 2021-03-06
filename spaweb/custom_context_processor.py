from spaweb.models import BusinessDirection


def add_variable_to_context(request):
    programs = BusinessDirection.objects.filter(title="ПРОГРАММЫ").prefetch_related('topics')
    calc_services = BusinessDirection.objects.filter(title="КАЛЬКУЛЯТОР").prefetch_related('topics')
    context = {
        'programs': programs,
        'calc_services': calc_services
    }
    return context
