$('.select2').select2();


function b64toBlob(b64Data, contentType, sliceSize) {
        contentType = contentType || '';
        sliceSize = sliceSize || 512;

        var byteCharacters = atob(b64Data);
        var byteArrays = [];

        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            var slice = byteCharacters.slice(offset, offset + sliceSize);

            var byteNumbers = new Array(slice.length);
            for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            var byteArray = new Uint8Array(byteNumbers);

            byteArrays.push(byteArray);
        }

      var blob = new Blob(byteArrays, {type: contentType});
      return blob;
}

function s_msg(msg){
    msg = '<div class="alert alert-success alert-dismissible alert-custom">\n' +
        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>\n' +
        '<i class="icon fa fa-check"></i>Success! ' + msg +
        '</div>';
    return msg;
}

function e_msg(msg){
    msg = '<div class="alert alert-danger alert-dismissible alert-custom">\n' +
        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>\n' +
        '<i class="icon fa fa-ban"></i>Error! ' + msg +
        '</div>';
    return msg;
}

function w_msg(msg){
    msg = '<div class="alert alert-warning alert-dismissible alert-custom">\n' +
        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>\n' +
        '<i class="icon fa fa-warning"></i>Warning! ' + msg +
        '</div>';
    return msg;
}

function i_msg(msg){
    msg = '<div class="alert alert-info alert-dismissible alert-custom">\n' +
        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>\n' +
        '<i class="icon fa fa-info"></i>Info! ' + msg +
        '</div>';
    return msg;
}

function displayNoti(type,msg) {
    if (type == 'error'){
        $('.msg-noti').append(e_msg(msg));
    }
    if (type == 'success'){
        $('.msg-noti').append(s_msg(msg));
    }
    if (type == 'warning'){
        $('.msg-noti').append(w_msg(msg));
    }
    if (type == 'info'){
        $('.msg-noti').append(i_msg(msg));
    }
}
function clearNoti() {
    $('.msg-noti').html("");
}
