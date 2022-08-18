<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>INDEX - Photos</title>
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <script src="/statics/photochecker.js"></script>
    </head>
    <body>
        <div class="container">
            <h1>INDEX - Photos</h1>

            <div class="row row-cols-2">
            % for photo in photo_list:
                <div class="col border bg-light p-1 my-2" style="height: 200px;">
                    <div class="row" id="{{ photo.name }}">
                        <div class="col-4 d-flex align-items-center">
                            <a href="/images/{{ photo.name }}">
                                <img src="/images/thumbs/{{ photo.name }}" class="img-thumbnail" />
                            </a>
                        </div>
                        <div class="col-8">
                            <h5>{{ photo.name }}</h5>
                            <p>
                                {{ photo_info[photo.name]['media_url'] }}
                                <span><a href="{{ photo_info[photo.name]['expanded_url'] }}" target="_blank">(link)</a></span>
                            </p>
                            <p>
                                <button type="button" class="btn btn-outline-primary post-button">Post</button>
                                <button type="button" class="btn btn-outline-danger delete-button">Delete</button>
                            </p>
                        </div>
                    </div>
                </div>
            % end
            </div>
        </div>

        <script>
            window.addEventListener('DOMContentLoaded', function() {
                const deleteButtons = document.getElementsByClassName("delete-button");
                for (let i = 0; i < deleteButtons.length; i++) {
                    deleteButtons[i].addEventListener("click", deletePhoto, false);
                }
                const postButtons = document.getElementsByClassName("post-button");
                for (let i = 0; i < postButtons.length; i++) {
                    postButtons[i].addEventListener("click", postPhoto, false);
                }
            });
        </script>
    </body>
</html>
