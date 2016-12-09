function(modal) {
    modal.respond('genericmodelChosen', {{ genericmodel_json|safe }});
    modal.close();
}
