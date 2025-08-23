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

    async function mostrarHorariosDisponibles(fecha) {
        timeSlotsContainer.innerHTML = '<p class="loading-message">Cargando horarios...</p>';
        
        const servicioId = servicioSelect.value;
        
        if (!servicioId) {
            timeSlotsContainer.innerHTML = '<p class="info-message">Primero selecciona un servicio</p>';
            return;
        }
        
        try {
            // Obtener horarios ya reservados para esta fecha y servicio
            const response = await fetch(`/reservas/horarios-reservados/?servicio_id=${servicioId}&fecha=${fecha}`);
                
            // Verificar si la respuesta es JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('La respuesta no es JSON');
            }
            
            const data = await response.json();
            
            if (data.status === 'error') {
                throw new Error(data.message);
            }
            
            // Normalizar los horarios reservados
            const horariosReservados = (data.horarios_reservados || []).map(normalizarHorario);
            console.log('Horarios reservados:', horariosReservados); // Para debugging
            
            // Resto del código para procesar disponibilidades...
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
                turnos.forEach(t => {
                    const [hora, minuto] = t.hora.split(':').map(Number);
                    let finMinuto = minuto + disp.intervalo;
                    let finHora = hora;

                    if (finMinuto >= 60) {
                        finHora += Math.floor(finMinuto / 60);
                        finMinuto = finMinuto % 60;
                    }

                    const horaInicioFormateada = `${String(hora).padStart(2, '0')}:${String(minuto).padStart(2, '0')}`;
                    const horaFinFormateada = `${String(finHora).padStart(2, '0')}:${String(finMinuto).padStart(2, '0')}`;
                    const horarioCompleto = normalizarHorario(`${horaInicioFormateada} - ${horaFinFormateada}`);
                    
                    console.log('Verificando horario:', horarioCompleto); // Para debugging
                    
                    // Verificar si este horario ya está reservado
                    const estaReservado = horariosReservados.some(hr => hr === horarioCompleto);
                    
                    if (!estaReservado) {
                        todosTurnos.push({
                            hora_inicio: horaInicioFormateada,
                            hora_fin: horaFinFormateada,
                            horario_completo: horarioCompleto,
                            ubicacion: disp.ubicacion,
                            disponibilidad_id: disp.id
                        });
                    } else {
                        console.log('Horario reservado encontrado:', horarioCompleto); // Para debugging
                    }
                });
            });
            
            console.log('Turnos disponibles:', todosTurnos.length); // Para debugging
            
            if (todosTurnos.length === 0) {
                timeSlotsContainer.innerHTML = '<p class="info-message">No hay horarios disponibles para esta fecha</p>';
                return;
            }
            
            timeSlotsContainer.innerHTML = todosTurnos.map(turno => `
                <div class="time-slot">
                    <input type="radio" 
                        name="turno_seleccionado" 
                        id="turno-${turno.disponibilidad_id}-${turno.hora_inicio.replace(':', '')}" 
                        value="${turno.disponibilidad_id}"
                        data-hora-inicio="${turno.hora_inicio}"
                        data-hora-fin="${turno.hora_fin}">
                    <label for="turno-${turno.disponibilidad_id}-${turno.hora_inicio.replace(':', '')}">
                        ${turno.horario_completo} (${turno.ubicacion})
                    </label>
                </div>
            `).join('');

            document.querySelectorAll('.time-slot input').forEach(radio => {
                radio.addEventListener('change', function() {
                    disponibilidadIdInput.value = this.value;
                    horarioSeleccionadoInput.value = `${this.dataset.horaInicio} - ${this.dataset.horaFin}`;
                });
            });
            
        } catch (error) {
            console.error('Error al obtener horarios reservados:', error);
            timeSlotsContainer.innerHTML = '<p class="error-message">Error al cargar horarios. Por favor, intenta nuevamente.</p>';
        }
    }

    // Función para normalizar formatos de horario (eliminar espacios extras, asegurar formato)
    function normalizarHorario(horario) {
        if (!horario) return '';
        
        // Eliminar espacios extras y normalizar
        let normalized = horario
            .replace(/\s+/g, ' ') // Reemplazar múltiples espacios por uno solo
            .trim(); // Eliminar espacios al inicio y final
        
        // Asegurar formato HH:MM - HH:MM
        const partes = normalized.split(' - ');
        if (partes.length === 2) {
            const [inicio, fin] = partes;
            
            // Normalizar cada parte del tiempo
            const normalizarTiempo = (tiempo) => {
                const [h, m] = tiempo.split(':');
                return `${String(h).padStart(2, '0')}:${String(m || '00').padStart(2, '0')}`;
            };
            
            normalized = `${normalizarTiempo(inicio)} - ${normalizarTiempo(fin)}`;
        }
        
        return normalized;
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
            
            // Calcular el próximo intervalo CORRECTAMENTE
            minActual += intervalo;
            
            // Ajustar horas y minutos si los minutos exceden 59
            if (minActual >= 60) {
                horaActual += Math.floor(minActual / 60);
                minActual = minActual % 60;
            }
            
            // Verificar si hemos superado el horario de fin
            if (horaActual > horaFin || (horaActual === horaFin && minActual >= minFin)) {
                break;
            }
        }
        
        return turnos;
    }

    function formatearFechaBonita(fechaStr) {
        // Crear la fecha en la zona horaria local, no UTC
        const [year, month, day] = fechaStr.split('-');
        const fecha = new Date(year, month - 1, day); // Meses son 0-indexados en JS
        
        const opciones = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            timeZone: 'America/Santiago' // Especifica la zona horaria de Chile
        };
        
        return fecha.toLocaleDateString('es-ES', opciones);
    }
});