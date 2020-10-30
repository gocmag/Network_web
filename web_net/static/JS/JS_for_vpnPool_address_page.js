const csrftoken = getCookie('csrftoken');
const changeNetworkButton = document.getElementById('changeNetwork')
const deleteButton = document.getElementById('delButton')
const changeDescriptionForm = document.getElementById('changeDescriptionForm')

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

$('#changeNetworkForm').hide()
$('#changeNetwork').on('click',function () {
    $('#changeDescriptionForm').fadeOut(500);
    $('#changeNetworkForm').fadeToggle(500).offset({top:positionNetworkButton, left:positionButtonsLeft});
});


$('#changeDescriptionForm').hide()
$('#descriptionNetwork').on('click', function () {
    $('#changeNetworkForm').fadeOut(500);
    $('#changeDescriptionForm').fadeToggle(500).offset({top:positionDescriptionButton, left:positionButtonsLeft})
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


