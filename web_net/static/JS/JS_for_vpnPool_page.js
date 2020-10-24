const addVpnButton = document.getElementById('addPool')


let positionButtonsLeft = 250
let positionVpnButton = $('#addPool').offset().top
////////////////////////////////////////////////////

$('#addPoolForm').hide()
$('#addPool').on('click', function () {
    $('#addPoolForm').fadeToggle(500).offset({top:positionVpnButton, left:positionButtonsLeft})
});