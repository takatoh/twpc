const deletePhoto = (event) => {
    const fileName = event.target.closest(".row").id;
    alert("Delete file: " + fileName + " ?");
};


const postPhoto = (event) => {
    const fileName = event.target.closest(".row").id;
    alert("Post file: " + fileName + " ?");
};
