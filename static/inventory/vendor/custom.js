
$(document).ready(function () {
    var table = $('#example').DataTable({
        lengthChange: false,
        buttons: ['pdf', 'print'],
        language: {
            emptyTable: "No hay datos disponibles",
            search: 'Buscar',
            previous: 'Anterior',
            info: "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            paginate: {
                first: "Primero",
                previous: "Anterior",
                next: "Siguiente",
                last: "Último"
            },
            infoEmpty: "Mostrando de 0 a 0 de 0 elementos",
            buttons: {
                print: "Imprimir"
            }
        }
    });
    table.buttons().container()
        .appendTo('#example_wrapper .col-md-6:eq(0)');
});