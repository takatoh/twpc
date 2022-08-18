const deletePhoto = (event) => {
    const fileName = event.target.closest(".row").id;
    alert("Delete file: " + fileName + "\n Are you sure?");
    window.location.href = '/delete/' + fileName;
};


const postPhoto = (event) => {
    const fileName = event.target.closest(".row").id;
    alert("Post file: " + fileName + " ?");
};
