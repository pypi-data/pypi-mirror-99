#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0OA
#
# Authors:
# - Wen Guan, <wen.guan@cern.ch>, 2019 - 2020


"""
operations related to Transform.
"""

# from idds.common import exceptions

from idds.common.constants import (TransformStatus, ContentRelationType,
                                   TransformLocking, CollectionRelationType)
from idds.orm.base.session import read_session, transactional_session
from idds.orm import (transforms as orm_transforms,
                      collections as orm_collections,
                      contents as orm_contents,
                      messages as orm_messages,
                      processings as orm_processings)


@transactional_session
def add_transform(request_id, workload_id, transform_type, transform_tag=None, priority=0,
                  status=TransformStatus.New, locking=TransformLocking.Idle,
                  retries=0, expired_at=None, transform_metadata=None, workprogress_id=None, session=None):
    """
    Add a transform.

    :param request_id: The request id.
    :param workload_id: The workload id.
    :param transform_type: Transform type.
    :param transform_tag: Transform tag.
    :param priority: priority.
    :param status: Transform status.
    :param locking: Transform locking.
    :param retries: The number of retries.
    :param expired_at: The datetime when it expires.
    :param transform_metadata: The metadata as json.

    :raises DuplicatedObject: If a transform with the same name exists.
    :raises DatabaseException: If there is a database error.

    :returns: transform id.
    """
    transform_id = orm_transforms.add_transform(request_id=request_id, workload_id=workload_id,
                                                transform_type=transform_type, transform_tag=transform_tag,
                                                priority=priority, status=status, locking=locking, retries=retries,
                                                expired_at=expired_at, transform_metadata=transform_metadata,
                                                workprogress_id=workprogress_id, session=session)
    return transform_id


@read_session
def get_transform(transform_id, to_json=False, session=None):
    """
    Get transform or raise a NoObject exception.

    :param transform_id: Transform id.
    :param to_json: return json format.
    :param session: The database session in use.

    :raises NoObject: If no transform is founded.

    :returns: Transform.
    """
    return orm_transforms.get_transform(transform_id=transform_id, to_json=to_json, session=session)


@read_session
def get_transforms_with_input_collection(transform_type, transform_tag, coll_scope, coll_name, to_json=False, session=None):
    """
    Get transform or raise a NoObject exception.

    :param transform_type: Transform type.
    :param transform_tag: Transform tag.
    :param coll_scope: The collection scope.
    :param coll_name: The collection name.
    :param to_json: return json format.
    :param session: The database session in use.

    :raises NoObject: If no transform is founded.

    :returns: Transforms.
    """
    return orm_transforms.get_transforms_with_input_collection(transform_type, transform_tag, coll_scope,
                                                               coll_name, to_json=to_json, session=session)


@read_session
def get_transform_ids(workprogress_id, request_id=None, workload_id=None, transform_id=None, session=None):
    """
    Get transform ids or raise a NoObject exception.

    :param workprogress_id: Workprogress id.
    :param session: The database session in use.

    :raises NoObject: If no transform is founded.

    :returns: list of transform ids.
    """
    return orm_transforms.get_transform_ids(workprogress_id=workprogress_id, request_id=request_id,
                                            workload_id=workload_id, transform_id=transform_id, session=session)


@read_session
def get_transforms(workprogress_id=None, to_json=False, request_id=None, workload_id=None, transform_id=None, session=None):
    """
    Get transforms or raise a NoObject exception.

    :param workprogress_id: Workprogress id.
    :param to_json: return json format.
    :param session: The database session in use.

    :raises NoObject: If no transform is founded.

    :returns: list of transform.
    """
    return orm_transforms.get_transforms(workprogress_id=workprogress_id, request_id=request_id,
                                         workload_id=workload_id, transform_id=transform_id,
                                         to_json=to_json, session=session)


@transactional_session
def get_transforms_by_status(status, period=None, locking=False, bulk_size=None, to_json=False, session=None):
    """
    Get transforms or raise a NoObject exception.

    :param status: Transform status or list of transform status.
    :param session: The database session in use.
    :param locking: Whether to lock retrieved items.
    :param to_json: return json format.

    :raises NoObject: If no transform is founded.

    :returns: list of transform.
    """
    transforms = orm_transforms.get_transforms_by_status(status=status, period=period, locking=locking,
                                                         bulk_size=bulk_size, to_json=to_json, session=session)
    if locking:
        parameters = {'locking': TransformLocking.Locking}
        for transform in transforms:
            orm_transforms.update_transform(transform_id=transform['transform_id'], parameters=parameters, session=session)
    return transforms


@transactional_session
def update_transform(transform_id, parameters, session=None):
    """
    update a transform.

    :param transform_id: the transform id.
    :param parameters: A dictionary of parameters.
    :param session: The database session in use.

    :raises NoObject: If no content is founded.
    :raises DatabaseException: If there is a database error.

    """
    orm_transforms.update_transform(transform_id=transform_id, parameters=parameters, session=session)


@transactional_session
def add_transform_outputs(transform, transform_parameters, input_collections=None, output_collections=None, log_collections=None,
                          update_input_collections=None, update_output_collections=None, update_log_collections=None,
                          new_contents=None, update_contents=None, new_processing=None, update_processing=None,
                          messages=None, message_bulk_size=1000, session=None):
    """
    For input contents, add corresponding output contents.

    :param transform: the transform.
    :param input_collections: The new input collections.
    :param output_collections: The new output collections.
    :param log_collections: The new log collections.
    :param update_input_collections: The updated input collections.
    :param update_output_collections: The updated output collections.
    :param update_log_collections: The updated log collections.
    :param new_contents: The new contents.
    :param update_contents: The updated contents.
    :param new_processing: The new processing.
    :param messages: Messages.
    :param message_bulk_size: The message bulk size.
    :param session: The database session in use.

    :raises DatabaseException: If there is a database error.
    """
    work = transform['transform_metadata']['work']

    if input_collections:
        for coll in input_collections:
            coll_id = orm_collections.add_collection(**coll, session=session)
            work.set_collection_id(coll, coll_id)
    if output_collections:
        for coll in output_collections:
            coll_id = orm_collections.add_collection(**coll, session=session)
            work.set_collection_id(coll, coll_id)
    if log_collections:
        for coll in log_collections:
            coll_id = orm_collections.add_collection(**coll, session=session)
            work.set_collection_id(coll, coll_id)

    if update_input_collections:
        orm_collections.update_collections(update_input_collections, session=session)
    if update_output_collections:
        orm_collections.update_collections(update_output_collections, session=session)
    if update_log_collections:
        orm_collections.update_collections(update_log_collections, session=session)

    if new_contents:
        orm_contents.add_contents(new_contents, session=session)
    if update_contents:
        orm_contents.update_contents(update_contents, session=session)

    processing_id = None
    if new_processing:
        # print(new_processing)
        processing_id = orm_processings.add_processing(**new_processing, session=session)
    if update_processing:
        for proc_id in update_processing:
            orm_processings.update_processing(processing_id=proc_id, parameters=update_processing[proc_id], session=session)

    if messages:
        if not type(messages) in [list, tuple]:
            messages = [messages]
        for message in messages:
            orm_messages.add_message(msg_type=message['msg_type'],
                                     status=message['status'],
                                     source=message['source'],
                                     request_id=message['request_id'],
                                     workload_id=message['workload_id'],
                                     transform_id=message['transform_id'],
                                     num_contents=message['num_contents'],
                                     msg_content=message['msg_content'],
                                     bulk_size=message_bulk_size,
                                     session=session)

    """
    if to_cancel_processing:
        to_cancel_params = {'status': ProcessingStatus.Cancel}
        for to_cancel_id in to_cancel_processing:
            orm_processings.update_processing(processing_id=to_cancel_id, parameters=to_cancel_params, session=session)
    processing_id = None
    if processing:
        processing_id = orm_processings.add_processing(**processing, session=session)
    """

    if transform:
        """
        if processing_id is not None:
            if not transform['transform_metadata']:
                transform['transform_metadata'] = {'processing_id': processing_id}
            else:
                transform['transform_metadata']['processing_id'] = processing_id
        """
        if processing_id:
            work.set_processing_id(new_processing, processing_id)
        orm_transforms.update_transform(transform_id=transform['transform_id'],
                                        parameters=transform_parameters,
                                        session=session)


@transactional_session
def delete_transform(transform_id=None, session=None):
    """
    delete a transform.

    :param transform_id: The id of the transform.
    :param session: The database session in use.

    :raises NoObject: If no content is founded.
    :raises DatabaseException: If there is a database error.
    """
    orm_transforms.delete_transform(transform_id=transform_id, session=session)


@transactional_session
def clean_locking(time_period=3600, session=None):
    """
    Clearn locking which is older than time period.

    :param time_period in seconds
    """
    orm_transforms.clean_locking(time_period=time_period, session=session)


@transactional_session
def clean_next_poll_at(status, session=None):
    """
    Clearn next_poll_at.

    :param status: status of the transform
    """
    orm_transforms.clean_next_poll_at(status=status, session=session)


@read_session
def get_transform_input_output_maps(transform_id, input_coll_ids, output_coll_ids, log_coll_ids=[], session=None):
    """
    Get transform input output maps.

    :param transform_id: transform id.
    """
    contents = orm_contents.get_contents_by_transform(transform_id=transform_id, session=session)
    ret = {}
    for content in contents:
        map_id = content['map_id']
        if map_id not in ret:
            ret[map_id] = {'inputs_dependency': [], 'inputs': [], 'outputs': [], 'logs': [], 'others': []}

        """
        if content['coll_id'] in input_coll_ids:
            ret[map_id]['inputs'].append(content)
        elif content['coll_id'] in output_coll_ids:
            ret[map_id]['outputs'].append(content)
        elif content['coll_id'] in log_coll_ids:
            ret[map_id]['logs'].append(content)
        else:
            ret[map_id]['others'].append(content)
        """
        if content['content_relation_type'] == ContentRelationType.Input:
            ret[map_id]['inputs'].append(content)
        elif content['content_relation_type'] == ContentRelationType.InputDependency:
            ret[map_id]['inputs_dependency'].append(content)
        elif content['content_relation_type'] == ContentRelationType.Output:
            ret[map_id]['outputs'].append(content)
        elif content['content_relation_type'] == ContentRelationType.Log:
            ret[map_id]['logs'].append(content)
        else:
            ret[map_id]['others'].append(content)
    return ret


def release_inputs(to_release_inputs):
    update_contents = []
    for to_release in to_release_inputs:
        contents = orm_contents.get_input_contents(request_id=to_release['request_id'],
                                                   coll_id=to_release['coll_id'],
                                                   name=to_release['name'])
        for content in contents:
            if content['content_relation_type'] == ContentRelationType.InputDependency:
                update_content = {'content_id': content['content_id'],
                                  'substatus': to_release['substatus'],
                                  'status': to_release['status']}
                update_contents.append(update_content)
    return update_contents


def get_work_name_to_coll_map(request_id):
    tfs = orm_transforms.get_transforms(request_id=request_id)
    colls = orm_collections.get_collections(request_id=request_id)
    work_name_to_coll_map = {}
    for tf in tfs:
        if ('transform_metadata' in tf and tf['transform_metadata']
            and 'work_name' in tf['transform_metadata'] and tf['transform_metadata']['work_name']):  # noqa: W503
            work_name = tf['transform_metadata']['work_name']
            transform_id = tf['transform_id']
            if work_name not in work_name_to_coll_map:
                work_name_to_coll_map[work_name] = {'inputs': [], 'outputs': []}
            for coll in colls:
                if coll['transform_id'] == transform_id:
                    if coll['relation_type'] == CollectionRelationType.Input:
                        work_name_to_coll_map[work_name]['inputs'].append({'coll_id': coll['coll_id'], 'scope': coll['scope'], 'name': coll['name']})
                    elif coll['relation_type'] == CollectionRelationType.Output:
                        work_name_to_coll_map[work_name]['outputs'].append({'coll_id': coll['coll_id'], 'scope': coll['scope'], 'name': coll['name']})
    return work_name_to_coll_map
