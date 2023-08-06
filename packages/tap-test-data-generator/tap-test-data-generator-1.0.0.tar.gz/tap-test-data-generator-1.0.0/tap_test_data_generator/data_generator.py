#!/usr/bin/env python3
import copy
import hashlib
import json
from collections import OrderedDict
from datetime import timedelta

import exrex
import singer

from tap_test_data_generator.string_generator import StringGenerator

LOGGER = singer.get_logger()


def generate_formatted_string(faker_factory, schema_json):
    generated_string = ""
    string_format = ""
    if "format" in schema_json:
        string_format = schema_json['format']
    if string_format == 'date':
        minimum = "-30y"
        maximum = "today"
        if "minimum" in schema_json:
            minimum = timedelta(days=schema_json['minimum'])
        if "maximum" in schema_json:
            maximum = timedelta(days=schema_json['maximum'])
        generated_string = str(faker_factory.date_between(start_date=minimum, end_date=maximum))
    return generated_string


def generate_string_with_type(faker_factory, schema_json):
    if "$generator" in schema_json:
        generator_value = schema_json['$generator']
        string_type = generator_value.split("#/string-type/", 1)[1]
        generate_function_name = "generate_" + string_type
        generate_function = getattr(StringGenerator, generate_function_name, None)
        if callable(generate_function):
            generated_string = generate_function(faker_factory, schema_json)
        else:
            LOGGER.warning("unknown string type " + string_type)
            generated_string = ""
    else:
        # running in random string mode
        min_char = 1
        max_char = 100
        if "minLength" in schema_json:
            min_char = schema_json['minLength']
        if "maxLength" in schema_json:
            max_char = schema_json['maxLength']
        generated_string = faker_factory.pystr(min_chars=min_char, max_chars=max_char)
    return generated_string


def generate_number(schema_json, faker_factory):
    max_digit = 10
    max_value = None
    min_value = None
    if "maximum" in schema_json:
        max_value = schema_json['maximum']
    if "minimum" in schema_json:
        min_value = schema_json['minimum']
    if "const" in schema_json:
        const_value = schema_json['const']
        generated_float = const_value
    elif max_value is not None and min_value is not None:
        generated_float = faker_factory.pyfloat(right_digits=2, positive=False, min_value=min_value,
                                                max_value=max_value)
    else:
        if "maxLength" in schema_json:
            max_digit = schema_json['maxLength']
        generated_float = faker_factory.pyfloat(left_digits=max_digit - 3, right_digits=2)
    return generated_float


def generate_integer(schema_json, faker_factory):
    max_digit = 10
    max_value = None
    min_value = None
    if "maximum" in schema_json:
        max_value = schema_json['maximum']
    if "minimum" in schema_json:
        min_value = schema_json['minimum']
    if "const" in schema_json:
        const_value = schema_json['const']
        generated_integer = const_value
    elif max_value is not None and min_value is not None:
        generated_integer = faker_factory.random_int(min=min_value, max=max_value, step=1)
    else:
        if "maxLength" in schema_json:
            max_digit = schema_json['maxLength']
        generated_integer = faker_factory.random_number(digits=max_digit)
    return generated_integer


def generate_boolean(property_name, schema_json, faker_factory, pairs):
    pairwise_value = False
    if "$pairwise" in schema_json:
        pairwise_value = schema_json['$pairwise']
    if pairwise_value and (pairs is not None):
        generated_boolean = getattr(pairs, property_name)
    elif "const" in schema_json:
        const_value = schema_json['const']
        generated_boolean = const_value
    else:
        generated_boolean = faker_factory.pybool()
    return generated_boolean


def generate_string(property_name, schema_json, faker_factory, pairs):
    pairwise_value = False
    if "$pairwise" in schema_json:
        pairwise_value = schema_json['$pairwise']
    if "pattern" in schema_json:
        if pairwise_value and (pairs is not None):
            generated_string = getattr(pairs, property_name)
        else:
            # running in regex mode
            generated_string = exrex.getone(schema_json['pattern'])
    elif "enum" in schema_json:
        if pairwise_value and (pairs is not None):
            generated_string = getattr(pairs, property_name)
        else:
            # running in random enum mode
            generated_string = faker_factory.random_element(elements=schema_json['enum'])
    elif "format" in schema_json:
        generated_string = generate_formatted_string(faker_factory, schema_json)
    elif "const" in schema_json:
        generated_string = schema_json['const']
    else:
        generated_string = generate_string_with_type(faker_factory, schema_json)
    return generated_string


def generate_dictionary(property_name, schema_json, dictionary, faker_factory, object_repositories, pairs, definitions):
    if "type" in schema_json:
        property_type = schema_json['type']
        if property_type == 'array':
            dictionary = generate_array(dictionary, property_name, schema_json, faker_factory, object_repositories,
                                        pairs, definitions)
        elif property_type == 'object':
            dictionary = generate_object(dictionary, property_name, schema_json, faker_factory, object_repositories,
                                         pairs, definitions)
        elif property_type == 'string' or property_type == ['string', 'null']:
            dictionary[property_name] = generate_string(property_name, schema_json, faker_factory, pairs)
        elif property_type == 'boolean' or property_type == ['boolean', 'null']:
            dictionary[property_name] = generate_boolean(property_name, schema_json, faker_factory, pairs)
        elif property_type == 'integer' or property_type == ['integer', 'null']:
            dictionary[property_name] = generate_integer(schema_json, faker_factory)
        elif property_type == 'number' or property_type == ['number', 'null']:
            dictionary[property_name] = generate_number(schema_json, faker_factory)
    else:
        # no type it is a $ref
        if "$ref" in schema_json:
            ref_value = schema_json['$ref']
            # inject the $generator and $pairwise into child schema
            ref_schema = copy.deepcopy(definitions[ref_value])
            if "$generator" in schema_json:
                ref_schema['$generator'] = schema_json['$generator']
            if "$pairwise" in schema_json:
                ref_schema['$pairwise'] = schema_json['$pairwise']
            dictionary.update(generate_dictionary(property_name, ref_schema, dictionary, faker_factory,
                                                  object_repositories, pairs, definitions))
    return dictionary


def generate_typed_object(generator_value, schema_json, faker_factory):
    object_type = generator_value[len("#/object-type/"):]
    if "empty" in object_type:
        return {}
    return {}


def generate_object(dictionary, property_name, schema_json, faker_factory, object_repositories, pairs, definitions):
    try:
        generator_value = ""
        if "$generator" in schema_json:
            generator_value = schema_json['$generator']
        pairwise_value = False
        if "$pairwise" in schema_json:
            pairwise_value = schema_json['$pairwise']
        if "#/object-repository/" in generator_value:
            if pairwise_value and (pairs is not None):
                dictionary[property_name] = getattr(pairs, property_name)
            else:
                # pic one value from repository
                object_name = generator_value[len("#/object-repository/"):]
                dictionary[property_name] = faker_factory.random_element(elements=object_repositories[object_name])
        elif "#/object-type/" in generator_value:
            dictionary[property_name] = generate_typed_object(generator_value, schema_json, faker_factory)
        else:
            # random child object mode
            if "properties" in schema_json:
                properties = schema_json['properties']
                child_dict = {}
                for key in properties.keys():
                    child_schema = properties[key]
                    child_dict = generate_dictionary(key, child_schema, child_dict, faker_factory, object_repositories,
                                                     pairs, definitions)
                if property_name is not None:
                    dictionary[property_name] = child_dict
                else:
                    dictionary = child_dict
            else:
                LOGGER.warning("No properties found for object : " + str(property_name))
                dictionary[property_name] = {}
    except Exception:
        LOGGER.exception("Unexpected error for property : " + str(property_name))
    return dictionary


def generate_array(dictionary, property_name, schema_json, faker_factory, object_repositories, pairs, definitions):
    child_dict = []
    item_schema = schema_json['items']
    min_items = 1
    max_items = 10
    if "minItems" in schema_json:
        min_items = schema_json['minItems']
    if "maxItems" in schema_json:
        max_items = schema_json['maxItems']
    # TODO the array element number is random -> not compliant with pairwise
    element_number = faker_factory.random_int(min=min_items, max=max_items, step=1)
    if item_schema['type'] == 'string':
        i = 0
        while i < element_number:
            child_dict.append(generate_string(property_name, item_schema, faker_factory, pairs))
            i += 1
    elif item_schema['type'] == 'object':
        i = 0
        while i < element_number:
            child_dict.append(generate_dictionary(None, item_schema, {}, faker_factory, object_repositories, pairs, definitions))
            i += 1
    if property_name is not None:
        dictionary[property_name] = child_dict
    else:
        dictionary = child_dict
    return dictionary


def extract_value_lists(property_name, schema_json, object_repositories, definitions):
    value_list = OrderedDict()
    if "type" in schema_json:
        property_type = schema_json['type']
        pairwise_value = False
        if "$pairwise" in schema_json:
            pairwise_value = schema_json['$pairwise']
        if property_type == 'object':
            value_list.update(extract_value_lists_from_object(property_name, schema_json, object_repositories,
                                                              definitions))
        elif (property_type == 'string') and pairwise_value:
            value_list.update(extract_value_lists_from_string(property_name, schema_json))
        elif (property_type == 'boolean') and pairwise_value:
            value_list[property_name] = [True, False]
    else:
        # no type it is a $ref
        if "$ref" in schema_json:
            ref_value = schema_json['$ref']
            # inject the $generator and $pairwise into child schema
            ref_schema = copy.deepcopy(definitions[ref_value])
            if "$generator" in schema_json:
                ref_schema['$generator'] = schema_json['$generator']
            if "$pairwise" in schema_json:
                ref_schema['$pairwise'] = schema_json['$pairwise']
            value_list.update(extract_value_lists(property_name, ref_schema, object_repositories, definitions))
    return value_list


def extract_value_lists_from_object(property_name, schema_json, object_repositories, definitions):
    value_list = OrderedDict()
    try:
        generator_value = ""
        pairwise_value = False
        if "$generator" in schema_json:
            generator_value = schema_json['$generator']
        if "$pairwise" in schema_json:
            pairwise_value = schema_json['$pairwise']
        if ("#/object-repository/" in generator_value) and pairwise_value:
            object_name = generator_value[len("#/object-repository/"):]
            # get the object list
            value_list[property_name] = object_repositories[object_name]
        else:
            # child object mode
            if "properties" in schema_json:
                properties = schema_json['properties']
                for key in properties.keys():
                    child_schema = properties[key]
                    child_value_lists = extract_value_lists(key, child_schema, object_repositories, definitions)
                    value_list.update(child_value_lists)
            else:
                LOGGER.warn("No properties found for object : " + property_name)
    except Exception:
        LOGGER.exception("Unexpected error for property : " + property_name)
    return value_list


def extract_value_lists_from_string(property_name, schema_json):
    value_list = OrderedDict()
    if "pattern" in schema_json:
        # extracting all pattern values
        limit = 100
        value_list[property_name] = list(exrex.generate(schema_json['pattern'], limit))
    elif "enum" in schema_json:
        # extracting enum values
        enum_values = schema_json['enum']
        value_list[property_name] = enum_values
    return value_list


def generate_pairwise_hash(pairs):
    hash_value = ""
    if pairs is not None:
        full_value = json.dumps(pairs)
        hash_object = hashlib.md5(full_value.encode('utf-8'))
        hash_value = hash_object.hexdigest()
    return hash_value
