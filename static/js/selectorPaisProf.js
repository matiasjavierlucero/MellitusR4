$(document).ready(function(){

    load_json_data('paisProfesional');
  
    function load_json_data(id, parent_id)
    {
    var html_code = '';
    $.getJSON('static/data/country_state_city.json', function(data){
  
      html_code += '<option value="1"> ... </option>';
      $.each(data, function(key, value){
      if(id == 'paisProfesional')
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
      $('[id = ' +id+ ']').html(html_code);
    });
  
    }
  
    $(document).on('change', '#paisProfesional', function(){
    var paisProfesional_id = $(this).val();
    if(paisProfesional_id != '')
    {
      load_json_data('provinciaProfesional', paisProfesional_id);
    }
    else
    {
      $('#provinciaProfesional').html('<option value=""></option>');
      $('#localidadProfesional').html('<option value=""></option>');
    }
    });
    $(document).on('change', '#provinciaProfesional', function(){
    var provinciaProfesional_id = $(this).val();
    if(provinciaProfesional_id != '')
    {
      load_json_data('localidadProfesional', provinciaProfesional_id);
    }
    else
    {
      $('#localidadProfesional').html('<option value=""></option>');
    }
    });
  });
  