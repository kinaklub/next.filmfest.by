from __future__ import absolute_import, unicode_literals

import json

from django.apps import apps
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils.six import text_type

from wagtail.utils.pagination import paginate
from wagtail.wagtailadmin.forms import SearchForm
from wagtail.wagtailadmin.modal_workflow import render_modal_workflow

from modeladminutils.helpers import get_edit_url


def get_model_or_404(app_label, model_name):
    try:
        return apps.get_model(app_label, model_name)
    except LookupError:
        raise Http404


def choose(request, app_label, model_name):
    model = get_model_or_404(app_label, model_name)
    objects = model.objects.all()

    q = None
    if ('q' in request.GET or 'p' in request.GET):
        # this request is triggered from search or pagination
        # we will just render the results.html fragment

        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']

            objects = objects.search(q)
            is_searching = True
        else:
            is_searching = False

        # Pagination
        paginator, objects = paginate(request, objects, per_page=12)

        return render(request, "modeladminutils/chooser/results.html", {
            'objects': objects,
            'is_searching': is_searching,
            'query_string': q,
            'will_select_format': request.GET.get('select_format'),
            'app_label': app_label,
            'model_name': model_name,
            'model_verbose_name_plural': model._meta.verbose_name_plural,
        })
    else:
        searchform = SearchForm()

        paginator, objects = paginate(request, objects, per_page=12)

    return render_modal_workflow(
        request,
        'modeladminutils/chooser/chooser.html',
        'modeladminutils/chooser/chooser.js',
        {
            'objects': objects,
            'searchform': searchform,
            'is_searching': False,
            'query_string': q,
            'app_label': app_label,
            'model_name': model_name,
            'model_verbose_name': model._meta.verbose_name,
        }
    )


def chosen(request, app_label, model_name, id):
    model = get_model_or_404(app_label, model_name)
    obj = get_object_or_404(model, id=id)

    adminmodel_json = json.dumps({
        'id': obj.id,
        'string': text_type(obj),
        'edit_link': get_edit_url(model, obj.id),
    })

    return render_modal_workflow(
        request,
        None, 'modeladminutils/chooser/chosen.js',
        {
            'adminmodel_json': adminmodel_json,
        }
    )
