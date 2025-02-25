from flask import Flask, request, jsonify, render_template
from Astronaugrapher import main as run_astronaugrapher
import AstroQuery as horizons
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/templates')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def simulate():
    user_params = request.json
    try:
        horizons_data = None
        if user_params['use_horizons']:
            horizons_data = horizons.retrieve_data(
                user_params['bodies'],
                EPHEM_TYPE=user_params['ephem_type'],
                CENTER=user_params['center'],
                START_TIME=user_params['start_date'],
                STEP_SIZE=f"{user_params['step_size']} s",
                OUT_UNITS=user_params['out_units'],
                VEC_TABLE=user_params['vec_table'],
                REF_PLANE=user_params['ref_plane'],
                REF_SYSTEM=user_params['ref_system'],
                VEC_CORR=user_params['vec_corr'],
                ANG_FORMAT=user_params['ang_format'],
                CSV_FORMAT=user_params['csv_format'],
                OBJ_DATA=user_params['obj_data']
            )
        trajectories = run_astronaugrapher(user_params, horizons_data)
        return jsonify({"status": "success", "trajectories": trajectories.tolist()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)