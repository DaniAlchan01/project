document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('unauthStartBtn');
    const modal = document.getElementById('authModal');
    const closeModal = document.getElementById('closeModal');

    if (startBtn && modal && closeModal) {
        startBtn.addEventListener('click', () => {
            modal.style.display = 'block';
        });

        closeModal.addEventListener('click', () => {
            modal.style.display = 'none';
        });

        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
});
