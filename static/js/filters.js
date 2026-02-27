const form = document.getElementById('filters-form');
const inputs = form.querySelectorAll('input');

document.body.addEventListener('htmx:configRequest', function(evt) {
    let params = evt.detail.parameters;
    for (let key in params) {
        // Удаляем параметр, если он пуст, null или undefined
        if (params[key] === "" || params[key] === null) {
            delete params[key];
        }
    }
});
