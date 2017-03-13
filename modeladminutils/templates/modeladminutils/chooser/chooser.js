{% load i18n %}
function(modal) {
    var searchUrl = $('form.image-search', modal.body).attr('action');

    function ajaxifyLinks (context) {
        $('.listing a', context).click(function() {
            modal.loadUrl(this.href);
            return false;
        });

        $('.pagination a', context).click(function() {
            var page = this.getAttribute("data-page");
            setPage(page);
            return false;
        });
    }

    function fetchResults(requestData) {
        $.ajax({
            url: searchUrl,
            data: requestData,
            success: function(data, status) {
                $('#adminmodel-results').html(data);
                ajaxifyLinks($('#adminmodel-results'));
            }
        });
    }

    function search() {
        /* Searching causes currentTag to be cleared - otherwise there's
        no way to de-select a tag */
        fetchResults({q: $('#id_q').val()});
        return false;
    }

    function setPage(page) {
        params = {p: page};
        if ($('#id_q').val().length){
            params['q'] = $('#id_q').val();
        }
        fetchResults(params);
        return false;
    }

    ajaxifyLinks(modal.body);

    $('#id_q').on('input', function() {
        clearTimeout($.data(this, 'timer'));
        var wait = setTimeout(search, 200);
        $(this).data('timer', wait);
    });

    {% url 'wagtailadmin_tag_autocomplete' as autocomplete_url %}

    /* Add tag entry interface (with autocompletion) to the tag field of the image upload form */
    $('#id_tags', modal.body).tagit({
        autocomplete: {source: "{{ autocomplete_url|addslashes }}"}
    });
}
