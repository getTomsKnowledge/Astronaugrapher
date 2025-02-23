<!-- Load Plotly.js for interactive plotting -->
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
    document.getElementById('simulationForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        const bodies = document.getElementById('bodies').value;
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        const stepSize = document.getElementById('stepSize').value;

        if (!bodies || !startDate || !endDate || !stepSize) {
           alert('Please fill in all fields.');
           return;
        }

       const payload = {
            bodies: bodies.split(',').map(body => body.trim()),
            start_date: startDate,
            end_date: endDate,
            step_size: parseInt(stepSize, 10)
        };

        try {
            const response = await fetch('/run-simulation', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
           });

            if (!response.ok) throw new Error('Simulation failed.');

            const data = await response.json();
           plotTrajectories(data);
        } catch (error) {
            alert(`Error: ${error.message}`);
       }
    });

   function plotTrajectories(data) {
       const traces = data.trajectories.map((trajectory, index) => ({
           x: trajectory.map(point => point[0]),
           y: trajectory.map(point => point[1]),
           z: trajectory.map(point => point[2]),
           mode: 'lines',
           name: data.bodies[index],
           type: 'scatter3d',
           line: { width: 3 }
       }));

       const layout = {
           title: 'Orbital Trajectories',
           scene: {
               xaxis: { title: 'X (km)' },
               yaxis: { title: 'Y (km)' },
               zaxis: { title: 'Z (km)' }
            },
            margin: { l: 0, r: 0, b: 0, t: 30 }
        };

       Plotly.newPlot('plot', traces, layout);
   }
</script>