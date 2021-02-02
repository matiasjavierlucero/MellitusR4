
$(document).ready(function(){

  load_json_data('obraSocialPaciente');

  function load_json_data(idOS, parent_idOS)
  {
  var html_code = '';
  $.getJSON('static/data/mutual_plan.json', function(data){

    html_code += '<option value="1"> ... </option>';
    $.each(data, function(key, value){
    if(idOS == 'obraSocialPaciente')
    {
      if(value.parent_idOS == '0')
      {
      html_code += '<option value="'+value.idOS+'">'+value.nameOS+'</option>';
      }
    }
    else
    {
      if(value.parent_idOS == parent_idOS)
      {
      html_code += '<option value="'+value.idOS+'">'+value.nameOS+'</option>';
      }
    }
    });
    $('[id = ' +idOS+ ']').html(html_code);
  });

  }

  $(document).on('change', '#obraSocialPaciente', function(){
  var obraSocialPaciente_idOS = $(this).val();
  if(obraSocialPaciente_idOS != '')
  {
    load_json_data('planObSoPaciente', obraSocialPaciente_idOS);
  }
  else
  {
    $('#planObSoPaciente').html('<option value=""></option>');
    $('#lcacadPaciente').html('<option value=""></option>');
  }
  });
});
