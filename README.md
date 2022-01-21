# WAHerb

A Django prototype to manage herbarium collection data and taxonomic information.

Requires Python 3.7+ and PostgreSQL 11+ with `postgis` and `pg_trgm` extensions
installed. Manage project virtual environment and dependencies using `Poetry`.

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

To import data from WACensus into this application, you need to generate three
CSV files from WACensus data and save them to the project root (column headings
are shown below to indicate the required schema):

1. `kingdoms.csv` - KINGDOM_NAME (list of all Kingdoms)
1. `names.csv` - NAME,TAXONOMIC_RANK,KINGDOM,NAME_ID (list of all taxa)
1. `taxon_tree.csv`- NAME,PARENT_NAME

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
