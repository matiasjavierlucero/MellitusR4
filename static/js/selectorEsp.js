$(document).ready(function() {
    $('#especialidadProfesional').multiselect({
        nonSelectedText: 'Seleccione especialidad/es',
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        numberDisplayed: 5,
        selectAll: false,
        buttonWidth: '400px'

    })
});