$(function () {
    // Populate the total score and max score
    $("#total-score").text(total_score);
    $("#max-score").text(max_score);

    // Populate the feedback
    const $feedbackContainer = $(".feedback-container");
    let hasIncorrectAnswers = false; // Track if there are any incorrect answers

    feedback.forEach((questionFeedback, questionIndex) => {
        questionFeedback.forEach((answer) => {
            if (!answer.correct) {
                hasIncorrectAnswers = true; // Mark that there is at least one incorrect answer

                // Create a feedback box for the incorrect answer
                const $answerDiv = $("<div></div>").addClass("answer-feedback");

                // Add the explanation for the incorrect answer
                const $explanation = $("<p></p>").html(answer.explanation);
                $answerDiv.append($explanation);

                // Append the feedback box to the container
                $feedbackContainer.append($answerDiv);
            }
        });
    });

    // If all answers are correct, hide the feedback section
    if (!hasIncorrectAnswers) {
        $feedbackContainer.remove(); // Remove the feedback container
    }
});