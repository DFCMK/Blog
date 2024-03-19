function changeTitleColor() {
    const postDetailTitles = document.getElementsByClassName('post-title');

    for (let i = 0; i < postDetailTitles.length; i++) {
        postDetailTitles[i].style.color = 'white';
    }
}

window.addEventListener('load', changeTitleColor);