# Product Browser API

## Overview

A scalable product browsing API built using FastAPI, PostgreSQL (Neon), and SQLAlchemy.

## Features

* Product listing
* Category filtering
* Cursor-based pagination
* Product details endpoint
* PostgreSQL database
* Swagger API documentation
* Database indexing for performance

## Tech Stack

* FastAPI
* PostgreSQL (Neon)
* SQLAlchemy
* Faker

## API Endpoints

### GET /

Health endpoint.

### GET /health

Returns API status.

### GET /products

Supports:

* page_size
* category
* cursor

Example:

/products?page_size=50

/products?category=electronics

/products?cursor=2026-06-22T17:04:13

### GET /products/{id}

Returns details of a single product.

## Why Cursor Pagination?

Offset pagination can produce duplicate or skipped records when new products are added while users are browsing.

Cursor pagination ensures stable and consistent navigation through large datasets.
