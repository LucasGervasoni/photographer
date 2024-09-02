var buttons = document.querySelectorAll('.viewInfo');
var infoSections = document.querySelectorAll('.listInfo');

// Get the order ID from the session variable
var openListInfo = '{{ request.session.open_list_info|default:"" }}';

// Loop through each button
buttons.forEach(function(button, index) {
    var info = infoSections[index];
    
    // Check if this info section matches the session-stored openListInfo ID
    if (info.getAttribute('data-order-id') === openListInfo) {
        info.classList.remove('d-none');
        button.textContent = 'Hide';
    }
    
    button.addEventListener('click', function() {
        if(info.classList.contains('d-none')){
            info.classList.remove('d-none')
            button.textContent = 'Hide';
        } else {
            info.classList.toggle('d-none')
            button.textContent = 'View';
        }
    });
});
