# PolyDoc Service 🚀

**PolyDoc** is a powerful API for generating documents (PDF, DOCX, etc.) from various sources like Markdown.

## Prerequisites

* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## 🚀 Getting Started

This project is fully containerized, so no local installation of Python or LaTeX is required.

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd PolyDoc
    ```

2.  **Build and run the service:**
    The service is managed by Docker Compose. To build the image and start the service, run:
    ```bash
    docker-compose up --build
    ```
    The API will be available at `http://localhost:4444`.

3.  **Stopping the service:**
    To stop the service and remove the containers, press `Ctrl+C` in the terminal, then run:
    ```bash
    docker-compose down
    ```

## ✨ Usage

The API documentation is available at **[http://localhost:4444/docs](http://localhost:4444/docs)** once the service is running.

For detailed API usage, refer to `API_DOCS.md`.