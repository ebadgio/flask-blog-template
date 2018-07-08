baseUrl = "http://localhost:5000/"

nextPage = 2;

function loadMore() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(JSON.parse(xhttp.responseText));

            posts = JSON.parse(xhttp.responseText);

            posts.forEach(function(post) {

                var child = document.createElement('div');

                child.innerHTML = `<article class="media content-section shadow">
                      <div class="media-body">
                        <div class="article-info">
                          <a class="mr-2" href="${ '/u/' + post.author}">u/${ post.author }</a>
                          <small class="text-muted">${ post.createdAt }</small>
                        </div>
                        <h5><span class="article-title">${ post.title }</a></h5>
                        <p class="article-content">${ post.content }</p>
                      </div>
                  </article>`;

                document.getElementById("feed-wrapper").appendChild(child);
            });
        }
    };

    // page = localStorage.getItem('page') ? parseInt(localStorage.getItem('page')) : 2;

    xhttp.open("POST", baseUrl + 'next/posts/' + nextPage, true);

    xhttp.send();

    nextPage++;

    // localStorage.setItem('page', page + 1);
}
