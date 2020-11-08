const csrftoken = getCookie('csrftoken');
const changeNetworkButton = document.getElementById('changeNetwork')
const deleteButton = document.getElementById('delButton')
const changeDescriptionForm = document.getElementById('changeDescriptionForm')
const changeNetworkBlock = document.getElementById('changeNetworkBlock')

let positionButtonsLeft = 250
let positionDescriptionButton = $('#descriptionNetwork').offset().top
let positionNetworkButton = $('#changeNetwork').offset().top
let inOppacity = '1'
let outOppacity = '0'
let toggleOppacity = 'toggle'
let hideOppacity = 'hide'




///////////////////////////////////////////////////////////////////
function checkDelete(e) {
    if (!confirm('Вы уверены что хотите удалить сеть ?')) {
        e.preventDefault()
    }
}

////////////////////////////////////////////////////////////////////

$('.oneStringBlock').hide()
$('#changeNetwork').click(function () {
    let blockCssOpacity = $('#changeNetworkBlock').css('display')

    if (blockCssOpacity === 'none') {
        $('#descriptionNetworkButtonBlock').animate({
            opacity: outOppacity
        });
        $('#delButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#classNetworkButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#changeNetworkBlock').delay(500).animate({
            opacity: toggleOppacity
        });
    } else {
            $('#changeNetworkBlock').animate({
            opacity: hideOppacity
        });
            $('#descriptionNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
             $('#delButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
             $('#classNetworkButtonBlock').delay(500).animate({
                 opacity: inOppacity
             });
    }
});



$('#descriptionNetwork').click(function () {
    let blockCssOpacity = $('#descriptionNetworkBlock').css('display')
    if (blockCssOpacity === 'none') {
        $('#changeNetworkButtonBlock').animate({
            opacity: outOppacity
        });
        $('#delButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#classNetworkButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#descriptionNetworkBlock').delay(500).animate({
            opacity: toggleOppacity
        });
    } else {
        $('#descriptionNetworkBlock').animate({
            opacity: hideOppacity
        });
        $('#changeNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#delButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#classNetworkButtonBlock').delay(500).animate({
                 opacity: inOppacity
        });
    }
})

$('#classNetwork').click(function () {
    let blockCssOpacity = $('#changeClassNetworkBlock').css('display')
    if (blockCssOpacity === 'none') {
        $('#changeNetworkButtonBlock').animate({
            opacity: outOppacity
        });
        $('#delButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#descriptionNetworkButtonBlock').animate({
            opacity: outOppacity
        }, {queue: false});
        $('#changeClassNetworkBlock').delay(500).animate({
            opacity: toggleOppacity
        });
    } else {
        $('#changeClassNetworkBlock').animate({
            opacity: hideOppacity
        });
        $('#changeNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#delButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
        $('#descriptionNetworkButtonBlock').delay(500).animate({
            opacity: inOppacity
        });
    }
})

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
    let newDescription = prompt('Введите новый дескрипшн')
    if (newDescription === null) {
        return
    }
    $.ajax({
        type: 'POST',
        async: true,
        url: '/changeDescription/',
        data: {csrfmiddlewaretoken: getCookie('csrftoken'),
                newDescription: newDescription,
                test: this.getAttribute('data-objectId')},
        success: function (data) {
            currentObject.innerHTML = data['newDescription']
        },
        dataType: 'json'
    })
});


////////////////////////////////////////// Test block //////////////////////////////////////////////////////////


