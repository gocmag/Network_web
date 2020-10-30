const addVpnButton = document.getElementById('addPool')


let positionButtonsLeft = 250
let positionVpnButton = $('#addPool').offset().top
////////////////////////////////////////////////////

$('.oneStringBlock').hide()
$('#addPool').on('click', function () {
    $('.oneStringBlock').fadeToggle(500)
});