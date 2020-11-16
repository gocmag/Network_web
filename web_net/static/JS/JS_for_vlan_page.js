const deleteButtons = document.getElementsByClassName('trashForm')

let positionVlanButton = $('#addVLAN').offset().top

///////////////////////////////////////////////////////////////////////////////
function checkDelete(e) {
    //alert("YES")
    if (!confirm('Вы уверены что хотите удалить VLAN ?')) {
        e.preventDefault()
    }
}

///////////////////////////////////////////////////////////////////////////////
$('#addForm').offset({top:positionVlanButton-18})
$('#addForm').hide()
$('#addVLAN').on('click',function () {
    $('#addForm').toggle(500);
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
        url: '/changeVlanDescription/',
        data: {csrfmiddlewaretoken: getCookie('csrftoken'),
                newDescription: newDescription,
                objectId: this.getAttribute('data-objectId')},
        success: function (data) {
            currentObject.innerHTML = data['newDescription']
        },
        dataType: 'json'
    })
});