document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.section-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
    });

    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02)';
        });
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    const forms = document.querySelectorAll('form[action*="insert"]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('.btn-insertar');
            const spinner = button.querySelector('.loading-spinner');
            if (spinner) {
                spinner.style.display = 'inline-block';
                button.disabled = true;
            }
        });
    });
    function formatCurrency(amount) {
        return new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }
    
    function updateStats() {
        const sucursales = document.querySelectorAll('#sucursales tbody tr').length;
        const prestamos = document.querySelectorAll('#prestamos tbody tr').length;
        
        document.getElementById('totalSucursales').textContent = sucursales;
        document.getElementById('totalPrestamos').textContent = prestamos;
    }

    function showSuccessMessage(type) {
        const message = document.getElementById(type + 'Success');
        if (message) {
            message.style.display = 'block';
            setTimeout(() => {
                message.style.display = 'none';
            }, 3000);
        }
    }
});