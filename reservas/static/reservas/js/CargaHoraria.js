document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const servicioSelect = document.getElementById('servicio');
    const diaSelect = document.getElementById('dia');
    const timeSlotsContainer = document.getElementById('time-slots');

    // Estado inicial
    timeSlotsContainer.innerHTML = '<p class="info-message">Seleccione un servicio y un día</p>';
    diaSelect.disabled = true;

    // ==============================================
    // 1. Función para cargar días según servicio
    // ==============================================
    const cargarDiasDisponibles = async (servicio) => {
        // Resetear estado
        diaSelect.innerHTML = '<option value="">Cargando días...</option>';
        diaSelect.disabled = true;
        timeSlotsContainer.innerHTML = '<p class="info-message">Seleccione un día</p>';

        try {
            const response = await fetch(`/reservas/get_dias_por_servicio/?servicio=${encodeURIComponent(servicio)}`);
            
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            if (!data.dias || data.dias.length === 0) {
                diaSelect.innerHTML = '<option value="">No hay días disponibles</option>';
                return;
            }

            // Llenar select de días
            diaSelect.innerHTML = [
                '<option value="">-- Seleccione día --</option>',
                ...data.dias.map(dia => `<option value="${dia.value}">${dia.text}</option>`)
            ].join('');
            
            diaSelect.disabled = false;

        } catch (error) {
            console.error('Error al cargar días:', error);
            diaSelect.innerHTML = '<option value="">Error al cargar días</option>';
            timeSlotsContainer.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
        }
    };

    // ==============================================
    // 2. Función para cargar horarios
    // ==============================================
        const cargarHorariosDisponibles = async (servicio, dia) => {
        timeSlotsContainer.innerHTML = '<p class="info-message">Cargando horarios...</p>';

        try {
            const response = await fetch(`/reservas/get_horarios/?servicio=${encodeURIComponent(servicio)}&dia=${encodeURIComponent(dia)}`);
            
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            // Verificar si hay error en la respuesta
            if (data.status === 'error') {
                throw new Error(data.error || 'Error desconocido del servidor');
            }
            
            // Usar data.total_disponibles para mejor feedback
            if (!data.horarios || data.total_disponibles === 0) {
                timeSlotsContainer.innerHTML = '<p class="info-message">No hay horarios disponibles para este día</p>';
                return;
            }

            // Mostrar horarios
            timeSlotsContainer.innerHTML = '';
            data.horarios.forEach((horario, index) => {
                const div = document.createElement('div');
                div.className = 'time-slot';

                const input = document.createElement('input');
                input.type = 'radio';
                input.id = `turno-${index}`;
                input.name = 'turno_seleccionado';
                input.value = horario;

                const label = document.createElement('label');
                label.htmlFor = `turno-${index}`;
                label.textContent = horario;

                input.addEventListener('change', function() {
                    document.getElementById('horario-seleccionado').value = this.value;
                    console.log('Horario seleccionado:', this.value);
                });

                div.appendChild(input);
                div.appendChild(label);
                timeSlotsContainer.appendChild(div);
            });

        } catch (error) {
            console.error('Error al cargar horarios:', error);
            timeSlotsContainer.innerHTML = `
                <p class="error-message">Error al cargar horarios</p>
                <p class="error-detail">${error.message}</p>
            `;
        }
    };
    // ==============================================
    // 3. Manejadores de Eventos
    // ==============================================
    servicioSelect.addEventListener('change', function() {
        const servicio = this.value;
        
        if (!servicio) {
            diaSelect.innerHTML = '<option value="">-- Seleccione servicio --</option>';
            diaSelect.disabled = true;
            timeSlotsContainer.innerHTML = '<p class="info-message">Seleccione un servicio</p>';
            return;
        }
        
        cargarDiasDisponibles(servicio);
    });

    diaSelect.addEventListener('change', function() {
        const servicio = servicioSelect.value;
        const dia = this.value;
        
        if (!servicio || !dia) {
            timeSlotsContainer.innerHTML = '<p class="info-message">Seleccione servicio y día</p>';
            return;
        }
        
        cargarHorariosDisponibles(servicio, dia);
    });

    // ==============================================
    // 4. Inicialización (opcional)
    // ==============================================
    // Si hay valores preseleccionados
    if (servicioSelect.value && diaSelect.value) {
        diaSelect.disabled = false;
        cargarHorariosDisponibles(servicioSelect.value, diaSelect.value);
    }
});