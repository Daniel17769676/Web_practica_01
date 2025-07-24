function establecerFechaHoy() {
    const hoy = new Date();
    const fechaFormateada = hoy.toISOString().split('T')[0];
    document.getElementById('fecha_inicio').value = fechaFormateada;
    document.getElementById('fecha_fin').value = fechaFormateada;
}
