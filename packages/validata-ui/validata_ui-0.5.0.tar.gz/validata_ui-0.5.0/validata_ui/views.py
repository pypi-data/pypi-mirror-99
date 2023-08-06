"""Routes."""
import copy
import io
import json
import logging
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode, urljoin

import frictionless
import jsonschema
import requests
import validata_core
from commonmark import commonmark
from flask import (abort, make_response, redirect, render_template, request,
                   url_for)
from opendataschema import GitSchemaReference, by_commit_date
from validata_core.helpers import (FileContentValidataResource,
                                   URLValidataResource, ValidataResource,
                                   is_body_error, is_structure_error)

from . import app, config, fetch_schema, pdf_service, schema_catalog_registry
from .model import Section
from .ui_util import flash_error, flash_warning
from .validata_util import strip_accents

log = logging.getLogger(__name__)


def get_schema_catalog(section_name):
    """Return a schema catalog associated to a section_name."""
    return schema_catalog_registry.build_schema_catalog(section_name)


class SchemaInstance:
    """Handy class to handle schema information."""

    def __init__(self, parameter_dict):
        """Initialize schema instance and tableschema catalog."""
        self.section_name = None
        self.section_title = None
        self.name = None
        self.url = None
        self.ref = None
        self.reference = None
        self.doc_url = None
        self.branches = None
        self.tags = None

        # From schema_url
        if parameter_dict.get("schema_url"):
            self.url = parameter_dict["schema_url"]
            self.section_title = "Autre schéma"

        # from schema_name (and schema_ref)
        elif parameter_dict.get("schema_name"):
            self.schema_and_section_name = parameter_dict["schema_name"]
            self.ref = parameter_dict.get("schema_ref")

            # Check schema name
            chunks = self.schema_and_section_name.split(".")
            if len(chunks) != 2:
                abort(400, "Paramètre 'schema_name' invalide")

            self.section_name, self.name = chunks
            self.section_title = self.find_section_title(self.section_name)

            # Look for schema catalog first
            try:
                table_schema_catalog = get_schema_catalog(self.section_name)
            except Exception:
                log.exception("")
                abort(400, "Erreur de traitement du catalogue")
            if table_schema_catalog is None:
                abort(400, "Catalogue indisponible")

            schema_reference = table_schema_catalog.reference_by_name.get(self.name)
            if schema_reference is None:
                abort(
                    400,
                    f"Schéma {self.name!r} non trouvé dans le catalogue de la "
                    f"section {self.section_name!r}",
                )

            if isinstance(schema_reference, GitSchemaReference):
                self.tags = sorted(
                    schema_reference.iter_tags(), key=by_commit_date, reverse=True
                )
                if self.ref is None:
                    schema_ref = (
                        self.tags[0]
                        if self.tags
                        else schema_reference.get_default_branch()
                    )
                    abort(
                        redirect(
                            compute_validation_form_url(
                                {
                                    "schema_name": self.schema_and_section_name,
                                    "schema_ref": schema_ref.name,
                                }
                            )
                        )
                    )
                tag_names = [tag.name for tag in self.tags]
                self.branches = [
                    branch
                    for branch in schema_reference.iter_branches()
                    if branch.name not in tag_names
                ]
                self.doc_url = schema_reference.get_doc_url(
                    ref=self.ref
                ) or schema_reference.get_project_url(ref=self.ref)

            self.url = schema_reference.get_schema_url(ref=self.ref)

        else:
            flash_error("Erreur dans la récupération des informations de schéma")
            abort(redirect(url_for("home")))

        try:
            self.schema = fetch_schema(self.url)
        except json.JSONDecodeError:
            err_msg = "Le format du schéma n'est pas reconnu"
            log.exception(err_msg)
            flash_error(err_msg)
            abort(redirect(url_for("home")))
        except Exception:
            err_msg = "Impossible de récupérer le schéma"
            log.exception(err_msg)
            flash_error(err_msg)
            abort(redirect(url_for("home")))

    def request_parameters(self):
        """Build request parameter dict to identify schema."""
        return {
            "schema_name": self.schema_and_section_name,
            "schema_ref": "" if self.ref is None else self.ref,
        } if self.name else {"schema_url": self.url}

    def find_section_title(self, section_name):
        """Return section title or None if not found."""
        if config.CONFIG:
            for section in config.CONFIG.homepage.sections:
                if section.name == section_name:
                    return section.title
        return None


def build_template_source_data(header, rows, preview_rows_nb=5):
    """Build source data information to preview in validation report page."""
    source_header_info = [(colname, False) for colname in header]

    rows_count = len(rows)
    preview_rows_count = min(preview_rows_nb, rows_count)
    return {
        "source_header_info": source_header_info,
        "header": header,
        "rows_nb": rows_count,
        "data_rows": rows,
        "preview_rows_count": preview_rows_count,
        "preview_rows": rows[:preview_rows_count],
    }


def build_ui_errors(errors):
    """Add context to errors, converts markdown content to HTML."""

    def improve_err(err):
        """Add context info based on row-nb presence and converts content to HTML."""
        # Context
        update_keys = {
            "context": "body"
            if "row-number" in err and err["row-number"] is not None
            else "table",
        }

        # Set title
        if "title" not in err:
            update_keys["title"] = err["name"]

        # Set content
        content = "*content soon available*"
        if "message" in err:
            content = err["message"]
        elif "description" in err:
            content = err["description"]
        update_keys["content"] = commonmark(content)

        return {**err, **update_keys}

    return list(map(improve_err, errors))


def create_validata_ui_report(rows_count: int, validata_core_report, schema_dict):
    """Create an error report easier to handle and display using templates.

    improvements done:
    - only one table
    - errors are contextualized
    - error-counts is ok
    - errors are grouped by lines
    - errors are separated into "structure" and "body"
    - error messages are improved
    """
    v_report = copy.deepcopy(validata_core_report.to_dict())

    # Create a new UI report from information picked in validata report
    ui_report = {}
    ui_report["table"] = {}

    # source headers
    headers = v_report["tasks"][0]["resource"]["data"][0]
    ui_report["table"]["header"] = headers

    # source dimension
    ui_report["table"]["col_count"] = len(headers)
    ui_report["table"]["row_count"] = rows_count

    # Computes column info from schema
    fields_dict = {
        f["name"]: (f.get("title", f["name"]), f.get("description", ""))
        for f in schema_dict.get("fields", [])
    }
    ui_report["table"]["headers_title"] = [
        fields_dict[h][0] if h in fields_dict else "Colonne inconnue" for h in headers
    ]
    ui_report["table"]["headers_description"] = [
        fields_dict[h][1]
        if h in fields_dict
        else "Cette colonne n'est pas définie dans le schema"
        for h in headers
    ]
    v_report_table = v_report["tasks"][0]
    missing_headers = [
        err["message-data"]["column-name"]
        for err in v_report_table["errors"]
        if err["code"] == "missing-header"
    ]
    ui_report["table"]["cols_alert"] = [
        "table-danger" if h not in fields_dict or h in missing_headers else ""
        for h in headers
    ]

    # prepare error structure for UI needs
    errors = build_ui_errors(v_report_table["errors"])

    # Count errors and warnings
    ui_report["error_count"] = len(errors)
    ui_report["warn_count"] = len(v_report_table["structure_warnings"])
    ui_report["warnings"] = v_report_table["structure_warnings"]

    # Then group them in 2 groups : structure and body
    ui_report["table"]["errors"] = {"structure": [], "body": []}
    for err in errors:
        if is_structure_error(err):
            ui_report["table"]["errors"]["structure"].append(err)
        elif is_body_error(err):
            ui_report["table"]["errors"]["body"].append(err)

    # Group body errors by row id
    rows = []
    current_row_id = 0
    for err in ui_report["table"]["errors"]["body"]:
        if "rowPosition" not in err:
            continue
        row_id = err["rowPosition"]
        if row_id != current_row_id:
            current_row_id = row_id
            rows.append({"row_id": current_row_id, "errors": {}})

        column_id = err.get("fieldPosition")
        if column_id is not None:
            rows[-1]["errors"][column_id] = err
        else:
            rows[-1]["errors"]["row"] = err
    ui_report["table"]["errors"]["body_by_rows"] = rows

    # Sort by error names in statistics
    ui_report["table"]["count-by-code"] = {}
    stats = {}
    total_errors_count = 0
    for key in ("structure", "body"):
        # convert dict into tuples with french title instead of error code
        # and sorts by title
        key_errors = ui_report["table"]["errors"][key]
        key_errors_count = len(key_errors)
        ct = Counter(ke["name"] for ke in key_errors)

        error_stats = {
            "count": key_errors_count,
            "count-by-code": sorted((k, v) for k, v in ct.items()),
        }
        total_errors_count += key_errors_count

        # Add error rows count
        if key == "body":
            error_rows = {
                err["rowPosition"] for err in key_errors if "rowPosition" in err
            }
            error_stats["rows-count"] = len(error_rows)

        stats[f"{key}-errors"] = error_stats

    stats["count"] = total_errors_count
    ui_report["table"]["error-stats"] = stats

    return ui_report


def compute_badge_message_and_color(badge):
    """Compute message and color from badge information."""
    structure = badge["structure"]
    body = badge.get("body")

    # Bad structure, stop here
    if structure == "KO":
        return ("structure invalide", "red")

    # No body error
    if body == "OK":
        return (
            ("partiellement valide", "yellowgreen")
            if structure == "WARN"
            else ("valide", "green")
        )

    # else compute quality ratio percent
    p = (1 - badge["error-ratio"]) * 100.0
    msg = "cellules valides : {:.1f}%".format(p)
    return (msg, "red") if body == "KO" else (msg, "orange")


def get_badge_url_and_message(badge):
    """Get badge url from badge information."""
    msg, color = compute_badge_message_and_color(badge)
    badge_url = "{}?{}".format(
        urljoin(config.SHIELDS_IO_BASE_URL, "/static/v1.svg"),
        urlencode({"label": "Validata", "message": msg, "color": color}),
    )
    return (badge_url, msg)


def validate(schema_instance: SchemaInstance, validata_resource: ValidataResource):
    """Validate source and display report."""
    def compute_resource_info(resource: ValidataResource):
        source = resource.get_source()
        return {
            "type": "url" if source.startswith("http") else "file",
            "url": source,
            "filename": Path(source).name,
        }

    # Parse source data once
    header, rows = validata_resource.extract_tabular_data()
    rows_count = len(rows)

    # Call validata_core with parsed data
    validata_core_report = validata_core.validate(
        [header] + rows, schema_instance.schema
    )

    # disable badge
    badge_config = config.BADGE_CONFIG

    # Computes badge from report and badge configuration
    badge_url, badge_msg = None, None
    display_badge = badge_config and config.SHIELDS_IO_BASE_URL
    if display_badge:
        badge_stats = validata_core.compute_badge_metrics(
            validata_core_report, badge_config
        )
        if badge_stats:
            badge_url, badge_msg = get_badge_url_and_message(badge_stats)

    # Non table errors
    if validata_core_report["errors"]:
        non_table_error = validata_core_report["errors"][0]
        msg = non_table_error.message
        log.error(msg)
        ui_error_msg = f"Une erreur est survenue durant la validation : {msg}"
        if msg.startswith("The validation task has an error"):
            ui_error_msg = (
                "La validation ne peut s'effectuer sur ce fichier, "
                "celui-ci n'est pas compatible avec le schéma."
            )
        flash_error(ui_error_msg)
        return redirect(
            compute_validation_form_url(schema_instance.request_parameters())
        )

    # Source error
    source_errors = [
        err
        for err in validata_core_report["tasks"][0]["errors"]
        if err["code"] in {"source-error", "unknown-csv-dialect"}
    ]
    if source_errors:
        err = source_errors[0]
        msg = (
            "l'encodage du fichier est invalide. Veuillez le corriger"
            if "charmap" in err["message"]
            else err["message"]
        )
        flash_error("Erreur de source : {}".format(msg))
        return redirect(url_for("custom_validator"))

    # handle report date
    report_datetime = datetime.fromisoformat(validata_core_report["date"]).astimezone()

    # create ui_report
    ui_report = create_validata_ui_report(
        rows_count, validata_core_report, schema_instance.schema
    )

    # Display report to the user
    validator_form_url = compute_validation_form_url(
        schema_instance.request_parameters()
    )
    schema_info = compute_schema_info(schema_instance.schema, schema_instance.url)

    # Build PDF report URL
    # PDF report is available if:
    # - a pdf_service has been configured
    # - tabular resource to validate is defined as an URL
    pdf_report_url = None
    if pdf_service and isinstance(validata_resource, URLValidataResource):
        base_url = url_for("pdf_report")
        query_string = urlencode(
            {
                **schema_instance.request_parameters(),
                "url": validata_resource.url,
            }
        )
        pdf_report_url = f"{base_url}?{query_string}"

    return render_template(
        "validation_report.html",
        config=config.CONFIG,
        badge_msg=badge_msg,
        badge_url=badge_url,
        breadcrumbs=[
            {"title": "Accueil", "url": url_for("home")},
            {"title": schema_instance.section_title},
            {"title": schema_info["title"], "url": validator_form_url},
            {"title": "Rapport de validation"},
        ],
        display_badge=display_badge,
        doc_url=schema_instance.doc_url,
        pdf_report_url=pdf_report_url,
        print_mode=request.args.get("print", "false") == "true",
        report=ui_report,
        schema_current_version=schema_instance.ref,
        schema_info=schema_info,
        section_title=schema_instance.section_title,
        source_data=build_template_source_data(header, rows),
        resource=compute_resource_info(validata_resource),
        validation_date=report_datetime.strftime("le %d/%m/%Y à %Hh%M"),
    )


def bytes_data(f):
    """Get bytes data from Werkzeug FileStorage instance."""
    iob = io.BytesIO()
    f.save(iob)
    iob.seek(0)
    return iob.getvalue()


def retrieve_schema_catalog(section: Section):
    """Retrieve schema catalog and return formatted error if it fails."""

    def format_error_message(err_message, exc):
        """Prepare a bootstrap error message with details if wanted."""
        exception_text = "\n".join([str(arg) for arg in exc.args])

        return f"""{err_msg}
        <div class="float-right">
            <button type="button" class="btn btn-info btn-xs" data-toggle="collapse"
                data-target="#exception_info">détails</button>
        </div>
        <div id="exception_info" class="collapse">
                <pre>{exception_text}</pre>
        </div>
"""

    try:
        schema_catalog = get_schema_catalog(section.name)
        return (schema_catalog, None)

    except Exception as exc:
        err_msg = "une erreur s'est produite"
        if isinstance(exc, requests.ConnectionError):
            err_msg = "problème de connexion"
        elif isinstance(exc, json.decoder.JSONDecodeError):
            err_msg = "format JSON incorrect"
        elif isinstance(exc, jsonschema.exceptions.ValidationError):
            err_msg = "le catalogue ne respecte pas le schéma de référence"
        log.exception(err_msg)

        error_catalog = {
            **{k: v for k, v in section.dict().items() if k != "catalog"},
            "err": format_error_message(err_msg, exc),
        }
        return None, error_catalog


# Routes


@app.route("/")
def home():
    """Home page."""

    def iter_sections():
        """Yield sections of the home page, filled with schema metadata."""
        # Iterate on all sections
        for section in config.CONFIG.homepage.sections:

            # section with only links to external validators
            if section.links:
                yield section
                continue

            # section with catalog
            if section.catalog is None:
                # skip section
                continue

            # retrieving schema catatalog
            schema_catalog, catalog_error = retrieve_schema_catalog(section)
            if schema_catalog is None:
                yield catalog_error
                continue

            # Working on catalog
            schema_info_list = []
            for schema_reference in schema_catalog.references:
                # retain tableschema only
                if schema_reference.get_schema_type() != "tableschema":
                    continue
                # Loads default table schema for each schema reference
                schema_info = {"name": schema_reference.name}
                try:
                    table_schema = fetch_schema(schema_reference.get_schema_url())
                except json.JSONDecodeError:
                    schema_info["err"] = True
                    schema_info["title"] = (
                        f"le format du schéma « {schema_info['name']} » "
                        "n'est pas reconnu"
                    )
                except Exception:
                    schema_info["err"] = True
                    schema_info["title"] = (
                        f"le schéma « {schema_info['name']} » " "n'est pas disponible"
                    )
                else:
                    schema_info["title"] = (
                        table_schema.get("title") or schema_info["name"]
                    )
                schema_info_list.append(schema_info)
            schema_info_list = sorted(
                schema_info_list, key=lambda sc: strip_accents(sc["title"].lower())
            )

            yield {
                **{k: v for k, v in section.dict().items() if k != "catalog"},
                "catalog": schema_info_list,
            }

    return render_template(
        "home.html", config=config.CONFIG, sections=list(iter_sections())
    )


@app.route("/pdf")
def pdf_report():
    """PDF report generation."""
    err_prefix = "Erreur de génération du rapport PDF"

    url_param = request.args.get("url")
    if not url_param:
        flash_error(err_prefix + " : URL non fournie")
        return redirect(url_for("home"))

    if pdf_service is None:
        flash_error(err_prefix + " : service de génération non configuré")
        return redirect(url_for("home"))

    # Compute validation report URL
    schema_instance = SchemaInstance(request.args)

    base_url = url_for("custom_validator", _external=True)
    parameter_dict = {
        "input": "url",
        "print": "true",
        "url": url_param,
        **schema_instance.request_parameters(),
    }
    validation_url = "{}?{}".format(base_url, urlencode(parameter_dict))
    log.info("Validation URL = %s", validation_url)

    # Ask for PDF report generation
    try:
        pdf_bytes_content = pdf_service.render(validation_url)
    except Exception:
        log.exception(err_prefix)
        flash_error(err_prefix + " : contactez votre administrateur")
        return redirect(url_for("home"))

    # Compute pdf filename
    pdf_filename = "Rapport de validation {}.pdf".format(
        datetime.now().strftime("%d-%m-%Y %Hh%M")
    )

    # Prepare and send response
    response = make_response(pdf_bytes_content)
    response.headers.set("Content-Disposition", "attachment", filename=pdf_filename)
    response.headers.set("Content-Length", len(pdf_bytes_content))
    response.headers.set("Content-Type", "application/pdf")
    return response


def extract_schema_metadata(table_schema: frictionless.Schema):
    """Get author, contibutor, version...metadata from schema header."""
    return {k: v for k, v in table_schema.items() if k != "fields"}


def compute_schema_info(table_schema: frictionless.Schema, schema_url):
    """Factor code for validator form page."""
    # Schema URL + schema metadata info
    schema_info = {
        "path": schema_url,
        # a "path" metadata property can be found in Table Schema,
        # and we'd like it to override the `schema_url`
        # given by the user (in case schema was given by URL)
        **extract_schema_metadata(table_schema),
    }
    return schema_info


def compute_validation_form_url(request_parameters: dict):
    """Compute validation form url with schema URL parameter."""
    url = url_for("custom_validator")
    return "{}?{}".format(url, urlencode(request_parameters))


@app.route("/table-schema", methods=["GET", "POST"])
def custom_validator():
    """Display validator form."""
    if request.method == "GET":

        # input is a hidden form parameter to know
        # if this is the initial page display or if the validation has been asked for
        input_param = request.args.get("input")

        # url of resource to be validated
        url_param = request.args.get("url")

        schema_instance = SchemaInstance(request.args)

        # First form display
        if input_param is None:
            schema_info = compute_schema_info(
                schema_instance.schema, schema_instance.url
            )
            return render_template(
                "validation_form.html",
                config=config.CONFIG,
                branches=schema_instance.branches,
                breadcrumbs=[
                    {"url": url_for("home"), "title": "Accueil"},
                    {"title": schema_instance.section_title},
                    {"title": schema_info["title"]},
                ],
                doc_url=schema_instance.doc_url,
                schema_current_version=schema_instance.ref,
                schema_info=schema_info,
                schema_params=schema_instance.request_parameters(),
                section_title=schema_instance.section_title,
                tags=schema_instance.tags,
            )

        # Process URL
        else:
            validation_form_url = compute_validation_form_url(
                schema_instance.request_parameters()
            )

            if not url_param:
                flash_error("Vous n'avez pas indiqué d'URL à valider")
                return redirect(validation_form_url)
            try:
                return validate(schema_instance, URLValidataResource(url_param))
            except frictionless.FrictionlessException as ex:
                flash_error(ex.error.message)
                return redirect(validation_form_url)

    elif request.method == "POST":

        schema_instance = SchemaInstance(request.form)

        input_param = request.form.get("input")
        if input_param is None:
            flash_error("Vous n'avez pas indiqué de fichier à valider")
            return redirect(
                compute_validation_form_url(schema_instance.request_parameters())
            )

        # File validation
        if input_param == "file":
            f = request.files.get("file")
            if f is None:
                flash_warning("Vous n'avez pas indiqué de fichier à valider")
                return redirect(
                    compute_validation_form_url(schema_instance.request_parameters())
                )
            return validate(
                schema_instance, FileContentValidataResource(f.filename, bytes_data(f))
            )

        return "Combinaison de paramètres non supportée", 400

    else:
        return "Method not allowed", 405
