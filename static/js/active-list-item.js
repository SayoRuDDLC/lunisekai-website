document.querySelectorAll('.anime-list__item').forEach(item => {
    item.addEventListener('click', function () {
        document.querySelectorAll('.anime-list__item').forEach(
            i => i.classList.remove('anime-list__item-active')
        );

        this.classList.add('anime-list__item-active');
    });
});