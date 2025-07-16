// Actualizar hora y fecha en tiempo real
function updateDateTime() {
  const now = new Date();

  // Formatear hora
  const timeOptions = {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  };
  const formattedTime = now.toLocaleTimeString("es-ES", timeOptions);

  // Formatear fecha
  const dateOptions = {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  };
  const formattedDate = now.toLocaleDateString("es-ES", dateOptions);

  // Capitalizar primera letra
  const capitalizedDate =
    formattedDate.charAt(0).toUpperCase() + formattedDate.slice(1);

  document.getElementById("live-time").textContent = formattedTime;
  document.getElementById("live-date").textContent = capitalizedDate;
}

// Actualizar inmediatamente y luego cada segundo
updateDateTime();
setInterval(updateDateTime, 1000);

// Efecto de sonido al interactuar con las tarjetas
document.querySelectorAll(".card-3d").forEach((card) => {
  card.addEventListener("click", function () {
    // Crear efecto de onda
    const ripple = document.createElement("div");
    ripple.style.position = "absolute";
    ripple.style.width = "10px";
    ripple.style.height = "10px";
    ripple.style.backgroundColor = "rgba(76, 175, 80, 0.5)";
    ripple.style.borderRadius = "50%";
    ripple.style.pointerEvents = "none";
    ripple.style.transform = "translate(-50%, -50%)";
    ripple.style.animation = "ripple 1s ease-out forwards";

    // Posicionar donde se hizo clic
    const rect = this.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;

    this.appendChild(ripple);

    // Eliminar después de la animación
    setTimeout(() => {
      ripple.remove();
    }, 1000);
  });
});


// Funciones para controlar el popup
    function openLoginModal() {
      document.getElementById('loginModal').style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }
    
    function closeModal() {
      document.getElementById('loginModal').style.display = 'none';
      document.body.style.overflow = 'auto';
    }
    
    // Cerrar al hacer clic fuera del popup
    window.onclick = function(event) {
      if (event.target.className === 'modal-login') {
        closeModal();
      }
    }
    
    // Cerrar con ESC
    document.onkeydown = function(evt) {
      evt = evt || window.event;
      if (evt.key === 'Escape') {
        closeModal();
      }
    };
