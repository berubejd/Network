// Set up partial for getPostsBase
let username = document.querySelector("#posts").dataset.username;
const getPosts = (page) => getPostsBase(page = page, username = username);

document.addEventListener('DOMContentLoaded', function () {
    // Add event to follow button
    let csrf = document.querySelector('#posts').dataset.csrf;
    let controlsDiv = document.querySelector('#user-controls');

    if (controlsDiv) {
        controlsDiv.addEventListener('click', () => toggleFollow(csrf, username));
    }

    // Load controls and stats
    getFollowStats(username);

    // Load profile posts
    getPosts();
});

function getFollowStats(username) {
    // Post to follow API
    fetch(`/follow/${username}`)
        .then((response) => response.json())
        .then((result) => {
            // Success, update controls and stats
            let controlDiv = document.querySelector('#user-controls');

            if (controlDiv) {
                controls = result.following ? '<i class="bi bi-star-fill"></i> Following!' : '<i class="bi bi-star"></i> Follow?';
                controlDiv.innerHTML = controls;
            }

            document.querySelector('#user-followers').textContent = `${result.countFollowers} Followers`;
            document.querySelector('#user-following').textContent = `${result.countFollowing} Following`;
        })
        .catch((error) => {
            console.error(`getFollowStats:  Error: ${error}`);
        });
}

function toggleFollow(csrf, username) {
    // Post to follow API
    fetch(`/follow/${username}`, {
        method: 'POST',
        headers: { "X-CSRFToken": csrf },
        credentials: 'same-origin',
    })
        .then((response) => response.json())
        .then((result) => {
            // Success, update follow details
            getFollowStats(username);
        })
        .catch((error) => {
            console.error(`toggleFollow:  Error: ${error}`);
        });
}