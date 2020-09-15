const deleteButtons = document.getElementsByClassName('trashForm')

///////////////////////////////////////////////////////////////////////////////
function checkDelete(e) {
    alert("YES")
 //   if (!confirm('Вы уверены что хотите удалить сеть ?')) {
 //       e.preventDefault()
 //   }
}

///////////////////////////////////////////////////////////////////////////////

console.log('JS for VLAN page its work!');
$('#addForm').hide()
$('#addVLAN').on('click',function () {
    $('#addForm').slideToggle(500);
});

//deleteButtons.addEventListener('submit', checkDelete, false)
