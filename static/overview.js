const slides = document.getElementById('slides');
const progressBar = document.getElementById('progressBar');
const allSlides = document.querySelectorAll('.slide');
const totalSlides = allSlides.length;
const nextBtn = document.querySelector('.nav-buttons button:nth-child(2)');
const prevBtn = document.querySelector('.nav-buttons button:nth-child(1)');

let currentIndex = 0;
let clickedMap = {}; // Track clicked hotspots for each slide

function updateSlider() {
    const offset = -currentIndex * 100;
    slides.style.transform = `translateX(${offset}%)`;
    progressBar.style.width = `${((currentIndex + 1) / totalSlides) * 100}%`;

    const tooltip = document.getElementById("tooltip");
    if (tooltip) tooltip.style.display = "none";

    const currentSlide = allSlides[currentIndex];
    const currentPlayers = currentSlide.querySelectorAll('.player');

    if (!clickedMap[currentIndex]) {
        clickedMap[currentIndex] = new Set();
    }

    if (currentPlayers.length === 0 || clickedMap[currentIndex].size === currentPlayers.length) {
        nextBtn.disabled = false;
    } else {
        nextBtn.disabled = true;
    }

    // Disable the Previous button on the first slide
    prevBtn.style.visibility = currentIndex === 0 ? "hidden" : "visible";


    // Change the "Next" button text and action on the last slide
    if (currentIndex === totalSlides - 1) {
        nextBtn.textContent = "Dismissals →";
        nextBtn.onclick = function() {
            window.location.href = "/dismissal";
        };
    } else {
        // Default Next button functionality
        nextBtn.textContent = "Next →";
        nextBtn.onclick = nextSlide;
    }
}


function nextSlide() {
    if (currentIndex < totalSlides - 1) {
        currentIndex++;
        updateSlider();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

}

function prevSlide() {
    if (currentIndex > 0) {
        currentIndex--;
        updateSlider();
    }
}

function showLabel(button, position) {
    const tooltip = document.getElementById("tooltip");
    const rect = button.getBoundingClientRect();
    const container = document.querySelector(".field-container").getBoundingClientRect();

    const top = rect.top - container.top;
    const left = rect.left - container.left;

    tooltip.style.top = `${top}px`;
    tooltip.style.left = `${left}px`;
    tooltip.textContent = position;
    tooltip.style.display = "block";

    // Mark the button as clicked to keep the label visible
    button.setAttribute("data-clicked", "true");

    // Change the color of the clicked hotspot to a lighter shade
    button.style.backgroundColor = "#a6c8e5"; // Lighten the red color

    if (!clickedMap[currentIndex]) {
        clickedMap[currentIndex] = new Set();
    }

    clickedMap[currentIndex].add(button);

    const currentSlide = allSlides[currentIndex];
    const currentPlayers = currentSlide.querySelectorAll('.player');

    if (clickedMap[currentIndex].size === currentPlayers.length) {
        nextBtn.disabled = false;
    }
}


updateSlider();

// Attach functions to global scope so HTML can call them
window.nextSlide = nextSlide;
window.prevSlide = prevSlide;
window.showLabel = showLabel;
