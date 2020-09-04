const changeVlanForm = document.getElementById('changeVlanForm')
const changeLocationForm = document.getElementById('changeLocationForm')
let valueVlan = Number(document.getElementById('valueVlan').value)

////////////////////////////////////////////////////////////////////////
function stopDefAction(evt) {
    evt.preventDefault();
}
///////////////////////////////////////////////////////////////////////
$('.changeDescriptions2').hide()

///////////////////////////////////////////////////////////////////////
let x = $('td *').on('click',function () {
    let id = this.id;
    let native_top = $(this).offset().top;
    let native_left = $(this).offset().left;

    let digits = parseInt(id.match(/\d+/));
    let newChangeDescriptionId = '#'+'changeDescription'+digits;
    $(newChangeDescriptionId).fadeIn(800);
});

$('#changeNetworkForm').hide()
$('#changeNetwork').on('click',function () {
    $('#changeLocationForm').fadeOut(500);
    $('#changeVlanForm').fadeOut(500);
    $('#changeNetworkForm').fadeToggle(500);
});


$('#changeVlanForm').hide()
$('#changeVLAN').on('click',function () {
    $('#changeNetworkForm').fadeOut(500);
    $('#changeLocationForm').fadeOut(500);
    $('#changeVlanForm').fadeToggle(500);
});

$('#changeLocationForm').hide()
$('#locateNetwork').on('click',function () {
    $('#changeNetworkForm').fadeOut(500);
    $('#changeVlanForm').fadeOut(500);
    $('#changeLocationForm').fadeToggle(500)
});

changeLocationForm.addEventListener('submit', checkNoneVlan, false)



function checkNoneVlan(e) {
    if (valueVlan !== 0) {
        e.preventDefault()
        alert('Перед переносом нужно отвязать VLAN от сети')
    }
}



