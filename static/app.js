$("#search-form").submit(function (e) {
    e.preventDefault();
    console.log("ON SUBMIT FORM");
    console.log($("#pettype").val());
});
