$(function () {
    // Populate the total score and max score
    $("#total-score").text(total_score);
    $("#max-score").text(max_score);

    const $feedbackContainer = $(".feedback-container");
    let hasIncorrectAnswers = false;

    feedback.forEach((questionFeedback, questionIndex) => {
        questionFeedback.forEach((answer) => {
            if (!answer.correct) {
                hasIncorrectAnswers = true;

                const $answerDiv = $("<div></div>").addClass("answer-feedback");

                // Display the descriptor (question)
                const descriptorText = typeof answer.descriptor === 'string' && answer.descriptor.includes("static")
                  ? `<img src="${answer.descriptor}" alt="Descriptor" class="descriptor-gif">`
                  : `<p><strong>Question:</strong> ${answer.descriptor}</p>`;
                $answerDiv.append(descriptorText);

                // Display user's answer
                $answerDiv.append(`<p><strong>Your Answer:</strong> ${answer.user_answer}</p>`);

                // Display correct answer
                $answerDiv.append(`<p><strong>Correct Answer:</strong> ${answer.correct ? "✔️" : answer.correct_answer || "Not Provided"}</p>`);

                // Explanation
                $answerDiv.append(`<p><strong>Explanation:</strong> ${answer.explanation}</p>`);

                $feedbackContainer.append($answerDiv);
            }
        });
    });

    if (!hasIncorrectAnswers) {
        $feedbackContainer.remove();
    }
});
