$(document).ready(function () {

    $('#formCerrarCaja').submit(function(event){
        event.preventDefault();
        var datos = new FormData($(this)[0]);
        $.ajax({                       
            method: 'POST',
            url: '',
            data: datos,
            processData: false,
            contentType: false,        
            success: function(data){
                alert(data['detail'])
            }
        }).fail(function(e){
            alert('Ocurrió un problema')
        });
    });

});
