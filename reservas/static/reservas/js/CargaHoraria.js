document.addEventListener('DOMContentLoaded', function() {
    const servicioSelect = document.getElementById('servicio');
    const fechaContainer = document.getElementById('fecha-container');
    const dateSlotsContainer = document.getElementById('date-slots');
    const horarioContainer = document.getElementById('horario-container');
    const timeSlotsContainer = document.getElementById('time-slots');
    const fechaReservaInput = document.getElementById('fecha-reserva-seleccionada');
    const horarioSeleccionadoInput = document.getElementById('horario-seleccionado');
    const disponibilidadIdInput = document.getElementById('disponibilidad-id');

    let disponibilidadesActuales = [];
    let fechaSeleccionada = null;

    servicioSelect.addEventListener('change', async function() {
        const servicioId = this.value;
        
        resetUI();
        if (!servicioId) return;

        try {
            showLoading();
            const response = await fetch(`/reservas/obtener-servicios/?servicio_id=${encodeURIComponent(servicioId)}`);
            const data = await response.json();
            
            if (!data.disponibilidades || data.disponibilidades.length === 0) {
                showMessage('No hay disponibilidades para este servicio');
                return;
            }

            disponibilidadesActuales = data.disponibilidades;
            mostrarFechasDisponibles(data.disponibilidades);
            fechaContainer.style.display = 'block';

        } catch (error) {
            console.error('Error:', error);
            showMessage(`Error: ${error.message}`, true);
        }
    });

    function resetUI() {
        fechaContainer.style.display = 'none';
        horarioContainer.style.display = 'none';
        dateSlotsContainer.innerHTML = '';
        timeSlotsContainer.innerHTML = '<p class="info-message">Seleccione un servicio</p>';
        fechaSeleccionada = null;
        fechaReservaInput.value = '';
        horarioSeleccionadoInput.value = '';
        disponibilidadIdInput.value = '';
    }

    function showLoading() {
        dateSlotsContainer.innerHTML = '<p class="loading-message">Cargando fechas disponibles...</p>';
    }

    function showMessage(message, isError = false) {
        dateSlotsContainer.innerHTML = `<p class="${isError ? 'error-message' : 'info-message'}">${message}</p>`;
    }

    function mostrarFechasDisponibles(disponibilidades) {
        const todasFechas = [];
        
        disponibilidades.forEach(disp => {
            const fechaInicio = new Date(disp.fecha_inicio);
            const fechaFin = new Date(disp.fecha_fin);
            
            for (let fecha = new Date(fechaInicio); fecha <= fechaFin; fecha.setDate(fecha.getDate() + 1)) {
                const fechaStr = fecha.toISOString().split('T')[0];
                if (!todasFechas.includes(fechaStr)) {
                    todasFechas.push(fechaStr);
                }
            }
        });

        todasFechas.sort();

        dateSlotsContainer.innerHTML = todasFechas.map(fecha => `
            <div class="date-slot">
                <input type="radio" 
                       name="fecha_seleccionada" 
                       id="fecha-${fecha}" 
                       value="${fecha}">
                <label for="fecha-${fecha}">
                    ${formatearFechaBonita(fecha)}
                </label>
            </div>
        `).join('');

        document.querySelectorAll('.date-slot input').forEach(radio => {
            radio.addEventListener('change', function() {
                fechaSeleccionada = this.value;
                fechaReservaInput.value = this.value;
                horarioContainer.style.display = 'block';
                mostrarHorariosDisponibles(this.value);
            });
        });
    }

    function mostrarHorariosDisponibles(fecha) {
        timeSlotsContainer.innerHTML = '<p class="loading-message">Cargando horarios...</p>';
        
        const disponibilidadesParaFecha = disponibilidadesActuales.filter(disp => {
            const dispFechaInicio = new Date(disp.fecha_inicio);
            const dispFechaFin = new Date(disp.fecha_fin);
            const fechaSeleccionadaObj = new Date(fecha);
            return fechaSeleccionadaObj >= dispFechaInicio && fechaSeleccionadaObj <= dispFechaFin;
        });

        if (disponibilidadesParaFecha.length === 0) {
            timeSlotsContainer.innerHTML = '<p class="info-message">No hay horarios para esta fecha</p>';
            return;
        }

        const todosTurnos = [];
        
        disponibilidadesParaFecha.forEach(disp => {
            const turnos = generarTurnosParaFecha(disp, fecha);
            todosTurnos.push(...turnos.map(t => {
                const [hora, minuto] = t.hora.split(':').map(Number);
                let finMinuto = minuto + disp.intervalo;
                let finHora = hora;

                if (finMinuto >= 60) {
                    finHora += Math.floor(finMinuto / 60);
                    finMinuto = finMinuto % 60;
                }

                const horaFin = `${String(finHora).padStart(2, '0')}:${String(finMinuto).padStart(2, '0')}`;
                return {
                    ...t,
                    hora_fin: horaFin,
                    ubicacion: disp.ubicacion,
                    disponibilidad_id: disp.id,
                    hora_inicio: t.hora,
                    hora_fin: horaFin
                };
            }));
        });
        
        timeSlotsContainer.innerHTML = todosTurnos.map(turno => `
            <div class="time-slot">
                <input type="radio" 
                    name="turno_seleccionado" 
                    id="turno-${turno.disponibilidad_id}" 
                    value="${turno.disponibilidad_id}"
                    data-hora-inicio="${turno.hora_inicio}"
                    data-hora-fin="${turno.hora_fin}">
                <label for="turno-${turno.disponibilidad_id}">
                    ${turno.hora_inicio} - ${turno.hora_fin} (${turno.ubicacion})
                </label>
            </div>
        `).join('');

        document.querySelectorAll('.time-slot input').forEach(radio => {
            radio.addEventListener('change', function() {
                // Guardar el ID de disponibilidad
                disponibilidadIdInput.value = this.value;
                
                // Guardar el horario formateado
                horarioSeleccionadoInput.value = `${this.dataset.horaInicio} - ${this.dataset.horaFin}`;
                
                console.log('Datos seleccionados:', {
                    disponibilidad_id: this.value,
                    horario: horarioSeleccionadoInput.value
                });
            });
        });
    }

    function generarTurnosParaFecha(disponibilidad, fecha) {
        const turnos = [];
        const [horaInicio, minInicio] = disponibilidad.hora_inicio.split(':').map(Number);
        const [horaFin, minFin] = disponibilidad.hora_fin.split(':').map(Number);
        const intervalo = disponibilidad.intervalo;
        
        let horaActual = horaInicio;
        let minActual = minInicio;
        
        while (horaActual < horaFin || (horaActual === horaFin && minActual < minFin)) {
            const horaFormateada = `${String(horaActual).padStart(2, '0')}:${String(minActual).padStart(2, '0')}`;
            turnos.push({
                hora: horaFormateada
            });
            
            minActual += intervalo;
            if (minActual >= 60) {
                horaActual += Math.floor(minActual / 60);
                minActual = minActual % 60;
            }
        }
        
        return turnos;
    }

    function formatearFechaBonita(fechaStr) {
        const opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const fecha = new Date(fechaStr);
        return fecha.toLocaleDateString('es-ES', opciones);
    }
});