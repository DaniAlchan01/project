document.addEventListener("DOMContentLoaded", function () {
    const profileAvatar = document.getElementById("profile-avatar");
    const profilePopup = document.getElementById("profile-popup");

    if (profileAvatar && profilePopup) {
        profileAvatar.addEventListener("click", function (event) {
            event.stopPropagation(); // Чтобы клик не закрывал окно

            // Получаем координаты аватарки
            const rect = profileAvatar.getBoundingClientRect();

            // Устанавливаем положение всплывающего окна
            profilePopup.style.top = `${rect.bottom + window.scrollY + 5}px`; // Чуть ниже аватарки
            profilePopup.style.left = `${rect.left + window.scrollX - 20}px`; // Центрируем

            // Переключаем видимость
            profilePopup.classList.toggle("visible");
        });

        // Закрытие при клике вне окна
        document.addEventListener("click", function (event) {
            if (!profilePopup.contains(event.target) && event.target !== profileAvatar) {
                profilePopup.classList.remove("visible");
            }
        });
    }
});
