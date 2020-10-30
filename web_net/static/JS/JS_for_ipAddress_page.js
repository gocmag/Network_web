const changeNetworkButton = document.getElementById('changeNetwork')
const deleteButton = document.getElementById('delButton')
const changeNetworkForm = document.getElementById('changeNetworkForm')
const changeVlanForm = document.getElementById('changeVlanForm')
const changeLocationForm = document.getElementById('changeLocationForm')
const changeDescriptionForm = document.getElementById('changeDescriptionForm')

let valueVlan = Number(document.getElementById('valueVlan').value)
let inOppacity = '1'
let outOppacity = '0'
let toggleOppacity = 'toggle'
let hideOppacity = 'hide'




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



changeLocationForm.addEventListener('submit', checkNoneVlan, false)
deleteButton.addEventListener('submit', checkDelete, false)

$('.oneStringBlock').hide()
$('#changeNetwork').click(function () {
    let blockCssOpacity = $('#changeNetworkBlock').css('display')

    if (blockCssOpacity === 'none') {
        $('#changeVlanButtonBlock').animate({
            opacity: outOppacity
        });
        $('#locateNetworkButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#descriptionNetworkButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#delNetButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#changeNetworkBlock').delay(500).animate({
            opacity: toggleOppacity
        });
    } else {
        $('#changeNetworkBlock').animate({
            opacity: hideOppacity
        });
        $('#changeVlanButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#locateNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#descriptionNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#delNetButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
    }
});

$('#changeVLAN').click(function () {
    let blockCssOpacity = $('#changeVlanBlock').css('display')

    if (blockCssOpacity === 'none') {
        $('#changeNetworkButtonBlock').animate({
            opacity: outOppacity
        });
        $('#locateNetworkButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#descriptionNetworkButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#delNetButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#changeVlanBlock').delay(500).animate({
            opacity: toggleOppacity
        });
    } else {
        $('#changeVlanBlock').animate({
            opacity: hideOppacity
        });
        $('#changeNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#locateNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#descriptionNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#delNetButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
    }
});

$('#locateNetwork').click(function () {
    let blockCssOpacity = $('#changeLocationBlock').css('display')

    if (blockCssOpacity === 'none') {
        $('#changeNetworkButtonBlock').animate({
            opacity: outOppacity
        });
        $('#changeVlanButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#descriptionNetworkButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#delNetButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#changeLocationBlock').delay(500).animate({
            opacity: toggleOppacity
        });
    } else {
        $('#changeLocationBlock').animate({
            opacity: hideOppacity
        });
        $('#changeNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#changeVlanButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#descriptionNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#delNetButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
    }
});


$('#descriptionNetwork').click(function () {
    let blockCssOpacity = $('#changeDescriptionBlock').css('display')

    if (blockCssOpacity === 'none') {
        $('#changeNetworkButtonBlock').animate({
            opacity: outOppacity
        });
        $('#changeVlanButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#locateNetworkButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#delNetButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#changeDescriptionBlock').delay(500).animate({
            opacity: toggleOppacity
        });
    } else {
        $('#changeDescriptionBlock').animate({
            opacity: hideOppacity
        });
        $('#changeNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#changeVlanButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#locateNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#delNetButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
    }
});




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





