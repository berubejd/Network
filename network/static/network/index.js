// Set up partial for getPostsBase
var getPosts = (page) => getPostsBase(page = page);

document.addEventListener('DOMContentLoaded', function () {
    // Post new message
    let postForm = document.querySelector('#post-form');

    if (postForm) {
        postForm.addEventListener('submit', postMessage);

        // Ensure post form is cleared
        clearPostForm();
    }

    getPosts();
});

function clearPostForm() {
    document.querySelector('#post-body').value = "";
}

function postMessage(event) {
    let csrf = document.querySelector('#post-form > input[name="csrfmiddlewaretoken"]').getAttribute('value');
    let post = document.querySelector('#post-body').value;

    // Post to post API
    fetch('/post', {
        method: 'POST',
        body: JSON.stringify({
            post_content: post
        }),
        headers: { "X-CSRFToken": csrf },
        credentials: 'same-origin',
    })
        .then((response) => response.json())
        .then((result) => {
            // Success, load clear form and load posts
            clearPostForm();
            getPosts();
        })
        .catch((error) => {
            console.error(`postMessage:  Error: ${error}`);
        });

    event.preventDefault();
}
