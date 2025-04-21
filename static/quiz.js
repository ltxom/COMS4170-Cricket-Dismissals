function addDismissal(dismissal) {
    let row = $("<div class='row'></div>");
    let dismissalElement = $("<div class='dismissal'></div>").text(dismissal);

    // Make the dismissal draggable
    dismissalElement.draggable({
        revert: "invalid", // Revert if not dropped in a valid droppable area
        helper: "clone",   // Create a clone of the element while dragging
        cursor: "move",    // Change the cursor to indicate dragging
        zIndex: 1000       // Ensure the dragged element stays in the foreground
    });

    row.append(dismissalElement);
    $("#quiz-dismissals").append(row);
}

function addDescriptor(descriptor, type) {
    let row = $("<div class='row'></div>");

    let col1 = $("<div class='col-6 droppable-area'></div>");
    let col2 = $("<div class='col-6'></div>");
    let descriptor_class = ''
    if (type == 'images') {
        descriptor_class = $("<img class='descriptor-gif'>").attr("src", descriptor).attr("alt", "Descriptor GIF");
    } else {
        descriptor_class = $("<div class='descriptor'></div>").text(descriptor);
    }

    col2.append(descriptor_class);

    // Make col1 a droppable area
    col1.droppable({
        accept: ".dismissal", // Accept only elements with the 'dismissal' class
        drop: function(event, ui) {
            let droppedElement = ui.draggable.clone(); // Clone the dragged element
            $(this).empty(); // Clear the droppable area
            $(this).append(droppedElement); // Append the dragged element
        }
    });

    row.append(col1);
    row.append(col2);
    $("#quiz-descriptors").append(row);
}

function populate_quiz_page(content) {
    content.dismissals.forEach(function(dismissal, i) {
        addDismissal(dismissal);
    });

    content.descriptors.forEach(function(descriptor, i) {
        addDescriptor(descriptor, content.descriptor_type);
    });
}

$(function() {
    console.log(content);
    $("#quiz-dismissals").empty();
    $("#quiz-descriptors").empty();

    populate_quiz_page(content);
});