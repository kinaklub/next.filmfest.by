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


def remove_subpage(parent, model, **kwargs):
    parent.numchild -= 1

    model.objects.filter(**kwargs).delete()
    parent.save()


def get_content_type(apps, app_label, model):
    ContentType = apps.get_model('contenttypes.ContentType')
    content_type, _ = ContentType.objects.get_or_create(
        model=model,
        app_label=app_label
    )
    return content_type


def get_image_model(apps):
    """ Return Image model that works in migrations.

    Models created by Django migration subsystem contain fields,
    but dont' contain methods of the original models.

    The hack with adding method get_upload_to lets us save images in
    migrations, e.g.:
    >>> from django.core.files import File
    >>> Image = get_image_model()
    >>> photo = Image(title='example title')
    >>> with open(path) as f:
    ...     photo.file.save(name='name.png', content=File(f))

    Args:
        apps (django.db.migrations.state.StateApps): Apps registry.

    Returns:
        type: Image model.
    """
    from wagtail.wagtailimages.models import Image as LatestImage

    Image = apps.get_model('wagtailimages.Image')
    Image.get_upload_to = LatestImage.get_upload_to.im_func

    return Image
