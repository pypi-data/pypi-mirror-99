# -*- coding:utf-8 -*-

from tccli.argument import CustomArgument
from tccli.exceptions import UnknownArgumentError


class CliUnfoldArgument(CustomArgument):
    ARG_DATA = {
        'name': 'cli-unfold-argument',
        'help_text': (
            'complex type parameters are expanded with dots'
        ),
        'action': 'store_true'
    }

    def __init__(self):
        super(CliUnfoldArgument, self).__init__(**self.ARG_DATA)

    def build_action_parameters(self, args):
        parsed_args = vars(args)
        for key in list(parsed_args.keys()):
            if parsed_args[key] is None:
                del parsed_args[key]
        params_set = {}
        for key, value in parsed_args.items():
            self.convert_to_dict(params_set, key, value)
        return self.handle_array(params_set, "--")

    def convert_to_dict(self, params_set, key, value):
        if "." in key:
            sub_key, sub_value = key.split(".", 1)
            if sub_key not in params_set:
                params_set[sub_key] = {}
            self.convert_to_dict(params_set[sub_key], sub_value, value)
        else:
            params_set[key] = value

    def handle_array(self, params, parent_key):
        if not isinstance(params, dict):
            return params
        if any(x.isdigit() for x in params.keys()):
            keys = params.keys()
            formal_keys = list(map(str, range(len(keys))))
            if set(keys) != set(formal_keys):
                raise UnknownArgumentError(
                    "The index of the array parameter: %s must start from 0, "
                    "and the step size is 1" % parent_key)
            params = list(params.values())
            for idx, item in enumerate(params):
                prefix_param = parent_key+str(idx) if parent_key == "--" else parent_key+"."+str(idx)
                params[idx] = self.handle_array(item, prefix_param)
        else:
            for k in params.keys():
                prefix_param = parent_key+k if parent_key == "--" else parent_key+"."+k
                params[k] = self.handle_array(params[k], prefix_param)
        return params

    def build_action_parameters_old(self, args):
        parsed_args = vars(args)
        for key in list(parsed_args.keys()):
            if parsed_args[key] is None:
                del parsed_args[key]
        param_dict = self.gen_param_dict(parsed_args)
        return self.merge_dict(param_dict)

    def gen_param_dict(self, cli_param):
        param_list = []
        for key, value in cli_param.items():
            param = list(map(lambda x: int(x) if x.isdigit() else x, key.split('.')))
            param.append(value)
            param_list.append(param)

        all_param_list = []
        param_list = sorted(param_list, reverse=True)
        for param in param_list:
            param_dict = {}
            self._gen_param_dict(list(map(str, param)), param_dict)
            all_param_list.append(param_dict)
        return all_param_list

    def _gen_param_dict(self, param, param_dict):
        if not param:
            return param_dict

        if len(param) > 2 and param[1].isdigit():
            param_dict[param[0]] = [None] * (int(param[1]) + 1)
            if len(param) == 3:
                param_dict[param[0]][int(param[1])] = param[-1]
                return param_dict
            param_dict[param[0]][int(param[1])] = {}
            if len(param) > 3:
                self._gen_param_dict(param[2:], param_dict[param[0]][int(param[1])])
        else:
            if len(param) == 2:
                param_dict[param[0]] = param[-1]
                return param_dict
            param_dict[param[0]] = {}
            if len(param) > 2:
                self._gen_param_dict(param[1:], param_dict[param[0]])

    def recur_merge_dict(self, src_dict, dis_dict):
        if isinstance(src_dict, list):
            for idx, item in enumerate(src_dict):
                if not isinstance(item, dict) and src_dict[idx] is not None:
                    dis_dict[idx] = src_dict[idx]
                elif src_dict[idx] is not None:
                    dis_dict[idx] = self.recur_merge_dict(src_dict[idx], dis_dict[idx])
        else:
            for k in src_dict.keys():
                if dis_dict is None:
                    dis_dict = src_dict
                elif k not in dis_dict:
                    dis_dict[k] = src_dict[k]
                else:
                    dis_dict[k] = self.recur_merge_dict(src_dict[k], dis_dict[k])
        return dis_dict

    def merge_dict(self, param_list):
        if not param_list:
            return {}
        param = param_list[0]
        for item in param_list[1:]:
            for k in item.keys():
                if k not in param:
                    param[k] = item[k]
                else:
                    param[k] = self.recur_merge_dict(item[k], param[k])
        return param
