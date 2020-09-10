const changeNetworkButton = document.getElementById('changeNetwork')
const deleteButton = document.getElementById('delButton')
const changeNetworkForm = document.getElementById('changeNetworkForm')
const changeVlanForm = document.getElementById('changeVlanForm')
const changeLocationForm = document.getElementById('changeLocationForm')

let valueVlan = Number(document.getElementById('valueVlan').value)

let positionNetworkButton = $('#changeNetwork').offset().top
let positionVlanButton = $('#changeVLAN').offset().top
let positionLocationButton = $('#locateNetwork').offset().top

////////////////////////////////////////////////////////////////////////
function stopDefAction(evt) {
    evt.preventDefault();
}

function checkNoneVlan(e) {
    if (valueVlan !== 0) {
        e.preventDefault()
        alert('Перед переносом нужно отвязать VLAN от сети')
    }
}

function checkDelete(e) {
    if (!confirm('Вы уверены что хотите удалить сеть ?')) {
        e.preventDefault()
    }
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
    $('#changeNetworkForm').fadeToggle(500).offset({top:positionNetworkButton});
});

$('#changeVlanForm').hide()
$('#changeVLAN').on('click',function () {
    $('#changeNetworkForm').fadeOut(500);
    $('#changeLocationForm').fadeOut(500);
    $('#changeVlanForm').fadeToggle(500).offset({top:positionVlanButton})
});

$('#changeLocationForm').hide()
$('#locateNetwork').on('click',function () {
    $('#changeNetworkForm').fadeOut(500);
    $('#changeVlanForm').fadeOut(500);
    $('#changeLocationForm').fadeToggle(500).offset({top:positionLocationButton})
});

changeLocationForm.addEventListener('submit', checkNoneVlan, false)
deleteButton.addEventListener('submit', checkDelete, false)






