document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('editExpenseModal');
  const form = document.getElementById('editExpenseForm');
  const photoPreview = document.getElementById('edit_photo_preview');
  const closeBtn = modal.querySelector('.close');
  const cancelBtn = modal.querySelector('.btn-cancel');

  window.openEditExpenseModal = function(id, categoryId, amount, comment, photoUrl) {
    // Показать модалку
    modal.classList.add('show');

    // Обновить action формы: заменить окончание "0/" на "{id}/"
    form.action = form.action.replace(/0\/$/, `${id}/`);

    // Заполнить поля
    document.getElementById('edit_category').value = categoryId;
    document.getElementById('edit_amount').value = amount;
    document.getElementById('edit_comment').value = comment;

    // Превью фото
    if (photoUrl) {
      photoPreview.src = photoUrl;
      photoPreview.classList.remove('hidden');
      photoPreview.style.display = 'block';
    } else {
      photoPreview.src = '';
      photoPreview.classList.add('hidden');
      photoPreview.style.display = 'none';
    }
  };

  window.closeEditExpenseModal = function() {
    // Скрыть модалку
    modal.classList.remove('show');

    // Сбросить форму
    form.reset();

    // Вернуть action к изначальному виду с "0/"
    form.action = form.action.replace(/\/\d+\/$/, '0/');

    // Скрыть фото-превью
    photoPreview.src = '';
    photoPreview.classList.add('hidden');
    photoPreview.style.display = 'none';
  };

  // Закрытие по кнопкам
  closeBtn.addEventListener('click', closeEditExpenseModal);
  cancelBtn.addEventListener('click', closeEditExpenseModal);

  // Закрытие по клику вне модалки
  window.addEventListener('click', function(e) {
    if (e.target === modal) closeEditExpenseModal();
  });
});