$('#drole').hide();
$('#nurole').hide();
$('#prole').hide();
$("#loginasrole").change(function() {
    if ($(this).val() == "Doctor") {
        $('#drole').show();
        $('#nurole').hide();
        $('#prole').hide();
    } 
    if ($(this).val() == "Nurse") {
        $('#drole').hide();
        $('#nurole').show();
        $('#prole').hide();				
    }
    if ($(this).val() == "Ptient") {
        $('#drole').hide();
        $('#nurole').hide();
        $('#prole').show();				
    }
    if ($(this).val() == "default"){
        $('#drole').hide();
        $('#nurole').hide();
        $('#prole').hide();
    }
});