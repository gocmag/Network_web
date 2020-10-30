const changeNetworkButton = document.getElementById('changeNetwork')
const deleteButton = document.getElementById('delButton')
const changeNetworkForm = document.getElementById('changeNetworkForm')
const changeVlanForm = document.getElementById('changeVlanForm')
const changeLocationForm = document.getElementById('changeLocationForm')
const changeDescriptionForm = document.getElementById('changeDescriptionForm')

let valueVlan = Number(document.getElementById('valueVlan').value)

let positionNetworkButton = $('#changeNetwork').offset().top
let positionVlanButton = $('#changeVLAN').offset().top
let positionLocationButton = $('#locateNetwork').offset().top
let positionDescriptionButton = $('#descriptionNetwork').offset().top


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
    $('#changeDescriptionForm').fadeOut(500);
    $('#changeNetworkForm').fadeToggle(500).offset({top:positionNetworkButton});
});

$('#changeVlanForm').hide()
$('#changeVLAN').on('click',function () {
    $('#changeNetworkForm').fadeOut(500);
    $('#changeLocationForm').fadeOut(500);
    $('#changeDescriptionForm').fadeOut(500);
    $('#changeVlanForm').fadeToggle(500).offset({top:positionVlanButton})
});

$('#changeLocationForm').hide()
$('#locateNetwork').on('click',function () {
    $('#changeNetworkForm').fadeOut(500);
    $('#changeVlanForm').fadeOut(500);
    $('#changeDescriptionForm').fadeOut(500);
    $('#changeLocationForm').fadeToggle(500).offset({top:positionLocationButton})
});

$('#changeDescriptionForm').hide()
$('#descriptionNetwork').on('click', function () {
    $('#changeNetworkForm').fadeOut(500);
    $('#changeVlanForm').fadeOut(500);
    $('#changeLocationForm').fadeOut(500);
    $('#changeDescriptionForm').fadeToggle(500).offset({top:positionDescriptionButton})
})

changeLocationForm.addEventListener('submit', checkNoneVlan, false)
deleteButton.addEventListener('submit', checkDelete, false)

////////////////////////////////////////// AJAX block //////////////////////////////////////////////////////////
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



$('.descriptions').click(function () {
    let x = this.getAttribute('data-objectId')
    let currentObject = this
    $.ajax({
        type: 'POST',
        async: true,
        url: '/changeDescription/',
        data: {csrfmiddlewaretoken: getCookie('csrftoken'),
               newDescription: prompt('Введите новый дескрипшн'),
               test: this.getAttribute('data-objectId')},
        success: function (data) {
            currentObject.innerHTML = data['newDescription']
        },
        dataType: 'json'
    })
});





