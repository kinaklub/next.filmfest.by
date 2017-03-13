function(modal) {
    modal.respond('adminmodelChosen', {{ adminmodel_json|safe }});
    modal.close();
}
