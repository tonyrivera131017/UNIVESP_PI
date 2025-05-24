document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('toggle-high-contrast');
    const body = document.body;

    // Função para aplicar o estado de alto contraste
    function applyHighContrast(isHighContrastEnabled) {
        if (isHighContrastEnabled) {
            body.classList.add('high-contrast');
            if (toggleButton) toggleButton.textContent = 'Desativar Alto Contraste';
        } else {
            body.classList.remove('high-contrast');
            if (toggleButton) toggleButton.textContent = 'Ativar Alto Contraste';
        }
    }

    // Verifica se há uma preferência salva no localStorage
    let highContrastEnabled = localStorage.getItem('highContrastEnabled') === 'true';
    applyHighContrast(highContrastEnabled);

    // Adiciona o evento de clique ao botão
    if (toggleButton) {
        toggleButton.addEventListener('click', function () {
            highContrastEnabled = !highContrastEnabled; // Alterna o estado
            localStorage.setItem('highContrastEnabled', highContrastEnabled);
            applyHighContrast(highContrastEnabled);
        });
    }
});
