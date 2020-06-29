# WAHerb

A Django prototype to manage herbarium collection data and taxonomic information.

Requires Python 3.7+. Manage project virtual environment and dependencies using
`Poetry`.

Example:

~~~bash
poetry install
poetry run python manage.py check
~~~

Define project-local variables in a `.env` file. As a minimum we need `DATABASE_URL`.
`GEOSERVER_WMS_URL` is also needed to display spatial data on the Naturemap map
widget.

# Project application descriptions

## nomenclature

This application is intended to be a repository of scientific names (either the
source of truth, or a local cache of another source e.g. APNI), plus literature
references for those names. It is envisaged that other internal applications
would reference these names as lookups.

This application also represents the taxonomic tree of names via `django-mptt`;
names have an optional taxonomic parent recorded, which can then be used to
define the tree of taxonomic relationships.

## herbarium

This application is a prototype repository of Herbarium specimen data. It may be
used to migrate data from the legacy Texpress database and to manage data.

## crossreference

This application is an experiment to prototype the ability to generate a graph
database style "edge" between any two object types in this project, using the
Django ContentType and GenericForeignKey. Each `CrossReference` object
represents a single "edge" between two objects.

For any `CrossReference` object a "source" object is defined (`content_type` and
`object_id`), a "target" object is defined (`target_content_type` and
`target_object_id`), and the "reference type" between them (`ref_type`) is defined.
The reference type is the "label" in graph database terms. Optional metadata about
the edge may be recorded in the JSON field.

## naturemap

This application is a prototype search interface for migrated Naturemap data in
order to test the performance/practicality of using PostgreSQL text search to
serve Naturemap data in a browser. It consists of a couple of API endpoints to
expose species name information and a basic map widget to allow searching on
that data.

## graphic

This application is another prototype to represent a graph database in a RDMS
such as PostgreSQL, using the Django ContentType mechanism. `Node` objects can
be created by defining a link to another database object (using `content_type`
and `object_id` as normal). `Edge` objects can then be defined by creating an
object that contains a link to `source` and `target` nodes, plus the `type` of
edge.

This application exposes a couple of API endpoints, but is not intended to be
editable using the Django admin interface.
