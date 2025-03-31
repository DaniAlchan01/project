document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("photo-upload");
    const previewImage = document.getElementById("preview-img");
    const defaultImage = previewImage.src; // Сохраняем путь к заглушке

    fileInput.addEventListener("change", function () {
        const file = this.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (event) {
                previewImage.src = event.target.result;
            };

            reader.readAsDataURL(file);
        } else {
            // Если файл не выбран, вернуть изображение по умолчанию
            previewImage.src = defaultImage;
        }
    });
});
