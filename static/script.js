document.getElementById('simulationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const bodies = document.getElementById('bodies').value.split(',').map(body => body.trim());
    const start_date = document.getElementById('start_date').value;
    const step_size = parseInt(document.getElementById('step_size').value);

    const params = {
        use_horizons: true,
        bodies: bodies,
        ephem_type: "VECTORS",
        center: "500@0",
        start_date: start_date,
        step_size: step_size,
        out_units: "KM-S",
        vec_table: "3",
        ref_plane: "ECLIPTIC",
        ref_system: "J2000",
        vec_corr: "NONE",
        ang_format: "DEG",
        csv_format: "YES",
        obj_data: "NO"
    };

    fetch('/simulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const output = document.getElementById('output');
            output.innerHTML = 'Simulation completed. Trajectories: ' + JSON.stringify(data.trajectories);
        } else {
            console.error(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});