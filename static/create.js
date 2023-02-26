const titleInput = document.getElementById('title');
const bodyInput = document.getElementById('body');
const shareBtn = document.getElementById('share-button');

titleInput.addEventListener('input', toggleShareButton);
bodyInput.addEventListener('input', toggleShareButton);

function toggleShareButton() {
  if (!titleInput.value || !bodyInput.value) {
    shareBtn.disabled = true;
  } else {
    shareBtn.disabled = false;
  }
}