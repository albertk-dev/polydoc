# PolyDoc API Documentation

Welcome to the PolyDoc API! This document explains how to use the endpoints to generate your documents.

## Main Endpoint

### `POST /generate/{format}`

This is the primary endpoint for document generation.

* `{format}`: The desired output format. Currently supported: `pdf`, `docx`.

#### Request Body

The request must be of type `multipart/form-data` and contain two parts:

1.  `content` (text): The raw Markdown content for the document.
2.  `options` (text): A JSON string containing conversion and styling options.

#### `options` JSON Object

The `options` object can contain the following keys:

| Key | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `metadata` | `object` | Document metadata. | `{"title": "Rapport", "author": "Mon Nom"}` |
| `header` | `string` | Text for the page header. | `"Rapport Mensuel"` |
| `footer` | `string` | Text for the page footer. | `"Page %p / %t"` |
| `pagination`| `boolean`| Enables page numbering (`true`/`false`). | `true` |
| `toc` | `boolean`| Generates a Table of Contents (`true`/`false`). | `true` |
| `lof` | `boolean`| Generates a List of Figures (`true`/`false`). | `true` |
| `margins` | `object`| Page margins (`top`, `bottom`, `left`, `right`). | `{"top": "2cm", "left": "2.5cm"}` |
| `orientation`| `string`| Page orientation (`portrait` or `landscape`). | `"landscape"` |
| `fontSize` | `number`| Main font size. | `12` |
| `fontFamily`| `string`| Main font family (must be installed). | `"Lato"` |

#### Example Usage with `curl`

Here's how to generate a PDF using `curl`:

```bash
curl -X POST http://localhost:4444/generate/pdf \
-F "content=# Hello World" \
-F "options={\"toc\": true, \"margins\": {\"top\": \"2cm\"}}" \
--output generated_document.pdf
```

This command sends a simple Markdown title and an `options` JSON to generate a PDF with a table of contents and a 2cm top margin, saving the result to `generated_document.pdf`.