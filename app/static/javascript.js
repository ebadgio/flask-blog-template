// Update this based on port or after moving to producion url
baseUrl = "http://localhost:5000/"

nextPage = 2;

/* This function fetches more posts from the server/db when a user clicks 'Load More' */
function loadMore() {

    // Create http request instance
    var xhttp = new XMLHttpRequest();

    // Listen for changes
    xhttp.onreadystatechange = function() {

        // If successful response
        if (this.readyState == 4 && this.status == 200) {

            // For debugging purposes
            console.log(JSON.parse(xhttp.responseText));

            // Parse the json to get the new posts
            posts = JSON.parse(xhttp.responseText);

            posts.forEach(function(post) {

                var child = document.createElement('div');

                // Create the post html
                child.innerHTML = `<article class="media content-section">
                      <div class="media-body">
                        <div class="article-info">
                          <a class="mr-2 user-link" href="${ '/u/' + post.author}">u/${ post.author }</a>
                          <small class="text-muted">${ post.createdAt }</small>
                        </div>
                        <h5><span class="article-title">${ post.title }</a></h5>
                        <p class="article-content">${ post.content }</p>
                      </div>
                  </article>`;

                // Append the post to the feed
                document.getElementById("feed-wrapper").appendChild(child);
            });

            // If there are no more posts left, we want to tell the user
            if (posts.length === 0) {

                // Get rid of load button
                elem = document.getElementById('load-btn');
                elem.style.display = 'none';

                // Create message text to replace button
                var p = document.createElement('p');
                var t = document.createTextNode("No more posts to load...");

                // Add message to below the feed
                p.appendChild(t);
                document.getElementById("load-wrapper").appendChild(p);
            }
        }
    };

    // Create and send an http get request to get the next posts
    xhttp.open("GET", baseUrl + 'next/posts/' + nextPage, true);
    xhttp.send();

    // Increment page
    nextPage++;

}
