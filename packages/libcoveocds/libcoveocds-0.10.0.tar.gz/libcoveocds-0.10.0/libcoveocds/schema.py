import json
import os
from collections import OrderedDict
from copy import deepcopy
from urllib.parse import urljoin

import json_merge_patch
import requests
from libcove.lib.common import SchemaJsonMixin, get_schema_codelist_paths, load_codelist, load_core_codelists
from libcove.lib.tools import get_request

import libcoveocds.config


class SchemaOCDS(SchemaJsonMixin):
    def __init__(
        self, select_version=None, release_data=None, cache_schema=False, lib_cove_ocds_config=None, record_pkg=False
    ):
        """Build the schema object using an specific OCDS schema version

        The version used will be select_version, release_data.get('version') or
        default version, in that order. Invalid version choices in select_version or
        release_data will be skipped and registered as self.invalid_version_argument
        and self.invalid_version_data respectively.
        """

        self.config = lib_cove_ocds_config or libcoveocds.config.LibCoveOCDSConfig()
        self.schema_name = self.config.config["schema_item_name"]
        self.pkg_schema_name = self.config.config["schema_name"]["release"]
        self.record_pkg = record_pkg
        if record_pkg:
            self.pkg_schema_name = self.config.config["schema_name"]["record"]
            self.release_schema = SchemaOCDS(
                select_version=select_version,
                release_data=release_data,
                cache_schema=cache_schema,
                lib_cove_ocds_config=lib_cove_ocds_config,
                record_pkg=False,
            )
        self.version_choices = self.config.config["schema_version_choices"]
        self.default_version = self.config.config["schema_version"]
        self.default_schema_host = self.version_choices[self.default_version][1]

        self.version = self.default_version
        self.schema_host = self.default_schema_host

        # cache_schema is a deprecated option - now set cache_all_requests in the config instead.
        if cache_schema:
            self.config.config["cache_all_requests"] = True

        # Missing package is only for original json data
        self.missing_package = False
        if release_data:
            if "version" not in release_data:
                self.version = "1.0"
                self.schema_host = self.version_choices["1.0"][1]
            if "releases" not in release_data and "records" not in release_data:
                self.missing_package = True

        self.invalid_version_argument = False
        self.invalid_version_data = False
        self.json_deref_error = None
        self.extensions = {}
        self.invalid_extension = {}
        self.extended = False
        self.extended_schema_file = None
        self.extended_schema_url = None
        self.codelists = self.config.config["schema_codelists"]["1.1"]

        if select_version:
            try:
                self.version_choices[select_version]
            except KeyError:
                select_version = None
                self.invalid_version_argument = True
            else:
                self.version = select_version
                self.schema_host = self.version_choices[select_version][1]

        if hasattr(release_data, "get"):
            data_extensions = release_data.get("extensions", {})
            if data_extensions:
                self.extensions = OrderedDict((ext, tuple()) for ext in data_extensions if type(ext) == str)
            if not select_version:
                release_version = release_data and release_data.get("version")
                if release_version:
                    version_choice = self.version_choices.get(release_version)
                    if version_choice:
                        self.version = release_version
                        self.schema_host = version_choice[1]
                    else:
                        self.invalid_version_data = True
        else:
            pass

        self.schema_url = urljoin(self.schema_host, self.schema_name)
        self.pkg_schema_url = urljoin(self.schema_host, self.pkg_schema_name)

    def process_codelists(self):
        self.core_codelist_schema_paths = get_schema_codelist_paths(self, use_extensions=False)
        self.extended_codelist_schema_paths = get_schema_codelist_paths(self, use_extensions=True)

        core_unique_files = frozenset(value[0] for value in self.core_codelist_schema_paths.values())
        self.core_codelists = load_core_codelists(self.codelists, core_unique_files, config=self.config)

        self.extended_codelists = deepcopy(self.core_codelists)
        self.extended_codelist_urls = {}
        # we do not want to cache if the requests failed.
        if not self.core_codelists:
            load_core_codelists.cache_clear()
            return

        for extension, extension_detail in self.extensions.items():
            if not isinstance(extension_detail, dict):
                continue

            codelist_list = extension_detail.get("codelists")
            if not codelist_list:
                continue

            base_url = "/".join(extension.split("/")[:-1]) + "/codelists/"

            for codelist in codelist_list:
                try:
                    codelist_map = load_codelist(base_url + codelist, config=self.config)
                except UnicodeDecodeError:
                    extension_detail["failed_codelists"][codelist] = "Unicode Error, codelists need to be in UTF-8"
                except Exception as e:
                    extension_detail["failed_codelists"][codelist] = "Unknown Exception, {}".format(str(e))
                    continue

                if not codelist_map:
                    extension_detail["failed_codelists"][
                        codelist
                    ] = "Codelist Error, Could not find code field in codelist"

                if codelist[0] in ("+", "-"):
                    codelist_extension = codelist[1:]
                    if codelist_extension not in self.extended_codelists:
                        extension_detail["failed_codelists"][
                            codelist
                        ] = "Extension error, Trying to extend non existing codelist {}".format(codelist_extension)
                        continue

                if codelist[0] == "+":
                    self.extended_codelists[codelist_extension].update(codelist_map)
                elif codelist[0] == "-":
                    for code in codelist_map:
                        value = self.extended_codelists[codelist_extension].pop(code, None)
                        if not value:
                            extension_detail["failed_codelists"][
                                codelist
                            ] = "Codelist error, Trying to remove non existing codelist value {}".format(code)
                else:
                    self.extended_codelists[codelist] = codelist_map

                try:
                    self.extended_codelist_urls[codelist].append(base_url + codelist)
                except KeyError:
                    self.extended_codelist_urls[codelist] = [base_url + codelist]

    def get_schema_obj(self, deref=False):
        schema_obj = self._schema_obj
        if self.extended_schema_file:
            with open(self.extended_schema_file) as fp:
                schema_obj = json.load(fp)
        elif self.extensions:
            schema_obj = deepcopy(self._schema_obj)
            self.apply_extensions(schema_obj)
        if deref:
            if self.extended:
                extended_schema_str = json.dumps(schema_obj)
                schema_obj = self.deref_schema(extended_schema_str)
            else:
                schema_obj = self.deref_schema(self.schema_str)
        return schema_obj

    def get_pkg_schema_obj(self, deref=False, use_extensions=True):
        package_schema_obj = deepcopy(self._pkg_schema_obj)
        if deref:
            if self.extended and use_extensions:

                if self.record_pkg:
                    package_schema_obj = self.deref_schema(self.pkg_schema_str)
                    deref_release_schema_obj = self.release_schema.get_schema_obj(deref=True)
                    package_schema_obj["properties"]["records"]["items"]["properties"][
                        "compiledRelease"
                    ] = deref_release_schema_obj
                    package_schema_obj["properties"]["records"]["items"]["properties"]["releases"]["oneOf"][
                        1
                    ] = deref_release_schema_obj
                else:
                    deref_schema_obj = self.get_schema_obj(deref=True)
                    package_schema_obj["properties"]["releases"]["items"] = {}
                    pkg_schema_str = json.dumps(package_schema_obj)
                    package_schema_obj = self.deref_schema(pkg_schema_str)
                    package_schema_obj["properties"]["releases"]["items"].update(deref_schema_obj)

            else:
                return self.deref_schema(self.pkg_schema_str)
        return package_schema_obj

    def apply_extensions(self, schema_obj):
        if not self.extensions:
            return
        for extensions_descriptor_url in self.extensions.keys():

            try:
                response = get_request(extensions_descriptor_url, config=self.config)
                if not response.ok:
                    # extension descriptor is required to proceed
                    self.invalid_extension[extensions_descriptor_url] = "{}: {}".format(
                        response.status_code, response.reason.lower()
                    )
                    continue
            except requests.exceptions.RequestException:
                self.invalid_extension[extensions_descriptor_url] = "fetching failed"
                continue

            i = extensions_descriptor_url.rfind("/")
            url = "{}/{}".format(extensions_descriptor_url[:i], "release-schema.json")

            try:
                extension = get_request(url, config=self.config)
            except requests.exceptions.RequestException:
                continue

            if extension.ok:
                try:
                    extension_data = extension.json()
                except ValueError:  # would be json.JSONDecodeError for Python 3.5+
                    self.invalid_extension[extensions_descriptor_url] = "release schema invalid JSON"
                    continue
            elif extension.status_code == 404:
                url = None
                extension_data = {}
            else:
                self.invalid_extension[extensions_descriptor_url] = "{}: {}".format(
                    extension.status_code, extension.reason.lower()
                )
                continue

            schema_obj = json_merge_patch.merge(schema_obj, extension_data)
            try:
                response = get_request(extensions_descriptor_url, config=self.config)
                extensions_descriptor = response.json()

            except ValueError:  # would be json.JSONDecodeError for Python 3.5+
                self.invalid_extension[extensions_descriptor_url] = "invalid JSON"
                continue
            cur_language = self.config.config["current_language"]

            extension_description = {"url": extensions_descriptor_url, "schema_url": url}

            for field in ["description", "name", "documentationUrl"]:
                field_object = extensions_descriptor.get(field, {})
                if isinstance(field_object, str):
                    field_value = field_object
                else:
                    field_value = field_object.get(cur_language)
                    if not field_value:
                        field_value = field_object.get("en", "")
                extension_description[field] = field_value
            extension_description["failed_codelists"] = {}
            codelists = extensions_descriptor.get("codelists")
            if codelists:
                extension_description["codelists"] = codelists

            self.extensions[extensions_descriptor_url] = extension_description
            self.extended = True

    def create_extended_schema_file(self, upload_dir, upload_url):
        filepath = os.path.join(upload_dir, "extended_schema.json")

        # Always replace any existing extended schema file
        if os.path.exists(filepath):
            os.remove(filepath)
            self.extended_schema_file = None
            self.extended_schema_url = None

        if not self.extensions:
            return

        schema_obj = self.get_schema_obj()
        if not self.extended:
            return

        with open(filepath, "w") as fp:
            schema_str = json.dumps(schema_obj, indent=4)
            fp.write(schema_str)

        self.extended_schema_file = filepath
        self.extended_schema_url = urljoin(upload_url, "extended_schema.json")
