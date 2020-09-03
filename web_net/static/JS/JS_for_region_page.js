//document.getElementById('addRegion').hidden = true;
$('#regionForm').hide()
$('#addRegion').on('click',function () {
    $('#regionForm').slideToggle(1500);
});

$('.geokodObject tr').on('click', function () {
    $(this).find('td').css({
        background: "rgb(201, 93, 16)",
        transition: "0.7s"
    });
    let elem = document.querySelector('.geokodObject td');
    let test = $(this).find('td').css('background');
    let test2 = $(event.target).css('background-color');
    console.log(test2);
    if (test2 === 'rgb(201, 93, 16)') {
        $(this).find('td').css({
        background: "rgb(248, 248, 255)",
        transition: "0.7s"})
    }
});

