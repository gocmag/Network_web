const csrftoken = getCookie('csrftoken');
const changeNetworkButton = document.getElementById('changeNetwork')
const deleteButton = document.getElementById('delButton')
const changeDescriptionForm = document.getElementById('changeDescriptionForm')
const changeNetworkBlock = document.getElementById('changeNetworkBlock')

let positionButtonsLeft = 250
let positionDescriptionButton = $('#descriptionNetwork').offset().top
let positionNetworkButton = $('#changeNetwork').offset().top




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
            opacity: 'toggle'
        });
        $('#delButtonBlock').animate({
            opacity: 'toggle'
        }, {queue: false});
        $('#changeNetworkBlock').delay(500).animate({
            opacity: 'toggle'
        });
    } else {
            $('#changeNetworkBlock').animate({
            opacity: 'toggle'
        });
            $('#descriptionNetworkButtonBlock').delay(500).animate({
            opacity: 'toggle'
        });
             $('#delButtonBlock').delay(500).animate({
            opacity: 'toggle'
        });
    }
});



$('#descriptionNetwork').click(function () {
    let blockCssOpacity = $('#descriptionNetworkBlock').css('display')
    if (blockCssOpacity === 'none') {
        $('#changeNetworkButtonBlock').animate({
            opacity: 'toggle'
        });
        $('#delButtonBlock').animate({
            opacity: 'toggle'
        }, {queue: false});
        $('#descriptionNetworkBlock').delay(500).animate({
            opacity: 'toggle'
        });
    } else {
        $('#descriptionNetworkBlock').animate({
            opacity: 'toggle'
        });
        $('#changeNetworkButtonBlock').delay(500).animate({
            opacity: 'toggle'
        });
        $('#delButtonBlock').delay(500).animate({
            opacity: 'toggle'
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


////////////////////////////////////////// Test block //////////////////////////////////////////////////////////


