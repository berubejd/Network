// Set up partial for getPostsBase
let username = document.querySelector("#posts").dataset.username;
const getPosts = (page) => getPostsBase(page = page, username = username, following = true);

document.addEventListener('DOMContentLoaded', function () {
    // Load following posts
    getPosts();
});