document.addEventListener("DOMContentLoaded", function () {
    const avatarInput = document.querySelector("#id_avatar");
    const avatarPreview = document.querySelector("#avatar-preview");
    const fileInfo = document.querySelector("#file-info");

    avatarInput.addEventListener("change", function () {
        const file = avatarInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                avatarPreview.src = e.target.result;
            };
            reader.readAsDataURL(file);

            // Добавление информации о файле
            const fileSize = (file.size / 1024).toFixed(2); // Размер в КБ
            fileInfo.innerHTML = `
                <p><strong>Имя:</strong> ${file.name}</p>
                <p><strong>Размер:</strong> ${fileSize} KB</p>
                <p><strong>Формат:</strong> ${file.type || "Неизвестный"}</p>
            `;
        } else {
            fileInfo.innerHTML = "";
        }
    });
});
