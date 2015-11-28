from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _

from wagtail.wagtailadmin.forms import SearchForm
from wagtail.wagtailadmin.utils import permission_required
from wagtail.utils.pagination import paginate

from submissions.models import Submission


@permission_required('submissions.view_submission')
def index(request):
    submissions = Submission.objects.all()

    # Ordering
    if request.GET.get('ordering') in ['title', '-submitted_at']:
        ordering = request.GET['ordering']
    else:
        ordering = '-submitted_at'
    submissions = submissions.order_by(ordering)

    # Search
    query_string = None
    if 'q' in request.GET:
        form = SearchForm(request.GET, placeholder=_("Search submissions"))
        if form.is_valid():
            query_string = form.cleaned_data['q']
            submissions = submissions.search(query_string)
    else:
        form = SearchForm(placeholder=_("Search submissions"))

    # Pagination
    paginator, submissions = paginate(request, submissions)

    return render(request, 'submissions/admin/index.html', {
        'submissions': submissions,
        'ordering': ordering,
        'query_string': query_string,
        'is_searching': bool(query_string),
        'search_form': form,
    })


@permission_required('submissions.view_submission')
def details(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    return render(request, 'submissions/admin/details.html', {
        'submission': submission,
    })
