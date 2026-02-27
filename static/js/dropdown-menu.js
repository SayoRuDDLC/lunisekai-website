const menu = document.getElementById('header-menu');
const button = document.getElementById('header-menu-btn');

function toggleMenu() {
    menu.style.display = menu.style.display === 'none' ? 'flex' : 'none';
}

if (menu && button) {
    document.addEventListener('click', (event) => {
        const target = event.target;

        if (!menu.contains(target) && !button.contains(target)) {
            menu.style.display = 'none'
        }
    });
}