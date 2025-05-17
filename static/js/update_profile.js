document.addEventListener("DOMContentLoaded", function () {
    const avatarInput = document.querySelector("#id_avatar");
    const avatarPreview = document.querySelector("#avatar-preview");
    const fileNameSpan = document.querySelector("#file-name");
    const fileSizeSpan = document.querySelector("#file-size");
    const fileTypeSpan = document.querySelector("#file-type");

    avatarInput.addEventListener("change", function () {
        const file = avatarInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                avatarPreview.src = e.target.result;
            };
            reader.readAsDataURL(file);

            fileNameSpan.textContent = file.name;
            fileSizeSpan.textContent = (file.size / 1024).toFixed(2) + " KB";
            fileTypeSpan.textContent = file.type || "Неизвестный";
        } else {
            avatarPreview.src = '/media/profile_pics/default_avatar.jpg';
            fileNameSpan.textContent = "Нет файла";
            fileSizeSpan.textContent = "-";
            fileTypeSpan.textContent = "-";
        }
    });
});
