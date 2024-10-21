$(document).ready(function() {
    // Mostrar el modal de cookies si el usuario no ha aceptado ni rechazado
    if (!localStorage.getItem('cookiesAccepted') && !localStorage.getItem('cookiesRejected')) {
        $('#cookiesModal').modal('show');
    }

    // Función para manejar la aceptación o rechazo de cookies
    function handleCookieConsent(action) {
        localStorage.setItem(action, 'true');
        $('#cookiesModal').modal('hide');
        console.log(`Cookies ${action === 'cookiesAccepted' ? 'accepted' : 'rejected'}.`);
    }

    $('#cookiesModal .btn-primary').click(function() {
        handleCookieConsent('cookiesAccepted');
    });

    $('#cookiesModal .btn-secondary').click(function() {
        handleCookieConsent('cookiesRejected');
    });

    $('#cookiesPolicyLink').click(function(event) {
        event.preventDefault();
        $('#cookiesModal').modal('show');
    });

    $('#privacyPolicyLink, #privacyPolicyModal').click(function(event) {
        event.preventDefault(); 
        $('#privacyPolicyModal').modal('show'); 
    });
});
