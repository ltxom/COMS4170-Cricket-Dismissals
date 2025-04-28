$(function () {
    // Populate the total score and max score
    $("#total-score").text(total_score);
    $("#max-score").text(max_score);

    // Populate the feedback
    const $feedbackContainer = $(".feedback-container");
    feedback.forEach((questionFeedback, questionIndex) => {

        questionFeedback.forEach((answer) => {
            const $answerDiv = $("<div></div>").addClass("answer-feedback");

            if (!answer.correct) {
                const $explanation = $("<p></p>").html(answer.explanation);
                $answerDiv.append($explanation);
            }
            $feedbackContainer.append($answerDiv);
        });

        
    });
});