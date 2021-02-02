
$(document).ready(function(){

  load_json_data('paisPaciente');

  function load_json_data(id, parent_id)
  {
  var html_code = '';
  $.getJSON('static/data/country_state_city.json', function(data){

    html_code += '<option value=""> ... </option>';
    $.each(data, function(key, value){
    if(id == 'paisPaciente')
    {
      if(value.parent_id == '0')
      {
      html_code += '<option value="'+value.id+'">'+value.name+'</option>';
      }
    }
    else
    {
      if(value.parent_id == parent_id)
      {
      html_code += '<option value="'+value.id+'">'+value.name+'</option>';
      }
    }
    });
    $('#'+id).html(html_code);
  });

  }

  $(document).on('change', '#paisPaciente', function(){
  var paisPaciente_id = $(this).val();
  if(paisPaciente_id != '')
  {
    load_json_data('provinciaPaciente', paisPaciente_id);
  }
  else
  {
    $('#provinciaPaciente').html('<option value=""></option>');
    $('#localidadPaciente').html('<option value=""></option>');
  }
  });
  $(document).on('change', '#provinciaPaciente', function(){
  var provinciaPaciente_id = $(this).val();
  if(provinciaPaciente_id != '')
  {
    load_json_data('localidadPaciente', provinciaPaciente_id);
  }
  else
  {
    $('#localidadPaciente').html('<option value=""></option>');
  }
  });
});

