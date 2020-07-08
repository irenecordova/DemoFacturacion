$(document).ready(function () {

    $(document).on('click', '#btnAddInput', function () {
        var num = $('.clonedInput').length;
        var newNum = new Number(num + 1);
        ids = $('a[name=btnDel]')
        ids.each(function () {
            if ($(this).attr('id') == newNum){
                num = new Number($(this).attr('id'));
                newNum += 1;
            }
            
        });

        var newElem = $('#filaitem_' + num).clone().attr('id', 'filaitem_' + newNum);

        
        newElem.children('td[data-name=item]').children('input').attr('id', 'item_id_' + newNum);
        newElem.find('input[name=item]').attr('id', 'item_' + newNum);
        newElem.find('button[name=btnBuscarItem]').attr('id', newNum);


        newElem.children('td[data-name=cantidad]').find('input').attr('id', 'cantidad_' + newNum);
        newElem.children('td[data-name=precio_unitario]').find('input').attr('id', 'precio_unitario_' + newNum);
        newElem.children('td[data-name=descuento_porcentaje]').find('input').attr('id', 'descuento_porcentaje_' + newNum);
        newElem.children('td[data-name=descuento_dolares]').find('input').attr('id', 'descuento_dolares_' + newNum);
        newElem.children('td[data-name=ice_porcentaje]').find('input').attr('id', 'ice_porcentaje_' + newNum);
        newElem.children('td[data-name=iva_porcentaje]').children(':last').attr('id', 'iva_porcentaje_' + newNum);
        newElem.children('td[data-name=iva_porcentaje]').children(':first').attr('id', 'iva_id_' + newNum);
        newElem.children('td[data-name=subtotal]').find('input').attr('id', 'subtotal_' + newNum);

        newElem.find('input').val('');
        newElem.children('td[data-name=idDetalleItem]').find('input').val('0');
        newElem.children('td[data-name=ice_porcentaje]').find('input').val('0');
        newElem.children('td[data-name=iva_porcentaje]').find('input').val('0');

        newElem.children(':first').children().attr('style', 'display:block;').attr('id', newNum);
        $('#filaitem_' + num).children(':last').children().attr('style', 'display:none;')
        $('#filaitem_' + num).after(newElem);

    });

    $('#formDocumentoVenta').submit(function(event){
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
                if (data['error']==0){
                    location.assign('/factura/'+data['data']);
                }
            }
        }).fail(function(e){
            alert('Ocurrió un problema')
        });
    });

});
