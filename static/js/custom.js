$('INPUT[type="file"]').change(function(){
    var ext = this.value.match(/\.(.+)$/)[1];
    console.log(ext)
    switch(ext){
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
        case 'pdf':
        case 'docx':
        case 'xlsx':
        case 'csv':
            $('#submit_form').attr('disabled', false);
            break;
        default:
            alert("This file format is not allowed");
            this.value = "";
        }
    });

    