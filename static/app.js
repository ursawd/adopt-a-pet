//###############################################################
// Listens for user to click on Save Note link on each pet card
//
$(".note-link").click(function (e) {
    // get the a tag element clicked
    let el = e.target;
    // get the id data attribute from the element
    let apiid = el.dataset.id;
    // use the retrieved id to get the value of the text area
    note = $(`#${apiid}`).val();
    console.log(note);
});
//###############################################################
