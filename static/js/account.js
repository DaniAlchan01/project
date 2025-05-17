document.addEventListener('DOMContentLoaded', function() {
    const deleteAccountBtn = document.getElementById('delete-account-btn');
    const deleteAccountModal = document.getElementById('delete-account-modal');
    const cancelDeleteBtn = document.getElementById('cancel-delete');

    // Открытие модального окна
    deleteAccountBtn.addEventListener('click', function() {
        deleteAccountModal.style.display = 'block'; // Показать модальное окно
    });

    // Закрытие модального окна при нажатии на "Отмена"
    cancelDeleteBtn.addEventListener('click', function() {
        deleteAccountModal.style.display = 'none'; // Скрыть модальное окно
    });

    // Закрытие модального окна при клике за пределами окна
    window.addEventListener('click', function(event) {
        if (event.target == deleteAccountModal) {
            deleteAccountModal.style.display = 'none';
        }
    });
});
