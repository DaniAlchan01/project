document.addEventListener("DOMContentLoaded", function () {
  const showButton = document.getElementById("showCategoryFormButton");
  const categoryForm = document.getElementById("categoryForm");
  const editCategoryForm = document.getElementById("editCategoryForm");

  // Показ/скрытие формы добавления категории
  if (showButton && categoryForm) {
    showButton.addEventListener("click", function () {
      categoryForm.classList.toggle("hidden");
      editCategoryForm.classList.add("hidden");
    });
  }

  // Логика редактирования категории
  const editUrlBase = document.querySelector(".expense-container").getAttribute("data-edit-url");

  window.showEditForm = function (categoryId) {
    const categoryItem = document.querySelector(`[data-category-id="${categoryId}"]`);
    if (categoryItem) {
      const name = categoryItem.getAttribute("data-name");
      const color = categoryItem.getAttribute("data-color");

      document.getElementById("edit_name").value = name;
      document.getElementById("edit_color").value = color;

      const form = document.getElementById("categoryEditForm");
      form.action = editUrlBase.replace('0', categoryId); // Исправленный URL

      editCategoryForm.classList.remove("hidden");
      categoryForm.classList.add("hidden");
    }
  };
});
