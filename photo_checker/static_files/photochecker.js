const deletePhoto = (event) => {
    const fileName = event.target.closest(".row").id;
    const result = confirm("Delete file: " + fileName + "\n Are you sure?");
    if (result) {
        window.location.href = '/delete/' + fileName;
    } else {
        window.location.href = '/';
    }
};


const postPhoto = (event) => {
    const fileName = event.target.closest(".row").id;
    const result = confirm("Post file: " + fileName + "\n Are you OK?");
    if (result) {
        window.location.href = '/post/' + fileName;
    } else {
        window.location.href = '/';
    }
};
