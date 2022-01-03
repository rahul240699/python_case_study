$(document).ready(function() {
    // show the alert
    setTimeout(function() {
        $(".alert").alert('close');
    }, 2000);
});

$(function () {
    $('.YetTORegister').on('click', function () {
        if (confirm("Are you sure!")) {
            var EventId = $(this).val();
        console.log(EventId)
        $.ajax({
            url: '/student/eventIdUpdate',
            data: {
                Eid: EventId
            },
            contentType: "application/json",
            dataType : 'json'
        });
        $(this).text("Registred")
          } else {
            
          }
        
    });
});

