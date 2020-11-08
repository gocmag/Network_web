const deleteButtons = document.getElementsByClassName('trashForm')

let positionButtonsLeft = 250
let positionNetworkButton = $('#addClassNetwork').offset().top


$('#addForm').offset({top:positionNetworkButton-18})

///////////////////////////////////////////////////////////////////////////////
function checkDelete(e) {
    //alert("YES")
    if (!confirm('Вы уверены что хотите удалить сеть ?')) {
        e.preventDefault()
    }
}

///////////////////////////////////////////////////////////////////////////////

$('#addForm').hide()
$('#addClassNetwork').on('click',function () {
    $('#addForm').slideToggle(500);
});


Array.from(deleteButtons).forEach(function (deleteButton){
     deleteButton.addEventListener('submit', checkDelete, false)
})
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



$('.classNetworkTd').click(function () {
    let currentObject = this
    $.ajax({
        type: 'POST',
        async: true,
        url: '/changeClassNetwork/',
        data: {csrfmiddlewaretoken: getCookie('csrftoken'),
               newClassNetwork: prompt('Введите новую классовую сеть'),
               objectId: this.getAttribute('data-objectId')},
        success: function (data) {
            currentObject.innerHTML = data['newClassNetwork']
        },
        dataType: 'json'
    })
});


$('.classNetworkDescriprion').click(function () {
    let currentObject = this
    let newDescription = prompt('Введите новый дескрипшн')
    if (newDescription === null) {
        return
    }
    $.ajax({
        type: 'POST',
        async: true,
        url: '/changeClassNetworkDescription/',
        data: {csrfmiddlewaretoken: getCookie('csrftoken'),
               newClassNetworkDescription: newDescription,
               objectId: this.getAttribute('data-objectId')},
        success: function (data) {
            currentObject.innerHTML = data['newClassNetworkDescription']
        },
        dataType: 'json'
    })
});