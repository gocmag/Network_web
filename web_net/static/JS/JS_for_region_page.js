//document.getElementById('addRegion').hidden = true;
$('#regionForm').hide()
$('#addRegion').on('click',function () {
    $('#regionForm').slideToggle(1500);
});