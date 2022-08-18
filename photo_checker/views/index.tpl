<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>INDEX - Photos</title>
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    </head>
    <body>
        <div class="container">
            <h1>INDEX - Photos</h1>

            <div class="row row-cols-2">
            % for photo in photo_list:
                <div class="col border rounded bg-light" style="height: 210px;">
                    <div class="row">
                        <div class="col-4">
                            <a href="/images/{{ photo.name }}">
                                <img src="/images/thumbs/{{ photo.name }}" class="img-thumbnail align-middle" />
                            </a>
                        </div>
                        <div class="col-8" style="height: 200px;">
                            <p>{{ photo.name }}</p>
                            <button type="button" class="btn btn-outline-primary">Post</button>
                            <button type="button" class="btn btn-outline-danger">Delete</button>
                        </div>
                    </div>
                </div>
            % end
            </div>
        </div>
    </body>
</html>
