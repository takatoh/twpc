<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>INDEX - Photos</title>
  </head>
  <body>
    <h1>INDEX - Photos</h1>

    <div>
        <ul>
            % for photo in photo_list:
            <li>
                <figure>
                    <a href="/images/{{ photo.name }}">
                        <img src="/images/thumbs/{{ photo.name }}" />
                    </a>
                    <caption>{{ photo.name }}</caption>
                </figure>
            </li>
            % end
        </ul>
    </div>
  </body>
</html>
