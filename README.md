# Network
## CS50w Project 4 - Network

This is a small project build for [Harvard's CS50 Web Programming course](https://cs50.harvard.edu/web/2020/) hosted by [edX](https://www.edx.org/).  The requirement was to:

>Design a Twitter-like social network website for making posts and following users.

This was to be done primarily using [Django](https://www.djangoproject.com/), [Bootstrap](https://getbootstrap.com/), and JavaScript.

## Screenshots

### All Posts and New Post Creation

The landing page will present users, authenticated or not, with the 10 most recent posts made to the site.  Additional posts can be viewed via provided pagination.  Logged in users can also create new public posts here.

![Index](Images/Index.png?raw=true)

### Editable Posts

Anywhere that displays a logged in user's posts will allow in-place editing.  Edited posts are provided with an indication that allows other users visibility that a post has changed since it was originally created.

![Index](Images/Edit.png?raw=true)

### Profile

Details about a user can be found on their profile page.  This includes their current followers, how many other users they follow, as well as their posts.  If the profile page is for someone other than the logged in user, they are also able to follow them from this view.

![Listing Page](Images/Profile.png?raw=true)

### Followed User's Posts

A view is provided that will list the most current posts for all users followed by the logged in user.

![Categories](Images/Following.png?raw=true)


## Potential Improvements

While a complete project, there were some "relatively simple to implement" improvements that would also provide more of the features expected by a social network:

- Tags and Tag Search - Supporting and indexing tags to allow for user's to search for specific topics would be easy enough to implement and a handy feature for users.
- Popular posts - Surfacing posts with a lot of activity may improve engagement.
- Post Replies - Implementing the ability to reply to a post would allow conversations on topics to form.
- Image support

## Additional Notes

The users provided in the data loader and in the photos above were created using [Random User Generator](https://randomuser.me/).  Posts created for those users were created through a conversation with [ChatGPT](https://chat.openai.com/).