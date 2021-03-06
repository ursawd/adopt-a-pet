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
    // save the note to the db
    saveNote(note, apiid);
    // show confirmation on the pet card
    displayNotice(e.target);
});
//###############################################################
// Saves users note about pet to db
async function saveNote(note, apiid) {
    // post to /postnote backend route to save note in db
    const response = await axios
        .post("/postnote", { note, apiid })
        .catch((error) => {
            console.log("error", error);
        });

    // response.status should be 204 no content
    return;
}
//###############################################################
// Displays message box at location specified by div with id of "message-wrap"
// modified logic from:
// https://code-boxx.com/display-message-javascript-without-alert/
// 4 Ways to Display Message in Javascript Without Alert
// By W.S. Toh / Tips & Tutorials - HTML & CSS, Tips & Tutorials - Javascript / December 24, 2019
var mbarM = {
    add: function (message, el) {
        //added e.target from Save Note listener as el
        var bar = document.createElement("div");
        bar.classList.add("message-bar");
        bar.innerHTML = message;
        bar.addEventListener("click", mbarM.close);
        // modified routine to get preceeding div with id of "message-wrap",
        // needed because div with that id in every pet card so unable to directly access
        $(el.parentElement).prev().get(0).appendChild(bar);
        // original -- document.getElementById("message-wrap").appendChild(bar);
    },
    close: function () {
        this.remove();
    },
};
//###############################################################
// Displays confirmation that user notes about pet have been saved
function displayNotice(el) {
    //passes through el
    const message =
        "<em class='mr-5'>Note Added</em><button class='ml-5 btn btn-info btn-sm btn-sm' type='button'>Close</button>";
    // executes add method of mbarM object which causes notification to be shown to user
    mbarM.add(message, el);
    return;
}
