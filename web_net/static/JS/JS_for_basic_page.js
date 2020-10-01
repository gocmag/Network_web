const closeButton = document.getElementById('closeMessageButton')
const messageBlock = document.getElementById('messageBlock')

closeButton.addEventListener('click', function () {
    messageBlock.remove()
})