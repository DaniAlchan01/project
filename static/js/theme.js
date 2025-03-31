// Получаем переключатель темы
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;
const header = document.querySelector('header'); // Получаем хеддер

// Проверяем сохранённую тему в localStorage
const savedTheme = localStorage.getItem('theme') || 'light';

// Функция для применения темы
function applyTheme(theme) {
    if (theme === 'dark') {
        body.classList.add('dark-theme');
        header.classList.add('dark-header'); // Добавляем класс для хедера
        themeToggle.checked = true;
    } else {
        body.classList.remove('dark-theme');
        header.classList.remove('dark-header'); // Убираем класс у хедера
        themeToggle.checked = false;
    }
}

// Устанавливаем сохранённую тему при загрузке страницы
applyTheme(savedTheme);

// Обработчик изменения темы
themeToggle.addEventListener('change', function () {
    const newTheme = this.checked ? 'dark' : 'light';
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
});
