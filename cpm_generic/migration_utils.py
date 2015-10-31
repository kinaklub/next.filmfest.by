def add_subpage(parent, model, *args, **kwargs):
    parent.numchild += 1
    kwargs.setdefault('depth', parent.depth + 1)
    kwargs.setdefault('path', '%s%04d' % (parent.path, parent.numchild))
    kwargs.setdefault('numchild', 0)
    kwargs.setdefault('url_path', '%s%s/' % (parent.url_path, kwargs['slug']))

    child = model(*args, **kwargs)

    child.save()
    parent.save()

    return child


def get_content_type(apps, app_label, model):
    ContentType = apps.get_model('contenttypes.ContentType')
    content_type, _ = ContentType.objects.get_or_create(
        model=model,
        app_label=app_label
    )
    return content_type
