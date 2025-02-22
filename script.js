document.getElementById('startButton').addEventListener('click', () => {
    const output = document.getElementById('output');
    output.innerHTML = 'Simulation started...';

    // Simulate some orbital mechanics calculations
    setTimeout(() => {
        output.innerHTML += '<br>Calculating orbits...';
    }, 1000);

    setTimeout(() => {
        output.innerHTML += '<br>Rendering results...';
    }, 2000);

    setTimeout(() => {
        output.innerHTML += '<br>Simulation completed.';
    }, 3000);
});