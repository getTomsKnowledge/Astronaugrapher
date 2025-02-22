import json
from Astronaugrapher import main as run_astronaugrapher

def handler(event, context):
    try:
        data = json.loads(event['body'])
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

        trajectories = run_astronaugrapher(user_params)
        response = {
            'statusCode': 200,
            'body': json.dumps({'bodies': data['bodies'], 'trajectories': trajectories.tolist()})
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    return response