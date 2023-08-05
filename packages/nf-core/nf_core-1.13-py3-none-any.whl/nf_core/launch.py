#!/usr/bin/env python
""" Launch a pipeline, interactively collecting params """

from __future__ import print_function
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Confirm

import copy
import json
import logging
import os
import questionary
import re
import subprocess
import webbrowser

import nf_core.schema, nf_core.utils

log = logging.getLogger(__name__)


class Launch(object):
    """ Class to hold config option to launch a pipeline """

    def __init__(
        self,
        pipeline=None,
        revision=None,
        command_only=False,
        params_in=None,
        params_out=None,
        save_all=False,
        show_hidden=False,
        url=None,
        web_id=None,
    ):
        """Initialise the Launcher class

        Args:
          schema: An nf_core.schema.PipelineSchema() object
        """

        self.pipeline = pipeline
        self.pipeline_revision = revision
        self.schema_obj = None
        self.use_params_file = False if command_only else True
        self.params_in = params_in
        self.params_out = params_out if params_out else os.path.join(os.getcwd(), "nf-params.json")
        self.save_all = save_all
        self.show_hidden = show_hidden
        self.web_schema_launch_url = url if url else "https://nf-co.re/launch"
        self.web_schema_launch_web_url = None
        self.web_schema_launch_api_url = None
        self.web_id = web_id
        if self.web_id:
            self.web_schema_launch_web_url = "{}?id={}".format(self.web_schema_launch_url, web_id)
            self.web_schema_launch_api_url = "{}?id={}&api=true".format(self.web_schema_launch_url, web_id)
        self.nextflow_cmd = "nextflow run {}".format(self.pipeline)

        # Prepend property names with a single hyphen in case we have parameters with the same ID
        self.nxf_flag_schema = {
            "coreNextflow": {
                "title": "Nextflow command-line flags",
                "type": "object",
                "description": "General Nextflow flags to control how the pipeline runs.",
                "help_text": "These are not specific to the pipeline and will not be saved in any parameter file. They are just used when building the `nextflow run` launch command.",
                "properties": {
                    "-name": {
                        "type": "string",
                        "description": "Unique name for this nextflow run",
                        "help_text": "If not specified, Nextflow will automatically generate a random mnemonic.",
                        "pattern": "^[a-zA-Z0-9-_]+$",
                    },
                    "-profile": {"type": "string", "description": "Configuration profile"},
                    "-work-dir": {
                        "type": "string",
                        "description": "Work directory for intermediate files",
                        "default": os.getenv("NXF_WORK") if os.getenv("NXF_WORK") else "./work",
                    },
                    "-resume": {
                        "type": "boolean",
                        "description": "Resume previous run, if found",
                        "help_text": "Execute the script using the cached results, useful to continue executions that was stopped by an error",
                        "default": False,
                    },
                },
            }
        }
        self.nxf_flags = {}
        self.params_user = {}
        self.cli_launch = True

    def launch_pipeline(self):

        # Check that we have everything we need
        if self.pipeline is None and self.web_id is None:
            log.error(
                "Either a pipeline name or web cache ID is required. Please see nf-core launch --help for more information."
            )
            return False

        # Check if the output file exists already
        if os.path.exists(self.params_out):
            log.warning("Parameter output file already exists! {}".format(os.path.relpath(self.params_out)))
            if Confirm.ask("[yellow]Do you want to overwrite this file?"):
                os.remove(self.params_out)
                log.info("Deleted {}\n".format(self.params_out))
            else:
                log.info("Exiting. Use --params-out to specify a custom filename.")
                return False

        log.info("This tool ignores any pipeline parameter defaults overwritten by Nextflow config files or profiles\n")

        # Check if we have a web ID
        if self.web_id is not None:
            self.schema_obj = nf_core.schema.PipelineSchema()
            try:
                if not self.get_web_launch_response():
                    log.info(
                        "Waiting for form to be completed in the browser. Remember to click Finished when you're done."
                    )
                    log.info("URL: {}".format(self.web_schema_launch_web_url))
                    nf_core.utils.wait_cli_function(self.get_web_launch_response)
            except AssertionError as e:
                log.error(e.args[0])
                return False

            # Load local params if supplied
            self.set_schema_inputs()
            # Load schema defaults
            self.schema_obj.get_schema_defaults()

        # No --id supplied, fetch parameter inputs
        else:
            # Build the schema and starting inputs
            if self.get_pipeline_schema() is False:
                return False
            self.set_schema_inputs()
            self.merge_nxf_flag_schema()

            # Collect user inputs via web or cli
            if self.prompt_web_gui():
                try:
                    self.launch_web_gui()
                except AssertionError as e:
                    log.error(e.args[0])
                    return False
            else:
                # Kick off the interactive wizard to collect user inputs
                self.prompt_schema()

        # Validate the parameters that we now have
        if not self.schema_obj.validate_params():
            return False

        # Strip out the defaults
        if not self.save_all:
            self.strip_default_params()

        # Build and launch the `nextflow run` command
        self.build_command()
        self.launch_workflow()

    def get_pipeline_schema(self):
        """ Load and validate the schema from the supplied pipeline """

        # Set up the schema
        self.schema_obj = nf_core.schema.PipelineSchema()

        # Check if this is a local directory
        if os.path.exists(self.pipeline):
            # Set the nextflow launch command to use full paths
            self.nextflow_cmd = "nextflow run {}".format(os.path.abspath(self.pipeline))
        else:
            # Assume nf-core if no org given
            if self.pipeline.count("/") == 0:
                self.nextflow_cmd = "nextflow run nf-core/{}".format(self.pipeline)
            # Add revision flag to commands if set
            if self.pipeline_revision:
                self.nextflow_cmd += " -r {}".format(self.pipeline_revision)

        # Get schema from name, load it and lint it
        try:
            self.schema_obj.get_schema_path(self.pipeline, revision=self.pipeline_revision)
            self.schema_obj.load_lint_schema()
        except AssertionError:
            # No schema found
            # Check that this was actually a pipeline
            if self.schema_obj.pipeline_dir is None or not os.path.exists(self.schema_obj.pipeline_dir):
                log.error("Could not find pipeline: {} ({})".format(self.pipeline, self.schema_obj.pipeline_dir))
                return False
            if not os.path.exists(os.path.join(self.schema_obj.pipeline_dir, "nextflow.config")) and not os.path.exists(
                os.path.join(self.schema_obj.pipeline_dir, "main.nf")
            ):
                log.error("Could not find a main.nf or nextfow.config file, are you sure this is a pipeline?")
                return False

            # Build a schema for this pipeline
            log.info("No pipeline schema found - creating one from the config")
            try:
                self.schema_obj.get_wf_params()
                self.schema_obj.make_skeleton_schema()
                self.schema_obj.remove_schema_notfound_configs()
                self.schema_obj.add_schema_found_configs()
                self.schema_obj.get_schema_defaults()
            except AssertionError as e:
                log.error("Could not build pipeline schema: {}".format(e))
                return False

    def set_schema_inputs(self):
        """
        Take the loaded schema and set the defaults as the input parameters
        If a nf_params.json file is supplied, apply these over the top
        """
        # Set the inputs to the schema defaults unless already set by --id
        if len(self.schema_obj.input_params) == 0:
            self.schema_obj.input_params = copy.deepcopy(self.schema_obj.schema_defaults)

        # If we have a params_file, load and validate it against the schema
        if self.params_in:
            log.info("Loading {}".format(self.params_in))
            self.schema_obj.load_input_params(self.params_in)
            self.schema_obj.validate_params()

    def merge_nxf_flag_schema(self):
        """ Take the Nextflow flag schema and merge it with the pipeline schema """
        # Add the coreNextflow subschema to the schema definitions
        if "definitions" not in self.schema_obj.schema:
            self.schema_obj.schema["definitions"] = {}
        self.schema_obj.schema["definitions"].update(self.nxf_flag_schema)
        # Add the new defintion to the allOf key so that it's included in validation
        # Put it at the start of the list so that it comes first
        if "allOf" not in self.schema_obj.schema:
            self.schema_obj.schema["allOf"] = []
        self.schema_obj.schema["allOf"].insert(0, {"$ref": "#/definitions/coreNextflow"})

    def prompt_web_gui(self):
        """ Ask whether to use the web-based or cli wizard to collect params """
        log.info(
            "[magenta]Would you like to enter pipeline parameters using a web-based interface or a command-line wizard?"
        )
        question = {
            "type": "list",
            "name": "use_web_gui",
            "message": "Choose launch method",
            "choices": ["Web based", "Command line"],
            "default": "Web based",
        }
        answer = questionary.unsafe_prompt([question], style=nf_core.utils.nfcore_question_style)
        return answer["use_web_gui"] == "Web based"

    def launch_web_gui(self):
        """ Send schema to nf-core website and launch input GUI """

        content = {
            "post_content": "json_schema_launcher",
            "api": "true",
            "version": nf_core.__version__,
            "status": "waiting_for_user",
            "schema": json.dumps(self.schema_obj.schema),
            "nxf_flags": json.dumps(self.nxf_flags),
            "input_params": json.dumps(self.schema_obj.input_params),
            "cli_launch": True,
            "nextflow_cmd": self.nextflow_cmd,
            "pipeline": self.pipeline,
            "revision": self.pipeline_revision,
        }
        web_response = nf_core.utils.poll_nfcore_web_api(self.web_schema_launch_url, content)
        try:
            assert "api_url" in web_response
            assert "web_url" in web_response
            assert web_response["status"] == "recieved"
        except AssertionError:
            log.debug("Response content:\n{}".format(json.dumps(web_response, indent=4)))
            raise AssertionError(
                "Web launch response not recognised: {}\n See verbose log for full response (nf-core -v launch)".format(
                    self.web_schema_launch_url
                )
            )
        else:
            self.web_schema_launch_web_url = web_response["web_url"]
            self.web_schema_launch_api_url = web_response["api_url"]

        # Launch the web GUI
        log.info("Opening URL: {}".format(self.web_schema_launch_web_url))
        webbrowser.open(self.web_schema_launch_web_url)
        log.info("Waiting for form to be completed in the browser. Remember to click Finished when you're done.\n")
        nf_core.utils.wait_cli_function(self.get_web_launch_response)

    def get_web_launch_response(self):
        """
        Given a URL for a web-gui launch response, recursively query it until results are ready.
        """
        web_response = nf_core.utils.poll_nfcore_web_api(self.web_schema_launch_api_url)
        if web_response["status"] == "error":
            raise AssertionError("Got error from launch API ({})".format(web_response.get("message")))
        elif web_response["status"] == "waiting_for_user":
            return False
        elif web_response["status"] == "launch_params_complete":
            log.info("Found completed parameters from nf-core launch GUI")
            try:
                # Set everything that we can with the cache results
                # NB: If using web builder, may have only run with --id and nothing else
                if len(web_response["nxf_flags"]) > 0:
                    self.nxf_flags = web_response["nxf_flags"]
                if len(web_response["input_params"]) > 0:
                    self.schema_obj.input_params = web_response["input_params"]
                self.schema_obj.schema = web_response["schema"]
                self.cli_launch = web_response["cli_launch"]
                self.nextflow_cmd = web_response["nextflow_cmd"]
                self.pipeline = web_response["pipeline"]
                self.pipeline_revision = web_response["revision"]
                # Sanitise form inputs, set proper variable types etc
                self.sanitise_web_response()
            except KeyError as e:
                raise AssertionError("Missing return key from web API: {}".format(e))
            except Exception as e:
                log.debug(web_response)
                raise AssertionError(
                    "Unknown exception ({}) - see verbose log for details. {}".format(type(e).__name__, e)
                )
            return True
        else:
            log.debug("Response content:\n{}".format(json.dumps(web_response, indent=4)))
            raise AssertionError(
                "Web launch GUI returned unexpected status ({}): {}\n See verbose log for full response".format(
                    web_response["status"], self.web_schema_launch_api_url
                )
            )

    def sanitise_web_response(self):
        """
        The web builder returns everything as strings.
        Use the functions defined in the cli wizard to convert to the correct types.
        """
        # Collect questionary objects for each defined input_param
        questionary_objects = {}
        for param_id, param_obj in self.schema_obj.schema.get("properties", {}).items():
            questionary_objects[param_id] = self.single_param_to_questionary(param_id, param_obj, print_help=False)

        for d_key, definition in self.schema_obj.schema.get("definitions", {}).items():
            for param_id, param_obj in definition.get("properties", {}).items():
                questionary_objects[param_id] = self.single_param_to_questionary(param_id, param_obj, print_help=False)

        # Go through input params and sanitise
        for params in [self.nxf_flags, self.schema_obj.input_params]:
            for param_id in list(params.keys()):
                # Remove if an empty string
                if str(params[param_id]).strip() == "":
                    del params[param_id]
                    continue
                # Run filter function on value
                filter_func = questionary_objects.get(param_id, {}).get("filter")
                if filter_func is not None:
                    params[param_id] = filter_func(params[param_id])

    def prompt_schema(self):
        """ Go through the pipeline schema and prompt user to change defaults """
        answers = {}
        # Start with the subschema in the definitions - use order of allOf
        for allOf in self.schema_obj.schema.get("allOf", []):
            d_key = allOf["$ref"][14:]
            answers.update(self.prompt_group(d_key, self.schema_obj.schema["definitions"][d_key]))

        # Top level schema params
        for param_id, param_obj in self.schema_obj.schema.get("properties", {}).items():
            if not param_obj.get("hidden", False) or self.show_hidden:
                is_required = param_id in self.schema_obj.schema.get("required", [])
                answers = self.prompt_param(param_id, param_obj, is_required, answers)

        # Split answers into core nextflow options and params
        for key, answer in answers.items():
            if key in self.nxf_flag_schema["coreNextflow"]["properties"]:
                self.nxf_flags[key] = answer
            else:
                self.params_user[key] = answer

        # Update schema with user params
        self.schema_obj.input_params.update(self.params_user)

    def prompt_param(self, param_id, param_obj, is_required, answers):
        """Prompt for a single parameter"""

        # Print the question
        question = self.single_param_to_questionary(param_id, param_obj, answers)
        answer = questionary.unsafe_prompt([question], style=nf_core.utils.nfcore_question_style)

        # If required and got an empty reponse, ask again
        while type(answer[param_id]) is str and answer[param_id].strip() == "" and is_required:
            log.error("'–-{}' is required".format(param_id))
            answer = questionary.unsafe_prompt([question], style=nf_core.utils.nfcore_question_style)

        # Ignore if empty
        if answer[param_id] == "":
            answer = {}

        # Previously entered something but this time we deleted it
        if param_id not in answer and param_id in answers:
            answers.pop(param_id)
        # Everything else (first time answer no response or normal response)
        else:
            answers.update(answer)

        return answers

    def prompt_group(self, group_id, group_obj):
        """
        Prompt for edits to a group of parameters (subschema in 'definitions')

        Args:
          group_id: Paramater ID (string)
          group_obj: JSON Schema keys (dict)

        Returns:
          Dict of param_id:val answers
        """
        while_break = False
        answers = {}
        error_msgs = []
        while not while_break:

            if len(error_msgs) == 0:
                self.print_param_header(group_id, group_obj, True)

            question = {
                "type": "list",
                "name": group_id,
                "qmark": "",
                "message": "",
                "instruction": " ",
                "choices": ["Continue >>", questionary.Separator()],
            }

            # Show error messages if we have any
            for msg in error_msgs:
                question["choices"].append(
                    questionary.Choice(
                        [("bg:ansiblack fg:ansired bold", " error "), ("fg:ansired", f" - {msg}")], disabled=True
                    )
                )
            error_msgs = []

            for param_id, param in group_obj["properties"].items():
                if not param.get("hidden", False) or self.show_hidden:
                    q_title = [("", "{}  ".format(param_id))]
                    # If already filled in, show value
                    if param_id in answers and answers.get(param_id) != param.get("default"):
                        q_title.append(("class:choice-default-changed", "[{}]".format(answers[param_id])))
                    # If the schema has a default, show default
                    elif "default" in param:
                        q_title.append(("class:choice-default", "[{}]".format(param["default"])))
                    # Show that it's required if not filled in and no default
                    elif param_id in group_obj.get("required", []):
                        q_title.append(("class:choice-required", "(required)"))
                    question["choices"].append(questionary.Choice(title=q_title, value=param_id))

            # Skip if all questions hidden
            if len(question["choices"]) == 2:
                return {}

            answer = questionary.unsafe_prompt([question], style=nf_core.utils.nfcore_question_style)
            if answer[group_id] == "Continue >>":
                while_break = True
                # Check if there are any required parameters that don't have answers
                for p_required in group_obj.get("required", []):
                    req_default = self.schema_obj.input_params.get(p_required, "")
                    req_answer = answers.get(p_required, "")
                    if req_default == "" and req_answer == "":
                        error_msgs.append(f"`{p_required}` is required")
                        while_break = False
            else:
                param_id = answer[group_id]
                is_required = param_id in group_obj.get("required", [])
                answers = self.prompt_param(param_id, group_obj["properties"][param_id], is_required, answers)

        return answers

    def single_param_to_questionary(self, param_id, param_obj, answers=None, print_help=True):
        """Convert a JSONSchema param to a Questionary question

        Args:
          param_id: Parameter ID (string)
          param_obj: JSON Schema keys (dict)
          answers: Optional preexisting answers (dict)
          print_help: If description and help_text should be printed (bool)

        Returns:
          Single Questionary dict, to be appended to questions list
        """
        if answers is None:
            answers = {}

        question = {"type": "input", "name": param_id, "message": ""}

        # Print the name, description & help text
        if print_help:
            nice_param_id = "--{}".format(param_id) if not param_id.startswith("-") else param_id
            self.print_param_header(nice_param_id, param_obj)

        if param_obj.get("type") == "boolean":
            question["type"] = "list"
            question["choices"] = ["True", "False"]
            question["default"] = "False"

        # Start with the default from the param object
        if "default" in param_obj:
            # Boolean default is cast back to a string later - this just normalises all inputs
            if param_obj["type"] == "boolean" and type(param_obj["default"]) is str:
                question["default"] = param_obj["default"].lower() == "true"
            else:
                question["default"] = param_obj["default"]

        # Overwrite default with parsed schema, includes --params-in etc
        if self.schema_obj is not None and param_id in self.schema_obj.input_params:
            if param_obj["type"] == "boolean" and type(self.schema_obj.input_params[param_id]) is str:
                question["default"] = "true" == self.schema_obj.input_params[param_id].lower()
            else:
                question["default"] = self.schema_obj.input_params[param_id]

        # Overwrite default if already had an answer
        if param_id in answers:
            question["default"] = answers[param_id]

        # Coerce default to a string
        if "default" in question:
            question["default"] = str(question["default"])

        if param_obj.get("type") == "boolean":
            # Filter returned value
            def filter_boolean(val):
                if isinstance(val, bool):
                    return val
                return val.lower() == "true"

            question["filter"] = filter_boolean

        if param_obj.get("type") == "number":
            # Validate number type
            def validate_number(val):
                try:
                    if val.strip() == "":
                        return True
                    fval = float(val)
                    if "minimum" in param_obj and fval < float(param_obj["minimum"]):
                        return "Must be greater than or equal to {}".format(param_obj["minimum"])
                    if "maximum" in param_obj and fval > float(param_obj["maximum"]):
                        return "Must be less than or equal to {}".format(param_obj["maximum"])
                except ValueError:
                    return "Must be a number"
                else:
                    return True

            question["validate"] = validate_number

            # Filter returned value
            def filter_number(val):
                if val.strip() == "":
                    return ""
                return float(val)

            question["filter"] = filter_number

        if param_obj.get("type") == "integer":
            # Validate integer type
            def validate_integer(val):
                try:
                    if val.strip() == "":
                        return True
                    assert int(val) == float(val)
                except (AssertionError, ValueError):
                    return "Must be an integer"
                else:
                    return True

            question["validate"] = validate_integer

            # Filter returned value
            def filter_integer(val):
                if val.strip() == "":
                    return ""
                return int(val)

            question["filter"] = filter_integer

        if "enum" in param_obj:
            # Use a selection list instead of free text input
            question["type"] = "list"
            question["choices"] = param_obj["enum"]

        # Validate pattern from schema
        if "pattern" in param_obj:

            def validate_pattern(val):
                if val == "":
                    return True
                if re.search(param_obj["pattern"], val) is not None:
                    return True
                return "Must match pattern: {}".format(param_obj["pattern"])

            question["validate"] = validate_pattern

        return question

    def print_param_header(self, param_id, param_obj, is_group=False):
        if "description" not in param_obj and "help_text" not in param_obj:
            return
        console = Console(force_terminal=nf_core.utils.rich_force_colors())
        console.print("\n")
        console.print("[bold blue]?[/] [bold on black] {} [/]".format(param_obj.get("title", param_id)))
        if "description" in param_obj:
            md = Markdown(param_obj["description"])
            console.print(md)
        if "help_text" in param_obj:
            help_md = Markdown(param_obj["help_text"].strip())
            console.print(help_md, style="dim")
        if is_group:
            console.print("(Use arrow keys)", style="italic", highlight=False)

    def strip_default_params(self):
        """ Strip parameters if they have not changed from the default """

        # Schema defaults
        for param_id, val in self.schema_obj.schema_defaults.items():
            if self.schema_obj.input_params.get(param_id) == val:
                del self.schema_obj.input_params[param_id]

        # Nextflow flag defaults
        for param_id, val in self.nxf_flag_schema["coreNextflow"]["properties"].items():
            if param_id in self.nxf_flags and self.nxf_flags[param_id] == val.get("default"):
                del self.nxf_flags[param_id]

    def build_command(self):
        """ Build the nextflow run command based on what we know """

        # Core nextflow options
        for flag, val in self.nxf_flags.items():
            # Boolean flags like -resume
            if isinstance(val, bool) and val:
                self.nextflow_cmd += " {}".format(flag)
            # String values
            elif not isinstance(val, bool):
                self.nextflow_cmd += ' {} "{}"'.format(flag, val.replace('"', '\\"'))

        # Pipeline parameters
        if len(self.schema_obj.input_params) > 0:

            # Write the user selection to a file and run nextflow with that
            if self.use_params_file:
                with open(self.params_out, "w") as fp:
                    json.dump(self.schema_obj.input_params, fp, indent=4)
                self.nextflow_cmd += ' {} "{}"'.format("-params-file", os.path.relpath(self.params_out))

            # Call nextflow with a list of command line flags
            else:
                for param, val in self.schema_obj.input_params.items():
                    # Boolean flags like --saveTrimmed
                    if isinstance(val, bool) and val:
                        self.nextflow_cmd += " --{}".format(param)
                    # everything else
                    else:
                        self.nextflow_cmd += ' --{} "{}"'.format(param, str(val).replace('"', '\\"'))

    def launch_workflow(self):
        """ Launch nextflow if required  """
        log.info("[bold underline]Nextflow command:[/]\n[magenta]{}\n\n".format(self.nextflow_cmd))

        if Confirm.ask("Do you want to run this command now? "):
            log.info("Launching workflow! :rocket:")
            subprocess.call(self.nextflow_cmd, shell=True)
