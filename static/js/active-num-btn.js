document.querySelectorAll('.player__num-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.player__num-btn')
            .forEach(b => b.classList.remove('btn-active'));

        this.classList.add('btn-active');
    });
});

// document.addEventListener('click', function(e) {
//
//     if (e.target.classList.contains('player__voice-btn')) {
//         document.querySelectorAll('.player__voice-btn')
//             .forEach(btn => btn.classList.remove('btn-active'));
//
//         e.target.classList.add('active');
//     }
//
// });