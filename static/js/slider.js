const slider = document.querySelector(".player__nums-slider");
const btnPrev = document.querySelector(".player__btn-prev");
const btnNext = document.querySelector(".player__btn-next");
const btnActive = document.querySelector('.btn-active')

const scrollAmount = 400;

btnNext.addEventListener("click", () => {
    slider.scrollBy({
        left: scrollAmount,
        behavior: "smooth"
    });
});

btnPrev.addEventListener("click", () => {
    slider.scrollBy({
        left: -scrollAmount,
        behavior: "smooth"
    });
});

if (btnActive) {
    btnActive.scrollIntoView({
        behavior: "smooth",
        inline: 'center'
    })
}