console.log('network JS its worksb!');
//document.getElementById('addNetwork').hidden = true;
$('#networkForm').hide()
$('#addNetwork').on('click',function () {
    $('#networkForm').slideToggle(500);
});

