function openEditExpenseModal(id, categoryId, amount, comment, photoUrl) {
    const modal = document.getElementById('editExpenseModal');
    modal.classList.add('show');

    const form = document.getElementById('editExpenseForm');
    const currentAction = form.getAttribute('action') || '';
    const newAction = `/edit-expense/${id}/`;

    if (!currentAction.includes(`/edit-expense/${id}/`)) {
        form.setAttribute('action', newAction);
    }

    document.getElementById('edit_category').value = categoryId;
    document.getElementById('edit_amount').value = amount;
    document.getElementById('edit_comment').value = comment;

    const photoPreview = document.getElementById('edit_photo_preview');
    if (photoUrl) {
        photoPreview.src = photoUrl;
        photoPreview.style.display = 'block';
    } else {
        photoPreview.style.display = 'none';
        photoPreview.src = '';
    }
}

function closeEditExpenseModal() {
    const modal = document.getElementById('editExpenseModal');
    modal.classList.remove('show');

    const form = document.getElementById('editExpenseForm');
    form.reset();
    form.setAttribute('action', '/edit-expense/0/');

    const photoPreview = document.getElementById('edit_photo_preview');
    photoPreview.classList.add('hidden');
    photoPreview.src = '';
}
