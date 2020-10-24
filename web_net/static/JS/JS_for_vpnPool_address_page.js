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