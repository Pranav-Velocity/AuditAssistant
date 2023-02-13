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

    document.addEventListener("wheel", function(event){
        if(document.activeElement.type === "number"){
            document.activeElement.blur();
        }
    });

    jQuery.validator.addMethod("alphanumeric", function(value, element) {
        return this.optional(element) || /^\w+$/i.test(value);
        }, "Letters, numbers, and underscores only please");
    
        $.validator.addMethod("alphabets_and_spaces", function(value, element) {
        return this.optional(element) || value == value.match(/^[a-zA-Z ]*$/);
     });

     $.validator.addMethod("pwcheck", function(value) {
        return /^[A-Za-z0-9\d=!\-@._*]*$/.test(value) // consists of only these
            && /[a-z]/.test(value) // has a lowercase letter
            && /\d/.test(value) // has a digit
      });
  
      $.validator.addMethod("emailcheck", function(value) {
        return /^\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,10}\b$/i.test(value) // consists of only these
      },"Please enter a valid email address");

      jQuery.validator.addMethod("validDate", function(value, element) {
        return this.optional(element) || moment(value,"dd/mm/yyyy").isValid();
    }, "Please enter a valid date in the format dd/mm/yyyy");

    $( document ).ready(function() {
        $('input').prop('autocomplete', 'off');
    });