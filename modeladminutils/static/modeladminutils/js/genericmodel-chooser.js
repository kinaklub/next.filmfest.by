function createGenericModelChooser(id, modelString) {
    var chooserElement = $('#' + id + '-chooser');
    var docTitle = chooserElement.find('.title');
    var input = $('#' + id);
    var editLink = chooserElement.find('.edit-link');

    $('.action-choose', chooserElement).click(function() {
        ModalWorkflow({
            url: window.chooserUrls.genericmodelChooser + modelString + '/',
            responses: {
                genericmodelChosen: function(genericModelData) {
                    input.val(genericModelData.id);
                    docTitle.text(genericModelData.string);
                    chooserElement.removeClass('blank');
                    editLink.attr('href', genericModelData.edit_link);
                }
            }
        });
    });

    $('.action-clear', chooserElement).click(function() {
        input.val('');
        chooserElement.addClass('blank');
    });
}
