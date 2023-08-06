import ckan.authz as authz
from ckan.common import asbool
from ckan import logic
import ckan.plugins.toolkit as toolkit

from . import helpers as dcor_helpers


def dataset_purge(context, data_dict):
    """Only allow deletion of deleted datasets"""
    # original auth function
    # (usually, only sysadmins are allowed to purge, so we test against
    # package_update)
    ao = logic.auth.update.package_update(context, data_dict)
    if not ao["success"]:
        return ao

    # get the current package dict
    show_context = {
        'model': context['model'],
        'session': context['session'],
        'user': context['user'],
        'auth_user_obj': context['auth_user_obj'],
    }
    package_dict = logic.get_action('package_show')(
        show_context,
        {'id': get_package_id(context, data_dict)})
    state = package_dict.get('state')
    if state != "deleted":
        return {"success": False,
                "msg": "Only deleted datasets can be purged!"}
    return {"success": True}


def deny(context, data_dict):
    return {'success': False,
            'msg': "Only admins may do so."}


def get_package_id(context, data_dict):
    """Convenience function that extracts the package_id"""
    package = context.get('package')
    if package:
        # web
        package_id = package.id
    else:
        package_id = logic.get_or_bust(data_dict, 'id')
    convert_package_name_or_id_to_id = toolkit.get_converter(
        'convert_package_name_or_id_to_id')
    return convert_package_name_or_id_to_id(package_id, context)


def package_create(context, data_dict):
    user = context['user']
    # If a group is given, check whether the user has the necessary permissions
    check_group = logic.auth.create._check_group_auth(context, data_dict)
    if not check_group:
        return {'success': False,
                'msg': 'User {} not authorized to edit '.format(user)
                       + 'these collections'}

    # Are we allowed to add a dataset to the given organization?
    org_id = None if data_dict is None else data_dict.get('owner_org', None)
    if org_id is None:
        # No organization was given. This means that we just have to check
        # whether the user can create packages in general. Since the user
        # is logged-in, he can do that.
        # elaboration:
        # - if `data_dict` is None, we currently want to create a new dataset
        #   (/dataset/new)
        # - if `data_dict["owner_org"] is None, we currently want to view
        #   the datasets (/dataset)
        pass
    else:
        if not authz.has_user_permission_for_group_or_org(
                org_id, user, 'create_dataset'):
            return {'success': False,
                    'msg': 'User {} not authorized to add '.format(user)
                           + 'datasets to circle {}!'.format(org_id)}

    return {"success": True}


def package_delete(context, data_dict):
    """Only allow deletion of draft datasets"""
    # original auth function
    ao = logic.auth.update.package_update(context, data_dict)
    if not ao["success"]:
        return ao

    # get the current package dict
    show_context = {
        'model': context['model'],
        'session': context['session'],
        'user': context['user'],
        'auth_user_obj': context['auth_user_obj'],
    }
    package_dict = logic.get_action('package_show')(
        show_context,
        {'id': get_package_id(context, data_dict)})
    state = package_dict.get('state')
    if state != "draft":
        return {"success": False,
                "msg": "Only draft datasets can be deleted!"}
    return {"success": True}


def package_update(context, data_dict=None):
    # original auth function
    ao = logic.auth.update.package_update(context, data_dict)
    if not ao["success"]:
        return ao

    if data_dict is None:
        data_dict = {}

    # get the current package dict
    show_context = {
        'model': context['model'],
        'session': context['session'],
        'user': context['user'],
        'auth_user_obj': context['auth_user_obj'],
    }
    pkg_dict = logic.get_action('package_show')(
        show_context,
        {'id': get_package_id(context, data_dict)})
    # do not allow switching to a more restrictive license
    if "license_id" in data_dict:
        allowed = dcor_helpers.get_valid_licenses(pkg_dict["license_id"])
        if data_dict["license_id"] not in allowed:
            return {'success': False,
                    'msg': 'Cannot switch to more-restrictive license'}
    # do not allow setting state from "active" to "draft"
    if pkg_dict["state"] != "draft" and data_dict.get("state") == "draft":
        return {'success': False,
                'msg': 'Changing dataset state to draft not allowed'}
    # do not allow setting the visibility from public to private
    if not pkg_dict["private"] and asbool(data_dict.get("private", False)):
        assert isinstance(pkg_dict["private"], bool)
        return {'success': False,
                'msg': 'Changing visibility to private not allowed'}
    # do not allow changing some of the keys
    prohibited_keys = ["name"]
    invalid = {}
    for key in data_dict:
        if (key in pkg_dict
            and key in prohibited_keys
                and data_dict[key] != pkg_dict[key]):
            invalid[key] = data_dict[key]
    if invalid:
        return {'success': False,
                'msg': 'Editing not allowed: {}'.format(invalid)}

    return {'success': True}


def resource_create(context, data_dict=None):
    # original auth function
    ao = logic.auth.create.resource_create(context, data_dict)
    if not ao["success"]:
        return ao

    if "package_id" in data_dict:
        pkg_dict = logic.get_action('package_show')(
            dict(context, return_type='dict'),
            {'id': data_dict["package_id"]})

        # do not allow adding resources to non-draft datasets
        if pkg_dict["state"] != "draft":
            return {'success': False,
                    'msg': 'Adding resources to non-draft datasets not '
                           'allowed!'}

        if "upload" in data_dict:
            # id must not be set
            if data_dict.get("id", ""):
                return {'success': False,
                        'msg': 'You are not allowed to set the id!'}

    return {'success': True}


def resource_update(context, data_dict=None):
    # original auth function
    ao = logic.auth.update.resource_update(context, data_dict)
    if not ao["success"]:
        return ao

    # get the current resource dict
    show_context = {
        'model': context['model'],
        'session': context['session'],
        'user': context['user'],
        'auth_user_obj': context['auth_user_obj'],
    }
    resource_dict = logic.get_action('resource_show')(
        show_context,
        {'id': logic.get_or_bust(data_dict, 'id')})
    data_dict["package_id"] = get_package_id(context, data_dict)
    # only allow updating the description
    allowed_keys = ["description"]
    invalid = {}
    for key in data_dict:
        if (key not in resource_dict
            or (key not in allowed_keys
                and data_dict[key] != resource_dict[key])):
            invalid[key] = data_dict[key]
    if invalid:
        return {'success': False,
                'msg': 'Editing not allowed: {}'.format(invalid)}

    return {'success': True}
