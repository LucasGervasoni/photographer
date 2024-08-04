var buttons = document.querySelectorAll('.viewInfo');
var infoSections = document.querySelectorAll('.listInfo');

// Loop through each button
buttons.forEach(function(button, index) {
    button.addEventListener('click', function() {
        var info = infoSections[index];
        if(info.classList.contains('d-none')){
            info.classList.remove('d-none')
            button.textContent = 'Hide';
        } else {
            info.classList.toggle('d-none')
            button.textContent = 'View';
        }
    });
});
