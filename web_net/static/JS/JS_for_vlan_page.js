const deleteButtons = document.getElementsByClassName('trashForm')

///////////////////////////////////////////////////////////////////////////////
function checkDelete(e) {
    //alert("YES")
    if (!confirm('Вы уверены что хотите удалить VLAN ?')) {
        e.preventDefault()
    }
}

///////////////////////////////////////////////////////////////////////////////

console.log('JS for VLAN page its work!');
$('#addForm').hide()
$('#addVLAN').on('click',function () {
    $('#addForm').slideToggle(500);
});

Array.from(deleteButtons).forEach(function (deleteButton){
     deleteButton.addEventListener('submit', checkDelete, false)
})


