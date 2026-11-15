document.addEventListener('DOMContentLoaded', () => {
    inicializarDataTables();
    inicializarTooltips();
});

function inicializarDataTables() {
    if (typeof DataTable === 'undefined') {
        return;
    }

    const tablas = document.querySelectorAll(
        'table[data-datatable="true"]'
    );

    tablas.forEach((tabla) => {
        new DataTable(tabla, {
            pageLength: 10,
            order: [],
            language: {
                emptyTable: 'No hay registros disponibles',
                info: 'Mostrando _START_ a _END_ de _TOTAL_ registros',
                infoEmpty: 'Mostrando 0 registros',
                infoFiltered: '(filtrado de _MAX_ registros totales)',
                lengthMenu: 'Mostrar _MENU_ registros',
                loadingRecords: 'Cargando...',
                processing: 'Procesando...',
                search: 'Buscar:',
                zeroRecords: 'No se encontraron resultados',
                paginate: {
                    first: 'Primero',
                    last: 'Ultimo',
                    next: 'Siguiente',
                    previous: 'Anterior'
                }
            }
        });
    });
}

function inicializarTooltips() {
    if (
        typeof coreui === 'undefined'
        || typeof coreui.Tooltip === 'undefined'
    ) {
        return;
    }

    const elementos = document.querySelectorAll(
        '[data-coreui-toggle="tooltip"]'
    );

    elementos.forEach((elemento) => {
        new coreui.Tooltip(elemento);
    });
}