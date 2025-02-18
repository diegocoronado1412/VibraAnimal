// app.js

document.addEventListener('DOMContentLoaded', () => {
    // Obtener todos los botones del índice
    const botones = document.querySelectorAll('.boton-indice');

    // Añadir un evento de clic a cada botón
    botones.forEach(boton => {
        boton.addEventListener('click', (evento) => {
            // Obtener el ID del botón clickeado
            const id = evento.target.id;

            // Realizar una acción basada en el ID del botón
            switch (id) {
                case 'boton-registro-dueno':
                    // Redirigir al formulario de registro de dueño
                    window.location.href = '/registro_dueno';
                    break;
                case 'boton-registro-mascota':
                    // Redirigir al formulario de registro de mascota
                    window.location.href = '/registro_mascota';
                    break;
                // Agregar más casos según sea necesario
                default:
                    console.log('Botón no reconocido');
            }
        });
    });
});
