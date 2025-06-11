 document.getElementById('servicio').addEventListener('change', async function () {
            const servicio = this.value;
            const selectDias = document.getElementById('dia');

            selectDias.innerHTML = '<option value="">Cargando días...</option>';
            selectDias.disabled = true;

            if (!servicio) {
                selectDias.innerHTML = '<option value="">-- Seleccione un servicio --</option>';
                return;
            }

            try {
                // ¡Asegúrate de incluir el prefijo /reservas/!
                const response = await fetch(`/reservas/get_dias_por_servicio/?servicio=${encodeURIComponent(servicio)}`);

                // Verifica si la respuesta es JSON
                if (!response.headers.get('content-type')?.includes('application/json')) {
                    const errorText = await response.text();
                    throw new Error(`Respuesta no JSON: ${errorText.substring(0, 100)}...`);
                }

                const data = await response.json();

                if (!response.ok) {  // Maneja errores HTTP 4xx/5xx
                    throw new Error(data.error || `Error ${response.status}`);
                }

                // Actualiza el select de días
                if (data.dias?.length > 0) {
                    selectDias.innerHTML = data.dias.map(dia =>
                        `<option value="${dia.value}">${dia.text}</option>`
                    ).join('');
                    selectDias.disabled = false;
                } else {
                    selectDias.innerHTML = '<option value="">No hay días disponibles</option>';
                }
            } catch (error) {
                selectDias.innerHTML = '<option value="">Error al cargar</option>';
                console.error("Error en fetch:", error);
                alert("Error al cargar días. Detalles en consola.");
            }
        });