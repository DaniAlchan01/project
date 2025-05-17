function confirmDelete(reviewId) {
    const modal = document.getElementById('deleteModal');
    const form = document.getElementById('deleteForm');
    if (!modal || !form) return;

    form.action = `/reviews/delete/${reviewId}/`;  // динамическое обновление пути
    modal.style.display = 'flex';
}

function closeModal() {
    document.getElementById('deleteModal').style.display = 'none';
}

// Закрытие по клику вне окна
window.onclick = function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
