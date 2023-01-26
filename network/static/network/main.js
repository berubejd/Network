// Helper functions
const clamp = (num, min, max) => Math.min(Math.max(num, min), max);

document.addEventListener('DOMContentLoaded', function () {
    // Set a cookie with the user's time zone
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    document.cookie = "time_zone=" + timezone;
});

function getPostsBase(page = 1, username = null, following = null) {
    // Set resource based on parameteres
    let resource = '/posts';

    if (username) { resource += `/${username}`; }
    if (following) { resource += '/following'; }

    resource += `?page_number=${page}`

    // Get posts from posts API
    fetch(resource)
        .then((response) => response.json())
        .then((result) => {
            let postsDiv = document.querySelector('#posts');
            let csrf = postsDiv.dataset.csrf;
            let newPosts = '';

            // Add returned posts to page
            for (let post of result.posts) {
                heartClass = post.likes ? "bi-heart-fill liked" : "bi-heart";
                editButton = post.editable ? '<span class="edit-button pe-2 float-end"><i class="bi bi-pencil-square pe-1"></i> Edit</span>' : "";
                editedText = post.edited ? ' · <small class="muted">Edited</small>' : "";

                newPosts +=
                    `<div class="post d-flex w-100 pb-1" data-id="${post.id}">
                        <div class="user-image pt-2 pe-2">
                        <a href="/profile/${post.user}"><img src="${post.userphoto}" alt="" width="48" height="48" class="rounded-circle me-2"></a>
                        </div>
                        <div class="user-comment d-flex flex-column w-100">
                            <div class="user-comment-header pb-1"><a href="/profile/${post.user}"><strong>${post.user}</strong></a> · <small class="muted">${post.timestamp}</small>${editedText}</div>
                            <div class="user-comment-content">${post.text}</div>
                            <div class="user-comment-buttons pt-2 muted">
                                <span class="like-button pe-2"><i class="bi ${heartClass} pe-1"></i> ${post.likecount}</span>
                                ${editButton}
                            </div>
                        </div>
                    </div>
                    <hr>`;
            }

            postsDiv.innerHTML = newPosts;

            // Add click events to like and edit buttons
            document.querySelectorAll(".post").forEach((post) => {
                let postId = post.dataset.id;

                let likeButton = post.querySelector(".like-button");
                if (likeButton) {
                    likeButton.addEventListener('click', () => toggleLike(csrf, postId));
                }

                let editButton = post.querySelector(".edit-button");
                if (editButton) {
                    editButton.addEventListener('click', () => editPost(csrf, postId));
                }
            });

            // Add Pagination to page
            if (result.page_max !== 1) {
                let pageDiv = document.querySelector("#pagination ul")
                let newPage = '';

                // Previous button
                newPage += `<li class="page-item ${result.page_current === 1 ? 'disabled' : ''}"><a class="page-link" href="#" data-num="${clamp(result.page_current - 1, 1, result.page_max)}">Previous</a></li>`;

                // Numbered page nav
                let first = clamp(result.page_current - 2, 1, result.page_max);
                let last = clamp(result.page_current + 2, 1, result.page_max);

                for (let i = first; i <= last; i++) {
                    newPage += `<li class="page-item ${result.page_current === i ? 'active' : ''}"><a class="page-link" href="#" data-num="${i}">${i}</a></li>`
                }

                // Next button
                newPage += `<li class="page-item ${result.page_current === result.page_max ? 'disabled' : ''}"><a class="page-link" href="#" data-num="${clamp(result.page_current + 1, 1, result.page_max)}">Next</a></li>`;

                pageDiv.innerHTML = newPage;
            }

            // Add click events to pagination
            document.querySelectorAll(".page-link").forEach((link) => {
                let page = link.dataset.num;

                link.addEventListener('click', () => getPosts(page = page));
            });

            // Scroll page to top after pagination
            document.querySelector('main').scrollTo({
                top: 0,
                left: 0,
                behavior: 'smooth'
            });
        })
        .catch((error) => {
            console.error(`getPosts:  Error: ${error}`);
        });
}

function toggleLike(csrf, postId) {
    // Post to like API
    fetch(`/like/${postId}`, {
        method: 'POST',
        headers: { "X-CSRFToken": csrf },
        credentials: 'same-origin',
    })
        .then((response) => response.json())
        .then((result) => {
            // Success, load posts  (Should just toggle like element?)
            getPosts();
        })
        .catch((error) => {
            console.error(`toggleLike:  Error: ${error}`);
        });
}

function editPost(csrf, postId) {
    // Hide buttons div
    document.querySelector(`.post[data-id="${postId}"] .user-comment-buttons`).style.display = 'none';

    // Find and collect current post content
    let contentDiv = document.querySelector(`.post[data-id="${postId}"] .user-comment-content`);
    let content = contentDiv.textContent;

    // Create new form
    let newForm =
        `<div class="w-100">
            <form id="edit-form" method="post">
                <input type="hidden" name="csrf" value="${csrf}">
                <textarea id="update-body" class="form-control" placeholder="Have something to say?">${content}</textarea>
                <input id="update-button" type="submit" class="btn btn-network rounded-pill float-end my-2 mx-1" value="Update it!">
                <input id="cancel-button" type="button" class="btn btn-secondary rounded-pill float-end my-2" value="Cancel it!">
            </form>
        </div>`;

    // Add form and attach button listener
    contentDiv.innerHTML = newForm;
    contentDiv.querySelector('#edit-form').addEventListener('submit', (event) => updatePost(event, csrf, postId));
    contentDiv.querySelector('#cancel-button').addEventListener('click', () => getPosts());
}

function updatePost(event, csrf, postId) {
    let newContent = document.querySelector(`.post[data-id="${postId}"] #update-body`).value;

    // Post to update API
    fetch(`/post/${postId}`, {
        method: 'PUT',
        body: JSON.stringify({
            post_content: newContent
        }),
        headers: { "X-CSRFToken": csrf },
        credentials: 'same-origin',
    })
        .then((response) => response.json())
        .then((result) => {
            // Success, load posts  (Should just toggle like element?)
            getPosts();
        })
        .catch((error) => {
            console.error(`toggleLike:  Error: ${error}`);
        });

    event.preventDefault();
}