from flask import jsonify, request, current_app, send_file
from polzybackend.general import bp
from polzybackend.utils.import_utils import all_stages
from polzybackend import auth, models, db
from datetime import datetime
import os
from uuid import uuid4

@bp.route('/stages')
def stages():
    #
    # returns list of all available stages for login
    #

    try:
        # get all stages
        stages = all_stages()()
        current_app.logger.debug(f"Value of stages: {stages}")

    except Exception as e:
        current_app.logger.warning(f'Failed to get All Stages: {e}')
        stages = []

    return jsonify(stages), 200


@bp.route('/values', methods=['POST'])
@auth.login_required
def values():
    #
    # returns value list
    #

    # get post data
    data = request.get_json()

    try:
        # get parent instance from app store
        # try policies first
        instance = current_app.config['ANTRAGS'].get(data['instanceId'])
        if instance is None:
            # try antrags then
            instance = current_app.config['POLICIES'].get(data['instanceId'])
            if instance is None:
                raise ValueError(f'Instance with id {data["instanceId"]} not found in PoLZy storage. Most probably app restarted.')

        # get value list
        result = instance.getValueList(data.get('valueListName'))
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.exception(f'Faild to get value-list for paylod {data}\n{e}')
    
    return jsonify({'error': f'Failed to get value-list'}), 400


@bp.route('/upload', methods=['POST'])
@bp.route('/upload/<string:parent_id>/<path:file_type>', methods=['POST'])
@auth.login_required
def upload(parent_id=None, file_type=None):
    # get file
    file = request.files.get('file')
    if file is None:
        return jsonify({'error': 'Request does not contain dataFile'}), 400

    # save file
    try:
        user = auth.current_user()
        filename_parts = (str(uuid4()), file.filename.split('.')[-1])
        path_to_file = os.path.join(current_app.config['UPLOADS'], '.'.join(filename_parts))
        file.save(path_to_file)
        # create file instance in db
        file_db = models.File.new(
            user=auth.current_user(),
            id=filename_parts[0],
            filename=file.filename,
            parent_id=parent_id,
            file_type=file_type,
        )
        return {'OK': f'File {file_db.filename} saved with id {file_db.id}'}, 200
    except Exception as error:
        current_app.logger.error(f'Failed to upload file "{file.filename}" by {user}: {error}.')
        return jsonify({'error': 'File upload failed'}), 400
    

@bp.route('/documents/<string:file_id>', methods=['GET', 'POST', 'DELETE'])
@auth.login_required
def manage_file(file_id):
    # get file record
    file = models.File.query.get(file_id)
    try:
        ext = file.filename.split('.')[-1]
    except AttributeError:
        ext = ""
    path_to_file = os.path.join(current_app.config['UPLOADS'], f'{file_id}.{ext}')

    # edit file type
    if request.method == 'POST':
        payload = request.get_json()
        file.type = payload.get('fileType')
        db.session.commit()
        return {}, 200

    # delete file
    if request.method == 'DELETE':
        # delete file record
        try:
            db.session.delete(file)
            db.session.commit()
        except UnmappedInstanceError as e:
            current_app.logger.critical(f"File {file} has not mapped instance. Error: {e}")
        return {}, 200

    # get file
    return send_file(
        path_to_file,
        attachment_filename=file.filename,
    )


@bp.route('/remotedocuments', methods=['POST'])
@auth.login_required
def remote_documents():
    #
    # returns link to a remote dokument or a ziped bunch of remote documents  
    #

    # get post data
    data = request.get_json()

    try:
        # get parent instance from app store
        # try policies first
        instance = current_app.config['ANTRAGS'].get(data['parentId'])
        if instance is None:
            # try antrags then
            instance = current_app.config['POLICIES'].get(data['parentId'])
            if instance is None:
                raise ValueError(f'Instance with id {data["parentId"]} not found in PoLZy storage. Most probably app restarted.')

        # get path
        path_to_document = instance.getRemoteDocuments(data.get('documentsId'))
        return send_file(path_to_document)

    except Exception as e:
        current_app.logger.exception(f'Faild to get remote documents for paylod {data}\n{e}')
    
    return jsonify({'error': f'Faild to get remote documents'}), 400