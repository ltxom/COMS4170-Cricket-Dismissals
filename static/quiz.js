function addDismissal(dismissal) {
    let row = $("<div class='row'></div>").text(dismissal);
    $("#quiz-dismissals").append(row);
}

function addDescriptor(descriptor) {
    let row = $("<div class='row'></div>");

    let col1 = $("<div class='col-6'></div>");
    let col2 = $("<div class='col-6'></div>");

    let descriptor_class = $("<div class=''></div>").text(descriptor);
    col2.append(descriptor_class);
    row.append(col1);
    row.append(col2);
    $("#quiz-descriptors").append(row);
}

function populate_quiz_page(content) {
    content.dismissals.forEach(function(dismissal, i) {
        addDismissal(dismissal);
    });

    content.descriptors.forEach(function(dismissal, i) {
        addDescriptor(dismissal);
    });
    
}


$(function() {
    console.log(content);
    $("quiz-dismissals").empty();
    $("quiz-descriptors").empty();

    populate_quiz_page(content);

});