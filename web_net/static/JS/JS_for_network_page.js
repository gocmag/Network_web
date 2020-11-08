let positionNetworkButton = $('#addNetwork').offset().top


$('#addForm').offset({top:positionNetworkButton-18})
$('#addForm').hide()
$('#addNetwork').on('click',function () {
    $('#addForm').slideToggle(500);
});


