function createAdminModelChooser(id, modelString) {
    var chooserElement = $('#' + id + '-chooser');
    var docTitle = chooserElement.find('.title');
    var input = $('#' + id);
    var editLink = chooserElement.find('.edit-link');

    $('.action-choose', chooserElement).click(function() {
        ModalWorkflow({
            url: window.chooserUrls.adminmodelChooser + modelString + '/',
            responses: {
                adminmodelChosen: function(adminModelData) {
                    input.val(adminModelData.id);
                    docTitle.text(adminModelData.string);
                    chooserElement.removeClass('blank');
                    editLink.attr('href', adminModelData.edit_link);
                }
            }
        });
    });

    $('.action-clear', chooserElement).click(function() {
        input.val('');
        chooserElement.addClass('blank');
    });
}
