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
            <h1>{{ status }}</h1>

            <div class="row">
                <div class="col border bg-light p-1 my-2" style="height: 200px;">
                    <div class="row" id="{{ filename }}">
                        <div class="col-4 d-flex align-items-center">
                            <a href="/images/{{ filename }}">
                                <img src="/images/thumbs/{{ filename }}" class="img-thumbnail" />
                            </a>
                        </div>
                        <div class="col-8">
                            <h5>{{ filename }}</h5>
                            <p>
                                {{ filename }} has been {{ status }}.
                            </p>
                            <p>
                                <button type="button" class="btn btn-outline-danger delete-button">Delete</button>
                                or
                                <button type="button" class="btn btn-outline-secondary back-button">Back to Home</button>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            window.addEventListener('DOMContentLoaded', function() {
                const deleteButtons = document.getElementsByClassName("delete-button");
                deleteButtons[0].addEventListener("click", deletePhoto, false);
                const backButtons = document.getElementsByClassName("back-button");
                backButtons[0].addEventListener("click", (event) => {
                    window.location.href = '/';
                }, false);
            });
        </script>
    </body>
</html>
