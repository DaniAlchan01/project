    // Функция для подтверждения удаления отзыва
    function confirmDelete(reviewId) {
        const modal = document.getElementById('deleteModal');
        const form = document.getElementById('deleteForm');
        if (!modal || !form) return;

        // Обновляем action формы с id отзыва
        form.action = `/reviews/delete/${reviewId}/`;

        // Показываем модальное окно
        modal.style.display = 'block';
    }

    // Закрытие модального окна
    function closeModal() {
        const modal = document.getElementById('deleteModal');
        modal.style.display = 'none';
    }
    
document.addEventListener('DOMContentLoaded', function() {
    const carouselInner = document.querySelector('.carousel-inner');
    const sliderDots = document.querySelector('.slider-dots');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const items = document.querySelectorAll('.demo-item');
    let currentIndex = 0;

    // Создание точек навигации
    items.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.className = 'slider-dot';
        if(index === 0) dot.classList.add('active');
        dot.addEventListener('click', () => goToSlide(index));
        sliderDots.appendChild(dot);
    });

    // Переход к слайду
    function goToSlide(index) {
        currentIndex = Math.max(0, Math.min(index, items.length - 1));
        carouselInner.scrollTo({
            left: items[currentIndex].offsetLeft,
            behavior: 'smooth'
        });
        updateDots();
    }

    // Обновление точек
    function updateDots() {
        document.querySelectorAll('.slider-dot').forEach((dot, i) => {
            dot.classList.toggle('active', i === currentIndex);
        });
    }

    // Обработчики кнопок
    prevBtn.addEventListener('click', () => {
        if(currentIndex > 0) {
            goToSlide(currentIndex - 1);
        }
    });

    nextBtn.addEventListener('click', () => {
        if(currentIndex < items.length - 1) {
            goToSlide(currentIndex + 1);
        }
    });

    // Инициализация
    updateDots();
});