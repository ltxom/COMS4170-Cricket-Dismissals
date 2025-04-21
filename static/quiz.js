function addDismissal(dismissal) {
    let row = $("<div class='row'></div>");
    let dismissalElement = $("<div class='dismissal'></div>").text(dismissal);

    // Store the original parent (quiz-dismissals) for later use
    dismissalElement.data("originalParent", "#quiz-dismissals");

    // Make the dismissal draggable
    dismissalElement.draggable({
        revert: "invalid", // Revert if not dropped in a valid droppable area
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
    let descriptor_class = '';
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
            let droppedElement = ui.draggable; // Use the original dragged element
            let currentDroppable = $(this);

            // Check if there is already a dismissal in the droppable area
            let existingElement = currentDroppable.children(".dismissal");
            if (existingElement.length > 0) {
                // Move the existing element back to its original parent
                let originalParentSelector = existingElement.data("originalParent");
                $(originalParentSelector).append(existingElement);
                existingElement.css({ top: "0", left: "0" }); // Reset position
            }

            // Append the new dragged element to the droppable area
            currentDroppable.empty(); // Clear the droppable area
            currentDroppable.append(droppedElement);
            droppedElement.css({ top: "0", left: "0" }); // Reset position
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

    // Handle the submit button click
    $("#submit-quiz").on("click", function() {
        let allAnswered = true;
        let answers = [];

        // Check if all droppable areas have an answer
        $(".droppable-area").each(function() {
            let droppedElement = $(this).children(".dismissal");
            if (droppedElement.length === 0) {
                allAnswered = false;
            } else {
                answers.push(droppedElement.text().trim());
            }
        });

        if (!allAnswered) {
            // Show the error pop-up
            $("#error-message").text("Please provide an answer for all descriptors before continuing.");
            $("#error-popup").removeClass("hidden");
            return;
        }

        // Send answers to the server
        $.ajax({
            url: "/submit-quiz", // Server endpoint to handle quiz submission
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ answers: answers }),
            success: function(response) {
                if (response.next_quiz) {
                    // Load the next quiz
                    content = response.next_quiz;
                    $("#quiz-dismissals").empty();
                    $("#quiz-descriptors").empty();
                    populate_quiz_page(content);
                } else {
                    // Redirect to the results page
                    window.location.href = "/quiz-results";
                }
            },
            error: function() {
                // Show the error pop-up for server errors
                $("#error-message").text("An error occurred while submitting your answers. Please try again.");
                $("#error-popup").removeClass("hidden");
            }
        });
    });

    // Close the error pop-up when the close button is clicked
    $("#close-popup").on("click", function() {
        $("#error-popup").addClass("hidden");
    });
});