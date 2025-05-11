function addDismissal(dismissal) {
    let row = $("<div class='row'></div>");

    let numberCol = $("<div class='quiz-number'></div>");
    let dismissalElement = $("<div class='dismissal'></div>").text(dismissal);

    dismissalElement.data("originalParent", "#quiz-dismissals");

    const droppableWidth = $(".droppable-area").first().width();
    dismissalElement.css("width", droppableWidth);

    dismissalElement.draggable({
        revert: "invalid",
        cursor: "move",
        zIndex: 1000
    });

    row.append(numberCol);
    row.append(dismissalElement);
    $("#quiz-dismissals").append(row);
}


function addDescriptor(descriptor, type, index, quizIndex) {
    let row = $("<div class='row'></div>");

    let col1 = $("<div class='col-6 droppable-area'></div>");
    let col2 = $("<div class='col-6'></div>");
    let descriptor_class = '';
    if (type == 'images') {
        descriptor_class = $("<img class='descriptor-gif'>").attr("src", descriptor).attr("alt", "Descriptor GIF");
        $('#instruction').text("Drag the dismissal to it's matching gif")
    } else {
        descriptor_class = $("<div class='descriptor'></div>").text(descriptor);
        $('#instruction').text("Drag the dismissal to it's matching descriptor")
    }
    title_row = $("<div class='title-row fw-bold'></div>");
    title_row.append($("<div class='title'>Descriptor</div>"));
    title_row.text(`Question ${quizIndex + 1}.${index + 1}`)
    col2.append(title_row);
    col2.append(descriptor_class);

    title_row = $("<div class='row title-row'></div>");
    
    descriptor_row = $("<div class='row'></div>");
    //descriptor_row.append(descriptor_class);
    //
    //col2.append(descriptor_row);

    // Make col1 a droppable area
    col1.droppable({
        accept: ".dismissal", // Accept only elements with the 'dismissal' class
        drop: function (event, ui) {
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
            droppedElement.css({
                top: "0",
                left: "0",
                width: currentDroppable.width() // Match the width of the droppable area
            });
        }
    });

    row.append(col1);
    row.append(col2);
    $("#quiz-descriptors").append(row);
}

function populate_quiz_page(content, quizIndex) {
    content.dismissals.forEach(function(dismissal, i) {
        addDismissal(dismissal);
    });

    content.descriptors.forEach(function(descriptor, i) {
        addDescriptor(descriptor, content.descriptor_type, i, quizIndex);
    });
}

let quizInProgress = false; // Initially set to false
let pendingNavigation = null; // Store the link the user wants to navigate to

$(function () {
    console.log(content);
    $("#quiz-dismissals").empty();
    $("#quiz-descriptors").empty();

    populate_quiz_page(content, content.quiz_index);

    // Set quizInProgress to true when the user interacts with the quiz
    $(document).on("dragstart", ".dismissal", function () {
        quizInProgress = true; // User starts interacting with the quiz
    });

    $("#submit-quiz").on("click", function () {
        quizInProgress = true; // User explicitly submits the quiz
    });

    // Show the custom pop-up when a navbar link is clicked
    $("nav a").on("click", function (event) {
        if (quizInProgress) {
            event.preventDefault(); // Prevent immediate navigation
            pendingNavigation = $(this).attr("href"); // Store the link
            $("#exit-popup").removeClass("hidden"); // Show the pop-up
        }
    });

    // Handle the "Leave quiz" button in the pop-up
    $("#confirm-exit").on("click", function () {
        quizInProgress = false; // Allow navigation
        window.location.href = pendingNavigation; // Navigate to the stored link
    });

    // Handle the "Go back to quiz" button in the pop-up
    $("#cancel-exit").on("click", function () {
        $("#exit-popup").addClass("hidden"); // Hide the pop-up
    });

    // Handle the submit button click
    $("#submit-quiz").on("click", function () {
        let allAnswered = true;
        let answers = [];

        // Check if all droppable areas have an answer
        $(".droppable-area").each(function () {
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
            success: function (response) {
                if (response.next_quiz) {
                    // Load the next quiz
                    let content = response.next_quiz;
                    const quizIndex = response.quiz_index;
                    $("#quiz-dismissals").empty();
                    $("#quiz-descriptors").empty();
                    populate_quiz_page(content, quizIndex);
                } else {
                    // Redirect to the results page
                    window.location.href = "/quiz-results";
                }
            },
            error: function () {
                // Show the error pop-up for server errors
                $("#error-message").text("An error occurred while submitting your answers. Please try again.");
                $("#error-popup").removeClass("hidden");
            }
        });
    });

    // Close the error pop-up when the close button is clicked
    $("#close-popup").on("click", function () {
        $("#error-popup").addClass("hidden");
    });
});