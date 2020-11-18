from spaweb.models import BusinessDirection


def add_variable_to_context(request):
    programs = BusinessDirection.objects.filter(title="ПРОГРАММЫ")
    context = {
        'programs': programs,
    }
    return context
