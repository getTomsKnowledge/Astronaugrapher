# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 04:43:45 2025
@project: Astronaugrapher
@author: Tom W
"""

#<!-- Python Backend (Flask) -->
#<!-- Save the following in a separate "app.py" file and run it to handle requests -->
#<!--
from flask import Flask, request, jsonify
from Astronaugrapher import main as run_astronaugrapher

app = Flask(__name__)

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    data = request.json

    # Pass user inputs to the existing Astronaugrapher main function
    try:
        user_params = {
            'use_horizons': True,
            'bodies': data['bodies'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'step_size': data['step_size'],
            'ephem_type': "VECTORS",
            'center': "500@0",
            'out_units': "KM-S",
            'vec_table': "3",
            'ref_plane': "ECLIPTIC",
            'ref_system': "J2000",
            'vec_corr': "NONE",
            'ang_format': "DEG",
            'csv_format': "YES",
            'obj_data': "NO",
        }

        # Run the main Astronaugrapher function with the given parameters
        trajectories = run_astronaugrapher(user_params)
        return jsonify({'bodies': data['bodies'], 'trajectories': trajectories.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
#-->