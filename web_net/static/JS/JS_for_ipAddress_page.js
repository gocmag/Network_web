console.log('network JS its fork for ipAddress page!');

$('.changeDescriptions2').hide()

let x = $('td *').on('click',function () {
    let id = this.id;
    let native_top = $(this).offset().top;
    let native_left = $(this).offset().left;

    let digits = parseInt(id.match(/\d+/));
    let newChangeDescriptionId = '#'+'changeDescription'+digits;
    $(newChangeDescriptionId).fadeIn(800);
});








